"""
scrapers/utils
--------------
Utilitários e classes-base compartilhadas para os scrapers do PulseFlat.
"""

from .anbima_data_base import BaseAnbimaDataScraper
from .anbima_data_client import (
    AnbimaApiError,
    AnbimaAuthError,
    AnbimaDataClient,
    AnbimaDataError,
    AnbimaMissingCredentialsError,
    AnbimaRateLimitError,
)
from .base import BaseScraper

__all__ = [
    "BaseScraper",
    "AnbimaDataClient",
    "BaseAnbimaDataScraper",
    "AnbimaDataError",
    "AnbimaMissingCredentialsError",
    "AnbimaAuthError",
    "AnbimaRateLimitError",
    "AnbimaApiError",
]
