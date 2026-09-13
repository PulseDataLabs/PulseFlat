"""
scrapers/ipea_template.py
-------------------------
Template e guia de referência para criação de novos scrapers baseados
na API OData v4 do IPEADATA.

Fonte: http://www.ipeadata.gov.br/api/odata4/

Instruções:
1. Copie este arquivo para `scrapers/ipea_minha_serie.py`.
2. Altere `name`, `title`, `description`, `tags` e `series_code`.
3. Defina as chaves de deduplicação em `chaves_dedup`.
4. Altere `enabled = True` para ativar no orquestrador `run_all.py`.
5. Execute localmente para testar: `python scrapers/ipea_minha_serie.py`.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.ipea_base import BaseIpeaScraper
from utils.base import get_logger

log = get_logger("ipea_template")


class IpeaTemplateScraper(BaseIpeaScraper):
    """Scraper modelo para consulta de séries econômicas do IPEADATA."""

    # Identificador do scraper (gera data/ipea_exemplo_template.csv)
    name = "ipea_exemplo_template"

    group = "ipea"
    enabled = False  # Deixar False até configurar a série desejada
    phase = 1
    accumulate = True

    # Chaves para evitar duplicatas em coletas incrementais
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    title = "IPEADATA — Template de Exemplo"
    description = (
        "Scraper modelo demonstrando a estrutura de consulta à API OData v4 do IPEADATA. "
        "Utilize este arquivo como base para implementar novas coletas do repositório econômico."
    )
    icon = "📊"
    icon_class = "icon-ipea"
    badge = "IPEA"
    badge_class = "badge-monthly"
    tags = ["ipea", "macroeconomia", "series_temporais", "indicadores"]
    source = "IPEA — Ipeadata (ipeadata.gov.br)"

    # Exemplo de código de série: 'BM12_TJOVER12' (Taxa Selic Over Mensal)
    series_code = "BM12_TJOVER12"

    def fetch(self) -> pd.DataFrame:
        """
        Executa a coleta e transformação das observações históricas da série IPEA.
        """
        log.info(f"Consultando série no IPEADATA: {self.series_code}")

        records = self.fetch_serie(self.series_code)
        if not records:
            log.warning("Nenhum dado retornado pelo IPEADATA.")
            return pd.DataFrame()

        df = self.normalize_dataframe(
            records=records,
            codigo=self.series_code,
            nome=self.title,
        )

        log.info(f"Total de observações tratadas: {len(df)}")
        return df


if __name__ == "__main__":
    IpeaTemplateScraper().run()
