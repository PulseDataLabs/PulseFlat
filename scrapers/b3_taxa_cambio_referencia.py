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
import pandas as pd
from scrapers.utils.base import BaseScraper

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

class B3TaxaCambioReferenciaScraper(BaseScraper):
    name = "b3_taxa_cambio_referencia"
    group = "b3"
    enabled = False
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'conjunto', 'registro_hash']
    
    # Catálogo de Metadados
    title = 'B3 — Taxa de Câmbio de Referência'
    description = 'Taxas de câmbio de referência divulgadas pela B3: compra e venda por moeda.'
    icon = '💱'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['câmbio', 'taxa compra', 'taxa venda', 'moeda']
    source = 'B3 API'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 — Taxa de Cambio de Referencia ===")
        rows, header = capturar()
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3TaxaCambioReferenciaScraper().run()
