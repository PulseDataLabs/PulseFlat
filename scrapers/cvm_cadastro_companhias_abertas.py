"""
scrapers/cvm_cadastro_companhias_abertas.py
--------------------------------------------
Cadastro de companhias abertas registradas na CVM.

Fonte: https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import get_logger, nova_session, salvar_csv
from utils.parsers import decode_bytes, csv_rows, enriquecer, read_existing_header

log = get_logger("cvm_cadastro_companhias_abertas")

URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv"
ARQUIVO = Path("data/cvm_cadastro_companhias_abertas.csv")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    log.info(f"Baixando {URL}")
    resp = session.get(URL, timeout=180)
    resp.raise_for_status()
    rows = csv_rows(decode_bytes(resp.content))
    enriched, header_novo = enriquecer("cvm_cadastro_companhias_abertas", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header


def main():
    log.info("=== CVM — Cadastro de Companhias Abertas ===")
    rows, header = capturar()
    salvar_csv(ARQUIVO, rows, header, chaves_dedup=["data_captura", "conjunto", "registro_hash"], acumular=False)
    log.info(f"{len(rows)} registro(s) salvo(s)")


if __name__ == "__main__":
    main()
