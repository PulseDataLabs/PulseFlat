#!/usr/bin/env python
# coding: utf-8
"""
tests/integration/test_scripts_cli.py
--------------------------------------
Testes de CLI para os scripts de pós-processamento e run_all.py.

Testa flags: --help, --dry-run, --quiet, --verbose, --no-color
"""

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
SCRIPTS = [
    ("limpar_duplicatas", SCRIPTS_DIR / "limpar_duplicatas.py"),
    ("migrate_portfolio_numbers", SCRIPTS_DIR / "migrate_portfolio_numbers.py"),
    ("populate_last_updates", SCRIPTS_DIR / "populate_last_updates.py"),
    ("generate_catalog", SCRIPTS_DIR / "generate_catalog.py"),
    ("generate_market_latest", SCRIPTS_DIR / "generate_market_latest.py"),
]
RUN_ALL = Path(__file__).resolve().parents[2] / "run_all.py"


def run_script(path: Path, *args) -> subprocess.CompletedProcess:
    """Executa um script com argumentos e retorna o resultado."""
    return subprocess.run(
        [sys.executable, str(path), *args],
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestHelpFlag:
    """Testes da flag --help em todos os scripts."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_help_exits_cleanly(self, name, path):
        result = run_script(path, "--help")
        assert result.returncode == 0

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_help_shows_usage(self, name, path):
        result = run_script(path, "--help")
        assert "usage:" in result.stdout.lower()

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_help_shows_common_flags(self, name, path):
        result = run_script(path, "--help")
        assert "--quiet" in result.stdout or "-q" in result.stdout
        assert "--verbose" in result.stdout or "-v" in result.stdout
        assert "--no-color" in result.stdout
        assert "--dry-run" in result.stdout

    def test_run_all_help(self):
        result = run_script(RUN_ALL, "--help")
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()


class TestDryRunFlag:
    """Testes da flag --dry-run."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_dry_run_exits_cleanly(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert result.returncode == 0

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_dry_run_shows_indicator(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert "dry-run" in result.stdout.lower() or "dry-run" in result.stderr.lower()


class TestQuietFlag:
    """Testes da flag --quiet (suprime output não-essencial)."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_quiet_exits_cleanly(self, name, path):
        result = run_script(path, "--quiet", "--dry-run", "--no-color")
        assert result.returncode == 0

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_quiet_exits_without_error(self, name, path):
        quiet = run_script(path, "--quiet", "--dry-run", "--no-color")
        assert quiet.returncode == 0
        assert len(quiet.stdout) > 0


class TestVerboseFlag:
    """Testes da flag --verbose (output detalhado)."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_verbose_exits_cleanly(self, name, path):
        result = run_script(path, "--verbose", "--dry-run", "--no-color")
        assert result.returncode == 0


class TestNoColorFlag:
    """Testes da flag --no-color."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_no_color_removes_ansi(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert "\033[" not in result.stdout

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_no_color_still_outputs_content(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert len(result.stdout) > 0


class TestRunAllFlags:
    """Testes específicos para run_all.py."""

    def test_list_exits_cleanly(self):
        result = run_script(RUN_ALL, "--list")
        assert result.returncode == 0

    def test_list_shows_scrapers(self):
        result = run_script(RUN_ALL, "--list")
        assert "Scrapers disponíveis" in result.stdout or "dispon" in result.stdout.lower()

    def test_generate_catalog_exits_cleanly(self):
        result = run_script(RUN_ALL, "--generate-catalog")
        assert result.returncode == 0

    def test_generate_catalog_shows_success(self):
        result = run_script(RUN_ALL, "--generate-catalog")
        assert "sucesso" in result.stdout.lower() or "success" in result.stdout.lower()

    def test_scraper_not_found(self):
        result = run_script(RUN_ALL, "--scraper", "nao_existe")
        assert result.returncode != 0

    def test_group_invalid(self):
        result = run_script(RUN_ALL, "--group", "invalido")
        assert result.returncode != 0


class TestErrorHandling:
    """Testes de tratamento de erros."""

    def test_invalid_flag_returns_error(self):
        for name, path in SCRIPTS:
            result = run_script(path, "--flag-invalida")
            assert result.returncode != 0

    def test_help_has_examples(self):
        for name, path in SCRIPTS:
            result = run_script(path, "--help")
            assert "exemplos" in result.stdout.lower() or "example" in result.stdout.lower()
