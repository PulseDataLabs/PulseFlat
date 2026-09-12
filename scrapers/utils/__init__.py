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
from .eulerpool_base import BaseEulerpoolScraper
from .eulerpool_client import (
    EulerpoolApiError,
    EulerpoolAuthError,
    EulerpoolClient,
    EulerpoolError,
    EulerpoolMissingApiKeyError,
    EulerpoolRateLimitError,
)

__all__ = [
    "BaseScraper",
    "AnbimaDataClient",
    "BaseAnbimaDataScraper",
    "AnbimaDataError",
    "AnbimaMissingCredentialsError",
    "AnbimaAuthError",
    "AnbimaRateLimitError",
    "AnbimaApiError",
    "EulerpoolClient",
    "BaseEulerpoolScraper",
    "EulerpoolError",
    "EulerpoolMissingApiKeyError",
    "EulerpoolAuthError",
    "EulerpoolRateLimitError",
    "EulerpoolApiError",
]
