"""
scrapers/utils/ipea_client.py
-----------------------------
Cliente HTTP especializado para a API OData v4 do IPEADATA (Instituto de Pesquisa Econômica Aplicada).
Fonte: http://www.ipeadata.gov.br/api/odata4/

Funcionalidades:
- Suporte nativo a parâmetros OData v4 ($top, $skip, $filter, $orderby, $select).
- Consulta de valores históricos por código de série: ValoresSerie(SERCODIGO='...').
- Consulta e busca de metadados das séries: Metadados('...').
- Retries automáticos com backoff exponencial para instabilidades e timeouts de rede.
- Fallback automático entre HTTP e HTTPS caso haja problemas de certificado SSL.
- Método test_connection() para diagnóstico e monitoramento de conectividade e latência.
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

log = get_logger("ipea_client")


class IpeaError(Exception):
    """Exceção base para erros relacionados à API do IPEADATA."""

    pass


class IpeaRateLimitError(IpeaError):
    """Lançada quando a API do IPEA retorna HTTP 429 (Too Many Requests)."""

    pass


class IpeaApiError(IpeaError):
    """Lançada quando a API do IPEA retorna erro HTTP (4xx/5xx) ou payload inválido."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: Any = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class IpeaClient:
    """
    Cliente especializado para consulta aos serviços OData v4 do IPEADATA.
    Totalmente público e aberto, sem necessidade de chave de API.
    """

    DEFAULT_BASE_URL = "http://www.ipeadata.gov.br/api/odata4"
    FALLBACK_BASE_URL = "https://www.ipeadata.gov.br/api/odata4"

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 45,
        max_retries: int = 3,
        session: requests.Session | None = None,
    ):
        self.base_url = (
            base_url or os.getenv("IPEA_BASE_URL", self.DEFAULT_BASE_URL)
        ).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = session or nova_session()

    def _build_url(self, endpoint: str, use_fallback: bool = False) -> str:
        """Monta a URL completa para um determinado endpoint OData."""
        endpoint = endpoint.strip()
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint

        base = self.FALLBACK_BASE_URL if use_fallback else self.base_url
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        return f"{base}{endpoint}"

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
        Executa requisição HTTP com injeção de headers adequados,
        fallback de protocolo e retries automáticos.
        """
        timeout = timeout or self.timeout
        req_headers = {
            "Accept": "application/json",
            "User-Agent": "PulseFlat/1.0 (+https://github.com/PulseDataLabs/PulseFlat; data@pulsedatalabs.com)",
        }
        if headers:
            req_headers.update(headers)

        clean_params = {k: v for k, v in (params or {}).items() if v is not None}

        last_exc: Exception | None = None
        use_fallback = False

        for attempt in range(1, self.max_retries + 1):
            url = self._build_url(endpoint, use_fallback=use_fallback)
            try:
                log.debug(f"[IPEA] {method.upper()} {url} (tentativa {attempt}/{self.max_retries})")
                resp = self._session.request(
                    method=method.upper(),
                    url=url,
                    params=clean_params,
                    json=json_data,
                    headers=req_headers,
                    timeout=timeout,
                    **kwargs,
                )

                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", 2 * attempt))
                    log.warning(f"[IPEA] Rate-limited (429). Aguardando {retry_after}s...")
                    time.sleep(retry_after)
                    continue

                if resp.status_code in (500, 502, 503, 504):
                    wait_time = 1.5 * (2 ** (attempt - 1))
                    log.warning(f"[IPEA] Erro servidor {resp.status_code}. Retry em {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    # Alterna entre HTTP e HTTPS caso persistam erros 5xx
                    if attempt >= 2:
                        use_fallback = not use_fallback
                    continue

                if not resp.ok:
                    raise IpeaApiError(
                        f"Erro HTTP {resp.status_code} da API IPEA ({url}): {resp.text[:300]}",
                        status_code=resp.status_code,
                        response_body=resp.text,
                    )

                return resp

            except (requests.Timeout, requests.ConnectionError) as net_err:
                last_exc = net_err
                wait_time = 1.5 * (2 ** (attempt - 1))
                log.warning(f"[IPEA] Falha de conexão/timeout ({net_err}). Retry em {wait_time:.1f}s...")
                use_fallback = not use_fallback
                time.sleep(wait_time)

        raise IpeaApiError(
            f"Falha na requisição IPEA após {self.max_retries} tentativas ({endpoint}): {last_exc}"
        ) from last_exc

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Executa GET e retorna o payload desempacotado em JSON."""
        resp = self.request("GET", endpoint, params=params, **kwargs)
        try:
            return resp.json()
        except Exception as e:
            raise IpeaApiError(f"Resposta IPEA não é um JSON válido: {e}", response_body=resp.text) from e

    def get_serie_values(
        self,
        sercodigo: str,
        top: int | None = None,
        skip: int | None = None,
        orderby: str | None = None,
        filter_str: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retorna os registros históricos de uma determinada série econômica.
        Endpoint: /ValoresSerie(SERCODIGO='{sercodigo}')
        """
        sercodigo_clean = sercodigo.strip().replace("'", "")
        endpoint = f"ValoresSerie(SERCODIGO='{sercodigo_clean}')"

        params: dict[str, Any] = {}
        if top is not None:
            params["$top"] = top
        if skip is not None:
            params["$skip"] = skip
        if orderby:
            params["$orderby"] = orderby
        if filter_str:
            params["$filter"] = filter_str

        data = self.get(endpoint, params=params if params else None)
        if isinstance(data, dict):
            return data.get("value", [])
        if isinstance(data, list):
            return data
        return []

    def get_metadata(self, sercodigo: str) -> dict[str, Any]:
        """
        Obtém os metadados cadastrais de uma determinada série (nome, unidade, periodicidade, fonte).
        Endpoint: /Metadados('{sercodigo}')
        """
        sercodigo_clean = sercodigo.strip().replace("'", "")
        endpoint = f"Metadados('{sercodigo_clean}')"

        data = self.get(endpoint)
        if isinstance(data, dict):
            val = data.get("value")
            if isinstance(val, list) and val:
                return val[0]
            return data
        return {}

    def search_series(self, query: str, top: int = 50) -> list[dict[str, Any]]:
        """
        Pesquisa séries por termo em seu código ou nome via endpoint OData /Metadados.
        """
        q = query.strip()
        filter_clause = f"contains(SERNOME, '{q}') or contains(SERCODIGO, '{q}')"
        params = {"$filter": filter_clause, "$top": top}

        data = self.get("Metadados", params=params)
        if isinstance(data, dict):
            return data.get("value", [])
        return []

    def test_connection(self, test_serie: str = "BM12_TJOVER12") -> dict[str, Any]:
        """
        Testa a conectividade com a API do IPEADATA medindo latência e integridade dos dados.
        Retorna dicionário com status, tempo de resposta em ms e metadados da série testada.
        """
        t0 = time.time()
        try:
            meta = self.get_metadata(test_serie)
            records = self.get_serie_values(test_serie, top=2)
            elapsed_ms = round((time.time() - t0) * 1000, 2)

            return {
                "ok": True,
                "status": "connected",
                "latency_ms": elapsed_ms,
                "serie_testada": test_serie,
                "serie_nome": meta.get("SERNOME", "N/A"),
                "periodicidade": meta.get("PERNOME", "N/A"),
                "unidade": meta.get("UNINOME", "N/A"),
                "fonte": meta.get("FNTSIGLA", "N/A"),
                "amostras_retornadas": len(records),
            }
        except Exception as e:
            elapsed_ms = round((time.time() - t0) * 1000, 2)
            return {
                "ok": False,
                "status": "error",
                "latency_ms": elapsed_ms,
                "error": str(e),
            }
