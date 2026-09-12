"""
scrapers/utils/anbima_data_client.py
------------------------------------
Cliente HTTP robusto para a API oficial ANBIMA Data / Developers.
Fonte: https://developers.anbima.com.br/pt/

Funcionalidades:
- Autenticação OAuth 2.0 via fluxo Client Credentials.
- Gerenciamento inteligente de token (cache em memória e auto-renovação pré-expiração).
- Injeção de cabeçalhos padrão (Bearer token, client_id, Accept: application/json).
- Retries automáticos com backoff exponencial para Rate Limiting (HTTP 429) e erros transientes (5xx).
- Método de diagnóstico test_connection() para validação de credenciais.
"""

import os
import time
from base64 import b64encode
from typing import Any

import requests

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from utils.base import get_logger, nova_session

log = get_logger("anbima_data_client")


class AnbimaDataError(Exception):
    """Exceção base para erros relacionados à API ANBIMA Data."""

    pass


class AnbimaMissingCredentialsError(AnbimaDataError):
    """Lançada quando ANBIMA_CLIENT_ID ou ANBIMA_CLIENT_SECRET não estão configurados."""

    pass


class AnbimaAuthError(AnbimaDataError):
    """Lançada quando a autenticação OAuth 2.0 falha (ex: credenciais inválidas)."""

    pass


class AnbimaRateLimitError(AnbimaDataError):
    """Lançada quando o limite de requisições por segundo/minuto é atingido (HTTP 429)."""

    pass


class AnbimaApiError(AnbimaDataError):
    """Lançada quando a API retorna um erro HTTP de negócio ou servidor (4xx/5xx)."""

    def __init__(self, message: str, status_code: int | None = None, response_body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class AnbimaDataClient:
    """Cliente especializado para comunicação com as APIs do portal ANBIMA Developers."""

    DEFAULT_OAUTH_URL = "https://api.anbima.com.br/oauth/access-token"
    DEFAULT_BASE_URL = "https://api.anbima.com.br"

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str | None = None,
        oauth_url: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
        session: requests.Session | None = None,
    ):
        if client_id is None:
            self.client_id = (
                os.getenv("ANBIMA_CLIENT_ID", "") or os.getenv("API_ANBIMA_CLIENT_ID", "")
            ).strip()
        else:
            self.client_id = client_id.strip()

        if client_secret is None:
            self.client_secret = (
                os.getenv("ANBIMA_CLIENT_SECRET", "") or os.getenv("API_ANBIMA_CLIENT_SECRET", "")
            ).strip()
        else:
            self.client_secret = client_secret.strip()
        self.base_url = (
            base_url or os.getenv("ANBIMA_API_BASE_URL", self.DEFAULT_BASE_URL)
        ).rstrip("/")
        self.oauth_url = (
            oauth_url or os.getenv("ANBIMA_OAUTH_URL", self.DEFAULT_OAUTH_URL)
        ).strip()
        self.timeout = timeout
        self.max_retries = max_retries

        self._session = session or nova_session()
        self._token: str | None = None
        self._token_expires_at: float = 0.0

    @property
    def has_credentials(self) -> bool:
        """Verifica se as credenciais mínimas estão presentes."""
        return bool(self.client_id and self.client_secret)

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        Obtém um access_token OAuth 2.0 válido.
        Se já existir um token em cache que não esteja próximo do vencimento (buffer de 60s),
        o mesmo é reutilizado sem fazer nova requisição de rede.
        """
        if not self.has_credentials:
            raise AnbimaMissingCredentialsError(
                "Credenciais da ANBIMA não configuradas. "
                "Defina ANBIMA_CLIENT_ID e ANBIMA_CLIENT_SECRET no arquivo .env ou variáveis de ambiente."
            )

        now = time.time()
        # Se o token existir e ainda tiver pelo menos 60 segundos de validade, reutiliza
        if not force_refresh and self._token and now < (self._token_expires_at - 60):
            return self._token

        log.info("[ANBIMA Data] Solicitando novo access token OAuth 2.0...")
        credencial = b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {credencial}",
            "Accept": "application/json",
        }
        payload = {"grant_type": "client_credentials"}

        try:
            resp = self._session.post(
                self.oauth_url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            raise AnbimaAuthError(f"Erro de conexão ao solicitar token OAuth ANBIMA: {e}") from e

        if resp.status_code in (400, 401, 403):
            raise AnbimaAuthError(
                f"Falha na autenticação ANBIMA (HTTP {resp.status_code}): {resp.text}"
            )

        try:
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise AnbimaAuthError(
                f"Resposta inválida do endpoint OAuth ANBIMA: {e} - Resposta: {resp.text}"
            ) from e

        token = data.get("access_token")
        if not token:
            raise AnbimaAuthError(f"Campo 'access_token' ausente na resposta OAuth: {data}")

        expires_in = int(data.get("expires_in", 3600))
        self._token = token
        self._token_expires_at = time.time() + expires_in
        log.info(f"[ANBIMA Data] Token obtido com sucesso (válido por ~{expires_in}s).")
        return self._token

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
        Executa uma chamada HTTP autenticada com retry automático em caso de rate-limit (429) ou 5xx.
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.timeout

        req_headers = {
            "Accept": "application/json",
            "client_id": self.client_id,
        }
        if headers:
            req_headers.update(headers)

        backoff = 2.0

        for tentativa in range(1, self.max_retries + 1):
            token = self.get_access_token()
            req_headers["Authorization"] = f"Bearer {token}"

            try:
                log.debug(
                    f"[ANBIMA Data] {method.upper()} {url} (tentativa {tentativa}/{self.max_retries})"
                )
                resp = self._session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    headers=req_headers,
                    timeout=timeout,
                    **kwargs,
                )

                # Se o token expirou remotamente (401), invalida cache local e tenta de novo
                if resp.status_code == 401 and tentativa < self.max_retries:
                    log.warning(
                        "[ANBIMA Data] Recebido HTTP 401 - renovando token e reexecutando..."
                    )
                    self._token = None
                    self._token_expires_at = 0.0
                    continue

                # Rate Limit (429)
                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    wait_time = float(retry_after) if retry_after else backoff
                    log.warning(
                        f"[ANBIMA Data] Rate limit atingido (HTTP 429). Aguardando {wait_time:.1f}s antes do retry..."
                    )
                    if tentativa == self.max_retries:
                        raise AnbimaRateLimitError(
                            f"Limite de requisições atingido na ANBIMA: {resp.text}"
                        )
                    time.sleep(wait_time)
                    backoff *= 2
                    continue

                # Erros transitórios de servidor (500, 502, 503, 504)
                if resp.status_code in (500, 502, 503, 504):
                    log.warning(
                        f"[ANBIMA Data] Erro do servidor ANBIMA HTTP {resp.status_code}. Aguardando {backoff:.1f}s..."
                    )
                    if tentativa == self.max_retries:
                        resp.raise_for_status()
                    time.sleep(backoff)
                    backoff *= 2
                    continue

                resp.raise_for_status()
                return resp

            except requests.HTTPError as e:
                status = e.response.status_code if e.response is not None else None
                body = e.response.text if e.response is not None else str(e)
                raise AnbimaApiError(
                    f"Erro na requisição ANBIMA [{method.upper()} {url}] (HTTP {status}): {body}",
                    status_code=status,
                    response_body=body,
                ) from e
            except requests.RequestException as e:
                if tentativa == self.max_retries:
                    raise AnbimaApiError(f"Falha de rede na requisição ANBIMA: {e}") from e
                log.warning(
                    f"[ANBIMA Data] Tentativa {tentativa} falhou: {e}. Aguardando {backoff}s..."
                )
                time.sleep(backoff)
                backoff *= 2

        raise AnbimaApiError("Número máximo de tentativas excedido.")

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
        Testa a autenticação com as credenciais atuais.
        Retorna um dicionário com o resultado do teste.
        """
        if not self.has_credentials:
            return {
                "ok": False,
                "message": "Credenciais não encontradas. Configure ANBIMA_CLIENT_ID e ANBIMA_CLIENT_SECRET no seu .env.",
                "client_id": self.client_id or "(vazio)",
                "oauth_url": self.oauth_url,
            }

        try:
            token = self.get_access_token(force_refresh=True)
            expires_in = int(self._token_expires_at - time.time())
            masked_token = f"{token[:8]}...{token[-6:]}" if len(token) > 14 else "***"
            return {
                "ok": True,
                "message": "Autenticação OAuth 2.0 bem-sucedida!",
                "client_id": self.client_id,
                "token_sample": masked_token,
                "expires_in_seconds": expires_in,
                "oauth_url": self.oauth_url,
                "base_url": self.base_url,
            }
        except Exception as e:
            return {
                "ok": False,
                "message": f"Falha na autenticação: {e}",
                "client_id": self.client_id,
                "oauth_url": self.oauth_url,
            }


if __name__ == "__main__":
    import json

    print("=== Teste de Conexão ANBIMA Data ===")
    client = AnbimaDataClient()
    resultado = client.test_connection()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
