"""
scrapers/b3_bvbg087.py
-----------------------
Boletim diário de operações com derivativos da B3 — arquivo IR (087).

Fonte: https://www.b3.com.br/pesquisapregao/download?filelist=IR%y%m%d.zip
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import get_logger, nova_session, salvar_csv
from utils.parsers import date_ref, replace_date_vars, rows_from_zip, enriquecer, read_existing_header

log = get_logger("b3_bvbg087")

URL = "https://www.b3.com.br/pesquisapregao/download?filelist=IR%y%m%d.zip"
ARQUIVO = Path("data/b3_bvbg087.csv")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    dt = date_ref("dia_anterior")
    url = replace_date_vars(URL, dt)
    log.info(f"Baixando {url}")
    resp = session.get(url, timeout=180)
    resp.raise_for_status()
    rows = rows_from_zip(resp.content)
    enriched, header_novo = enriquecer("b3_bvbg087", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header


def main():
    log.info("=== B3 — BVBG 087 (Operações com Derivativos) ===")
    rows, header = capturar()
    salvar_csv(ARQUIVO, rows, header, chaves_dedup=["data_captura", "conjunto", "registro_hash"])
    log.info(f"{len(rows)} registro(s) salvo(s)")


if __name__ == "__main__":
    main()
