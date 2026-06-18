#!/usr/bin/env python
# coding: utf-8
"""
tests/unit/test_ux.py
---------------------
Testes unitários do módulo ux.py: status prints, ColorLogger, CLI args, summary.
"""

import logging
import argparse
import io
from contextlib import redirect_stdout

import pytest
import scripts.utils.ux as ux


def capture_print(func, *args, **kwargs) -> str:
    """Executa func com stdout capturado e retorna a string."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        func(*args, **kwargs)
    return buf.getvalue()


# ── Status Prints ─────────────────────────────────────────────────────

class TestStatusPrints:
    """Testes das funções print_start/done/fail/warn/skip/info."""

    def test_print_start(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_start, "iniciando algo")
        assert "iniciando algo" in out

    def test_print_done(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_done, "pronto", elapsed=1.5)
        assert "pronto" in out
        assert "1.5s" in out

    def test_print_done_no_elapsed(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_done, "pronto")
        assert "pronto" in out
        assert "s" not in out

    def test_print_fail(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_fail, "deu erro", elapsed=0.5)
        assert "deu erro" in out
        assert "0.5s" in out

    def test_print_warn(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_warn, "cuidado")
        assert "cuidado" in out

    def test_print_skip(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_skip, "pulado")
        assert "pulado" in out

    def test_print_info(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_info, "informativo")
        assert "informativo" in out

    def test_custom_icon(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_start, "com ícone", icon="clean")
        assert "com ícone" in out

    def test_ansi_codes_when_color_enabled(self):
        ux.configure(use_color=True, use_unicode=False)
        out = capture_print(ux.print_done, "ok")
        assert "\033[" in out

    def test_no_ansi_when_color_disabled(self):
        ux.configure(use_color=False, use_unicode=False)
        out = capture_print(ux.print_done, "ok")
        assert "\033[" not in out


# ── Print Summary ─────────────────────────────────────────────────────

class TestPrintSummary:
    """Testes da função print_summary."""

    def test_summary_no_errors(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_summary, "Teste", total=10, success=10, failed=0, elapsed=5.0)
        assert "Teste" in out
        assert "10" in out
        assert "0 erros" in out
        assert "5.0s" in out

    def test_summary_with_errors(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_summary, "Teste", total=10, success=7, failed=3, elapsed=5.0)
        assert "3 erro(s)" in out

    def test_summary_with_skipped(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_summary, "Teste", total=10, success=7, failed=2, skipped=1, elapsed=5.0)
        assert "1" in out
        assert "pulado" in out

    def test_summary_with_details(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_summary, "Teste", total=5, success=5, failed=0, elapsed=3.0,
                            details=[("file", "Arquivos", "10"), ("clock", "Tempo", "3s")])
        assert "Arquivos" in out
        assert "10" in out
        assert "Tempo" in out
        assert "3s" in out

    def test_summary_empty(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.print_summary, "Teste", total=0, success=0, failed=0, elapsed=0.0)
        assert "Teste" in out


# ── ColorLogger ───────────────────────────────────────────────────────

class TestColorLogger:
    """Testes do ColorLogger."""

    def test_debug(self):
        ux.configure(use_color=False, use_unicode=False)
        log = ux.ColorLogger("test_debug")
        log.debug("debug msg")

    def test_info(self):
        ux.configure(use_color=False, use_unicode=False)
        log = ux.ColorLogger("test_info")
        log.info("info msg")

    def test_success(self, capsys):
        ux.configure(use_color=False, use_unicode=True)
        log = ux.ColorLogger("test_success")
        log.success("sucesso")
        out = capsys.readouterr()
        assert "sucesso" in (out.out + out.err)

    def test_warning(self, capsys):
        ux.configure(use_color=False, use_unicode=True)
        log = ux.ColorLogger("test_warn")
        log.warning("aviso")
        out = capsys.readouterr()
        assert "aviso" in (out.out + out.err)

    def test_error(self, capsys):
        ux.configure(use_color=False, use_unicode=True)
        log = ux.ColorLogger("test_err")
        log.error("erro!")
        out = capsys.readouterr()
        assert "erro!" in (out.out + out.err)

    def test_critical(self, capsys):
        ux.configure(use_color=False, use_unicode=True)
        log = ux.ColorLogger("test_crit")
        log.critical("critico")
        out = capsys.readouterr()
        assert "critico" in (out.out + out.err)

    def test_ansi_applied(self, capsys):
        ux.configure(use_color=True, use_unicode=False)
        log = ux.ColorLogger("test_ansi")
        log.success("ok")
        out = capsys.readouterr()
        assert "\033[" in (out.out + out.err)

    def test_no_ansi_when_disabled(self):
        ux.configure(use_color=False, use_unicode=False)
        log = ux.ColorLogger("test_no_ansi")
        out = capture_print(log.success, "ok")
        assert "\033[" not in out

    def test_set_level(self):
        ux.configure(use_color=False, use_unicode=False)
        log = ux.ColorLogger("test_level")
        log.setLevel(logging.WARNING)
        buf = io.StringIO()
        handler = logging.StreamHandler(buf)
        handler.setFormatter(logging.Formatter("%(message)s"))
        log._logger.addHandler(handler)
        log.info("não deve aparecer")
        log.warning("deve aparecer")
        assert "deve aparecer" in buf.getvalue()
        assert "não deve aparecer" not in buf.getvalue()

    def test_logger_name(self):
        ux.configure(use_color=False, use_unicode=False)
        log = ux.ColorLogger("meu_logger")
        assert log._logger.name == "meu_logger"


# ── CLI Common Args ───────────────────────────────────────────────────

class TestCLIArgs:
    """Testes de add_common_args e apply_common_args."""

    def test_add_common_args_creates_flags(self):
        parser = argparse.ArgumentParser()
        ux.add_common_args(parser)
        args = parser.parse_args([])
        assert args.quiet is False
        assert args.verbose is False
        assert args.no_color is False
        assert args.dry_run is False

    def test_quiet_flag(self):
        parser = argparse.ArgumentParser()
        ux.add_common_args(parser)
        args = parser.parse_args(["--quiet"])
        assert args.quiet is True

    def test_verbose_flag(self):
        parser = argparse.ArgumentParser()
        ux.add_common_args(parser)
        args = parser.parse_args(["--verbose"])
        assert args.verbose is True

    def test_no_color_flag(self):
        parser = argparse.ArgumentParser()
        ux.add_common_args(parser)
        args = parser.parse_args(["--no-color"])
        assert args.no_color is True

    def test_dry_run_flag(self):
        parser = argparse.ArgumentParser()
        ux.add_common_args(parser)
        args = parser.parse_args(["--dry-run"])
        assert args.dry_run is True

    def test_short_forms(self):
        parser = argparse.ArgumentParser()
        ux.add_common_args(parser)
        args = parser.parse_args(["-q", "-v"])
        assert args.quiet is True
        assert args.verbose is True

    def test_apply_no_color(self):
        ux.configure(use_color=True, use_unicode=False)
        assert ux.USE_COLOR is True
        parser = argparse.ArgumentParser()
        ux.add_common_args(parser)
        args = parser.parse_args(["--no-color"])
        ux.apply_common_args(args)
        assert ux.USE_COLOR is False
        ux.configure(use_color=True, use_unicode=False)

    def test_apply_quiet_warning(self):
        original_level = logging.getLogger().level
        parser = argparse.ArgumentParser()
        ux.add_common_args(parser)
        args = parser.parse_args(["--quiet"])
        ux.apply_common_args(args)
        assert logging.getLogger().level == logging.WARNING
        logging.getLogger().setLevel(original_level)

    def test_apply_verbose_debug(self):
        original_level = logging.getLogger().level
        parser = argparse.ArgumentParser()
        ux.add_common_args(parser)
        args = parser.parse_args(["--verbose"])
        ux.apply_common_args(args)
        assert logging.getLogger().level == logging.DEBUG
        logging.getLogger().setLevel(original_level)


# ── Banner and Section ────────────────────────────────────────────────

class TestBannerSection:
    """Testes de banner() e section()."""

    def test_banner_shows_title(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.banner, "Meu Script")
        assert "Meu Script" in out

    def test_banner_with_subtitle(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.banner, "Meu Script", "Subtitle aqui")
        assert "Meu Script" in out
        assert "Subtitle aqui" in out

    def test_banner_no_subtitle(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.banner, "Só título")
        assert "Só título" in out

    def test_section_shows_title(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.section, "Processando...", icon="clean")
        assert "Processando..." in out

    def test_section_default_icon(self):
        ux.configure(use_color=False, use_unicode=True)
        out = capture_print(ux.section, "Seção")
        assert "Seção" in out

    def test_banner_ansi_lines(self):
        ux.configure(use_color=True, use_unicode=False)
        out = capture_print(ux.banner, "Teste")
        assert "\033[" in out


# ── Module __all__ ────────────────────────────────────────────────────

class TestModuleAll:
    """Testa que __all__ está completo e exporta tudo."""

    def test_all_exports_exist(self):
        for name in ux.__all__:
            assert hasattr(ux, name), f"{name} não encontrado no módulo"
