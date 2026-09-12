"""
scrapers/fred_template.py
-------------------------
Template e guia de referência para criação de novos scrapers baseados
na API do Federal Reserve Economic Data (FRED).

Fonte: https://fred.stlouisfed.org/docs/api/fred/
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.fred_base import BaseFredScraper
from utils.base import agora_brt, get_logger

log = get_logger("fred_template")


class FredTemplateScraper(BaseFredScraper):
    # Identificador único do dataset (gera data/fred_exemplo_template.csv)
    name = "fred_exemplo_template"

    group = "fred"
    enabled = False  # Deixar False até configurar a série específica
    phase = 1
    accumulate = True

    # Chaves para evitar duplicatas em coletas periódicas
    chaves_dedup = ["data_captura", "data_referencia", "serie_id"]

    title = "FRED — Template de Exemplo (St. Louis Fed)"
    description = (
        "Scraper modelo demonstrando a estrutura de consulta à API do FRED. "
        "Utilize este arquivo como base para implementar novas séries macroeconômicas globais."
    )
    icon = "🦅"
    icon_class = "icon-fred"
    badge = "FRED Global"
    badge_class = "badge-dynamic"
    tags = ["fred", "fed", "macro", "treasury", "global"]
    source = "Federal Reserve Economic Data — FRED (stlouisfed.org)"

    # Exemplo: US 10-Year Treasury Yield ('DGS10')
    series_id = "DGS10"

    def fetch(self) -> pd.DataFrame:
        """
        Executa a coleta e transformação das observações da série do FRED.
        """
        log.info(f"Consultando série no FRED: {self.series_id}")

        registros = self.fetch_series(self.series_id, limit=100)
        if not registros:
            log.warning("Nenhum dado retornado pelo FRED.")
            return pd.DataFrame()

        data_captura, _ = agora_brt()
        linhas_normalizadas = []

        for item in registros:
            val = item.get("value", "")
            # O FRED utiliza '.' para dias sem negociação/feriados
            if val == ".":
                continue

            linhas_normalizadas.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": item.get("date", ""),
                    "serie_id": self.series_id,
                    "valor": val,
                }
            )

        df = pd.DataFrame(linhas_normalizadas)
        log.info(f"{len(df)} observações preparadas com sucesso.")
        return df


if __name__ == "__main__":
    FredTemplateScraper().run()
