"""
Scraper: IPEADATA – Taxas de Juros
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/ipea_taxas_juros.csv
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.ipea_base import BaseIpeaScraper

SERIES = [
    {
        "code": "ANBIMA12_TJPOUP12",
        "title": "Poupança Rentabilidade Antiga",
        "desc": "Rentabilidade mensal da poupança para depósitos até 03/05/2012 (% a.m.)",
        "icon": "💵",
        "tags": ["juros", "poupanca", "ipea"],
    },
    {
        "code": "BM12_RNDPO12",
        "title": "Poupança Rentabilidade Nova",
        "desc": "Rentabilidade mensal da poupança para depósitos a partir de 04/05/2012 (% a.m.)",
        "icon": "💵",
        "tags": ["juros", "poupanca", "ipea"],
    },
    {
        "code": "ANBIMA12_TJTLN112",
        "title": "Taxa LTN 1m",
        "desc": "Taxa de juros prefixada - estrutura a termo - LTN - 1 mês (% a.m.)",
        "icon": "🏛",
        "tags": ["juros", "ltn", "ipea"],
    },
    {
        "code": "ANBIMA12_TJTLN312",
        "title": "Taxa LTN 3m",
        "desc": "Taxa de juros prefixada - estrutura a termo - LTN - 3 meses (% a.m.)",
        "icon": "🏛",
        "tags": ["juros", "ltn", "ipea"],
    },
    {
        "code": "ANBIMA12_TJTLN612",
        "title": "Taxa LTN 6m",
        "desc": "Taxa de juros prefixada - estrutura a termo - LTN - 6 meses (% a.m.)",
        "icon": "🏛",
        "tags": ["juros", "ltn", "ipea"],
    },
    {
        "code": "ANBIMA12_TJTLN1212",
        "title": "Taxa LTN 12m",
        "desc": "Taxa de juros prefixada - estrutura a termo - LTN - 12 meses (% a.m.)",
        "icon": "🏛",
        "tags": ["juros", "ltn", "ipea"],
    },
    {
        "code": "BM12_TJCDI12",
        "title": "Taxa CDI Mensal",
        "desc": "Taxa de juros - CDI / Over - acumulada no mês (% a.m.)",
        "icon": "📊",
        "tags": ["juros", "cdi", "ipea"],
    },
    {
        "code": "BM12_TJLP12",
        "title": "Taxa TJLP",
        "desc": "Taxa de Juros de Longo Prazo (TJLP) (% a.m.)",
        "icon": "🏭",
        "tags": ["juros", "tjlp", "ipea"],
    },
    {
        "code": "BM12_TJOVER12",
        "title": "Taxa Selic Mensal",
        "desc": "Taxa de juros - Over / Selic - acumulada no mês (% a.m.)",
        "icon": "💰",
        "tags": ["juros", "selic", "ipea"],
    },
    {
        "code": "BM12_TJTBF12",
        "title": "Taxa TBF",
        "desc": "Taxa Básica Financeira (TBF) - 1º dia do mês (% a.m.)",
        "icon": "📈",
        "tags": ["juros", "tbf", "ipea"],
    },
    {
        "code": "BM12_TJTR12",
        "title": "Taxa TR",
        "desc": "Taxa Referencial (TR) - 1º dia do mês (% a.m.)",
        "icon": "🏠",
        "tags": ["juros", "tr", "ipea"],
    },
]


class IpeaTaxasJurosScraper(BaseIpeaScraper):
    title = "IPEADATA — Taxas de Juros e Rendimentos"
    description = "Série histórica abrangente das taxas nominais e reais de juros brasileiras (Selic over, Selic meta, TJLP, TLP, TR, TBF e Caderneta de Poupança) disponibilizada pelo IPEA."
    badge = "Mensal"
    source = "IPEA"
    tags = ['ipea', 'taxas_juros', 'selic', 'cdi', 'poupanca']
    name = "ipea_taxas_juros"
    group = "ipea"
    enabled = True
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    def fetch(self) -> pd.DataFrame:
        return self.fetch_series_list(SERIES)


if __name__ == "__main__":
    IpeaTaxasJurosScraper().run()
