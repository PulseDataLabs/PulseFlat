#!/usr/bin/env python
"""
tests/test_scrapers_ipea.py
---------------------------
Testes unitários para os scrapers consolidados do Ipeadata.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.ipea_calendario import IpeaCalendarioScraper
from scrapers.ipea_comercio_exterior import IpeaComercioExteriorScraper
from scrapers.ipea_fbcf import IpeaFbcfScraper
from scrapers.ipea_macroeconomia import IpeaMacroeconomiaScraper
from scrapers.ipea_mercados_diarios import IpeaMercadosDiariosScraper
from scrapers.ipea_precos_inflacao import IpeaPrecosInflacaoScraper
from scrapers.ipea_producao_mineral import IpeaProducaoMineralScraper
from scrapers.ipea_taxas_juros import IpeaTaxasJurosScraper


def test_ipea_macroeconomia_fetch(requests_mock):
    """Deve baixar e parsear com sucesso as séries da categoria macroeconomia."""
    mock_json = {
        "value": [
            {
                "SERCODIGO": "BM12_PIBAC12",
                "VALDATA": "2026-05-01T00:00:00-03:00",
                "VALVALOR": 11200300.0,
            }
        ]
    }

    requests_mock.get(
        "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='BM12_PIBAC12')",
        json=mock_json,
        status_code=200,
    )
    # Mock para os outros códigos da mesma seção para não dar erro
    for code in [
        "PNADC12_TDESOC12",
        "GAC12_SALMINRE12",
        "MTE12_SALMIN12",
        "SGS12_7836",
    ]:
        requests_mock.get(
            f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{code}')",
            json={"value": []},
            status_code=200,
        )

    scraper = IpeaMacroeconomiaScraper()
    df = scraper.fetch()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert "data_referencia" in df.columns
    assert "valor" in df.columns
    assert df.iloc[0]["data_referencia"] == "2026-05-01"
    assert df.iloc[0]["valor"] == 11200300.0


def test_ipea_daily_scrapers_fetch_and_filtering(requests_mock):
    """Deve baixar, parsear e filtrar corretamente por data em scrapers diários."""
    mock_json = {
        "value": [
            {
                "SERCODIGO": "EIA366_PBRENT366",
                "VALDATA": "2026-06-01T00:00:00-03:00",
                "VALVALOR": 75.0,
            },
            {
                "SERCODIGO": "EIA366_PBRENT366",
                "VALDATA": "2026-06-02T00:00:00-03:00",
                "VALVALOR": 76.0,
            },
            {
                "SERCODIGO": "EIA366_PBRENT366",
                "VALDATA": "2026-06-03T00:00:00-03:00",
                "VALVALOR": 77.0,
            },
        ]
    }

    requests_mock.get(
        "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='EIA366_PBRENT366')",
        json=mock_json,
        status_code=200,
    )
    # Mock para os outros códigos da mesma seção para não dar erro
    for code in ["EIA366_PWTI366", "GM366_DOW366", "SGS366_NASDAQ366"]:
        requests_mock.get(
            f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{code}')",
            json={"value": []},
            status_code=200,
        )

    scraper = IpeaMercadosDiariosScraper()

    # 1. Sem filtros
    df = scraper.fetch()
    assert len(df) == 3

    # 2. Com target_date
    scraper.target_date = date(2026, 6, 2)
    df_target = scraper.fetch()
    assert len(df_target) == 1
    assert df_target.iloc[0]["data_referencia"] == "2026-06-02"
    assert df_target.iloc[0]["valor"] == 76.0

    # 3. Com start/end date
    scraper.target_date = None
    scraper.start_date = date(2026, 6, 2)
    scraper.end_date = date(2026, 6, 3)
    df_range = scraper.fetch()
    assert len(df_range) == 2
    assert list(df_range["data_referencia"]) == ["2026-06-02", "2026-06-03"]


def test_import_and_instantiation():
    """Verifica se os 8 scrapers consolidados importam e inicializam corretamente."""
    scrapers = [
        IpeaMacroeconomiaScraper(),
        IpeaMercadosDiariosScraper(),
        IpeaTaxasJurosScraper(),
        IpeaPrecosInflacaoScraper(),
        IpeaFbcfScraper(),
        IpeaComercioExteriorScraper(),
        IpeaProducaoMineralScraper(),
        IpeaCalendarioScraper(),
    ]
    for s in scrapers:
        assert s.name.startswith("ipea_")
        assert s.enabled is True
