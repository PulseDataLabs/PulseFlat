"""
scrapers/b3_opcoes_posicoes_resumo.py
--------------------------------------
Consolidado histórico de posições em aberto de opções na B3 por ativo objeto
(PETR, VALE, BOVA, IBOV, etc.), com contagem de contratos de CALL e PUT,
cálculo do Put/Call Ratio diário, distribuição entre posições cobertas, descobertas
e em travas, e identificação dos strikes com maior concentração de Open Interest.

Fonte:
- Derivado do dataset granular de posições em aberto da B3.
Saída:
- data/b3_opcoes_posicoes_resumo.csv (Resumo acumulado por pregão e ativo)
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.b3_opcoes_posicoes_aberto import (
    ARQUIVO_GRANULAR,
    CABECALHO_RESUMO,
    capturar,
    gerar_resumo_por_ativo,
)
from scrapers.utils.base import BaseScraper
from utils import get_logger

log = get_logger("b3_opcoes_posicoes_resumo")


class B3OpcoesPosicoesResumoScraper(BaseScraper):
    name = "b3_opcoes_posicoes_resumo"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = True
    compress = False
    chaves_dedup = ["data_referencia", "codigo_ativo_objeto"]

    # Catálogo de Metadados
    title = "B3 Opções — Resumo de Posições em Aberto e Put/Call Ratio"
    description = (
        "Consolidado diário e histórico de Open Interest por ativo objeto negociado na B3. "
        "Inclui total de contratos em CALL e PUT, Put/Call Ratio, posições cobertas/descobertas/travadas "
        "e os strikes com maior concentração de posições em aberto."
    )
    icon = "📊"
    icon_class = "icon-b3"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = [
        "opções",
        "put call ratio",
        "open interest",
        "posições em aberto",
        "call",
        "put",
        "derivativos",
        "B3",
    ]
    source = "B3"

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 Opções — Resumo de Posições em Aberto por Ativo ===")

        # 1. Se existir snapshot granular recente no disco compatível com a data alvo
        if ARQUIVO_GRANULAR.exists():
            try:
                df_gran = pd.read_csv(ARQUIVO_GRANULAR, compression="gzip", dtype={"data_referencia": str})
                if not df_gran.empty and (not self.target_date or (df_gran["data_referencia"].iloc[0] == self.target_date.strftime("%Y-%m-%d"))):
                    ref_data = df_gran["data_referencia"].iloc[0]
                    log.info(f"Reutilizando snapshot granular de {ref_data} ({len(df_gran)} séries).")
                    return gerar_resumo_por_ativo(df_gran, ref_data)
            except Exception as e:
                log.warning(f"Erro ao ler snapshot granular ({e}), buscando diretamente da B3.")

        # 2. Caso contrário, captura direto da B3
        dados, str_data = capturar(self.target_date)
        if not dados:
            return pd.DataFrame(columns=CABECALHO_RESUMO)

        df_dia = pd.DataFrame(dados)
        return gerar_resumo_por_ativo(df_dia, str_data)


if __name__ == "__main__":
    B3OpcoesPosicoesResumoScraper().run()
