"""
scrapers/brasilapi_template.py
------------------------------
Template e guia de referência para criação de novos scrapers baseados
na BrasilAPI (API aberta de dados brasileiros).

Fonte: https://brasilapi.com.br/docs / https://brasilapi.com.br/api

COMO USAR ESTE TEMPLATE:
1. Copie este arquivo para um novo nome, por exemplo: `scrapers/brasilapi_taxas.py` ou `scrapers/brasilapi_bancos.py`
2. Ajuste o nome da classe, `name`, `title`, `description`, `tags`, etc.
3. Configure o `endpoint` desejado (ex: '/taxas/v1', '/banks/v1', '/cvm/corretoras/v1', etc.)
4. Implemente a lógica de transformação no método `fetch()`.
5. Ative o scraper alterando `enabled = True`.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.brasilapi_base import BaseBrasilApiScraper
from utils.base import agora_brt, get_logger

log = get_logger("brasilapi_template")


class BrasilapiTemplateScraper(BaseBrasilApiScraper):
    # Identificador único do dataset (gera data/brasilapi_exemplo_template.csv)
    name = "brasilapi_exemplo_template"

    # Grupo e controle de pipeline
    group = "brasilapi"
    enabled = False  # Deixar False até configurar o endpoint e campos específicos
    phase = 1
    accumulate = True

    # Chaves para evitar duplicatas em coletas periódicas
    chaves_dedup = ["data_captura", "codigo"]

    # Metadados para o catálogo web e index.html
    title = "BrasilAPI — Template de Exemplo"
    description = (
        "Scraper modelo demonstrando a estrutura de coleta da BrasilAPI. "
        "Utilize este arquivo como base para implementar novos endpoints abertos."
    )
    icon = "🇧🇷"
    icon_class = "icon-brasilapi"
    badge = "BrasilAPI"
    badge_class = "badge-dynamic"
    tags = ["brasilapi", "api", "template", "brasil"]
    source = "BrasilAPI (brasilapi.com.br)"

    # Endpoint da API (relativo a https://brasilapi.com.br/api)
    # Exemplo: "/taxas/v1", "/banks/v1", "/cvm/corretoras/v1"
    endpoint = "/taxas/v1"

    def fetch(self) -> pd.DataFrame:
        """
        Executa a coleta e transformação dos dados.
        Retorna um pd.DataFrame pronto para ser salvo em CSV.
        """
        log.info(f"Consultando endpoint BrasilAPI: {self.endpoint}")

        # O BaseBrasilApiScraper cuida de headers, retries em caso de 429/5xx e desempacotamento
        registros = self.fetch_endpoint(self.endpoint)

        if not registros:
            log.warning("Nenhum dado retornado pela BrasilAPI.")
            return pd.DataFrame()

        # Transforma os registros recebidos no formato tabular desejado
        data_captura, _ = agora_brt()
        linhas_normalizadas = []

        for item in registros:
            linhas_normalizadas.append(
                {
                    "data_captura": data_captura,
                    "codigo": item.get("nome") or item.get("code") or item.get("ispb", ""),
                    "descricao": item.get("nome") or item.get("name", ""),
                    "valor": item.get("valor", ""),
                }
            )

        df = pd.DataFrame(linhas_normalizadas)
        log.info(f"{len(df)} registros preparados com sucesso.")
        return df


if __name__ == "__main__":
    BrasilapiTemplateScraper().run()

BrasilApiTemplateScraper = BrasilapiTemplateScraper
