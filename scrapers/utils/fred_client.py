"""
scrapers/utils/fred_client.py
-----------------------------
Cliente HTTP especializado para a API do FRED (Federal Reserve Economic Data - St. Louis Fed).
Fonte: https://fred.stlouisfed.org/docs/api/fred/

Funcionalidades:
- Autenticação via FRED_API_KEY (injetada como api_key e file_type=json).
- Retries automáticos com backoff exponencial para Rate Limiting (HTTP 429) e erros de servidor (5xx).
- Método test_connection() para diagnóstico de conectividade e validação da chave.
"""

import os
import time
from typing import Any

import requests

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from utils.base import get_logger, nova_session

log = get_logger("fred_client")


class FredError(Exception):
    """Exceção base para erros relacionados à API do FRED."""

    pass


class FredMissingApiKeyError(FredError):
    """Lançada quando FRED_API_KEY não está configurada."""

    pass


class FredAuthError(FredError):
    """Lançada quando a chave de API do FRED é inválida (HTTP 400 com erro de api_key ou 401/403)."""

    pass


class FredRateLimitError(FredError):
    """Lançada quando o limite de requisições do FRED é atingido (HTTP 429)."""

    pass


class FredApiError(FredError):
    """Lançada quando a API retorna erro HTTP de negócio ou servidor (4xx/5xx)."""

    def __init__(self, message: str, status_code: int | None = None, response_body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class FredClient:
    """Cliente especializado para comunicação com a API REST do FRED."""

    DEFAULT_BASE_URL = "https://api.stlouisfed.org/fred"

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
        session: requests.Session | None = None,
    ):
        if api_key is None:
            self.api_key = (os.getenv("FRED_API_KEY", "") or os.getenv("API_FRED_KEY", "")).strip()
        else:
            self.api_key = api_key.strip()

        self.base_url = (base_url or os.getenv("FRED_BASE_URL", self.DEFAULT_BASE_URL)).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = session or nova_session()

    @property
    def has_credentials(self) -> bool:
        """Verifica se a API Key do FRED está configurada."""
        return bool(self.api_key)

    def _build_url(self, endpoint: str) -> str:
        """Monta a URL completa para um determinado endpoint FRED."""
        endpoint = endpoint.strip()
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        return f"{self.base_url}{endpoint}"

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: Any | None = None,
        headers: dict[str, str] | None = None,
        timeout: int | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Executa uma requisição HTTP autenticada com injeção de api_key e file_type=json.
        """
        if not self.has_credentials:
            raise FredMissingApiKeyError(
                "Chave de API do FRED não configurada. "
                "Defina FRED_API_KEY no arquivo .env ou variáveis de ambiente."
            )

        url = self._build_url(endpoint)
        timeout = timeout or self.timeout

        req_headers = {
            "Accept": "application/json",
            "User-Agent": "PulseFlat/1.0 (+https://github.com/PulseDataLabs/PulseFlat)",
        }
        if headers:
            req_headers.update(headers)

        req_params = dict(params) if params else {}
        req_params["api_key"] = self.api_key
        req_params["file_type"] = "json"

        backoff = 2.0

        for tentativa in range(1, self.max_retries + 1):
            try:
                log.debug(
                    f"[FRED] {method.upper()} {url} (tentativa {tentativa}/{self.max_retries})"
                )
                resp = self._session.request(
                    method=method,
                    url=url,
                    params=req_params,
                    json=json_data,
                    headers=req_headers,
                    timeout=timeout,
                    **kwargs,
                )

                # O FRED retorna 400 com mensagem explicativa quando a chave é inválida
                if resp.status_code == 400 and "api_key" in resp.text.lower():
                    raise FredAuthError(f"Chave de API do FRED inválida: {resp.text}")

                if resp.status_code in (401, 403):
                    raise FredAuthError(
                        f"Acesso negado no FRED (HTTP {resp.status_code}): {resp.text}"
                    )

                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    wait_time = float(retry_after) if retry_after else backoff
                    log.warning(
                        f"[FRED] Rate limit atingido (HTTP 429). Aguardando {wait_time:.1f}s..."
                    )
                    if tentativa == self.max_retries:
                        raise FredRateLimitError(
                            f"Limite de requisições atingido no FRED: {resp.text}"
                        )
                    time.sleep(wait_time)
                    backoff *= 2
                    continue

                if resp.status_code in (500, 502, 503, 504):
                    log.warning(
                        f"[FRED] Erro de servidor HTTP {resp.status_code}. Aguardando {backoff:.1f}s..."
                    )
                    if tentativa == self.max_retries:
                        resp.raise_for_status()
                    time.sleep(backoff)
                    backoff *= 2
                    continue

                resp.raise_for_status()
                return resp

            except FredAuthError:
                raise
            except requests.HTTPError as e:
                status = e.response.status_code if e.response is not None else None
                body = e.response.text if e.response is not None else str(e)
                raise FredApiError(
                    f"Erro na requisição FRED [{method.upper()} {url}] (HTTP {status}): {body}",
                    status_code=status,
                    response_body=body,
                ) from e
            except requests.RequestException as e:
                if tentativa == self.max_retries:
                    raise FredApiError(f"Falha de rede na requisição FRED: {e}") from e
                log.warning(f"[FRED] Tentativa {tentativa} falhou: {e}. Aguardando {backoff}s...")
                time.sleep(backoff)
                backoff *= 2

        raise FredApiError("Número máximo de tentativas excedido no FRED.")

    def get(self, endpoint: str, params: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        """Executa GET e retorna o conteúdo JSON parseado."""
        resp = self.request("GET", endpoint, params=params, **kwargs)
        if not resp.content or resp.content.strip() == b"null":
            return {}
        return resp.json()

    def get_series_observations(
        self,
        series_id: str,
        observation_start: str | None = None,
        observation_end: str | None = None,
        limit: int | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Consulta as observações de uma série temporal específica (ex: 'DGS10' para US 10Y Treasury).
        """
        params: dict[str, Any] = {"series_id": series_id}
        if observation_start:
            params["observation_start"] = observation_start
        if observation_end:
            params["observation_end"] = observation_end
        if limit:
            params["limit"] = limit

        data = self.get("/series/observations", params=params, **kwargs)
        return data.get("observations", [])

    def test_connection(self) -> dict[str, Any]:
        """
        Testa a autenticação e conectividade com a API do FRED chamando metadados de US 10Y (DGS10).
        """
        if not self.has_credentials:
            return {
                "ok": False,
                "message": "API Key do FRED não encontrada. Configure FRED_API_KEY no seu arquivo .env.",
                "api_key": "(vazio)",
                "base_url": self.base_url,
            }

        t0 = time.time()
        try:
            resp = self.request("GET", "/series", params={"series_id": "DGS10"}, timeout=10)
            elapsed = time.time() - t0
            masked_key = (
                f"{self.api_key[:6]}...{self.api_key[-4:]}" if len(self.api_key) > 10 else "***"
            )
            return {
                "ok": True,
                "message": "Autenticação e conexão com FRED bem-sucedidas!",
                "api_key_sample": masked_key,
                "base_url": self.base_url,
                "status_code": resp.status_code,
                "latency_seconds": round(elapsed, 3),
            }
        except FredAuthError as e:
            return {
                "ok": False,
                "message": f"Chave inválida ou não autorizada no FRED: {e}",
                "base_url": self.base_url,
            }
        except Exception as e:
            return {
                "ok": False,
                "message": f"Erro de conexão com o FRED: {e}",
                "base_url": self.base_url,
            }


if __name__ == "__main__":
    import json

    print("=== Teste de Conexão FRED API ===")
    client = FredClient()
    resultado = client.test_connection()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
