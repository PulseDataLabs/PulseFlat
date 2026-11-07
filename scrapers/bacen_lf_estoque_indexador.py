"""
scrapers/bacen_lf_estoque_indexador.py
--------------------------------------
Estatísticas sobre Letras Financeiras (BACEN) — Estoque por Indexador.

Fonte:
  https://www.bcb.gov.br/estatisticas/estats_letras_financeiras
  https://www.bcb.gov.br/content/estatisticas/estatisticas_sfn/estatisticas_letras_financeiras/EstoquePorIndexador.xlsx
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.bacen_lf_helper import (
    download_workbook_bytes,
    parse_annual_indexer,
)
from scrapers.utils.base import BaseScraper
from utils.base import get_logger

log = get_logger("bacen_lf_estoque_indexador")

EXCEL_FILENAME = "EstoquePorIndexador.xlsx"

CABECALHO = [
    "data_captura",
    "data_referencia",
    "indexador",
    "valor",
    "participacao_perc",
]


def capturar() -> list[dict[str, str]]:
    content = download_workbook_bytes(EXCEL_FILENAME)
    return parse_annual_indexer(content)


class BacenLfEstoqueIndexadorScraper(BaseScraper):
    name = "bacen_lf_estoque_indexador"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = True
    compress = True
    chaves_dedup = ["data_referencia", "indexador"]

    title = "BACEN — Letras Financeiras: Estoque por Indexador"
    description = (
        "Posição anual (dezembro de cada ano) do estoque de Letras Financeiras "
        "aberto por indexador de remuneração (DI, IPCA, Pré-fixado, SELIC, IGP-M, INPC e VCP), "
        "padronizado em Reais (R$) e participação percentual."
    )
    icon = "🏛️"
    icon_class = "icon-bcb"
    badge = "Anual"
    badge_class = "badge-annual"
    tags = [
        "bacen",
        "bcb",
        "letras financeiras",
        "lf",
        "lfs",
        "estoque",
        "indexador",
        "di",
        "ipca",
    ]
    source = "BACEN"

    def fetch(self) -> pd.DataFrame:
        log.info("=== BACEN — Letras Financeiras: Estoque por Indexador ===")
        dados = capturar()
        if not dados:
            return pd.DataFrame(columns=CABECALHO)
        df = pd.DataFrame(dados)
        df = df.sort_values(by=["data_referencia", "indexador"]).reset_index(drop=True)
        return df[CABECALHO]


if __name__ == "__main__":
    BacenLfEstoqueIndexadorScraper().run()

