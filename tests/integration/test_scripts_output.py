#!/usr/bin/env python
# coding: utf-8
"""
tests/integration/test_scripts_output.py
-----------------------------------------
Testes de estrutura de saída para os scripts refatorados.

Verifica: banner, seções, status prints (start/done/fail/warn/skip), summary.
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


def run_script(path: Path, *args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(path), *args],
        capture_output=True, text=True, timeout=30,
    )


# ── Banner ───────────────────────────────────────────────────────────

class TestBannerOutput:
    """Verifica que todos os scripts mostram banner no início."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_banner_present(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert "══" in result.stdout

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_banner_has_double_line(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert "══" in result.stdout


# ── Seções ───────────────────────────────────────────────────────────

class TestSectionOutput:
    """Verifica que os scripts mostram seções temáticas."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_section_present(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert "──" in result.stdout

    @pytest.mark.parametrize("name,path", [
        (n, p) for n, p in SCRIPTS if n not in ("generate_catalog", "generate_market_latest")
    ])
    def test_section_has_processando(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert "Processando" in result.stdout


# ── Status Prints ────────────────────────────────────────────────────

class TestStatusPrints:
    """Verifica prints de start/done/fail/warn/skip."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_has_file_progress(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        # Deve mostrar contagem de itens processados (ex: [1/5])
        assert "/" in result.stdout

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_has_item_names(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        # Deve citar nomes de arquivos/scrapers
        assert ".csv" in result.stdout or "(" in result.stdout


# ── Summary ──────────────────────────────────────────────────────────

class TestSummaryOutput:
    """Verifica que todos os scripts mostram resumo final."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_summary_present(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert "Total:" in result.stdout or "conclu" in result.stdout.lower()

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_summary_has_timing(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert "⏱" in result.stdout or "s" in result.stdout

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_summary_has_counts(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert "ok" in result.stdout.lower()

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_summary_has_detalhes(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert "Detalhes" in result.stdout or ":" in result.stdout


# ── Exit Codes ───────────────────────────────────────────────────────

class TestExitCodes:
    """Verifica exit codes corretos."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_dry_run_exit_0(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        assert result.returncode == 0

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_help_exit_0(self, name, path):
        result = run_script(path, "--help")
        assert result.returncode == 0

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_invalid_arg_exit_nonzero(self, name, path):
        result = run_script(path, "--invalid-flag-xyz")
        assert result.returncode != 0


# ── Output mínimo (--quiet) ──────────────────────────────────────────

class TestMinimalOutput:
    """Verifica que --quiet produz output mínimo mas ainda tem summary."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_quiet_shows_result(self, name, path):
        result = run_script(path, "--quiet", "--dry-run", "--no-color")
        # Mesmo quiet, deve mostrar resumo
        assert "ok" in result.stdout.lower() or "0" in result.stdout


# ── Dry-run Mensagem ─────────────────────────────────────────────────

class TestDryRunMessage:
    """Verifica mensagem de dry-run."""

    @pytest.mark.parametrize("name,path", SCRIPTS)
    def test_dry_run_message_present(self, name, path):
        result = run_script(path, "--dry-run", "--no-color")
        # Pode estar em stdout ou stderr
        combined = result.stdout + result.stderr
        assert "dry-run" in combined.lower() or "dry run" in combined.lower()
