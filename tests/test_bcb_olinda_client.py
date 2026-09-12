"""
tests/test_bcb_olinda_client.py
-------------------------------
Testes unitários para o BcbOlindaClient e BaseBcbOlindaScraper.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.bcb_olinda_base import BaseBcbOlindaScraper
from scrapers.utils.bcb_olinda_client import (
    BcbOlindaClient,
)


def test_client_default_base_url_and_format(requests_mock):
    """Testa requisição OData garantindo injeção de $format=json."""
    endpoint_url = "https://olinda.bcb.gov.br/olinda/servico/test/odata"
    requests_mock.get(
        endpoint_url,
        json={"value": [{"Indicador": "IPCA", "Mediana": 3.9}]},
        status_code=200,
    )

    client = BcbOlindaClient()
    dados = client.get("/test/odata")
    assert "value" in dados
    assert dados["value"][0]["Indicador"] == "IPCA"

    history = requests_mock.request_history
    assert len(history) == 1
    assert "format=json" in history[0].query


def test_client_rate_limit_retry(requests_mock, monkeypatch):
    """Testa retry automático em caso de rate limit (429)."""
    monkeypatch.setattr(time, "sleep", lambda s: None)

    endpoint_url = "https://olinda.bcb.gov.br/olinda/servico/test"
    requests_mock.get(
        endpoint_url,
        [
            {"text": "Too Many Requests", "status_code": 429},
            {"json": {"value": [{"id": 1}]}, "status_code": 200},
        ],
    )

    client = BcbOlindaClient(max_retries=2)
    dados = client.get("/test")
    assert dados == {"value": [{"id": 1}]}


def test_client_test_connection(requests_mock):
    """Testa método test_connection() do cliente OData."""
    endpoint_url = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativaMercadoMensais"
    requests_mock.get(
        endpoint_url,
        json={"value": [{"Indicador": "Selic"}]},
        status_code=200,
    )

    client = BcbOlindaClient()
    result = client.test_connection()
    assert result["ok"] is True
    assert result["sample_count"] == 1


def test_base_bcb_olinda_scraper_extract_records():
    """Testa extração do array 'value' do OData."""
    scraper = BaseBcbOlindaScraper()

    # OData padrão: envelope com 'value'
    assert scraper.extract_records({"value": [{"Indicador": "PIB"}]}) == [{"Indicador": "PIB"}]

    # Lista direta
    assert scraper.extract_records([{"Indicador": "Câmbio"}]) == [{"Indicador": "Câmbio"}]

    # Vazio
    assert scraper.extract_records(None) == []
    assert scraper.extract_records({}) == []


def test_base_bcb_olinda_scraper_fetch_endpoint(requests_mock):
    """Testa fetch_endpoint do BaseBcbOlindaScraper."""
    endpoint_url = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativaMercadoMensais"
    requests_mock.get(
        endpoint_url,
        json={"value": [{"Indicador": "IPCA", "Mediana": 4.0}]},
        status_code=200,
    )

    scraper = BaseBcbOlindaScraper()
    registros = scraper.fetch_endpoint("/Expectativas/versao/v1/odata/ExpectativaMercadoMensais")
    assert len(registros) == 1
    assert registros[0]["Indicador"] == "IPCA"
