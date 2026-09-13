"""
Scraper: IPEADATA – Produção Transformação Mineral
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/ipea_producao_mineral.csv
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.ipea_base import BaseIpeaScraper

SERIES = [
    {
        "code": "IBSIE12_QSCFG12",
        "title": "Produção de Ferro-Gusa",
        "desc": "Produção mensal de ferro-gusa (em toneladas)",
        "icon": "🧱",
        "tags": ["ferro_gusa", "producao", "ipea"],
    },
    {
        "code": "IBSIE12_QSCAB12",
        "title": "Produção de Aço Bruto",
        "desc": "Produção mensal de aço bruto (em toneladas)",
        "icon": "🧱",
        "tags": ["aco_bruto", "producao", "ipea"],
    },
    {
        "code": "IBSIE12_QSCL12",
        "title": "Produção de Laminados",
        "desc": "Produção mensal de laminados (em toneladas)",
        "icon": "🧱",
        "tags": ["laminados", "producao", "ipea"],
    },
]


class IpeaProducaoMineralScraper(BaseIpeaScraper):
    title = "IPEADATA — Produção Mineral e Siderurgia"
    description = "Série histórica mensal da produção, extração e beneficiamento de minério de ferro, petróleo, gás natural e produtos siderúrgicos no Brasil apurados pelo IPEA."
    badge = "Mensal"
    source = "IPEA"
    tags = ['ipea', 'producao_mineral', 'mineracao', 'siderurgia']
    name = "ipea_producao_mineral"
    group = "ipea"
    enabled = True
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    def fetch(self) -> pd.DataFrame:
        return self.fetch_series_list(SERIES)


if __name__ == "__main__":
    IpeaProducaoMineralScraper().run()
