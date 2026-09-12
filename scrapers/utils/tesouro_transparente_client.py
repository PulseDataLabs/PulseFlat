"""
scrapers/utils/tesouro_transparente_client.py
--------------------------------------------
Cliente HTTP especializado para a API CKAN do Tesouro Transparente (Tesouro Nacional).
Fonte: https://www.tesourotransparente.gov.br/ckan/api/3

Funcionalidades:
- Consulta simplificada ao catálogo e datastore CKAN (/action/datastore_search, /action/package_show).
- Retries automáticos com backoff exponencial para estabilidade de rede e rate limiting (429).
- Método test_connection() para diagnóstico de conectividade.
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

log = get_logger("tesouro_transparente_client")


class TesouroTransparenteError(Exception):
    """Exceção base para erros relacionados ao Tesouro Transparente."""

    pass


class TesouroTransparenteRateLimitError(TesouroTransparenteError):
    """Lançada quando o limite de requisições do portal é atingido (HTTP 429)."""

    pass


class TesouroTransparenteApiError(TesouroTransparenteError):
    """Lançada quando a API retorna erro HTTP ou success: false."""

    def __init__(self, message: str, status_code: int | None = None, response_body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class TesouroTransparenteClient:
    """Cliente especializado para comunicação com a API CKAN do Tesouro Nacional."""

    DEFAULT_BASE_URL = "https://www.tesourotransparente.gov.br/ckan/api/3"

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
        session: requests.Session | None = None,
    ):
        self.base_url = (
            base_url or os.getenv("TESOURO_TRANSPARENTE_BASE_URL", self.DEFAULT_BASE_URL)
        ).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = session or nova_session()

    def _build_url(self, endpoint: str) -> str:
        """Monta a URL completa para um determinado endpoint CKAN."""
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
        Executa uma requisição HTTP à API CKAN com retries automáticos.
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.timeout

        req_headers = {
            "Accept": "application/json",
            "User-Agent": "PulseFlat/1.0 (+https://github.com/PulseDataLabs/PulseFlat)",
        }
        if headers:
            req_headers.update(headers)

        backoff = 2.0

        for tentativa in range(1, self.max_retries + 1):
            try:
                log.debug(
                    f"[Tesouro Transparente] {method.upper()} {url} (tentativa {tentativa}/{self.max_retries})"
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

                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    wait_time = float(retry_after) if retry_after else backoff
                    log.warning(
                        f"[Tesouro Transparente] Rate limit atingido (HTTP 429). Aguardando {wait_time:.1f}s..."
                    )
                    if tentativa == self.max_retries:
                        raise TesouroTransparenteRateLimitError(
                            f"Limite de requisições atingido no Tesouro Transparente: {resp.text}"
                        )
                    time.sleep(wait_time)
                    backoff *= 2
                    continue

                if resp.status_code in (500, 502, 503, 504):
                    log.warning(
                        f"[Tesouro Transparente] Erro de servidor HTTP {resp.status_code}. Aguardando {backoff:.1f}s..."
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
                raise TesouroTransparenteApiError(
                    f"Erro na requisição Tesouro Transparente [{method.upper()} {url}] (HTTP {status}): {body}",
                    status_code=status,
                    response_body=body,
                ) from e
            except requests.RequestException as e:
                if tentativa == self.max_retries:
                    raise TesouroTransparenteApiError(
                        f"Falha de rede no Tesouro Transparente: {e}"
                    ) from e
                log.warning(
                    f"[Tesouro Transparente] Tentativa {tentativa} falhou: {e}. Aguardando {backoff}s..."
                )
                time.sleep(backoff)
                backoff *= 2

        raise TesouroTransparenteApiError(
            "Número máximo de tentativas excedido no Tesouro Transparente."
        )

    def get(self, endpoint: str, params: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        """Executa GET e retorna o conteúdo JSON parseado."""
        resp = self.request("GET", endpoint, params=params, **kwargs)
        if not resp.content or resp.content.strip() == b"null":
            return {}
        return resp.json()

    def datastore_search(
        self,
        resource_id: str,
        limit: int = 100,
        offset: int = 0,
        filters: dict[str, Any] | None = None,
        q: str | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Executa uma consulta datastore_search no recurso especificado e retorna a lista de registros.
        """
        params: dict[str, Any] = {
            "resource_id": resource_id,
            "limit": limit,
            "offset": offset,
        }
        if filters:
            import json

            params["filters"] = json.dumps(filters)
        if q:
            params["q"] = q

        data = self.get("/action/datastore_search", params=params, **kwargs)
        result = data.get("result", {})
        return result.get("records", [])

    def test_connection(self) -> dict[str, Any]:
        """
        Testa a conectividade com a API CKAN consultando os pacotes disponíveis.
        """
        t0 = time.time()
        try:
            resp = self.request("GET", "/action/package_list", params={"limit": 5}, timeout=15)
            elapsed = time.time() - t0
            data = resp.json() if resp.content else {}
            packages = data.get("result", [])
            return {
                "ok": True,
                "message": "Conexão com a API do Tesouro Transparente bem-sucedida!",
                "base_url": self.base_url,
                "status_code": resp.status_code,
                "latency_seconds": round(elapsed, 3),
                "sample_packages_count": len(packages),
            }
        except Exception as e:
            elapsed = time.time() - t0
            return {
                "ok": False,
                "message": f"Falha de conexão com o Tesouro Transparente: {e}",
                "base_url": self.base_url,
                "latency_seconds": round(elapsed, 3),
            }


if __name__ == "__main__":
    import json

    print("=== Teste de Conexão Tesouro Transparente (CKAN) ===")
    client = TesouroTransparenteClient()
    resultado = client.test_connection()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
