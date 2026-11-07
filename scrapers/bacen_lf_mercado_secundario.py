"""
scrapers/bacen_lf_mercado_secundario.py
---------------------------------------
Estatísticas sobre Letras Financeiras (BACEN) — Mercado Secundário (Quantidade de Operações e Valor).

Fonte:
  https://www.bcb.gov.br/estatisticas/estats_letras_financeiras
  https://www.bcb.gov.br/content/estatisticas/estatisticas_sfn/estatisticas_letras_financeiras/MercadoSecundario.xlsx
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.bacen_lf_helper import (
    download_workbook_bytes,
    parse_monthly_secondary_market,
)
from scrapers.utils.base import BaseScraper
from utils.base import get_logger

log = get_logger("bacen_lf_mercado_secundario")

EXCEL_FILENAME = "MercadoSecundario.xlsx"

CABECALHO = [
    "data_captura",
    "data_referencia",
    "numero_negocios",
    "valor",
]


def capturar() -> list[dict[str, str]]:
    content = download_workbook_bytes(EXCEL_FILENAME)
    return parse_monthly_secondary_market(content)


class BacenLfMercadoSecundarioScraper(BaseScraper):
    name = "bacen_lf_mercado_secundario"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = True
    compress = True
    chaves_dedup = ["data_referencia"]

    title = "BACEN — Letras Financeiras: Mercado Secundário"
    description = (
        "Série histórica mensal da quantidade de negócios e do volume financeiro total "
        "transacionado no mercado secundário de Letras Financeiras no SFN, em Reais (R$)."
    )
    icon = "🏛️"
    icon_class = "icon-bcb"
    badge = "Mensal"
    badge_class = "badge-monthly"
    tags = [
        "bacen",
        "bcb",
        "letras financeiras",
        "lf",
        "lfs",
        "mercado secundário",
        "negociações",
        "liquidez",
    ]
    source = "BACEN"

    def fetch(self) -> pd.DataFrame:
        log.info("=== BACEN — Letras Financeiras: Mercado Secundário ===")
        dados = capturar()
        if not dados:
            return pd.DataFrame(columns=CABECALHO)
        df = pd.DataFrame(dados)
        df = df.sort_values(by=["data_referencia"]).reset_index(drop=True)
        return df[CABECALHO]


if __name__ == "__main__":
    BacenLfMercadoSecundarioScraper().run()

