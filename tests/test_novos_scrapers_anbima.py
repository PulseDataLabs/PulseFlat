"""
tests/test_novos_scrapers_anbima.py
-----------------------------------
Testes unitários para a suíte de novos scrapers da API ANBIMA Data (A a I).
"""

import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.anbima_cri_cra_mercado_secundario import AnbimaCriCraMercadoSecundarioScraper
from scrapers.anbima_curvas_credito import AnbimaCurvasCreditoScraper
from scrapers.anbima_curvas_juros_ettj import AnbimaCurvasJurosEttjScraper
from scrapers.anbima_fidc_mercado_secundario import AnbimaFidcMercadoSecundarioScraper
from scrapers.anbima_indice_ida import AnbimaIndiceIdaScraper
from scrapers.anbima_indices_ima_resultados import AnbimaIndicesImaResultadosScraper
from scrapers.anbima_letras_financeiras import AnbimaLetrasFinanceirasScraper
from scrapers.anbima_titulos_publicos_mercado_secundario import (
    AnbimaTitulosPublicosMercadoSecundarioScraper,
)
from scrapers.anbima_titulos_publicos_vna import AnbimaTitulosPublicosVnaScraper

SCRAPER_CLASSES = [
    (AnbimaCriCraMercadoSecundarioScraper, "anbima_cri_cra_mercado_secundario"),
    (AnbimaLetrasFinanceirasScraper, "anbima_letras_financeiras"),
    (AnbimaFidcMercadoSecundarioScraper, "anbima_fidc_mercado_secundario"),
    (AnbimaCurvasCreditoScraper, "anbima_curvas_credito"),
    (AnbimaCurvasJurosEttjScraper, "anbima_curvas_juros_ettj"),
    (AnbimaIndiceIdaScraper, "anbima_indice_ida"),
    (AnbimaIndicesImaResultadosScraper, "anbima_indices_ima_resultados"),
    (AnbimaTitulosPublicosMercadoSecundarioScraper, "anbima_titulos_publicos_mercado_secundario"),
    (AnbimaTitulosPublicosVnaScraper, "anbima_titulos_publicos_vna"),
]


@pytest.mark.parametrize("cls,expected_name", SCRAPER_CLASSES)
def test_new_scrapers_metadata(cls, expected_name):
    inst = cls()
    assert inst.name == expected_name
    assert inst.group == "anbima"
    assert inst.enabled is True
    assert inst.accumulate is True
    assert inst.compress is True
    assert len(inst.chaves_dedup) >= 1
    assert "ANBIMA" in inst.title


def test_cri_cra_fetch_mock(requests_mock):
    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    api_url = "https://api.anbima.com.br/feed/precos-indices/v1/cri-cra/mercado-secundario"

    requests_mock.post(
        oauth_url, json={"access_token": "mock_token", "expires_in": 3600}, status_code=200
    )
    requests_mock.get(
        api_url,
        json=[
            {
                "codigo_ativo": "22J0000801",
                "emissor": "TRUE SECURITIZADORA",
                "originador": "TRISUL",
                "tipo_contrato": "CRI",
                "taxa_indicativa": 1.70,
                "pu": 1050.20,
            }
        ],
        status_code=200,
    )

    scraper = AnbimaCriCraMercadoSecundarioScraper()
    scraper.client.client_id = "test"
    scraper.client.client_secret = "test"
    scraper.target_date = date(2026, 9, 10)

    df = scraper.fetch()
    assert not df.empty
    assert df["codigo_ativo"].iloc[0] == "22J0000801"
    assert df["tipo_contrato"].iloc[0] == "CRI"
    assert df["registro_hash"].iloc[0] != ""


def test_vna_fetch_mock(requests_mock):
    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    api_url = "https://api.anbima.com.br/feed/precos-indices/v1/titulos-publicos/vna"

    requests_mock.post(
        oauth_url, json={"access_token": "mock_token", "expires_in": 3600}, status_code=200
    )
    requests_mock.get(
        api_url,
        json={
            "data_referencia": "2026-09-10",
            "titulos": [{"tipo_titulo": "NTN-B", "codigo_selic": "760199", "vna": 4731.454317}],
        },
        status_code=200,
    )

    scraper = AnbimaTitulosPublicosVnaScraper()
    scraper.client.client_id = "test"
    scraper.client.client_secret = "test"
    scraper.target_date = date(2026, 9, 10)

    df = scraper.fetch()
    assert not df.empty
    assert df["tipo_titulo"].iloc[0] == "NTN-B"
    assert df["vna"].iloc[0] == "4731.454317"
    assert df["registro_hash"].iloc[0] != ""
