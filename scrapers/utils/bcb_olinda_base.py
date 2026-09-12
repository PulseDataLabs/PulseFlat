"""
scrapers/utils/bcb_olinda_base.py
---------------------------------
Classe base para todos os scrapers que consomem dados OData do BCB Olinda.
Integra-se nativamente ao BaseScraper e ao pipeline PulseFlat (run_all.py).
"""

import sys
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scrapers.utils.base import BaseScraper
from scrapers.utils.bcb_olinda_client import BcbOlindaClient
from utils.base import get_logger

log = get_logger("bcb_olinda_base")


class BaseBcbOlindaScraper(BaseScraper):
    """
    Classe base especializada para scrapers que utilizam os serviços OData do Banco Central (Olinda).
    Herda todas as funcionalidades de BaseScraper (deduplicação, particionamento, salvamento CSV,
    catálogo de metadados e compatibilidade com o orquestrador run_all.py).
    """

    group: str = "bcb"
    source: str = "Banco Central do Brasil — Olinda (bcb.gov.br)"
    icon: str = "🏛️"
    icon_class: str = "icon-bcb"
    badge: str = "BCB Olinda"
    badge_class: str = "badge-dynamic"
    enabled: bool = True
    phase: int = 1
    accumulate: bool = True

    # Endpoint OData associado ao scraper (ex: '/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais')
    endpoint: str = ""

    def __init__(self, client: BcbOlindaClient | None = None):
        super().__init__()
        self.client = client or BcbOlindaClient()

    def extract_records(self, raw_data: Any) -> list[dict[str, Any]]:
        """
        Extrai a lista de registros a partir da resposta OData (chave padrão 'value').
        """
        if not raw_data:
            return []

        if isinstance(raw_data, list):
            return [item for item in raw_data if isinstance(item, dict)]

        if isinstance(raw_data, dict):
            val = raw_data.get("value")
            if isinstance(val, list):
                return [item for item in val if isinstance(item, dict)]
            return [raw_data]

        return []

    def fetch_endpoint(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Executa uma requisição GET ao endpoint especificado e retorna a lista de registros.
        """
        try:
            raw_data = self.client.get(endpoint, params=params)
            records = self.extract_records(raw_data)
            self.logger.info(f"[BCB Olinda] {len(records)} registros retornados de {endpoint}")
            return records
        except Exception as e:
            self.logger.error(f"Erro ao requisitar dados do BCB Olinda ({endpoint}): {e}")
            raise

    def fetch(self) -> pd.DataFrame:
        """
        Método padrão que deve ser implementado pelas subclasses específicas.
        """
        if not self.endpoint:
            raise NotImplementedError(
                f"O scraper {self.__class__.__name__} deve definir 'endpoint' ou implementar 'fetch()'."
            )

        records = self.fetch_endpoint(self.endpoint)
        if not records:
            return pd.DataFrame()

        return pd.DataFrame(records)
