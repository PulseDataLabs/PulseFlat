"""
scrapers/eulerpool_template.py
------------------------------
Template e guia de referência para criação de novos scrapers baseados
na API oficial do Eulerpool Financial Data.

Fonte: https://eulerpool.com/developers / https://api.eulerpool.com

COMO USAR ESTE TEMPLATE:
1. Copie este arquivo para um novo nome, por exemplo: `scrapers/eulerpool_acoes_globais.py`
2. Ajuste o nome da classe, `name`, `title`, `description`, `tags`, etc.
3. Configure o `endpoint` desejado (ex: '/api/1/stocks/AAPL/financials', '/api/1/trends/ticker-trends', etc.)
4. Implemente a lógica de transformação no método `fetch()`.
5. Ative o scraper alterando `enabled = True`.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.eulerpool_base import BaseEulerpoolScraper
from utils.base import agora_brt, get_logger

log = get_logger("eulerpool_template")


class EulerpoolTemplateScraper(BaseEulerpoolScraper):
    # Identificador único do dataset (gera data/eulerpool_exemplo_template.csv)
    name = "eulerpool_exemplo_template"

    # Grupo e controle de pipeline
    group = "eulerpool"
    enabled = False  # Deixar False até configurar o endpoint e campos específicos
    phase = 1
    accumulate = True

    # Chaves para evitar duplicatas em coletas periódicas
    chaves_dedup = ["data_captura", "data_referencia", "ticker"]

    # Metadados para o catálogo web e index.html
    title = "Eulerpool — Template de Exemplo (Financial Data API)"
    description = (
        "Scraper modelo demonstrando a estrutura de coleta da API oficial Eulerpool. "
        "Utilize este arquivo como base para implementar novos endpoints financeiros."
    )
    icon = "🌐"
    icon_class = "icon-eulerpool"
    badge = "Eulerpool API"
    badge_class = "badge-dynamic"
    tags = ["eulerpool", "api", "template", "global"]
    source = "Eulerpool Financial Data (eulerpool.com)"

    # Endpoint da API (relativo a https://api.eulerpool.com)
    # Exemplo: "/api/1/trends/ticker-trends"
    endpoint = "/api/1/exemplo/dados"

    def fetch(self) -> pd.DataFrame:
        """
        Executa a coleta e transformação dos dados.
        Retorna um pd.DataFrame pronto para ser salvo em CSV.
        """
        # 1. Verifica se a chave de API está presente
        if not self.check_credentials():
            log.warning("Chave da Eulerpool ausente. Encerrando coleta.")
            return pd.DataFrame()

        # 2. Configura parâmetros de busca (se aplicável)
        params = {}
        if self.target_date:
            params["date"] = self.target_date.strftime("%Y-%m-%d")

        log.info(f"Consultando endpoint Eulerpool: {self.endpoint} com params: {params}")

        # 3. Faz a requisição autenticada e extrai os registros
        # O BaseEulerpoolScraper cuida do token Bearer, retries automáticos e desempacotamento
        registros = self.fetch_endpoint(self.endpoint, params=params)

        if not registros:
            log.warning("Nenhum dado retornado pela API da Eulerpool.")
            return pd.DataFrame()

        # 4. Transforma os registros recebidos no formato tabular desejado
        data_captura, _ = agora_brt()
        linhas_normalizadas = []

        for item in registros:
            linhas_normalizadas.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": item.get("date") or item.get("dataReferencia", ""),
                    "ticker": item.get("ticker") or item.get("symbol", ""),
                    "nome": item.get("name") or item.get("companyName", ""),
                    "preco": item.get("price") or item.get("close", ""),
                    "moeda": item.get("currency", "USD"),
                }
            )

        df = pd.DataFrame(linhas_normalizadas)
        log.info(f"{len(df)} registros preparados com sucesso.")
        return df


if __name__ == "__main__":
    EulerpoolTemplateScraper().run()
