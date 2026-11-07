"""
scrapers/bacen_lf_estoque.py
----------------------------
Estatísticas sobre Letras Financeiras (BACEN) — Estoque Mensal (LF e LFS).

Fonte:
  https://www.bcb.gov.br/estatisticas/estats_letras_financeiras
  https://www.bcb.gov.br/content/estatisticas/estatisticas_sfn/estatisticas_letras_financeiras/Estoque.xlsx
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.bacen_lf_helper import (
    download_workbook_bytes,
    parse_monthly_lf_lfs,
)
from scrapers.utils.base import BaseScraper
from utils.base import get_logger

log = get_logger("bacen_lf_estoque")

EXCEL_FILENAME = "Estoque.xlsx"

CABECALHO = [
    "data_captura",
    "data_referencia",
    "estoque_lf",
    "estoque_lfs",
]


def capturar() -> list[dict[str, str]]:
    content = download_workbook_bytes(EXCEL_FILENAME)
    return parse_monthly_lf_lfs(
        content,
        col_lf="estoque_lf",
        col_lfs="estoque_lfs",
    )


class BacenLfEstoqueScraper(BaseScraper):
    name = "bacen_lf_estoque"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = True
    compress = True
    chaves_dedup = ["data_referencia"]

    title = "BACEN — Letras Financeiras: Estoque Mensal"
    description = (
        "Série histórica mensal do estoque total em circulação de "
        "Letras Financeiras (LF) e Letras Financeiras Subordinadas (LFS) "
        "no Sistema Financeiro Nacional (SFN), em Reais (R$)."
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
        "estoque",
        "renda fixa",
        "funding bancário",
    ]
    source = "BACEN"

    def fetch(self) -> pd.DataFrame:
        log.info("=== BACEN — Letras Financeiras: Estoque Mensal ===")
        dados = capturar()
        if not dados:
            return pd.DataFrame(columns=CABECALHO)
        df = pd.DataFrame(dados)
        df = df.sort_values(by=["data_referencia"]).reset_index(drop=True)
        return df[CABECALHO]


if __name__ == "__main__":
    BacenLfEstoqueScraper().run()

