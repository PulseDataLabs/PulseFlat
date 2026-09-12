"""
scrapers/utils/eulerpool_client.py
----------------------------------
Cliente HTTP robusto para a API oficial Eulerpool Financial Data.
Fonte: https://eulerpool.com/developers / https://api.eulerpool.com

Funcionalidades:
- Autenticação via Bearer token / apiKey através de EULERPOOL_API_KEY.
- Injeção de cabeçalhos padrão (Authorization: Bearer <token>, Accept: application/json).
- Retries automáticos com backoff exponencial para Rate Limiting (HTTP 429) e erros transientes (5xx).
- Método de diagnóstico test_connection() para validação de credenciais.
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

log = get_logger("eulerpool_client")


class EulerpoolError(Exception):
    """Exceção base para erros relacionados à API Eulerpool."""

    pass


class EulerpoolMissingApiKeyError(EulerpoolError):
    """Lançada quando EULERPOOL_API_KEY não está configurada."""

    pass


class EulerpoolAuthError(EulerpoolError):
    """Lançada quando a autenticação falha (HTTP 401/403)."""

    pass


class EulerpoolRateLimitError(EulerpoolError):
    """Lançada quando o limite de requisições é atingido (HTTP 429)."""

    pass


class EulerpoolApiError(EulerpoolError):
    """Lançada quando a API retorna erro HTTP de negócio ou servidor (4xx/5xx)."""

    def __init__(self, message: str, status_code: int | None = None, response_body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class EulerpoolClient:
    """Cliente especializado para comunicação com a API REST da Eulerpool."""

    DEFAULT_BASE_URL = "https://api.eulerpool.com"

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
        session: requests.Session | None = None,
    ):
        if api_key is None:
            self.api_key = (
                os.getenv("EULERPOOL_API_KEY", "")
                or os.getenv("API_EULERPOOL_KEY", "")
                or os.getenv("EULERPOOL_TOKEN", "")
            ).strip()
        else:
            self.api_key = api_key.strip()

        self.base_url = (
            base_url or os.getenv("EULERPOOL_API_BASE_URL", self.DEFAULT_BASE_URL)
        ).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = session or nova_session()

    @property
    def has_credentials(self) -> bool:
        """Verifica se a API Key da Eulerpool está configurada."""
        return bool(self.api_key)

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
        Executa uma requisição HTTP autenticada com retry automático em caso de rate limit (429) ou erro de servidor (5xx).
        """
        if not self.has_credentials:
            raise EulerpoolMissingApiKeyError(
                "Chave de API Eulerpool não configurada. "
                "Defina EULERPOOL_API_KEY no arquivo .env ou variáveis de ambiente."
            )

        url = self._build_url(endpoint)
        timeout = timeout or self.timeout

        req_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if headers:
            req_headers.update(headers)

        req_params = dict(params) if params else {}

        backoff = 2.0

        for tentativa in range(1, self.max_retries + 1):
            try:
                log.debug(
                    f"[Eulerpool] {method.upper()} {url} (tentativa {tentativa}/{self.max_retries})"
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

                # Autenticação inválida / Plano insuficiente
                if resp.status_code in (401, 403):
                    raise EulerpoolAuthError(
                        f"Falha de autenticação/permissão Eulerpool (HTTP {resp.status_code}): {resp.text}"
                    )

                # Rate Limit (429)
                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    wait_time = float(retry_after) if retry_after else backoff
                    log.warning(
                        f"[Eulerpool] Rate limit atingido (HTTP 429). Aguardando {wait_time:.1f}s antes do retry..."
                    )
                    if tentativa == self.max_retries:
                        raise EulerpoolRateLimitError(
                            f"Limite de requisições atingido na Eulerpool: {resp.text}"
                        )
                    time.sleep(wait_time)
                    backoff *= 2
                    continue

                # Erros de servidor (500, 502, 503, 504)
                if resp.status_code in (500, 502, 503, 504):
                    log.warning(
                        f"[Eulerpool] Erro de servidor Eulerpool HTTP {resp.status_code}. Aguardando {backoff:.1f}s..."
                    )
                    if tentativa == self.max_retries:
                        resp.raise_for_status()
                    time.sleep(backoff)
                    backoff *= 2
                    continue

                resp.raise_for_status()
                return resp

            except EulerpoolAuthError:
                raise
            except requests.HTTPError as e:
                status = e.response.status_code if e.response is not None else None
                body = e.response.text if e.response is not None else str(e)
                raise EulerpoolApiError(
                    f"Erro na requisição Eulerpool [{method.upper()} {url}] (HTTP {status}): {body}",
                    status_code=status,
                    response_body=body,
                ) from e
            except requests.RequestException as e:
                if tentativa == self.max_retries:
                    raise EulerpoolApiError(f"Falha de rede na requisição Eulerpool: {e}") from e
                log.warning(
                    f"[Eulerpool] Tentativa {tentativa} falhou: {e}. Aguardando {backoff}s..."
                )
                time.sleep(backoff)
                backoff *= 2

        raise EulerpoolApiError("Número máximo de tentativas excedido na Eulerpool.")

    def get(self, endpoint: str, params: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        """Executa GET autenticado e retorna o conteúdo JSON parseado."""
        resp = self.request("GET", endpoint, params=params, **kwargs)
        if not resp.content or resp.content.strip() == b"null":
            return []
        return resp.json()

    def post(self, endpoint: str, json_data: Any | None = None, **kwargs: Any) -> Any:
        """Executa POST autenticado e retorna o conteúdo JSON parseado."""
        resp = self.request("POST", endpoint, json_data=json_data, **kwargs)
        if not resp.content or resp.content.strip() == b"null":
            return []
        return resp.json()

    def test_connection(self) -> dict[str, Any]:
        """
        Testa a autenticação com as credenciais atuais chamando um endpoint leve.
        Retorna um dicionário com o resultado do teste.
        """
        if not self.has_credentials:
            return {
                "ok": False,
                "message": "API Key não encontrada. Configure EULERPOOL_API_KEY no seu arquivo .env.",
                "api_key": "(vazio)",
                "base_url": self.base_url,
            }

        try:
            # Testa contra endpoint leve de status ou tendências
            resp = self.request("GET", "/api/1/trends/ticker-trends", timeout=10)
            masked_key = (
                f"{self.api_key[:6]}...{self.api_key[-4:]}" if len(self.api_key) > 10 else "***"
            )
            return {
                "ok": True,
                "message": "Autenticação e conexão com Eulerpool bem-sucedidas!",
                "api_key_sample": masked_key,
                "base_url": self.base_url,
                "status_code": resp.status_code,
            }
        except EulerpoolAuthError as e:
            return {
                "ok": False,
                "message": f"Chave inválida ou não autorizada: {e}",
                "base_url": self.base_url,
            }
        except Exception as e:
            return {
                "ok": False,
                "message": f"Erro de conexão com a Eulerpool: {e}",
                "base_url": self.base_url,
            }


if __name__ == "__main__":
    import json

    print("=== Teste de Conexão Eulerpool API ===")
    client = EulerpoolClient()
    resultado = client.test_connection()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
