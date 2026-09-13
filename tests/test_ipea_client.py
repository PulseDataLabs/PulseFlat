"""
tests/test_ipea_client.py
-------------------------
Testes unitários para IpeaClient e BaseIpeaScraper.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.ipea_base import BaseIpeaScraper
from scrapers.utils.ipea_client import (
    IpeaApiError,
    IpeaClient,
)


def test_client_init():
    """Verifica inicialização padrão do IpeaClient."""
    client = IpeaClient()
    assert "ipeadata.gov.br" in client.base_url
    assert client.timeout == 45
    assert client.max_retries == 3


def test_client_get_serie_values_success(requests_mock):
    """Testa consulta de valores OData v4 de uma série."""
    url = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='BM12_TJOVER12')"
    mock_payload = {
        "@odata.context": "http://ipeadata.gov.br/api/odata4/$metadata",
        "value": [
            {"SERCODIGO": "BM12_TJOVER12", "VALDATA": "2026-01-01T00:00:00-02:00", "VALVALOR": 1.15},
            {"SERCODIGO": "BM12_TJOVER12", "VALDATA": "2026-02-01T00:00:00-02:00", "VALVALOR": 1.20},
        ],
    }
    requests_mock.get(url, json=mock_payload, status_code=200)

    client = IpeaClient()
    records = client.get_serie_values("BM12_TJOVER12")
    assert len(records) == 2
    assert records[0]["VALVALOR"] == 1.15
    assert records[1]["VALDATA"] == "2026-02-01T00:00:00-02:00"


def test_client_get_metadata_success(requests_mock):
    """Testa consulta de metadados OData v4 de uma série."""
    url = "http://www.ipeadata.gov.br/api/odata4/Metadados('BM12_TJOVER12')"
    mock_payload = {
        "value": [
            {
                "SERCODIGO": "BM12_TJOVER12",
                "SERNOME": "Taxa Selic Over Mensal",
                "PERNOME": "Mensal",
                "UNINOME": "(% a.m.)",
                "FNTSIGLA": "Bacen",
            }
        ]
    }
    requests_mock.get(url, json=mock_payload, status_code=200)

    client = IpeaClient()
    meta = client.get_metadata("BM12_TJOVER12")
    assert meta["SERNOME"] == "Taxa Selic Over Mensal"
    assert meta["PERNOME"] == "Mensal"


def test_client_test_connection_success(requests_mock):
    """Testa o diagnóstico de test_connection()."""
    meta_url = "http://www.ipeadata.gov.br/api/odata4/Metadados('BM12_TJOVER12')"
    values_url = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='BM12_TJOVER12')?$top=2"

    requests_mock.get(meta_url, json={"SERNOME": "Selic", "PERNOME": "Mensal", "UNINOME": "%", "FNTSIGLA": "Bacen"})
    requests_mock.get(values_url, json={"value": [{"VALDATA": "2026-01-01T00:00:00-02:00", "VALVALOR": 1.0}]})

    client = IpeaClient()
    diag = client.test_connection("BM12_TJOVER12")
    assert diag["ok"] is True
    assert diag["status"] == "connected"
    assert diag["serie_nome"] == "Selic"
    assert diag["amostras_retornadas"] == 1


def test_client_api_error(requests_mock):
    """Testa erro HTTP retornado pela API."""
    url = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='INVALID_SERIE')"
    requests_mock.get(url, text="Resource not found", status_code=404)

    client = IpeaClient(max_retries=1)
    with pytest.raises(IpeaApiError) as exc_info:
        client.get_serie_values("INVALID_SERIE")
    assert exc_info.value.status_code == 404


def test_base_scraper_normalize_dataframe():
    """Testa a normalização defensiva do BaseIpeaScraper."""
    scraper = BaseIpeaScraper()
    raw_records = [
        {"SERCODIGO": "SERIE1", "VALDATA": "2026-01-01T00:00:00-02:00", "VALVALOR": "12.5", "NIVNOME": ""},
        {"SERCODIGO": "SERIE1", "VALDATA": "2026-02-01T00:00:00-02:00", "VALVALOR": 13.0, "NIVNOME": ""},
        {"SERCODIGO": "SERIE1", "VALDATA": "2026-02-01T00:00:00-02:00", "VALVALOR": 13.0, "NIVNOME": ""},  # duplicado
    ]

    df = scraper.normalize_dataframe(raw_records, codigo="SERIE1", nome="Série de Teste")
    assert len(df) == 2  # deduplicado
    assert list(df.columns) == ["data_captura", "data_referencia", "codigo_ativo", "nome_ativo", "valor"]
    assert df["data_referencia"].iloc[0] == "2026-01-01"
    assert df["data_referencia"].iloc[1] == "2026-02-01"
    assert df["valor"].iloc[0] == 12.5
    assert df["valor"].iloc[1] == 13.0


def test_base_scraper_fetch_series_list(requests_mock):
    """Testa fetch_series_list do BaseIpeaScraper."""
    url = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='SERIE_A')"
    requests_mock.get(
        url,
        json={"value": [{"VALDATA": "2026-01-01T00:00:00-02:00", "VALVALOR": 10.0}]},
    )

    scraper = BaseIpeaScraper()
    df = scraper.fetch_series_list([{"code": "SERIE_A", "title": "Série A"}])
    assert len(df) == 1
    assert df["codigo_ativo"].iloc[0] == "SERIE_A"
    assert df["label"].iloc[0] == "Série A"
    assert df["valor"].iloc[0] == 10.0
