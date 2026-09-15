"""
tests/unit/test_consolidate_formatting.py
-----------------------------------------
Testes unitários para validar a formatação de métricas e cotações de câmbio
com 4 casas decimais em scripts/consolidate.py.
"""

import pytest
from scripts.consolidate import _fmt_val, _fmt_pct, _parse_br_float, _fmt


class TestConsolidateFormatting:
    """Valida funções de conversão e formatação numérica da consolidação."""

    def test_parse_br_float(self):
        assert _parse_br_float("14,50") == 14.50
        assert _parse_br_float("14.50") == 14.50
        assert _parse_br_float("  5.4321  ") == 5.4321
        assert _parse_br_float("invalid") is None
        assert _parse_br_float("") is None

    def test_fmt_val_explicit_decimals(self):
        # 4 casas decimais para câmbio
        assert _fmt_val("5.4321", decimals=4) == "5,4321"
        assert _fmt_val("5.4", decimals=4) == "5,4000"
        assert _fmt_val("5.43219", decimals=4) == "5,4322"
        # 2 casas decimais
        assert _fmt_val("10.5", decimals=2) == "10,50"
        # 0 casas decimais
        assert _fmt_val("1250.75", decimals=0) == "1.251"

    def test_fmt_val_auto_decimals(self):
        # Grandes números >= 1000: 0 casas decimais
        assert _fmt_val("1500.2") == "1.500"
        # Números >= 1: 2 casas decimais
        assert _fmt_val("14.567") == "14,57"
        # Números entre 0.01 e 1: 4 casas decimais
        assert _fmt_val("0.0541") == "0,0541"
        # Números < 0.01: 6 casas decimais
        assert _fmt_val("0.003184") == "0,003184"

    def test_fmt_pct(self):
        assert _fmt_pct("14.5") == "14,50%"
        assert _fmt_pct("0.8503", decimals=4) == "0,8503%"
        assert _fmt_pct("-0.0693") == "-0,07%"

    def test_format_value_fx_rates_preserves_4_decimals(self):
        """Cotações de câmbio (PTAX, Dólar, Euro) devem obrigatoriamente ter 4 casas decimais."""
        # 1. Categoria 'Taxas de Câmbio'
        idef_cambio = {"category": "Taxas de Câmbio"}
        res = _fmt(idef_cambio, raw_val="5.4321", indicator_name="Dólar Comercial")
        assert res == "5,4321"

        # 2. Categoria 'Câmbio / Moedas'
        idef_moedas = {"category": "Câmbio / Moedas"}
        res = _fmt(idef_moedas, raw_val="5.40", indicator_name="EUR/BRL")
        assert res == "5,4000"

        # 3. Nome do indicador contém 'ptax'
        idef_ptax = {"category": "Outros"}
        res = _fmt(idef_ptax, raw_val="5.3987", indicator_name="PTAX Venda")
        assert res == "5,3987"

    def test_format_value_percentage_indicators(self):
        idef_selic = {"category": "Taxas de Juros", "fmt": "pct"}
        res = _fmt(idef_selic, raw_val="13.75", indicator_name="Meta Selic")
        assert res == "13,75%"
