#!/usr/bin/env python
# coding: utf-8
"""
tests/test_backfill_buracos.py
------------------------------
Testes unitários para scripts/backfill_buracos.py
"""

import sys
import importlib
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.backfill_buracos import main

real_import = importlib.import_module
main_module = sys.modules[main.__module__]


class TestBackfillBuracos:
    def test_backfill_dry_run(self):
        mock_exists = MagicMock(return_value=True)
        mock_load = MagicMock(return_value={("*",): {"2026-06-01", "2026-06-03"}})
        mock_check_gaps = MagicMock(return_value={("*",): ["2026-06-02"]})
        mock_import = MagicMock(side_effect=real_import)

        with patch.object(main_module, "load_entity_dates", mock_load), \
             patch.object(main_module, "check_gaps", mock_check_gaps), \
             patch.object(main_module.importlib, "import_module", mock_import), \
             patch.object(main_module.Path, "exists", mock_exists):
            
            # Executa no modo dry_run
            main(
                csv_filter=["anbima_550.csv"],
                threshold=2,
                dry_run=True,
                quiet=True,
            )

        # No dry run, o scraper anbima_550 não deve ser chamado
        for call_args in mock_import.call_args_list:
            assert "scrapers" not in call_args[0][0]

    def test_backfill_execution_generic(self):
        mock_exists = MagicMock(return_value=True)
        mock_load = MagicMock(return_value={("*",): {"2026-06-01", "2026-06-03"}})
        mock_check_gaps = MagicMock(return_value={("*",): ["2026-06-02"]})

        # Mock da classe Scraper
        mock_scraper_instance = MagicMock()
        mock_scraper_class = MagicMock(return_value=mock_scraper_instance)
        
        mock_module = MagicMock()
        setattr(mock_module, "Anbima550Scraper", mock_scraper_class)

        def side_effect(name, *args, **kwargs):
            if name == "scrapers.anbima_550":
                return mock_module
            return real_import(name, *args, **kwargs)
        mock_import = MagicMock(side_effect=side_effect)

        with patch.object(main_module, "load_entity_dates", mock_load), \
             patch.object(main_module, "check_gaps", mock_check_gaps), \
             patch.object(main_module.importlib, "import_module", mock_import), \
             patch.object(main_module.Path, "exists", mock_exists):

            # Executa de fato
            main(
                csv_filter=["anbima_550.csv"],
                threshold=2,
                dry_run=False,
                quiet=True,
            )

        # Verifica se o scraper foi importado e executado com target_date correto
        mock_scraper_class.assert_called_once()
        assert mock_scraper_instance.target_date == date(2026, 6, 2)
        mock_scraper_instance.run.assert_called_once()

    def test_backfill_execution_yahoo(self):
        mock_exists = MagicMock(return_value=True)
        mock_load = MagicMock(return_value={("*",): {"2026-06-01", "2026-06-05"}})
        mock_check_gaps = MagicMock(return_value={("*",): ["2026-06-02", "2026-06-03", "2026-06-04"]})

        # Mock da classe Scraper
        mock_scraper_instance = MagicMock()
        mock_scraper_class = MagicMock(return_value=mock_scraper_instance)
        
        mock_module = MagicMock()
        setattr(mock_module, "YahooEtfsScraper", mock_scraper_class)

        def side_effect(name, *args, **kwargs):
            if name == "scrapers.yahoo_etfs":
                return mock_module
            return real_import(name, *args, **kwargs)
        mock_import = MagicMock(side_effect=side_effect)

        with patch.object(main_module, "load_entity_dates", mock_load), \
             patch.object(main_module, "check_gaps", mock_check_gaps), \
             patch.object(main_module.importlib, "import_module", mock_import), \
             patch.object(main_module.Path, "exists", mock_exists):

            # Executa de fato
            main(
                csv_filter=["yahoo_etfs.csv"],
                threshold=2,
                dry_run=False,
                quiet=True,
            )

        # Verifica se o scraper do Yahoo Finance foi importado e executado com start/end dates
        mock_scraper_class.assert_called_once()
        assert mock_scraper_instance.start_date == date(2026, 6, 2)
        assert mock_scraper_instance.end_date == date(2026, 6, 4)
        mock_scraper_instance.run.assert_called_once()
