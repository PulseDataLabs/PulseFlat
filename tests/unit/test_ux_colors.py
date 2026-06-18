#!/usr/bin/env python
# coding: utf-8
"""
tests/unit/test_ux_colors.py
----------------------------
Testes de detecção de ambiente e cores (USE_COLOR, USE_UNICODE).
"""

import os
import sys
from unittest.mock import patch

import pytest
import scripts.utils.ux as ux


class TestColorDetection:
    """Testes de detecção USE_COLOR baseada em ambiente."""

    def test_tty_enables_color(self):
        ux.configure(use_color=True, use_unicode=False)
        assert ux.USE_COLOR is True

    def test_no_color_disables(self):
        ux.configure(use_color=False, use_unicode=False)
        assert ux.USE_COLOR is False

    def test_configure_preserves_unicode(self):
        ux.configure(use_color=True, use_unicode=True)
        assert ux.USE_COLOR is True
        assert ux.USE_UNICODE is True

    def test_configure_preserves_color(self):
        ux.configure(use_color=False, use_unicode=False)
        assert ux.USE_COLOR is False
        assert ux.USE_UNICODE is False


class TestAnsiCodeFunction:
    """Testes da função _c(code, text)."""

    def test_applies_ansi_when_color_enabled(self):
        ux.configure(use_color=True, use_unicode=False)
        result = ux._c("31", "test")
        assert result == "\033[31mtest\033[0m"

    def test_returns_plain_when_color_disabled(self):
        ux.configure(use_color=False, use_unicode=False)
        result = ux._c("31", "test")
        assert result == "test"


class TestPaletteFunctions:
    """Testes das 14 funções de paleta."""

    def test_basic_colors(self):
        ux.configure(use_color=True, use_unicode=False)
        assert ux.red("x") == "\033[31mx\033[0m"
        assert ux.green("x") == "\033[32mx\033[0m"
        assert ux.yellow("x") == "\033[33mx\033[0m"
        assert ux.blue("x") == "\033[34mx\033[0m"
        assert ux.magenta("x") == "\033[35mx\033[0m"
        assert ux.cyan("x") == "\033[36mx\033[0m"
        assert ux.white("x") == "\033[97mx\033[0m"

    def test_bold_and_dim(self):
        ux.configure(use_color=True, use_unicode=False)
        assert ux.bold("x") == "\033[1mx\033[0m"
        assert ux.dim("x") == "\033[2mx\033[0m"

    def test_bright_colors(self):
        ux.configure(use_color=True, use_unicode=False)
        assert ux.b_red("x") == "\033[1;31mx\033[0m"
        assert ux.b_green("x") == "\033[1;32mx\033[0m"
        assert ux.b_yellow("x") == "\033[1;33mx\033[0m"
        assert ux.b_blue("x") == "\033[1;34mx\033[0m"
        assert ux.b_magenta("x") == "\033[1;35mx\033[0m"
        assert ux.b_cyan("x") == "\033[1;36mx\033[0m"
        assert ux.b_white("x") == "\033[1;97mx\033[0m"

    def test_all_return_plain_when_disabled(self):
        ux.configure(use_color=False, use_unicode=False)
        for fn in [ux.red, ux.green, ux.yellow, ux.blue, ux.magenta, ux.cyan, ux.white,
                   ux.bold, ux.dim,
                   ux.b_red, ux.b_green, ux.b_yellow, ux.b_blue, ux.b_magenta, ux.b_cyan, ux.b_white]:
            assert fn("test") == "test"


class TestUnicodeDetection:
    """Testes de detecção USE_UNICODE."""

    def test_tty_utf8_enables_unicode(self):
        ux.configure(use_color=False, use_unicode=True)
        assert ux.USE_UNICODE is True

    def test_non_utf8_disables_unicode(self):
        ux.configure(use_color=False, use_unicode=False)
        assert ux.USE_UNICODE is False

    def test_unicode_icons_enabled(self):
        ux.configure(use_color=False, use_unicode=True)
        assert ux.ICON["success"] == "✔"
        assert ux.ICON["fail"] == "✖"

    def test_ascii_fallback(self):
        ux.configure(use_color=False, use_unicode=False)
        assert ux.ICON["success"] == "[OK]"
        assert ux.ICON["fail"] == "[FAIL]"
