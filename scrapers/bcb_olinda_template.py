"""
scrapers/bcb_olinda_template.py
-------------------------------
Template e guia de referência para criação de novos scrapers baseados
na API OData do Banco Central do Brasil (BCB Olinda).

Fonte: https://olinda.bcb.gov.br/olinda/servico
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.bcb_olinda_base import BaseBcbOlindaScraper
from utils.base import agora_brt, get_logger

log = get_logger("bcb_olinda_template")


class BcbolindaTemplateScraper(BaseBcbOlindaScraper):
    # Identificador único do dataset (gera data/bcb_olinda_exemplo_template.csv)
    name = "bcb_olinda_exemplo_template"

    group = "bcb"
    enabled = False  # Deixar False até configurar o endpoint específico
    phase = 1
    accumulate = True

    # Chaves para evitar duplicatas em coletas diárias
    chaves_dedup = ["data_captura", "data_referencia", "indicador"]

    title = "BCB Olinda — Template de Exemplo (OData)"
    description = (
        "Scraper modelo demonstrando a estrutura de coleta da API OData do Banco Central. "
        "Utilize este arquivo como base para implementar novas consultas (Focus, Crédito, etc.)."
    )
    icon = "🏛️"
    icon_class = "icon-bcb"
    badge = "BCB Olinda"
    badge_class = "badge-dynamic"
    tags = ["bcb", "olinda", "odata", "macro"]
    source = "Banco Central do Brasil — Olinda (bcb.gov.br)"

    # Exemplo: Expectativas de Mercado Mensais (Boletim Focus)
    endpoint = "/Expectativas/versao/v1/odata/ExpectativaMercadoMensais"

    def fetch(self) -> pd.DataFrame:
        """
        Executa a coleta e transformação dos dados OData.
        """
        log.info(f"Consultando endpoint OData do BCB: {self.endpoint}")

        # Parâmetros OData: $top, $filter, $orderby, etc.
        params = {"$top": 10}

        registros = self.fetch_endpoint(self.endpoint, params=params)
        if not registros:
            log.warning("Nenhum dado retornado pelo BCB Olinda.")
            return pd.DataFrame()

        data_captura, _ = agora_brt()
        linhas_normalizadas = []

        for item in registros:
            linhas_normalizadas.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": item.get("Data") or item.get("DataReferencia", ""),
                    "indicador": item.get("Indicador", ""),
                    "media": item.get("Media", ""),
                    "mediana": item.get("Mediana", ""),
                    "minimo": item.get("Minimo", ""),
                    "maximo": item.get("Maximo", ""),
                }
            )

        df = pd.DataFrame(linhas_normalizadas)
        log.info(f"{len(df)} registros preparados com sucesso.")
        return df


BcbOlindaTemplateScraper = BcbolindaTemplateScraper

if __name__ == "__main__":
    BcbolindaTemplateScraper().run()
