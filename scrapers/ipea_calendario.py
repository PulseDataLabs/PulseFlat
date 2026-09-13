"""
Scraper: IPEADATA – Calendário e Dias Úteis
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/ipea_calendario.csv
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.ipea_base import BaseIpeaScraper

SERIES = [
    {
        "code": "SGS12_NDIASUTEISFUT12",
        "title": "Dias Úteis Futuros",
        "desc": "Número de dias úteis futuros estimados mensalmente",
        "icon": "📆",
        "tags": ["dias_uteis", "calendario", "ipea"],
    },
    {
        "code": "SGS12_NDIASUTEISPAS12",
        "title": "Dias Úteis Passados",
        "desc": "Número de dias úteis passados no mês correspondente",
        "icon": "📅",
        "tags": ["dias_uteis", "calendario", "ipea"],
    },
]


class IpeaCalendarioScraper(BaseIpeaScraper):
    title = "IPEADATA — Calendário e Dias Úteis"
    description = "Calendário de dias úteis e feriados nacionais compilado pelo IPEADATA para ajuste sazonal e conversão de séries temporais financeiras e econômicas."
    badge = "Mensal"
    source = "IPEA"
    tags = ['ipea', 'calendario', 'dias_uteis']
    name = "ipea_calendario"
    group = "ipea"
    enabled = True
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    def fetch(self) -> pd.DataFrame:
        return self.fetch_series_list(SERIES)


if __name__ == "__main__":
    IpeaCalendarioScraper().run()
