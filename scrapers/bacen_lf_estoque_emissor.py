"""
scrapers/bacen_lf_estoque_emissor.py
------------------------------------
Estatísticas sobre Letras Financeiras (BACEN) — Estoque por Emissor (IF/Conglomerado).

Fonte:
  https://www.bcb.gov.br/estatisticas/estats_letras_financeiras
  https://www.bcb.gov.br/content/estatisticas/estatisticas_sfn/estatisticas_letras_financeiras/EstoquePorEmissor.xlsx
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.bacen_lf_helper import (
    download_workbook_bytes,
    parse_annual_issuer,
)
from scrapers.utils.base import BaseScraper
from utils.base import get_logger

log = get_logger("bacen_lf_estoque_emissor")

EXCEL_FILENAME = "EstoquePorEmissor.xlsx"

CABECALHO = [
    "data_captura",
    "data_referencia",
    "cnpj",
    "instituicao_conglomerado",
    "estoque_lf",
    "estoque_lfs",
    "estoque_total",
]


def capturar() -> list[dict[str, str]]:
    content = download_workbook_bytes(EXCEL_FILENAME)
    return parse_annual_issuer(content)


class BacenLfEstoqueEmissorScraper(BaseScraper):
    name = "bacen_lf_estoque_emissor"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = True
    compress = True
    chaves_dedup = ["data_referencia", "instituicao_conglomerado"]

    title = "BACEN — Letras Financeiras: Estoque por Emissor"
    description = (
        "Posição anual (dezembro de cada ano) do estoque de Letras Financeiras (LF) "
        "e Letras Financeiras Subordinadas (LFS) aberto por instituição financeira "
        "ou conglomerado emissor no SFN (enriquecido com o CNPJ de 14 posições da "
        "instituição/líder do conglomerado), em Reais (R$)."
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
        "emissores",
        "cnpj",
        "bancos",
    ]
    source = "BACEN"

    def fetch(self) -> pd.DataFrame:
        log.info("=== BACEN — Letras Financeiras: Estoque por Emissor ===")
        dados = capturar()
        if not dados:
            return pd.DataFrame(columns=CABECALHO)
        df = pd.DataFrame(dados)
        df = df.sort_values(by=["data_referencia", "instituicao_conglomerado"]).reset_index(drop=True)
        return df[CABECALHO]


if __name__ == "__main__":
    BacenLfEstoqueEmissorScraper().run()

