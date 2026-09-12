"""
scrapers/anbima_data_template.py
--------------------------------
Template e guia de referência para criação de novos scrapers baseados
na API do portal ANBIMA Developers (ANBIMA Data).

Fonte: https://developers.anbima.com.br/pt/

COMO USAR ESTE TEMPLATE:
1. Copie este arquivo para um novo nome, por exemplo: `scrapers/anbima_curvas_juros.py`
2. Ajuste o nome da classe, `name`, `title`, `description`, `tags`, etc.
3. Configure o `endpoint` da API (ex: '/feed/precos-indices/v1/...')
4. Implemente a lógica de extração e transformação no método `fetch()`.
5. Ative o scraper alterando `enabled = True`.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger

log = get_logger("anbima_data_template")


class AnbimaDataTemplateScraper(BaseAnbimaDataScraper):
    # Identificador único do dataset (gera data/anbima_exemplo_template.csv)
    name = "anbima_exemplo_template"

    # Pertence ao grupo ANBIMA no orquestrador PulseFlat
    group = "anbima"

    # Deixar False até que o endpoint e as regras do dataset específico sejam configurados
    enabled = False

    phase = 1
    accumulate = True

    # Chaves para evitar duplicatas em coletas diárias
    chaves_dedup = ["data_captura", "data_referencia", "codigo_identificador"]

    # Metadados para o catálogo web e index.html
    title = "ANBIMA — Template de Exemplo (ANBIMA Data)"
    description = (
        "Scraper modelo demonstrando a estrutura de coleta da API oficial ANBIMA Data. "
        "Utilize este arquivo como base para implementar novos endpoints."
    )
    icon = "🏛️"
    icon_class = "icon-anbima"
    badge = "ANBIMA Data"
    badge_class = "badge-dynamic"
    tags = ["anbima", "api", "template"]
    source = "ANBIMA Data (developers.anbima.com.br)"

    # Endpoint da API (relativo à base_url https://api.anbima.com.br)
    # Exemplo: "/feed/precos-indices/v1/titulos-publicos/curvas-juros"
    endpoint = "/feed/exemplo/v1/dados"

    def fetch(self) -> pd.DataFrame:
        """
        Executa a coleta e transformação dos dados.
        Retorna um pd.DataFrame pronto para ser salvo em CSV.
        """
        # 1. Verifica se as credenciais estão presentes
        if not self.check_credentials():
            log.warning("Credenciais da ANBIMA ausentes. Encerrando coleta.")
            return pd.DataFrame()

        # 2. Configura parâmetros de busca (ex: data alvo, filtros)
        data_ref = self.target_date.strftime("%Y-%m-%d") if self.target_date else None
        params = {}
        if data_ref:
            params["data"] = data_ref

        log.info(f"Consultando endpoint ANBIMA Data: {self.endpoint} com params: {params}")

        # 3. Faz a requisição autenticada e extrai os registros
        # O BaseAnbimaDataScraper cuida do token OAuth2, cabeçalhos, retries e extração
        registros = self.fetch_endpoint(self.endpoint, params=params)

        if not registros:
            log.warning("Nenhum dado retornado pela API da ANBIMA.")
            return pd.DataFrame()

        # 4. Transforma os registros recebidos no formato desejado
        data_captura, _ = agora_brt()
        linhas_normalizadas = []

        for item in registros:
            linhas_normalizadas.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": item.get("dataReferencia")
                    or item.get("data", data_ref or ""),
                    "codigo_identificador": item.get("codigo") or item.get("id", ""),
                    "descricao": item.get("nome") or item.get("descricao", ""),
                    "valor": item.get("valor", ""),
                }
            )

        df = pd.DataFrame(linhas_normalizadas)
        log.info(f"{len(df)} registros preparados com sucesso.")
        return df


if __name__ == "__main__":
    AnbimaDataTemplateScraper().run()
