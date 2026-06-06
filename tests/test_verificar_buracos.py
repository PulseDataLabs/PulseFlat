#!/usr/bin/env python
# coding: utf-8
"""
tests/test_verificar_buracos.py
--------------------------------
Testes unitários para scripts/verificar_buracos.py

Rodar: python -m pytest tests/test_verificar_buracos.py -v
"""

import csv
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.parsers import _CAL
from scripts.verificar_buracos import (
    _parse_date,
    load_entity_dates,
    check_gaps,
    _entity_label,
)


# ── _parse_date ──────────────────────────────────────────────────────

class TestParseDate:
    def test_iso_format(self):
        assert _parse_date("2026-06-01") == "2026-06-01"

    def test_datetime_format(self):
        assert _parse_date("2026-06-01T00:00:00") == "2026-06-01"

    def test_yyyymmdd_format(self):
        assert _parse_date("20260601") == "2026-06-01"

    def test_empty_string(self):
        assert _parse_date("") is None

    def test_whitespace_string(self):
        assert _parse_date("  ") is None

    def test_invalid_string(self):
        assert _parse_date("not-a-date") is None

    def test_partial_date(self):
        assert _parse_date("2026-06") is None

    def test_trailing_whitespace(self):
        assert _parse_date("  2026-06-01  ") == "2026-06-01"

    def test_datetime_with_timezone(self):
        assert _parse_date("2026-06-01T12:30:00-03:00") == "2026-06-01"

    def test_yyyymmdd_nondigit(self):
        assert _parse_date("abc") is None


# ── load_entity_dates ────────────────────────────────────────────────

class TestLoadEntityDates:
    def test_single_entity_no_group_by(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text(
            "data_captura,indicador,valor\n"
            "2026-06-01,CDI,14.40\n"
            "2026-06-02,CDI,14.40\n"
            "2026-06-03,CDI,14.40\n"
        )
        result = load_entity_dates(csv_path, "data_captura", [])
        assert ("*",) in result
        assert result[("*",)] == {"2026-06-01", "2026-06-02", "2026-06-03"}

    def test_group_by_column(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text(
            "data_captura,indice,numero_indice\n"
            "2026-06-01,IRF-M,100.0\n"
            "2026-06-01,IMA-B,200.0\n"
            "2026-06-02,IRF-M,101.0\n"
            "2026-06-02,IMA-B,201.0\n"
        )
        result = load_entity_dates(csv_path, "data_captura", ["indice"])
        assert ("IRF-M",) in result
        assert ("IMA-B",) in result
        assert result[("IRF-M",)] == {"2026-06-01", "2026-06-02"}
        assert result[("IMA-B",)] == {"2026-06-01", "2026-06-02"}

    def test_datetime_date_column(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text(
            "rpt_dt,volume\n"
            "2026-06-01T00:00:00,100\n"
            "2026-06-02T00:00:00,200\n"
        )
        result = load_entity_dates(csv_path, "rpt_dt", [])
        assert result[("*",)] == {"2026-06-01", "2026-06-02"}

    def test_missing_date_column(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text("nome,valor\nfoo,1\nbar,2\n")
        result = load_entity_dates(csv_path, "data_captura", [])
        assert result == {}

    def test_empty_csv(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text("data_captura,valor\n")
        result = load_entity_dates(csv_path, "data_captura", [])
        assert result == {}

    def test_case_insensitive_column(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text(
            "DATA_CAPTURA,valor\n"
            "2026-06-01,10\n"
        )
        result = load_entity_dates(csv_path, "data_captura", [])
        assert result[("*",)] == {"2026-06-01"}

    def test_mixed_date_formats(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text(
            "data_captura,valor\n"
            "2026-06-01,10\n"
            "20260602,20\n"
            "2026-06-03T00:00:00,30\n"
        )
        result = load_entity_dates(csv_path, "data_captura", [])
        assert result[("*",)] == {"2026-06-01", "2026-06-02", "2026-06-03"}

    def test_multiple_group_cols(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text(
            "dt_ref,ticker,price\n"
            "2026-06-01,PETR4,10\n"
            "2026-06-01,VALE3,20\n"
            "2026-06-02,PETR4,11\n"
        )
        result = load_entity_dates(csv_path, "dt_ref", ["ticker"])
        assert result[("PETR4",)] == {"2026-06-01", "2026-06-02"}
        assert result[("VALE3",)] == {"2026-06-01"}

    def test_skip_empty_dates(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text(
            "data_captura,valor\n"
            "2026-06-01,10\n"
            ",20\n"
            "2026-06-03,30\n"
        )
        result = load_entity_dates(csv_path, "data_captura", [])
        assert result[("*",)] == {"2026-06-01", "2026-06-03"}


# ── check_gaps ───────────────────────────────────────────────────────

class TestCheckGaps:
    def test_no_gaps(self):
        dates = {("IRF-M",): {"2026-06-01", "2026-06-02", "2026-06-03"}}
        gaps = check_gaps(dates, threshold=3)
        assert gaps == {}

    def test_gap_in_middle(self):
        dates = {("*",): {"2026-06-01", "2026-06-03"}}
        gaps = check_gaps(dates, threshold=2)
        assert ("*",) in gaps
        assert "2026-06-02" in gaps[("*",)]

    def test_gap_at_start(self):
        dates = {("*",): {"2026-06-02", "2026-06-05", "2026-06-06"}}
        gaps = check_gaps(dates, threshold=3)
        assert ("*",) in gaps
        assert "2026-06-03" in gaps[("*",)]

    def test_gap_at_end(self):
        dates = {("*",): {"2026-06-01", "2026-06-02", "2026-06-04"}}
        gaps = check_gaps(dates, threshold=3)
        assert ("*",) in gaps
        assert "2026-06-03" in gaps[("*",)]

    def test_multiple_gaps(self):
        dates = {("*",): {"2026-06-01", "2026-06-05"}}
        gaps = check_gaps(dates, threshold=2)
        assert len(gaps[("*",)]) == 2
        assert gaps[("*",)] == ["2026-06-02", "2026-06-03"]

    def test_below_threshold(self):
        dates = {("*",): {"2026-06-01", "2026-06-02"}}
        gaps = check_gaps(dates, threshold=3)
        assert gaps == {}

    def test_threshold_boundary(self):
        dates = {("*",): {"2026-06-01", "2026-06-02", "2026-06-03"}}
        gaps = check_gaps(dates, threshold=3)
        assert gaps == {}

    def test_weekend_not_counted_as_gap(self):
        dates = {("*",): {"2026-06-05", "2026-06-08"}}
        gaps = check_gaps(dates, threshold=2)
        assert gaps == {}

    def test_holiday_not_counted_as_gap(self):
        dates = {("*",): {"2026-04-20", "2026-04-22"}}
        gaps = check_gaps(dates, threshold=2)
        assert gaps == {}

    def test_multiple_entities_partial_gaps(self):
        dates = {
            ("A",): {"2026-06-01", "2026-06-02", "2026-06-03"},
            ("B",): {"2026-06-01", "2026-06-03"},
            ("C",): {"2026-06-01"},
        }
        gaps = check_gaps(dates, threshold=2)
        assert ("A",) not in gaps
        assert ("B",) in gaps
        assert "2026-06-02" in gaps[("B",)]
        assert ("C",) not in gaps

    def test_single_date_below_threshold(self):
        dates = {("*",): {"2026-06-01"}}
        gaps = check_gaps(dates, threshold=2)
        assert gaps == {}

    def test_bizdays_seq_is_correct(self):
        may_4 = date(2026, 5, 4)
        may_8 = date(2026, 5, 8)
        expected = _CAL.seq(may_4, may_8)
        expected_str = {d.strftime("%Y-%m-%d") for d in expected}
        assert "2026-05-04" in expected_str
        assert "2026-05-05" in expected_str
        assert "2026-05-06" in expected_str
        assert "2026-05-07" in expected_str
        assert "2026-05-08" in expected_str


# ── _entity_label ────────────────────────────────────────────────────

class TestEntityLabel:
    def test_single_star_entity(self):
        assert _entity_label(("*",)) == ""

    def test_single_group_col(self):
        _entity_label._csv_name = "anbima_ima_completo.csv"
        label = _entity_label(("IRF-M",))
        assert "indice=IRF-M" in label

    def test_multiple_group_cols(self):
        _entity_label._csv_name = "anbima_idka.csv"
        label = _entity_label(("PREFIXADO", "IDkA Pré 3M"))
        assert "no_indexador=PREFIXADO" in label
        assert "no_indice=IDkA Pré 3M" in label

    def test_unknown_csv(self):
        _entity_label._csv_name = "nonexistent.csv"
        label = _entity_label(("foo", "bar"))
        assert label == ""
