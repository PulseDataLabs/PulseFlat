"""
scrapers/utils/bcb_olinda_client.py
----------------------------------
Cliente HTTP especializado para a API OData do Banco Central do Brasil (BCB Olinda).
Fonte: https://olinda.bcb.gov.br/olinda/servico

Funcionalidades:
- Suporte nativo a parâmetros do protocolo OData ($format=json, $top, $skip, $filter, $select, $orderby).
- Retries automáticos com backoff exponencial para picos de concorrência ou erros transientes (5xx).
- Método test_connection() para validação de conectividade com a API do BCB.
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

log = get_logger("bcb_olinda_client")


class BcbOlindaError(Exception):
    """Exceção base para erros relacionados à API BCB Olinda."""

    pass


class BcbOlindaRateLimitError(BcbOlindaError):
    """Lançada quando o limite de requisições do BCB é atingido (HTTP 429)."""

    pass


class BcbOlindaApiError(BcbOlindaError):
    """Lançada quando a API retorna erro HTTP (4xx/5xx)."""

    def __init__(self, message: str, status_code: int | None = None, response_body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class BcbOlindaClient:
    """Cliente especializado para consulta a serviços OData do Banco Central (Olinda)."""

    DEFAULT_BASE_URL = "https://olinda.bcb.gov.br/olinda/servico"

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
        session: requests.Session | None = None,
    ):
        self.base_url = (
            base_url or os.getenv("BCB_OLINDA_BASE_URL", self.DEFAULT_BASE_URL)
        ).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = session or nova_session()

    def _build_url(self, endpoint: str) -> str:
        """Monta a URL completa para um determinado serviço OData."""
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
        Executa requisição HTTP com injeção de parâmetros OData e retry automático.
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
        # Garante formato JSON do OData
        if "$format" not in req_params:
            req_params["$format"] = "json"

        backoff = 2.0

        for tentativa in range(1, self.max_retries + 1):
            try:
                log.debug(
                    f"[BCB Olinda] {method.upper()} {url} (tentativa {tentativa}/{self.max_retries})"
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

                # Rate Limit (429)
                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    wait_time = float(retry_after) if retry_after else backoff
                    log.warning(
                        f"[BCB Olinda] Rate limit atingido (HTTP 429). Aguardando {wait_time:.1f}s antes do retry..."
                    )
                    if tentativa == self.max_retries:
                        raise BcbOlindaRateLimitError(
                            f"Limite de requisições atingido no BCB Olinda: {resp.text}"
                        )
                    time.sleep(wait_time)
                    backoff *= 2
                    continue

                # Erros transitórios de servidor (500, 502, 503, 504)
                if resp.status_code in (500, 502, 503, 504):
                    log.warning(
                        f"[BCB Olinda] Erro do servidor BCB HTTP {resp.status_code}. Aguardando {backoff:.1f}s..."
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
                raise BcbOlindaApiError(
                    f"Erro na requisição BCB Olinda [{method.upper()} {url}] (HTTP {status}): {body}",
                    status_code=status,
                    response_body=body,
                ) from e
            except requests.RequestException as e:
                if tentativa == self.max_retries:
                    raise BcbOlindaApiError(f"Falha de rede na requisição BCB Olinda: {e}") from e
                log.warning(
                    f"[BCB Olinda] Tentativa {tentativa} falhou: {e}. Aguardando {backoff}s..."
                )
                time.sleep(backoff)
                backoff *= 2

        raise BcbOlindaApiError("Número máximo de tentativas excedido no BCB Olinda.")

    def get(self, endpoint: str, params: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        """Executa GET e retorna o conteúdo JSON parseado."""
        resp = self.request("GET", endpoint, params=params, **kwargs)
        if not resp.content or resp.content.strip() == b"null":
            return {}
        return resp.json()

    def test_connection(self) -> dict[str, Any]:
        """
        Testa a conectividade com o serviço OData do BCB chamando uma consulta mínima do Boletim Focus.
        """
        t0 = time.time()
        endpoint = "/Expectativas/versao/v1/odata/ExpectativaMercadoMensais"
        try:
            resp = self.request("GET", endpoint, params={"$top": 1}, timeout=15)
            elapsed = time.time() - t0
            data = resp.json() if resp.content else {}
            records = data.get("value", [])
            return {
                "ok": True,
                "message": "Conexão com a API OData do BCB Olinda bem-sucedida!",
                "base_url": self.base_url,
                "status_code": resp.status_code,
                "latency_seconds": round(elapsed, 3),
                "sample_count": len(records),
            }
        except Exception as e:
            elapsed = time.time() - t0
            return {
                "ok": False,
                "message": f"Falha de conexão com o BCB Olinda: {e}",
                "base_url": self.base_url,
                "latency_seconds": round(elapsed, 3),
            }


if __name__ == "__main__":
    import json

    print("=== Teste de Conexão BCB Olinda (OData) ===")
    client = BcbOlindaClient()
    resultado = client.test_connection()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
