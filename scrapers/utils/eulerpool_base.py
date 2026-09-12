"""
scrapers/utils/eulerpool_base.py
--------------------------------
Classe base para todos os scrapers que consomem dados do portal Eulerpool Financial Data API.
Integra-se nativamente ao BaseScraper e ao pipeline PulseFlat (run_all.py).
"""

import sys
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scrapers.utils.base import BaseScraper
from scrapers.utils.eulerpool_client import (
    EulerpoolAuthError,
    EulerpoolClient,
    EulerpoolMissingApiKeyError,
)
from utils.base import get_logger

log = get_logger("eulerpool_base")


class BaseEulerpoolScraper(BaseScraper):
    """
    Classe base especializada para scrapers que utilizam a API REST oficial da Eulerpool.
    Herda todas as funcionalidades de BaseScraper (deduplicação, particionamento, salvamento CSV,
    catálogo de metadados e compatibilidade com o orquestrador run_all.py).
    """

    # Configurações padrão de catálogo e pipeline
    group: str = "eulerpool"
    source: str = "Eulerpool Financial Data (eulerpool.com)"
    icon: str = "🌐"
    icon_class: str = "icon-eulerpool"
    badge: str = "Eulerpool API"
    badge_class: str = "badge-dynamic"
    enabled: bool = True
    phase: int = 1
    accumulate: bool = True

    # Endpoint da Eulerpool associado ao scraper (opcional para scrapers declarativos)
    # Exemplo: "/api/1/stocks/AAPL/financials"
    endpoint: str = ""

    def __init__(self, client: EulerpoolClient | None = None):
        super().__init__()
        self.client = client or EulerpoolClient()

    def check_credentials(self) -> bool:
        """Verifica se a chave da Eulerpool está configurada."""
        if not self.client.has_credentials:
            self.logger.warning(
                "Chave Eulerpool não configurada (EULERPOOL_API_KEY). "
                "Para coletar este dataset, configure sua chave no arquivo .env."
            )
            return False
        return True

    def extract_records(self, raw_data: Any) -> list[dict[str, Any]]:
        """
        Extrai uma lista de registros a partir da resposta JSON da Eulerpool.
        Lida com respostas em formato de lista direta ou envelopes comuns (data, results, tickers, items, etc.).
        """
        if raw_data is None:
            return []

        if isinstance(raw_data, list):
            return [item for item in raw_data if isinstance(item, dict)]

        if isinstance(raw_data, dict):
            for key in ("data", "results", "tickers", "items", "content", "resultado"):
                val = raw_data.get(key)
                if isinstance(val, list):
                    return [item for item in val if isinstance(item, dict)]

            # Se o próprio dict for o registro único
            return [raw_data]

        return []

    def fetch_endpoint(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Executa uma requisição GET autenticada ao endpoint especificado da Eulerpool
        e retorna a lista de registros extraída.
        """
        if not self.check_credentials():
            return []

        try:
            raw_data = self.client.get(endpoint, params=params)
            records = self.extract_records(raw_data)
            self.logger.info(f"[Eulerpool] {len(records)} registros retornados de {endpoint}")
            return records
        except EulerpoolMissingApiKeyError as e:
            self.logger.warning(str(e))
            return []
        except EulerpoolAuthError as e:
            self.logger.error(f"Falha de autenticação ao consultar {endpoint}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Erro ao requisitar dados da Eulerpool ({endpoint}): {e}")
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
