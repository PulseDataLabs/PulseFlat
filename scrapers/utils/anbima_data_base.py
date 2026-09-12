"""
scrapers/utils/anbima_data_base.py
----------------------------------
Classe base para todos os scrapers que consomem dados do portal ANBIMA Data / Developers.
Integra-se nativamente ao BaseScraper e ao pipeline PulseFlat (run_all.py).
"""

import sys
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scrapers.utils.anbima_data_client import (
    AnbimaAuthError,
    AnbimaDataClient,
    AnbimaMissingCredentialsError,
)
from scrapers.utils.base import BaseScraper
from utils.base import get_logger

log = get_logger("anbima_data_base")


class BaseAnbimaDataScraper(BaseScraper):
    """
    Classe base especializada para scrapers que utilizam a API oficial ANBIMA Data.
    Herda todas as funcionalidades de BaseScraper (deduplicação, particionamento, salvamento CSV,
    catálogo de metadados e compatibilidade com o orquestrador run_all.py).
    """

    # Configurações padrão de catálogo e pipeline
    group: str = "anbima"
    source: str = "ANBIMA Data (developers.anbima.com.br)"
    icon: str = "🏛️"
    icon_class: str = "icon-anbima"
    badge: str = "ANBIMA Data"
    badge_class: str = "badge-dynamic"
    enabled: bool = True
    phase: int = 1
    accumulate: bool = True

    # Endpoint da ANBIMA associado ao scraper (opcional para scrapers declarativos)
    endpoint: str = ""

    def __init__(self, client: AnbimaDataClient | None = None):
        super().__init__()
        self.client = client or AnbimaDataClient()

    def check_credentials(self) -> bool:
        """Verifica se as credenciais necessárias da ANBIMA estão configuradas."""
        if not self.client.has_credentials:
            self.logger.warning(
                "Credenciais ANBIMA não configuradas (ANBIMA_CLIENT_ID / ANBIMA_CLIENT_SECRET). "
                "Para coletar este dataset, configure suas credenciais no arquivo .env."
            )
            return False
        return True

    def extract_records(self, raw_data: Any) -> list[dict[str, Any]]:
        """
        Extrai uma lista de registros a partir da resposta JSON da ANBIMA.
        Lida com respostas em formato de lista direta ou encapsuladas em envelopes comuns
        (como 'data', 'content', 'itens', 'results', 'resultado', etc.).
        """
        if raw_data is None:
            return []

        if isinstance(raw_data, list):
            return [item for item in raw_data if isinstance(item, dict)]

        if isinstance(raw_data, dict):
            for key in ("data", "content", "itens", "items", "results", "resultado", "registros"):
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
        Executa uma requisição GET autenticada ao endpoint especificado e retorna
        a lista de registros já extraída.
        """
        if not self.check_credentials():
            return []

        try:
            raw_data = self.client.get(endpoint, params=params)
            records = self.extract_records(raw_data)
            self.logger.info(f"[ANBIMA Data] {len(records)} registros retornados de {endpoint}")
            return records
        except AnbimaMissingCredentialsError as e:
            self.logger.warning(str(e))
            return []
        except AnbimaAuthError as e:
            self.logger.error(f"Falha de autenticação ao consultar {endpoint}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Erro ao requisitar dados da ANBIMA ({endpoint}): {e}")
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

        df = pd.DataFrame(records)
        return df
