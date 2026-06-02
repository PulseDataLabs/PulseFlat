"""
scrapers/anbima_indice_imab.py
-------------------------------
Índice IMA-B da ANBIMA — histórico completo de rentabilidade
do índice de Mercado ANBIMA (IMA-B).

Fonte: https://s3-data-prd-use1-precos.s3.us-east-1.amazonaws.com/arquivos/indices-historico/IMAGERAL-HISTORICO.xls
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import get_logger, nova_session, salvar_csv
from utils.parsers import xls_rows, enriquecer, read_existing_header

log = get_logger("anbima_indice_imab")

URL = "https://s3-data-prd-use1-precos.s3.us-east-1.amazonaws.com/arquivos/indices-historico/IMAGERAL-HISTORICO.xls"
ARQUIVO = Path("data/anbima_indice_imab.csv")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    log.info(f"Baixando {URL}")
    resp = session.get(URL, timeout=180)
    resp.raise_for_status()
    rows = xls_rows(resp.content)
    enriched, header_novo = enriquecer("anbima_indice_imab", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header


def main():
    log.info("=== ANBIMA — Índice IMA-B ===")
    rows, header = capturar()
    salvar_csv(ARQUIVO, rows, header, chaves_dedup=["data_captura", "conjunto", "registro_hash"])
    log.info(f"{len(rows)} registro(s) salvo(s)")


if __name__ == "__main__":
    main()
