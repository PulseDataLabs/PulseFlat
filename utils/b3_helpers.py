"""
utils/b3_helpers.py
--------------------
Funções auxiliares compartilhadas entre scrapers da B3.
"""

import re
import time

from .base import b64_encode_params, get_logger, limpar

log = get_logger("b3_helpers")


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
