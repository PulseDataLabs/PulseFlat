"""
tests/test_scrapers_fred.py
---------------------------
Testes unitários para os 5 scrapers consolidados do FRED:
- FredUsTreasuriesYieldCurveScraper
- FredGlobalLiquidityCreditSpreadsScraper
- FredUsMacroIndicatorsScraper
- FredBrazilMacroFxAndCyclesScraper
- FredBrazilExportCommoditiesScraper
"""

import sys
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.fred_brazil_export_commodities import FredBrazilExportCommoditiesScraper
from scrapers.fred_brazil_macro_fx_and_cycles import FredBrazilMacroFxAndCyclesScraper
from scrapers.fred_global_liquidity_credit_spreads import FredGlobalLiquidityCreditSpreadsScraper
from scrapers.fred_us_macro_indicators import FredUsMacroIndicatorsScraper
from scrapers.fred_us_treasuries_yield_curve import FredUsTreasuriesYieldCurveScraper

FRED_SCRAPERS = [
    (FredUsTreasuriesYieldCurveScraper, "fred_us_treasuries_yield_curve"),
    (FredGlobalLiquidityCreditSpreadsScraper, "fred_global_liquidity_credit_spreads"),
    (FredUsMacroIndicatorsScraper, "fred_us_macro_indicators"),
    (FredBrazilMacroFxAndCyclesScraper, "fred_brazil_macro_fx_and_cycles"),
    (FredBrazilExportCommoditiesScraper, "fred_brazil_export_commodities"),
]


@pytest.mark.parametrize("cls,expected_name", FRED_SCRAPERS)
def test_fred_scrapers_metadata(cls, expected_name):
    inst = cls()
    assert inst.name == expected_name
    assert inst.group == "fred"
    assert inst.enabled is True
    assert inst.accumulate is True
    assert inst.compress is True
    assert len(inst.chaves_dedup) >= 1
    assert "FRED" in inst.title


def test_fred_missing_api_key_graceful():
    scraper = FredUsTreasuriesYieldCurveScraper()
    with patch.object(scraper, "check_credentials", return_value=False):
        df = scraper.fetch()
        assert df.empty


def test_us_treasuries_fetch_mock():
    scraper = FredUsTreasuriesYieldCurveScraper()
    scraper.target_date = date(2026, 9, 11)

    mock_observations = [
        {"date": "2026-09-11", "value": "4.15"},
        {"date": "2026-09-10", "value": "4.12"},
    ]

    with (
        patch.object(scraper, "check_credentials", return_value=True),
        patch.object(scraper, "fetch_series", return_value=mock_observations),
    ):
        df = scraper.fetch()

        assert not df.empty
        assert len(df) == 2
        assert "dgs10" in df.columns
        assert "t10y2y_spread" in df.columns
        assert "registro_hash" in df.columns
        assert df.iloc[0]["data_referencia"] in ("2026-09-10", "2026-09-11")


def test_global_liquidity_credit_spreads_fetch_mock():
    scraper = FredGlobalLiquidityCreditSpreadsScraper()
    scraper.target_date = date(2026, 9, 11)

    mock_obs = [{"date": "2026-09-11", "value": "5.33"}]

    with (
        patch.object(scraper, "check_credentials", return_value=True),
        patch.object(scraper, "fetch_series", return_value=mock_obs),
    ):
        df = scraper.fetch()

        assert not df.empty
        assert len(df) == 1
        assert "fed_funds_rate" in df.columns
        assert "sofr_rate" in df.columns
        assert "credit_spread_corp_ig" in df.columns
        assert "registro_hash" in df.columns


def test_us_macro_indicators_fetch_mock():
    scraper = FredUsMacroIndicatorsScraper()
    scraper.start_date = date(2026, 1, 1)
    scraper.end_date = date(2026, 9, 1)

    mock_obs = [{"date": "2026-08-01", "value": "314.5"}]

    with (
        patch.object(scraper, "check_credentials", return_value=True),
        patch.object(scraper, "fetch_series", return_value=mock_obs),
    ):
        df = scraper.fetch()

        assert not df.empty
        assert len(df) == 1
        assert "cpi_headline" in df.columns
        assert "nonfarm_payroll" in df.columns
        assert "registro_hash" in df.columns


def test_brazil_macro_fx_and_cycles_fetch_mock():
    scraper = FredBrazilMacroFxAndCyclesScraper()
    scraper.start_date = date(2026, 1, 1)
    scraper.end_date = date(2026, 9, 1)

    mock_obs = [{"date": "2026-08-01", "value": "5.4520"}]

    with (
        patch.object(scraper, "check_credentials", return_value=True),
        patch.object(scraper, "fetch_series", return_value=mock_obs),
    ):
        df = scraper.fetch()

        assert not df.empty
        assert len(df) == 1
        assert "cambio_brl_usd_fed" in df.columns
        assert "reer_bis_brasil" in df.columns
        assert "cli_ocde_brasil" in df.columns
        assert "registro_hash" in df.columns


def test_brazil_export_commodities_fetch_mock():
    scraper = FredBrazilExportCommoditiesScraper()
    scraper.start_date = date(2026, 1, 1)
    scraper.end_date = date(2026, 9, 1)

    mock_obs = [{"date": "2026-08-01", "value": "105.50"}]

    with (
        patch.object(scraper, "check_credentials", return_value=True),
        patch.object(scraper, "fetch_series", return_value=mock_obs),
    ):
        df = scraper.fetch()

        assert not df.empty
        assert len(df) == 1
        assert "minerio_ferro_global_usd" in df.columns
        assert "soja_global_usd" in df.columns
        assert "petroleo_brent_global_usd" in df.columns
        assert "registro_hash" in df.columns
