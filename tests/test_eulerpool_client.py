"""
tests/test_eulerpool_client.py
------------------------------
Testes unitários para o EulerpoolClient e BaseEulerpoolScraper.
"""

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.eulerpool_base import BaseEulerpoolScraper
from scrapers.utils.eulerpool_client import (
    EulerpoolAuthError,
    EulerpoolClient,
    EulerpoolMissingApiKeyError,
)


def test_client_missing_api_key():
    """Verifica comportamento quando a API Key não é fornecida."""
    client = EulerpoolClient(api_key="")
    assert not client.has_credentials

    with pytest.raises(EulerpoolMissingApiKeyError):
        client.get("/api/1/test")

    diag = client.test_connection()
    assert diag["ok"] is False
    assert "API Key não encontrada" in diag["message"]


def test_client_get_request_success(requests_mock):
    """Testa execução de GET autenticado com Authorization Bearer na Eulerpool."""
    endpoint_url = "https://api.eulerpool.com/api/1/trends/ticker-trends"

    requests_mock.get(
        endpoint_url,
        json={"data": [{"ticker": "AAPL", "trend": "bullish"}]},
        status_code=200,
    )

    client = EulerpoolClient(
        api_key="minha_chave_secreta_123",
        base_url="https://api.eulerpool.com",
    )
    assert client.has_credentials

    dados = client.get("/api/1/trends/ticker-trends")
    assert isinstance(dados, dict)
    assert "data" in dados

    history = requests_mock.request_history
    assert len(history) == 1
    assert history[0].headers["Authorization"] == "Bearer minha_chave_secreta_123"


def test_client_auth_error(requests_mock):
    """Testa tratamento de erro ao receber HTTP 401 ou 403."""
    endpoint_url = "https://api.eulerpool.com/api/1/private/dados"

    requests_mock.get(
        endpoint_url,
        text="Missing or invalid API key",
        status_code=401,
    )
    requests_mock.get(
        "https://api.eulerpool.com/api/1/trends/ticker-trends",
        text="Missing or invalid API key",
        status_code=401,
    )

    client = EulerpoolClient(api_key="chave_invalida")
    with pytest.raises(EulerpoolAuthError) as exc_info:
        client.get("/api/1/private/dados")
    assert "Falha de autenticação/permissão Eulerpool (HTTP 401)" in str(exc_info.value)

    # Diagnóstico deve reportar falha sem quebrar execução
    diag = client.test_connection()
    assert diag["ok"] is False
    assert "Chave inválida" in diag["message"]


def test_client_rate_limit_retry(requests_mock, monkeypatch):
    """Testa retry automático com backoff em HTTP 429."""
    monkeypatch.setattr(time, "sleep", lambda s: None)

    endpoint_url = "https://api.eulerpool.com/api/1/test"

    requests_mock.get(
        endpoint_url,
        [
            {"text": "Too Many Requests", "status_code": 429},
            {"json": {"results": [{"id": 1}]}, "status_code": 200},
        ],
    )

    client = EulerpoolClient(api_key="chave", max_retries=2)
    resp = client.get("/api/1/test")
    assert resp == {"results": [{"id": 1}]}


def test_base_eulerpool_scraper_extract_records():
    """Testa o extrator de registros em múltiplos envelopes da Eulerpool."""
    scraper = BaseEulerpoolScraper()

    # Formato lista direta
    assert scraper.extract_records([{"id": 1}, {"id": 2}]) == [{"id": 1}, {"id": 2}]

    # Formato envelopado com 'data'
    assert scraper.extract_records({"data": [{"id": 10}]}) == [{"id": 10}]

    # Formato envelopado com 'results'
    assert scraper.extract_records({"results": [{"id": 20}]}) == [{"id": 20}]

    # Formato envelopado com 'tickers'
    assert scraper.extract_records({"tickers": [{"symbol": "PETR4"}]}) == [{"symbol": "PETR4"}]

    # Formato envelopado com 'items'
    assert scraper.extract_records({"items": [{"id": 30}]}) == [{"id": 30}]

    # Dict único
    assert scraper.extract_records({"symbol": "VALE3", "price": 60.0}) == [
        {"symbol": "VALE3", "price": 60.0}
    ]

    # Vazio / None
    assert scraper.extract_records(None) == []
    assert scraper.extract_records([]) == []


def test_base_eulerpool_scraper_fetch_endpoint(requests_mock):
    """Testa o fetch_endpoint do BaseEulerpoolScraper."""
    endpoint_url = "https://api.eulerpool.com/api/1/stocks/AAPL"

    requests_mock.get(
        endpoint_url,
        json={"data": [{"ticker": "AAPL", "price": 220.5}]},
        status_code=200,
    )

    client = EulerpoolClient(api_key="valid_key")
    scraper = BaseEulerpoolScraper(client=client)
    registros = scraper.fetch_endpoint("/api/1/stocks/AAPL")

    assert len(registros) == 1
    assert registros[0]["ticker"] == "AAPL"
    assert registros[0]["price"] == 220.5
