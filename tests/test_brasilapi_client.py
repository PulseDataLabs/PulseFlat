"""
tests/test_brasilapi_client.py
------------------------------
Testes unitários para o BrasilApiClient e BaseBrasilApiScraper.
"""

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.brasilapi_base import BaseBrasilApiScraper
from scrapers.utils.brasilapi_client import (
    BrasilApiClient,
    BrasilApiNotFoundError,
)


def test_client_default_base_url_and_request(requests_mock):
    """Testa requisição com base_url padrão e headers informativos."""
    endpoint_url = "https://brasilapi.com.br/api/taxas/v1"
    requests_mock.get(
        endpoint_url,
        json=[{"nome": "Selic", "valor": 10.5}],
        status_code=200,
    )

    client = BrasilApiClient()
    assert client.base_url == "https://brasilapi.com.br/api"

    dados = client.get("/taxas/v1")
    assert isinstance(dados, list)
    assert dados[0]["nome"] == "Selic"

    history = requests_mock.request_history
    assert len(history) == 1
    assert "PulseFlat" in history[0].headers["User-Agent"]


def test_client_not_found_error_404(requests_mock):
    """Testa tratamento de erro HTTP 404."""
    endpoint_url = "https://brasilapi.com.br/api/cnpj/v1/00000000000000"
    requests_mock.get(
        endpoint_url,
        text="CNPJ não encontrado",
        status_code=404,
    )

    client = BrasilApiClient()
    with pytest.raises(BrasilApiNotFoundError):
        client.get("/cnpj/v1/00000000000000")


def test_client_rate_limit_retry(requests_mock, monkeypatch):
    """Testa retry automático com backoff em HTTP 429."""
    monkeypatch.setattr(time, "sleep", lambda s: None)

    endpoint_url = "https://brasilapi.com.br/api/banks/v1"
    requests_mock.get(
        endpoint_url,
        [
            {"text": "Rate Limit Exceeded", "status_code": 429},
            {"json": [{"ispb": "00000000", "name": "BCO DO BRASIL S.A."}], "status_code": 200},
        ],
    )

    client = BrasilApiClient(max_retries=2)
    dados = client.get("/banks/v1")
    assert len(dados) == 1
    assert dados[0]["name"] == "BCO DO BRASIL S.A."


def test_client_test_connection(requests_mock):
    """Testa método test_connection()."""
    endpoint_url = "https://brasilapi.com.br/api/taxas/v1"
    requests_mock.get(
        endpoint_url,
        json=[{"nome": "Selic", "valor": 10.5}],
        status_code=200,
    )

    client = BrasilApiClient()
    result = client.test_connection()
    assert result["ok"] is True
    assert result["status_code"] == 200


def test_base_brasilapi_scraper_extract_records():
    """Testa extração de registros do BaseBrasilApiScraper."""
    scraper = BaseBrasilApiScraper()

    # Lista direta
    assert scraper.extract_records([{"id": 1}]) == [{"id": 1}]

    # Envelope 'data'
    assert scraper.extract_records({"data": [{"id": 2}]}) == [{"id": 2}]

    # Dict único
    assert scraper.extract_records({"nome": "CDI", "valor": 10.4}) == [
        {"nome": "CDI", "valor": 10.4}
    ]

    # Vazio
    assert scraper.extract_records(None) == []
    assert scraper.extract_records([]) == []


def test_base_brasilapi_scraper_fetch_endpoint(requests_mock):
    """Testa fetch_endpoint do BaseBrasilApiScraper."""
    endpoint_url = "https://brasilapi.com.br/api/taxas/v1"
    requests_mock.get(
        endpoint_url,
        json=[{"nome": "IPCA", "valor": 3.8}],
        status_code=200,
    )

    scraper = BaseBrasilApiScraper()
    registros = scraper.fetch_endpoint("/taxas/v1")
    assert len(registros) == 1
    assert registros[0]["nome"] == "IPCA"
