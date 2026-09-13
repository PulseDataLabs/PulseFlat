"""
Scraper: IPEADATA – Preços e Inflação
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/ipea_precos_inflacao.csv
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.ipea_base import BaseIpeaScraper

SERIES = [
    {
        "code": "IGP12_IGPDI12",
        "title": "IGP-DI Índice Geral",
        "desc": "Índice Geral de Preços - Disponibilidade Interna (IGP-DI) - índice (ago 1994 = 100)",
        "icon": "📊",
        "tags": ["igp_di", "inflacao", "ipea"],
    },
    {
        "code": "IGP12_INCC12",
        "title": "INCC-DI Índice Geral",
        "desc": "Índice Nacional de Custo da Construção - Disponibilidade Interna (INCC-DI) - índice (ago 1994 = 100)",
        "icon": "🏗",
        "tags": ["incc_di", "construcao", "ipea"],
    },
    {
        "code": "PRECOS12_INPC12",
        "title": "INPC Índice Geral",
        "desc": "Índice Nacional de Preços ao Consumidor (INPC) - geral - índice (dez 1993 = 100)",
        "icon": "🛒",
        "tags": ["inpc", "inflacao", "ipea"],
    },
    {
        "code": "PRECOS12_INPCBR12",
        "title": "INPC Taxa de Variação",
        "desc": "Índice Nacional de Preços ao Consumidor (INPC) - geral - taxa de variação (% a.m.)",
        "icon": "📈",
        "tags": ["inpc", "inflacao", "ipea"],
    },
]


class IpeaPrecosInflacaoScraper(BaseIpeaScraper):
    title = "IPEADATA — Preços e Inflação"
    description = "Série histórica completa dos índices de preços ao consumidor e no atacado no Brasil (IPCA, IGP-DI, IGP-M, IPC-Fipe, IPA-OG) apurados desde a década de 1980."
    badge = "Mensal"
    source = "IPEA"
    tags = ['ipea', 'inflacao', 'ipca', 'igpm']
    name = "ipea_precos_inflacao"
    group = "ipea"
    enabled = True
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    def fetch(self) -> pd.DataFrame:
        return self.fetch_series_list(SERIES)


if __name__ == "__main__":
    IpeaPrecosInflacaoScraper().run()
