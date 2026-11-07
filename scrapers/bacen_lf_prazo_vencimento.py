"""
scrapers/bacen_lf_prazo_vencimento.py
-------------------------------------
Estatísticas sobre Letras Financeiras (BACEN) — Prazo Médio até o Vencimento (LF e LFS).

Fonte:
  https://www.bcb.gov.br/estatisticas/estats_letras_financeiras
  https://www.bcb.gov.br/content/estatisticas/estatisticas_sfn/estatisticas_letras_financeiras/PrazoVencimento.xlsx
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

log = get_logger("bacen_lf_prazo_vencimento")

EXCEL_FILENAME = "PrazoVencimento.xlsx"

CABECALHO = [
    "data_captura",
    "data_referencia",
    "prazo_medio_vencimento_lf_meses",
    "prazo_medio_vencimento_lfs_meses",
]


def capturar() -> list[dict[str, str]]:
    content = download_workbook_bytes(EXCEL_FILENAME)
    return parse_monthly_lf_lfs(
        content,
        col_lf="prazo_medio_vencimento_lf_meses",
        col_lfs="prazo_medio_vencimento_lfs_meses",
    )


class BacenLfPrazoVencimentoScraper(BaseScraper):
    name = "bacen_lf_prazo_vencimento"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = True
    compress = True
    chaves_dedup = ["data_referencia"]

    title = "BACEN — Letras Financeiras: Prazo Médio até o Vencimento"
    description = (
        "Série histórica mensal do prazo médio remanescente até o vencimento (em meses, "
        "excluindo títulos perpétuos) do estoque de Letras Financeiras (LF) e "
        "Letras Financeiras Subordinadas (LFS) no SFN."
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
        "prazo médio",
        "vencimento",
    ]
    source = "BACEN"

    def fetch(self) -> pd.DataFrame:
        log.info("=== BACEN — Letras Financeiras: Prazo Médio até o Vencimento ===")
        dados = capturar()
        if not dados:
            return pd.DataFrame(columns=CABECALHO)
        df = pd.DataFrame(dados)
        df = df.sort_values(by=["data_referencia"]).reset_index(drop=True)
        return df[CABECALHO]


if __name__ == "__main__":
    BacenLfPrazoVencimentoScraper().run()

