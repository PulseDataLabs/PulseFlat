#!/usr/bin/env python
# coding: utf-8
"""
tests/unit/test_ux_helpers.py
-----------------------------
Testes dos helpers visuais (_line, _progress_bar, _spinner) e ícones.
"""

import scripts.utils.ux as ux


class TestLineHelper:
    """Testes da função _line(char, width)."""

    def test_default_line(self):
        ux.configure(use_color=True, use_unicode=False)
        result = ux._line()
        assert len(result) >= 72
        assert "─" in result

    def test_custom_char_and_width(self):
        ux.configure(use_color=True, use_unicode=False)
        result = ux._line("=", 20)
        # Remove ANSI codes to verify core content
        import re
        plain = re.sub(r'\033\[[0-9;]*m', '', result)
        assert len(plain) == 20
        assert plain == "=" * 20

    def test_applies_dim_when_color_enabled(self):
        ux.configure(use_color=True, use_unicode=False)
        result = ux._line("─", 10)
        assert "\033[2m" in result
        assert "\033[0m" in result

    def test_plain_when_color_disabled(self):
        ux.configure(use_color=False, use_unicode=False)
        result = ux._line("─", 10)
        assert result == "─" * 10
        assert "\033" not in result


class TestProgressBar:
    """Testes da função _progress_bar(done, total, width)."""

    def test_zero_total_returns_empty(self):
        ux.configure(use_color=True, use_unicode=False)
        assert ux._progress_bar(0, 0) == ""
        assert ux._progress_bar(5, 0) == ""

    def test_zero_percent(self):
        ux.configure(use_color=True, use_unicode=False)
        result = ux._progress_bar(0, 10, width=10)
        assert "░" * 10 in result
        assert "0%" in result
        assert "(0/10)" in result

    def test_hundred_percent(self):
        ux.configure(use_color=True, use_unicode=False)
        result = ux._progress_bar(10, 10, width=10)
        assert "█" * 10 in result
        assert "100%" in result
        assert "(10/10)" in result

    def test_fifty_percent(self):
        ux.configure(use_color=True, use_unicode=False)
        result = ux._progress_bar(5, 10, width=10)
        assert "█" * 5 in result
        assert "░" * 5 in result
        assert "50%" in result

    def test_applies_cyan_to_bar_dim_to_text(self):
        ux.configure(use_color=True, use_unicode=False)
        result = ux._progress_bar(5, 10, width=10)
        assert "\033[36m" in result  # cyan
        assert "\033[2m" in result   # dim


class TestSpinner:
    """Testes do generator _spinner()."""

    def test_yields_frames_in_order(self):
        spinner = ux._spinner("ABC")
        frames = [next(spinner) for _ in range(6)]
        assert frames == ["A", "B", "C", "A", "B", "C"]

    def test_default_frames(self):
        spinner = ux._spinner()
        frames = [next(spinner) for _ in range(12)]
        assert len(set(frames)) > 1
        assert all(len(f) == 1 for f in frames)


class TestIcons:
    """Testes dos dicionários de ícones."""

    def test_icon_keys_exist(self):
        ux.configure(use_color=True, use_unicode=False)
        expected_keys = {"success", "fail", "warn", "info", "skip", "file", "package",
                         "refresh", "clean", "chart", "clock", "folder", "search", "gear", "rocket"}
        assert set(ux.ICON.keys()) == expected_keys

    def test_group_icons_complete(self):
        expected_groups = {"anbima", "b3", "bcb", "cvm", "ibge", "ratings", "misc"}
        assert set(ux.GROUP_ICON.keys()) == expected_groups
        assert set(ux.GROUP_COLOR.keys()) == expected_groups

    def test_group_color_functions_are_callable(self):
        for group, color_fn in ux.GROUP_COLOR.items():
            result = color_fn("test")
            assert isinstance(result, str)
            assert len(result) > 0
