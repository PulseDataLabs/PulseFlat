"""
scrapers/utils/brasilapi_base.py
--------------------------------
Classe base para todos os scrapers que consomem dados da BrasilAPI.
Integra-se nativamente ao BaseScraper e ao pipeline PulseFlat (run_all.py).
"""

import sys
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scrapers.utils.base import BaseScraper
from scrapers.utils.brasilapi_client import (
    BrasilApiClient,
    BrasilApiNotFoundError,
)
from utils.base import get_logger

log = get_logger("brasilapi_base")


class BaseBrasilApiScraper(BaseScraper):
    """
    Classe base especializada para scrapers que utilizam a BrasilAPI.
    Herda todas as funcionalidades de BaseScraper (deduplicação, particionamento, salvamento CSV,
    catálogo de metadados e compatibilidade com o orquestrador run_all.py).
    """

    # Configurações padrão de catálogo e pipeline
    group: str = "brasilapi"
    source: str = "BrasilAPI (brasilapi.com.br)"
    icon: str = "🇧🇷"
    icon_class: str = "icon-brasilapi"
    badge: str = "BrasilAPI"
    badge_class: str = "badge-dynamic"
    enabled: bool = True
    phase: int = 1
    accumulate: bool = True

    # Endpoint da BrasilAPI associado ao scraper (opcional para scrapers declarativos)
    # Exemplo: "/taxas/v1", "/banks/v1", "/cvm/corretoras/v1"
    endpoint: str = ""

    def __init__(self, client: BrasilApiClient | None = None):
        super().__init__()
        self.client = client or BrasilApiClient()

    def extract_records(self, raw_data: Any) -> list[dict[str, Any]]:
        """
        Extrai uma lista de registros a partir da resposta JSON da BrasilAPI.
        Lida com respostas em formato de lista direta ou envelopes de objetos únicos.
        """
        if raw_data is None:
            return []

        if isinstance(raw_data, list):
            return [item for item in raw_data if isinstance(item, dict)]

        if isinstance(raw_data, dict):
            # Se for um envelope comum
            for key in ("data", "results", "itens", "items", "content"):
                val = raw_data.get(key)
                if isinstance(val, list):
                    return [item for item in val if isinstance(item, dict)]

            # Se o próprio dict for o registro
            return [raw_data]

        return []

    def fetch_endpoint(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Executa uma requisição GET ao endpoint especificado da BrasilAPI
        e retorna a lista de registros extraída.
        """
        try:
            raw_data = self.client.get(endpoint, params=params)
            records = self.extract_records(raw_data)
            self.logger.info(f"[BrasilAPI] {len(records)} registros retornados de {endpoint}")
            return records
        except BrasilApiNotFoundError as e:
            self.logger.warning(f"Recurso não encontrado na BrasilAPI ({endpoint}): {e}")
            return []
        except Exception as e:
            self.logger.error(f"Erro ao requisitar dados da BrasilAPI ({endpoint}): {e}")
            raise

    def fetch(self) -> pd.DataFrame:
        """
        Método padrão que deve ser implementado pelas subclasses específicas.
        Se 'endpoint' estiver definido na classe, tenta consultá-lo por padrão.
        """
        if not self.endpoint:
            raise NotImplementedError(
                f"O scraper {self.__class__.__name__} deve definir 'endpoint' ou implementar 'fetch()'."
            )

        records = self.fetch_endpoint(self.endpoint)
        if not records:
            return pd.DataFrame()

        return pd.DataFrame(records)
