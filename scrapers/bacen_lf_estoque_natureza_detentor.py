"""
scrapers/bacen_lf_estoque_natureza_detentor.py
----------------------------------------------
Estatísticas sobre Letras Financeiras (BACEN) — Estoque por Natureza do Detentor.

Fonte:
  https://www.bcb.gov.br/estatisticas/estats_letras_financeiras
  https://www.bcb.gov.br/content/estatisticas/estatisticas_sfn/estatisticas_letras_financeiras/EstoqueNaturezaDetentor.xlsx
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.bacen_lf_helper import (
    download_workbook_bytes,
    parse_annual_holder_nature,
)
from scrapers.utils.base import BaseScraper
from utils.base import get_logger

log = get_logger("bacen_lf_estoque_natureza_detentor")

EXCEL_FILENAME = "EstoqueNaturezaDetentor.xlsx"

CABECALHO = [
    "data_captura",
    "data_referencia",
    "natureza_detentor",
    "estoque_lf",
    "estoque_lfs",
    "estoque_total",
    "participacao_perc",
]


def capturar() -> list[dict[str, str]]:
    content = download_workbook_bytes(EXCEL_FILENAME)
    return parse_annual_holder_nature(content)


class BacenLfEstoqueNaturezaDetentorScraper(BaseScraper):
    name = "bacen_lf_estoque_natureza_detentor"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = True
    compress = True
    chaves_dedup = ["data_referencia", "natureza_detentor"]

    title = "BACEN — Letras Financeiras: Estoque por Natureza do Detentor"
    description = (
        "Posição anual (dezembro de cada ano) do estoque de Letras Financeiras (LF) "
        "e Letras Financeiras Subordinadas (LFS) aberto pela natureza jurídica dos "
        "investidores detentores (fundos, bancos, clientes PF/PJ e institucionais), em Reais (R$)."
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
        "detentores",
        "investidores",
    ]
    source = "BACEN"

    def fetch(self) -> pd.DataFrame:
        log.info("=== BACEN — Letras Financeiras: Estoque por Natureza do Detentor ===")
        dados = capturar()
        if not dados:
            return pd.DataFrame(columns=CABECALHO)
        df = pd.DataFrame(dados)
        df = df.sort_values(by=["data_referencia", "natureza_detentor"]).reset_index(drop=True)
        return df[CABECALHO]


if __name__ == "__main__":
    BacenLfEstoqueNaturezaDetentorScraper().run()

