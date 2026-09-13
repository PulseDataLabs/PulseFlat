"""
Scraper: IPEADATA – Investimento FBCF
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/ipea_fbcf.csv
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.ipea_base import BaseIpeaScraper

SERIES = [
    {
        "code": "GAC12_INDFBCF12",
        "title": "FBCF Índice Geral",
        "desc": "Indicador IPEA de FBCF - índice real (média 1995 = 100)",
        "icon": "🏗",
        "tags": ["fbcf", "investimento", "ipea"],
    },
    {
        "code": "GAC12_INDFBCFDESSAZ12",
        "title": "FBCF Geral Dessazonalizado",
        "desc": "Indicador IPEA de FBCF - índice real dessazonalizado (média 1995 = 100)",
        "icon": "🏗",
        "tags": ["fbcf", "investimento", "ipea"],
    },
    {
        "code": "GAC12_INDFBCFCC12",
        "title": "FBCF Construção Civil",
        "desc": "Indicador IPEA de FBCF - construção civil - índice real (média 1995 = 100)",
        "icon": "🏗",
        "tags": ["fbcf", "construcao", "ipea"],
    },
    {
        "code": "GAC12_INDFBCFCCDESSAZ12",
        "title": "FBCF Construção Civil Dessazonalizado",
        "desc": "Indicador IPEA de FBCF - construção civil - índice real dessazonalizado (média 1995 = 100)",
        "icon": "🏗",
        "tags": ["fbcf", "construcao", "ipea"],
    },
]


class IpeaFbcfScraper(BaseIpeaScraper):
    title = "IPEADATA — Formação Bruta de Capital Fixo (FBCF)"
    description = "Indicador mensal do IPEA para a Formação Bruta de Capital Fixo (FBCF), medindo a taxa de investimentos da economia brasileira em máquinas, equipamentos e construção civil."
    badge = "Mensal"
    source = "IPEA"
    tags = ['ipea', 'fbcf', 'investimentos', 'pib']
    name = "ipea_fbcf"
    group = "ipea"
    enabled = True
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    def fetch(self) -> pd.DataFrame:
        return self.fetch_series_list(SERIES)


if __name__ == "__main__":
    IpeaFbcfScraper().run()
