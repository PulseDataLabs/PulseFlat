"""
scrapers/b3_taxa_cambio_referencia.py
--------------------------------------
Captura a Taxa de Cambio de Referencia divulgada pela B3.

Fonte: https://sistemaswebb3-derivativos.b3.com.br/financialIndicatorsProxy/
       ReferenceExchangeRate/GetReferenceExchangeRate/<base64>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import get_logger, nova_session, salvar_csv
from utils.parsers import json_rows, enriquecer, read_existing_header

log = get_logger("b3_taxa_cambio_referencia")

URL = (
    "https://sistemaswebb3-derivativos.b3.com.br/"
    "financialIndicatorsProxy/ReferenceExchangeRate/"
    "GetReferenceExchangeRate/"
    "eyJsYW5ndWFnZSI6InB0LWJyIn0="
)
ARQUIVO = Path("data/b3_taxa_cambio_referencia.csv")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    log.info(f"Acessando {URL}")
    resp = session.get(URL, timeout=30)
    resp.raise_for_status()
    rows = json_rows(resp.json())
    enriched, header_novo = enriquecer("b3_taxa_cambio_referencia", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header


def main():
    log.info("=== B3 — Taxa de Cambio de Referencia ===")
    rows, header = capturar()
    salvar_csv(ARQUIVO, rows, header, chaves_dedup=["data_captura", "conjunto", "registro_hash"])
    log.info(f"{len(rows)} registro(s) salvo(s)")


if __name__ == "__main__":
    main()
