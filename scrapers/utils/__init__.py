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
from .bcb_olinda_base import BaseBcbOlindaScraper
from .bcb_olinda_client import (
    BcbOlindaApiError,
    BcbOlindaClient,
    BcbOlindaError,
    BcbOlindaRateLimitError,
)
from .brasilapi_base import BaseBrasilApiScraper
from .brasilapi_client import (
    BrasilApiClient,
    BrasilApiError,
    BrasilApiHttpError,
    BrasilApiNotFoundError,
    BrasilApiRateLimitError,
)
from .eulerpool_base import BaseEulerpoolScraper
from .eulerpool_client import (
    EulerpoolApiError,
    EulerpoolAuthError,
    EulerpoolClient,
    EulerpoolError,
    EulerpoolMissingApiKeyError,
    EulerpoolRateLimitError,
)
from .fred_base import BaseFredScraper
from .fred_client import (
    FredApiError,
    FredAuthError,
    FredClient,
    FredError,
    FredMissingApiKeyError,
    FredRateLimitError,
)
from .tesouro_transparente_base import BaseTesouroTransparenteScraper
from .tesouro_transparente_client import (
    TesouroTransparenteApiError,
    TesouroTransparenteClient,
    TesouroTransparenteError,
    TesouroTransparenteRateLimitError,
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
    "BrasilApiClient",
    "BaseBrasilApiScraper",
    "BrasilApiError",
    "BrasilApiNotFoundError",
    "BrasilApiRateLimitError",
    "BrasilApiHttpError",
    "BcbOlindaClient",
    "BaseBcbOlindaScraper",
    "BcbOlindaError",
    "BcbOlindaRateLimitError",
    "BcbOlindaApiError",
    "TesouroTransparenteClient",
    "BaseTesouroTransparenteScraper",
    "TesouroTransparenteError",
    "TesouroTransparenteRateLimitError",
    "TesouroTransparenteApiError",
    "FredClient",
    "BaseFredScraper",
    "FredError",
    "FredMissingApiKeyError",
    "FredAuthError",
    "FredRateLimitError",
    "FredApiError",
]
