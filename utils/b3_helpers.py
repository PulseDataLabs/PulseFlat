"""
utils/b3_helpers.py
--------------------
Funções auxiliares compartilhadas entre scrapers da B3.
"""

import re
import time
from datetime import datetime, date
from pathlib import Path
import base64

from .base import b64_encode_params, get_logger, limpar

log = get_logger("b3_helpers")


def get_isin_zip(session) -> bytes:
    root_dir = Path(__file__).resolve().parents[1]
    cache_path = root_dir / "data" / "isinp.zip"

    # Se o arquivo existe e foi modificado hoje, usa o cache
    if cache_path.exists():
        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
        if mtime.date() == date.today():
            log.info("Carregando isinp.zip do cache local (modificado hoje).")
            return cache_path.read_bytes()

    # Caso contrário, faz o download
    log.info("Buscando metadados de download de ISIN B3...")
    url_meta = "https://sistemaswebb3-listados.b3.com.br/isinProxy/IsinCall/GetTextDownload/"
    resp_meta = session.get(url_meta, timeout=30)
    resp_meta.raise_for_status()
    meta_data = resp_meta.json()

    geral_pt = meta_data.get("geralPt", {})
    file_id = geral_pt.get("id")
    if not file_id:
        raise RuntimeError("Não foi possível encontrar o ID do arquivo geralPt nos metadados da B3.")

    encoded_id = base64.b64encode(str(file_id).encode("utf-8")).decode("utf-8")
    download_url = f"https://sistemaswebb3-listados.b3.com.br/isinProxy/IsinCall/GetFileDownload/{encoded_id}"

    log.info(f"Fazendo download de isinp.zip de {download_url}...")
    resp_zip = session.get(download_url, timeout=120)
    resp_zip.raise_for_status()

    # Salva no cache local
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(resp_zip.content)

    return resp_zip.content



def get_company_seeds(session) -> list[dict]:
    base = "https://sistemaswebb3-listados.b3.com.br/shareCapitalProxy/ShareCapitalCall/GetList/"
    seeds = []
    page = 1
    while True:
        payload = {"name": "", "pageNumber": page, "pageSize": 200, "language": "pt-br"}
        url = base + b64_encode_params(payload)
        resp = session.get(url, timeout=120)
        resp.raise_for_status()
        data = resp.json() or {}
        items = data.get("results") or data.get("result") or data.get("data") or []
        for it in items:
            code_cvm = limpar(it.get("codeCVM") or it.get("codeCvm") or it.get("codCvm"))
            trading_name = limpar(it.get("companyName") or it.get("tradingName") or it.get("name"))
            issuing = limpar(it.get("issuingCompany") or it.get("code") or it.get("acronym"))
            if not issuing and trading_name:
                issuing = re.sub(r"\W+", "", trading_name.upper())
            seeds.append({
                "codeCVM": code_cvm,
                "tradingName": trading_name,
                "issuingCompany": issuing,
            })
        total_pages = (data.get("page") or {}).get("totalPages") or 1
        if page >= int(total_pages):
            break
        page += 1
        time.sleep(0.2)
    uniq = []
    seen = set()
    for s in seeds:
        key = (s["codeCVM"], s["tradingName"], s["issuingCompany"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(s)
    return uniq
