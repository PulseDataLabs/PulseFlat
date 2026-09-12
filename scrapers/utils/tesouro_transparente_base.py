"""
scrapers/utils/tesouro_transparente_base.py
-------------------------------------------
Classe base para todos os scrapers que consomem dados do Tesouro Transparente (CKAN).
Integra-se nativamente ao BaseScraper e ao pipeline PulseFlat (run_all.py).
"""

import sys
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scrapers.utils.base import BaseScraper
from scrapers.utils.tesouro_transparente_client import TesouroTransparenteClient
from utils.base import get_logger

log = get_logger("tesouro_transparente_base")


class BaseTesouroTransparenteScraper(BaseScraper):
    """
    Classe base especializada para scrapers que utilizam a API CKAN do Tesouro Nacional.
    Herda todas as funcionalidades de BaseScraper (deduplicação, particionamento, salvamento CSV,
    catálogo de metadados e compatibilidade com o orquestrador run_all.py).
    """

    group: str = "tesouro"
    source: str = "Tesouro Transparente — Tesouro Nacional (tesourotransparente.gov.br)"
    icon: str = "🪙"
    icon_class: str = "icon-tesouro"
    badge: str = "Tesouro Direto"
    badge_class: str = "badge-dynamic"
    enabled: bool = True
    phase: int = 1
    accumulate: bool = True

    # Resource ID CKAN associado ao dataset
    resource_id: str = ""

    def __init__(self, client: TesouroTransparenteClient | None = None):
        super().__init__()
        self.client = client or TesouroTransparenteClient()

    def extract_records(self, raw_data: Any) -> list[dict[str, Any]]:
        """
        Extrai os registros da resposta CKAN (result.records ou lista direta).
        """
        if raw_data is None:
            return []

        if isinstance(raw_data, list):
            return [item for item in raw_data if isinstance(item, dict)]

        if isinstance(raw_data, dict):
            res = raw_data.get("result", raw_data)
            if isinstance(res, dict):
                records = res.get("records")
                if isinstance(records, list):
                    return [item for item in records if isinstance(item, dict)]
            return [raw_data]

        return []

    def fetch_resource(
        self, resource_id: str, limit: int = 500, filters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Consulta o datastore CKAN para o resource_id especificado.
        """
        try:
            records = self.client.datastore_search(
                resource_id=resource_id, limit=limit, filters=filters
            )
            self.logger.info(
                f"[Tesouro Transparente] {len(records)} registros retornados de {resource_id}"
            )
            return records
        except Exception as e:
            self.logger.error(f"Erro ao consultar Tesouro Transparente ({resource_id}): {e}")
            raise

    def fetch(self) -> pd.DataFrame:
        """
        Método padrão que deve ser implementado pelas subclasses específicas.
        """
        if not self.resource_id:
            raise NotImplementedError(
                f"O scraper {self.__class__.__name__} deve definir 'resource_id' ou implementar 'fetch()'."
            )

        records = self.fetch_resource(self.resource_id)
        if not records:
            return pd.DataFrame()

        return pd.DataFrame(records)
