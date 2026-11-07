"""
scrapers/bacen_lf_estoque_segmento.py
-------------------------------------
Estatísticas sobre Letras Financeiras (BACEN) — LF: Estoque por Segmento do Emissor.

Fonte:
  https://www.bcb.gov.br/estatisticas/estats_letras_financeiras
  https://www.bcb.gov.br/content/estatisticas/estatisticas_sfn/estatisticas_letras_financeiras/LFEstoqueSegmento.xlsx
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.bacen_lf_helper import (
    download_workbook_bytes,
    parse_monthly_segments,
)
from scrapers.utils.base import BaseScraper
from utils.base import get_logger

log = get_logger("bacen_lf_estoque_segmento")

EXCEL_FILENAME = "LFEstoqueSegmento.xlsx"

SEGMENT_COLS = [
    "bancos_comerciais",
    "bancos_investimento",
    "bancos_multiplos",
    "scfi",
    "bancos_desenvolvimento",
    "companhias_hipotecarias",
    "cooperativas_credito",
    "total",
]

CABECALHO = [
    "data_captura",
    "data_referencia",
    *SEGMENT_COLS,
]


def capturar() -> list[dict[str, str]]:
    content = download_workbook_bytes(EXCEL_FILENAME)
    return parse_monthly_segments(content, expected_segment_cols=SEGMENT_COLS)


class BacenLfEstoqueSegmentoScraper(BaseScraper):
    name = "bacen_lf_estoque_segmento"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = True
    compress = True
    chaves_dedup = ["data_referencia"]

    title = "BACEN — Letras Financeiras (LF): Estoque por Segmento do Emissor"
    description = (
        "Série histórica mensal do estoque de Letras Financeiras não subordinadas (LF) "
        "aberto pelo segmento da instituição emissora (Bancos Comerciais, Investimento, "
        "Múltiplos, SCFI, Desenvolvimento, Companhias Hipotecárias e Cooperativas de Crédito), em Reais (R$)."
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
        "estoque",
        "segmento",
        "bancos",
    ]
    source = "BACEN"

    def fetch(self) -> pd.DataFrame:
        log.info("=== BACEN — LF: Estoque por Segmento do Emissor ===")
        dados = capturar()
        if not dados:
            return pd.DataFrame(columns=CABECALHO)
        df = pd.DataFrame(dados)
        df = df.sort_values(by=["data_referencia"]).reset_index(drop=True)
        return df[CABECALHO]


if __name__ == "__main__":
    BacenLfEstoqueSegmentoScraper().run()

