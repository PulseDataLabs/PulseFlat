"""
scrapers/utils/brasilapi_client.py
----------------------------------
Cliente HTTP robusto para a BrasilAPI.
Fonte: https://brasilapi.com.br/docs / https://brasilapi.com.br/api

Funcionalidades:
- Cliente HTTP com cabeçalhos apropriados (User-Agent amigável e Accept: application/json).
- Retries automáticos com backoff exponencial para Rate Limiting (HTTP 429) e erros de servidor (5xx).
- Método de diagnóstico test_connection() para validação de conectividade e latência.
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

log = get_logger("brasilapi_client")


class BrasilApiError(Exception):
    """Exceção base para erros relacionados à BrasilAPI."""

    pass


class BrasilApiNotFoundError(BrasilApiError):
    """Lançada quando um recurso ou registro específico não é encontrado (HTTP 404)."""

    pass


class BrasilApiRateLimitError(BrasilApiError):
    """Lançada quando o limite de requisições da BrasilAPI é atingido (HTTP 429)."""

    pass


class BrasilApiHttpError(BrasilApiError):
    """Lançada quando a BrasilAPI retorna erro HTTP (4xx/5xx)."""

    def __init__(self, message: str, status_code: int | None = None, response_body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class BrasilApiClient:
    """Cliente especializado para comunicação com a BrasilAPI."""

    DEFAULT_BASE_URL = "https://brasilapi.com.br/api"

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
        session: requests.Session | None = None,
    ):
        self.base_url = (base_url or os.getenv("BRASILAPI_BASE_URL", self.DEFAULT_BASE_URL)).rstrip(
            "/"
        )
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = session or nova_session()

    def _build_url(self, endpoint: str) -> str:
        """Monta a URL completa para um determinado endpoint."""
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
        Executa uma chamada HTTP com retry automático em caso de 429 ou 5xx.
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.timeout

        req_headers = {
            "Accept": "application/json",
            "User-Agent": "PulseFlat/1.0 (+https://github.com/PulseDataLabs/PulseFlat)",
        }
        if headers:
            req_headers.update(headers)

        req_params = dict(params) if params else {}

        backoff = 2.0

        for tentativa in range(1, self.max_retries + 1):
            try:
                log.debug(
                    f"[BrasilAPI] {method.upper()} {url} (tentativa {tentativa}/{self.max_retries})"
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

                # Não encontrado
                if resp.status_code == 404:
                    raise BrasilApiNotFoundError(
                        f"Recurso não encontrado na BrasilAPI ({url}): {resp.text}"
                    )

                # Rate Limit (429)
                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    wait_time = float(retry_after) if retry_after else backoff
                    log.warning(
                        f"[BrasilAPI] Rate limit atingido (HTTP 429). Aguardando {wait_time:.1f}s antes do retry..."
                    )
                    if tentativa == self.max_retries:
                        raise BrasilApiRateLimitError(
                            f"Limite de requisições excedido na BrasilAPI: {resp.text}"
                        )
                    time.sleep(wait_time)
                    backoff *= 2
                    continue

                # Erros transitórios de servidor (500, 502, 503, 504)
                if resp.status_code in (500, 502, 503, 504):
                    log.warning(
                        f"[BrasilAPI] Erro de servidor BrasilAPI HTTP {resp.status_code}. Aguardando {backoff:.1f}s..."
                    )
                    if tentativa == self.max_retries:
                        resp.raise_for_status()
                    time.sleep(backoff)
                    backoff *= 2
                    continue

                resp.raise_for_status()
                return resp

            except BrasilApiNotFoundError:
                raise
            except requests.HTTPError as e:
                status = e.response.status_code if e.response is not None else None
                body = e.response.text if e.response is not None else str(e)
                raise BrasilApiHttpError(
                    f"Erro na requisição BrasilAPI [{method.upper()} {url}] (HTTP {status}): {body}",
                    status_code=status,
                    response_body=body,
                ) from e
            except requests.RequestException as e:
                if tentativa == self.max_retries:
                    raise BrasilApiError(f"Falha de rede na requisição BrasilAPI: {e}") from e
                log.warning(
                    f"[BrasilAPI] Tentativa {tentativa} falhou: {e}. Aguardando {backoff}s..."
                )
                time.sleep(backoff)
                backoff *= 2

        raise BrasilApiError("Número máximo de tentativas excedido na BrasilAPI.")

    def get(self, endpoint: str, params: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        """Executa GET e retorna o conteúdo JSON parseado."""
        resp = self.request("GET", endpoint, params=params, **kwargs)
        if not resp.content or resp.content.strip() == b"null":
            return []
        return resp.json()

    def test_connection(self) -> dict[str, Any]:
        """
        Testa a conectividade chamando o endpoint estável de taxas oficiais (/taxas/v1).
        Retorna um dicionário com o resultado do teste e tempo de resposta.
        """
        t0 = time.time()
        try:
            resp = self.request("GET", "/taxas/v1", timeout=10)
            elapsed = time.time() - t0
            data = resp.json() if resp.content else []
            return {
                "ok": True,
                "message": "Conexão com a BrasilAPI realizada com sucesso!",
                "base_url": self.base_url,
                "status_code": resp.status_code,
                "latency_seconds": round(elapsed, 3),
                "sample_count": len(data) if isinstance(data, list) else 1,
            }
        except Exception as e:
            elapsed = time.time() - t0
            return {
                "ok": False,
                "message": f"Erro de conexão com a BrasilAPI: {e}",
                "base_url": self.base_url,
                "latency_seconds": round(elapsed, 3),
            }


if __name__ == "__main__":
    import json

    print("=== Teste de Conexão BrasilAPI ===")
    client = BrasilApiClient()
    resultado = client.test_connection()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
