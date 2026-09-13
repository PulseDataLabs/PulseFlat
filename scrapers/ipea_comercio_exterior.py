"""
Scraper: IPEADATA – Comércio Exterior
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/ipea_comercio_exterior.csv
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.ipea_base import BaseIpeaScraper

SERIES = [
    {
        "code": "FUNCEX12_XPT12",
        "title": "Exportações Preços Índice",
        "desc": "Índice de preços das exportações gerais (média 2018 = 100)",
        "icon": "🚢",
        "tags": ["exportacao", "precos", "ipea"],
    },
    {
        "code": "FUNCEX12_MDPT12",
        "title": "Importações Preços Índice",
        "desc": "Índice de preços das importações gerais (média 2018 = 100)",
        "icon": "🚢",
        "tags": ["importacao", "precos", "ipea"],
    },
]


class IpeaComercioExteriorScraper(BaseIpeaScraper):
    title = "IPEADATA — Comércio Exterior e Balança Comercial"
    description = "Estatísticas mensais consolidadas de comércio exterior brasileiro (exportações, importações, saldo comercial, termos de troca e quantum) disponibilizadas pelo IPEADATA."
    badge = "Mensal"
    source = "IPEA"
    tags = ['ipea', 'comercio_exterior', 'exportacao', 'importacao']
    name = "ipea_comercio_exterior"
    group = "ipea"
    enabled = True
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    def fetch(self) -> pd.DataFrame:
        return self.fetch_series_list(SERIES)


if __name__ == "__main__":
    IpeaComercioExteriorScraper().run()
