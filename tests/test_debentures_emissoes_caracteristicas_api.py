"""
tests/test_debentures_emissoes_caracteristicas_api.py
----------------------------------------------------
Testes unitários para DebenturesEmissoesCaracteristicasApiScraper.
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.debentures_emissoes_caracteristicas_api import (
    DebenturesEmissoesCaracteristicasApiScraper,
)


def test_scraper_metadata():
    scraper = DebenturesEmissoesCaracteristicasApiScraper()
    assert scraper.name == "debentures_emissoes_caracteristicas_api"
    assert scraper.group == "anbima"
    assert scraper.enabled is True
    assert scraper.accumulate is False
    assert scraper.compress is False
    assert scraper.chaves_dedup == ["codigo_ativo"]
    assert "Debêntures+" in scraper.description or "Debêntures" in scraper.title


def test_scraper_fetch_mock(requests_mock):
    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    api_url = "https://api.anbima.com.br/feed/precos-indices/v1/debentures-mais/mercado-secundario"
    reune_url = "https://api.anbima.com.br/feed/precos-indices/v1/reune/negociacoes"

    requests_mock.post(
        oauth_url,
        json={"access_token": "mock_token", "expires_in": 3600},
        status_code=200,
    )

    mock_debs = [
        {
            "codigo_ativo": "VALE38",
            "emissor": "VALE S.A.",
            "grupo": "DI SPREAD",
            "percentual_taxa": "DI + 1,2000%",
            "data_vencimento": "2030-05-15",
            "vna": 1000.0,
            "pu_par": 1050.25,
            "pu": 1052.10,
            "percent_pu_par": 100.17,
            "duration": 520,
            "z_spread": 0.85,
            "spread_incentivado_sem_gross_up": None,
            "referencia_ntnb": None,
            "lei_12431": "NÃO",
            "taxa_indicativa": 0.85,
            "taxa_compra": 0.90,
            "taxa_venda": 0.80,
            "desvio_padrao": 0.05,
            "val_min_intervalo": 0.75,
            "val_max_intervalo": 0.95,
            "percent_reune": "15%",
        }
    ]

    requests_mock.get(
        api_url,
        json=mock_debs,
        status_code=200,
    )

    requests_mock.get(
        reune_url,
        json={"content": [{"codigo_ativo": "VALE38", "isin": "BRVALEDBS038"}]},
        status_code=200,
    )

    scraper = DebenturesEmissoesCaracteristicasApiScraper()
    scraper.client.client_id = "test_id"
    scraper.client.client_secret = "test_secret"
    scraper.target_date = date(2026, 9, 10)

    df = scraper.fetch()
    assert not df.empty
    assert len(df) == 1
    assert df["codigo_ativo"].iloc[0] == "VALE38"
    assert df["isin"].iloc[0] == "BRVALEDBS038"
    assert df["vna"].iloc[0] == "1000"
    assert df["duration"].iloc[0] == "520"
    assert df["z_spread"].iloc[0] == "0.85"
    assert df["registro_hash"].iloc[0] != ""
