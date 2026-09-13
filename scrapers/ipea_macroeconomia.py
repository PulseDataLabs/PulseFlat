"""
Scraper: IPEADATA – Macroeconomia Geral
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/ipea_macroeconomia.csv
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.ipea_base import BaseIpeaScraper

SERIES = [
    {
        "code": "BM12_PIBAC12",
        "title": "PIB Acumulado 12m",
        "desc": "PIB acumulado em 12 meses (R$)",
        "icon": "📈",
        "tags": ["pib", "macroeconomia", "ipea"],
    },
    {
        "code": "PNADC12_TDESOC12",
        "title": "Taxa de Desocupação",
        "desc": "Taxa de desocupação da PNAD Contínua (%)",
        "icon": "👥",
        "tags": ["desemprego", "trabalho", "ipea"],
    },
    {
        "code": "GAC12_SALMINRE12",
        "title": "Salário Mínimo Real",
        "desc": "Salário mínimo real mensal (em R$ do último mês)",
        "icon": "💰",
        "tags": ["salario_minimo", "renda", "ipea"],
    },
    {
        "code": "MTE12_SALMIN12",
        "title": "Salário Mínimo Vigente",
        "desc": "Salário mínimo vigente nominal (R$)",
        "icon": "💰",
        "tags": ["salario_minimo", "renda", "ipea"],
    },
    {
        "code": "SGS12_7836",
        "title": "Saldo da Poupança",
        "desc": "Saldo total de depósitos em poupança SBPE e rural (R$ milhões)",
        "icon": "🏦",
        "tags": ["poupanca", "saldo", "ipea"],
    },
]


class IpeaMacroeconomiaScraper(BaseIpeaScraper):
    title = "IPEADATA — Macroeconomia e Contas Nacionais"
    description = "Conjunto de séries temporais macroeconômicas de longo prazo compiladas pelo IPEA, abrangendo consumo das famílias, arrecadação tributária, dívida pública e produtividade industrial."
    badge = "Mensal"
    source = "IPEA"
    tags = ['ipea', 'macroeconomia', 'pib']
    name = "ipea_macroeconomia"
    group = "ipea"
    enabled = True
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    def fetch(self) -> pd.DataFrame:
        return self.fetch_series_list(SERIES)


if __name__ == "__main__":
    IpeaMacroeconomiaScraper().run()
