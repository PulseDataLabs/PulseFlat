"""
tests/test_tesouro_transparente_client.py
-----------------------------------------
Testes unitários para o TesouroTransparenteClient e BaseTesouroTransparenteScraper.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.tesouro_transparente_base import BaseTesouroTransparenteScraper
from scrapers.utils.tesouro_transparente_client import (
    TesouroTransparenteClient,
)


def test_client_datastore_search(requests_mock):
    """Testa consulta ao endpoint datastore_search da API CKAN."""
    endpoint_url = "https://www.tesourotransparente.gov.br/ckan/api/3/action/datastore_search"
    requests_mock.get(
        endpoint_url,
        json={
            "success": True,
            "result": {
                "records": [{"Tipo Titulo": "Tesouro Selic 2029", "Taxa Compra Manha": "0.05"}]
            },
        },
        status_code=200,
    )

    client = TesouroTransparenteClient()
    records = client.datastore_search("resource-123", limit=1)
    assert len(records) == 1
    assert records[0]["Tipo Titulo"] == "Tesouro Selic 2029"


def test_client_rate_limit_retry(requests_mock, monkeypatch):
    """Testa retry automático em caso de rate limit (429)."""
    monkeypatch.setattr(time, "sleep", lambda s: None)

    endpoint_url = "https://www.tesourotransparente.gov.br/ckan/api/3/action/package_list"
    requests_mock.get(
        endpoint_url,
        [
            {"text": "Rate Limit Exceeded", "status_code": 429},
            {"json": {"result": ["pkg1", "pkg2"]}, "status_code": 200},
        ],
    )

    client = TesouroTransparenteClient(max_retries=2)
    data = client.get("/action/package_list")
    assert "result" in data
    assert len(data["result"]) == 2


def test_client_test_connection(requests_mock):
    """Testa método test_connection()."""
    endpoint_url = "https://www.tesourotransparente.gov.br/ckan/api/3/action/package_list"
    requests_mock.get(
        endpoint_url,
        json={"success": True, "result": ["tesouro-direto"]},
        status_code=200,
    )

    client = TesouroTransparenteClient()
    result = client.test_connection()
    assert result["ok"] is True
    assert result["sample_packages_count"] == 1


def test_base_tesouro_scraper_extract_records():
    """Testa extração de registros do envelope CKAN."""
    scraper = BaseTesouroTransparenteScraper()

    # Formato result.records
    raw = {"result": {"records": [{"titulo": "Tesouro IPCA+"}]}}
    assert scraper.extract_records(raw) == [{"titulo": "Tesouro IPCA+"}]

    # Lista direta
    assert scraper.extract_records([{"titulo": "Prefixado"}]) == [{"titulo": "Prefixado"}]

    # Vazio
    assert scraper.extract_records(None) == []


def test_base_tesouro_scraper_fetch_resource(requests_mock):
    """Testa fetch_resource do BaseTesouroTransparenteScraper."""
    endpoint_url = "https://www.tesourotransparente.gov.br/ckan/api/3/action/datastore_search"
    requests_mock.get(
        endpoint_url,
        json={"result": {"records": [{"Tipo Titulo": "Tesouro Selic"}]}},
        status_code=200,
    )

    scraper = BaseTesouroTransparenteScraper()
    records = scraper.fetch_resource("resource-abc")
    assert len(records) == 1
    assert records[0]["Tipo Titulo"] == "Tesouro Selic"
