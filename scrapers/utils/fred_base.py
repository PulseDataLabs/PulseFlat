"""
scrapers/utils/fred_base.py
---------------------------
Classe base para todos os scrapers que consomem dados do FRED (St. Louis Fed).
Integra-se nativamente ao BaseScraper e ao pipeline PulseFlat (run_all.py).
"""

import sys
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scrapers.utils.base import BaseScraper
from scrapers.utils.fred_client import (
    FredAuthError,
    FredClient,
    FredMissingApiKeyError,
)
from utils.base import get_logger

log = get_logger("fred_base")


class BaseFredScraper(BaseScraper):
    """
    Classe base especializada para scrapers que utilizam a API do Federal Reserve Economic Data (FRED).
    Herda todas as funcionalidades de BaseScraper (deduplicação, particionamento, salvamento CSV,
    catálogo de metadados e compatibilidade com o orquestrador run_all.py).
    """

    group: str = "fred"
    source: str = "Federal Reserve Economic Data — FRED (stlouisfed.org)"
    icon: str = "🦅"
    icon_class: str = "icon-fred"
    badge: str = "FRED Global"
    badge_class: str = "badge-dynamic"
    enabled: bool = True
    phase: int = 1
    accumulate: bool = True

    # Identificador da série do FRED (ex: 'DGS10', 'FEDFUNDS', 'DTWEXBGS')
    series_id: str = ""

    def __init__(self, client: FredClient | None = None):
        super().__init__()
        self.client = client or FredClient()

    def check_credentials(self) -> bool:
        """Verifica se a chave do FRED está configurada."""
        if not self.client.has_credentials:
            self.logger.warning(
                "Chave do FRED não configurada (FRED_API_KEY). "
                "Para coletar este dataset, configure sua chave no arquivo .env."
            )
            return False
        return True

    def extract_records(self, raw_data: Any) -> list[dict[str, Any]]:
        """
        Extrai a lista de observações retornada pelo FRED.
        """
        if raw_data is None:
            return []

        if isinstance(raw_data, list):
            return [item for item in raw_data if isinstance(item, dict)]

        if isinstance(raw_data, dict):
            obs = raw_data.get("observations")
            if isinstance(obs, list):
                return [item for item in obs if isinstance(item, dict)]
            return [raw_data]

        return []

    def fetch_series(
        self,
        series_id: str,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Consulta as observações da série informada.
        """
        if not self.check_credentials():
            return []

        try:
            records = self.client.get_series_observations(
                series_id=series_id,
                observation_start=start_date,
                observation_end=end_date,
                limit=limit,
            )
            self.logger.info(f"[FRED] {len(records)} observações retornadas de {series_id}")
            return records
        except FredMissingApiKeyError as e:
            self.logger.warning(str(e))
            return []
        except FredAuthError as e:
            self.logger.error(f"Falha de autenticação ao consultar FRED ({series_id}): {e}")
            raise
        except Exception as e:
            self.logger.error(f"Erro ao requisitar dados do FRED ({series_id}): {e}")
            raise

    def fetch(self) -> pd.DataFrame:
        """
        Método padrão que deve ser implementado pelas subclasses específicas.
        """
        if not self.series_id:
            raise NotImplementedError(
                f"O scraper {self.__class__.__name__} deve definir 'series_id' ou implementar 'fetch()'."
            )

        start_str = self.start_date.strftime("%Y-%m-%d") if self.start_date else None
        end_str = self.end_date.strftime("%Y-%m-%d") if self.end_date else None

        records = self.fetch_series(self.series_id, start_date=start_str, end_date=end_str)
        if not records:
            return pd.DataFrame()

        return pd.DataFrame(records)
