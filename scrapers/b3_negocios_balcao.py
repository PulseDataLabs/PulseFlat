"""
scrapers/b3_negocios_balcao.py
-------------------------------
Negócios realizados em mercado de balcão da B3 — arquivo OTC
codificado em Base64.

Fonte: https://bvmf.bmfbovespa.com.br/NegociosRealizados/Registro/DownloadArquivoDiretorio?data=%d-%m-%Y
"""

import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import get_logger, nova_session, salvar_csv
from utils.parsers import date_ref, replace_date_vars, decode_bytes, csv_rows, enriquecer, read_existing_header

log = get_logger("b3_negocios_balcao")

URL = "https://bvmf.bmfbovespa.com.br/NegociosRealizados/Registro/DownloadArquivoDiretorio?data=%d-%m-%Y"
ARQUIVO = Path("data/b3_negocios_balcao.csv")


def _parse_otc_content(content: bytes) -> list[dict]:
    txt = decode_bytes(content).strip()
    decoded = txt
    if not txt.startswith("Data;") and not txt.startswith("Instrumento"):
        try:
            decoded_bytes = base64.b64decode(txt, validate=False)
            decoded = decode_bytes(decoded_bytes)
        except Exception:
            decoded = txt
    rows = csv_rows(decoded, delimiter=";")
    return [r for r in rows if str(r.get("data", "")).lower() != "data"]


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    dt = date_ref("dia_anterior")
    url = replace_date_vars(URL, dt)
    log.info(f"Baixando {url}")
    resp = session.get(url, timeout=180)
    resp.raise_for_status()
    rows = _parse_otc_content(resp.content)
    enriched, header_novo = enriquecer("b3_negocios_balcao", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header


def main():
    log.info("=== B3 — Negócios de Balcão (OTC) ===")
    rows, header = capturar()
    salvar_csv(ARQUIVO, rows, header, chaves_dedup=["data_captura", "conjunto", "registro_hash"])
    log.info(f"{len(rows)} registro(s) salvo(s)")


if __name__ == "__main__":
    main()
