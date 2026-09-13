"""
Scraper: IPEADATA – Mercados Globais Diários
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/ipea_mercados_diarios.csv
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.ipea_base import BaseIpeaScraper

SERIES = [
    {
        "code": "EIA366_PBRENT366",
        "title": "Petróleo Brent",
        "desc": "Preço do petróleo bruto Brent (FOB, US$)",
        "icon": "🛢",
        "tags": ["petroleo", "brent", "commodities", "ipea"],
    },
    {
        "code": "EIA366_PWTI366",
        "title": "Petróleo WTI",
        "desc": "Preço do petróleo bruto WTI (FOB, US$)",
        "icon": "🛢",
        "tags": ["petroleo", "wti", "commodities", "ipea"],
    },
    {
        "code": "GM366_DOW366",
        "title": "Índice Dow Jones",
        "desc": "Índice de ações Dow Jones (fechamento)",
        "icon": "📈",
        "tags": ["dow_jones", "acoes", "ipea"],
    },
    {
        "code": "SGS366_NASDAQ366",
        "title": "Índice NASDAQ",
        "desc": "Índice de ações NASDAQ (fechamento)",
        "icon": "📈",
        "tags": ["nasdaq", "acoes", "ipea"],
    },
]


class IpeaMercadosDiariosScraper(BaseIpeaScraper):
    title = "IPEADATA — Mercados Financeiros Diários"
    description = "Cotações financeiras diárias de mercados internacionais compiladas pelo IPEA, incluindo Petróleo Brent, WTI, Ouro e índices cambiais de economias emergentes."
    badge = "Diário"
    source = "IPEA"
    tags = ['ipea', 'mercados_diarios', 'brent', 'wti', 'commodities']
    name = "ipea_mercados_diarios"
    group = "ipea"
    enabled = True
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    def fetch(self) -> pd.DataFrame:
        return self.fetch_series_list(SERIES)


if __name__ == "__main__":
    IpeaMercadosDiariosScraper().run()
