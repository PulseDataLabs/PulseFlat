"""
tests/test_fred_client.py
-------------------------
Testes unitários para o FredClient e BaseFredScraper.
"""

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.fred_base import BaseFredScraper
from scrapers.utils.fred_client import (
    FredAuthError,
    FredClient,
    FredMissingApiKeyError,
)


def test_client_missing_api_key():
    """Verifica comportamento quando FRED_API_KEY não é fornecida."""
    client = FredClient(api_key="")
    assert not client.has_credentials

    with pytest.raises(FredMissingApiKeyError):
        client.get("/series/observations")

    diag = client.test_connection()
    assert diag["ok"] is False
    assert "API Key do FRED não encontrada" in diag["message"]


def test_client_get_observations_success(requests_mock):
    """Testa consulta de observações com api_key e file_type=json."""
    endpoint_url = "https://api.stlouisfed.org/fred/series/observations"
    requests_mock.get(
        endpoint_url,
        json={"observations": [{"date": "2026-06-01", "value": "4.35"}]},
        status_code=200,
    )

    client = FredClient(api_key="minha_chave_fred")
    records = client.get_series_observations("DGS10", limit=1)
    assert len(records) == 1
    assert records[0]["value"] == "4.35"

    history = requests_mock.request_history
    assert len(history) == 1
    assert "api_key=minha_chave_fred" in history[0].query
    assert "file_type=json" in history[0].query


def test_client_auth_error(requests_mock):
    """Testa tratamento de erro de chave inválida do FRED."""
    endpoint_url = "https://api.stlouisfed.org/fred/series"
    requests_mock.get(
        endpoint_url,
        text="Bad Request. The api_key provided is not a valid 32 character alphanumeric lower-case string.",
        status_code=400,
    )

    client = FredClient(api_key="chave_invalida")
    with pytest.raises(FredAuthError):
        client.get("/series")

    diag = client.test_connection()
    assert diag["ok"] is False
    assert "Chave inválida" in diag["message"]


def test_client_rate_limit_retry(requests_mock, monkeypatch):
    """Testa retry automático em caso de rate limit (429)."""
    monkeypatch.setattr(time, "sleep", lambda s: None)

    endpoint_url = "https://api.stlouisfed.org/fred/series"
    requests_mock.get(
        endpoint_url,
        [
            {"text": "Too Many Requests", "status_code": 429},
            {"json": {"seriess": [{"id": "DGS10"}]}, "status_code": 200},
        ],
    )

    client = FredClient(api_key="valid_key", max_retries=2)
    data = client.get("/series")
    assert "seriess" in data


def test_base_fred_scraper_extract_records():
    """Testa extração de observações do BaseFredScraper."""
    scraper = BaseFredScraper()

    # Formato envelope com 'observations'
    raw = {"observations": [{"date": "2026-01-01", "value": "4.20"}]}
    assert scraper.extract_records(raw) == [{"date": "2026-01-01", "value": "4.20"}]

    # Lista direta
    assert scraper.extract_records([{"date": "2026-01-01"}]) == [{"date": "2026-01-01"}]

    # Vazio
    assert scraper.extract_records(None) == []


def test_base_fred_scraper_fetch_series(requests_mock):
    """Testa fetch_series do BaseFredScraper."""
    endpoint_url = "https://api.stlouisfed.org/fred/series/observations"
    requests_mock.get(
        endpoint_url,
        json={"observations": [{"date": "2026-05-15", "value": "4.15"}]},
        status_code=200,
    )

    client = FredClient(api_key="valid_key")
    scraper = BaseFredScraper(client=client)
    records = scraper.fetch_series("DGS10")
    assert len(records) == 1
    assert records[0]["value"] == "4.15"
