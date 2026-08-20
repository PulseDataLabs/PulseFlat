import decimal
from datetime import date, datetime

import numpy as np
import pandas as pd
import pytest

import utils.db as db


class TestSanitizeColumnName:
    """Testes defensivos para sanitização de nomes de colunas SQL."""

    def test_remover_acentos_e_especiais(self):
        assert db.sanitize_column_name("Cotação Ação (R$)") == "COTACAO_ACAO_R_"
        assert db.sanitize_column_name("Preço Médio / Volume") == "PRECO_MEDIO_VOLUME"
        assert db.sanitize_column_name("Taxa de Juros % a.a.") == "TAXA_DE_JUROS_A_A_"

    def test_prefixo_numerico(self):
        assert db.sanitize_column_name("123_ativo") == "C_123_ATIVO"
        assert db.sanitize_column_name("2026_ano") == "C_2026_ANO"

    def test_palavras_reservadas(self):
        assert db.sanitize_column_name("DATE") == "DATE_VAL"
        assert db.sanitize_column_name("number") == "NUMBER_VAL"
        assert db.sanitize_column_name("Table") == "TABLE_VAL"
        assert db.sanitize_column_name("user") == "USER_VAL"

    def test_tamanho_maximo(self):
        long_name = "A" * 200
        sanitized = db.sanitize_column_name(long_name)
        assert len(sanitized) <= 128
        assert sanitized == "A" * 128

    def test_caracteres_vazios_ou_extremos(self):
        assert db.sanitize_column_name("") == ""
        assert db.sanitize_column_name("___") == "_"
        assert db.sanitize_column_name("   ") == ""


class TestInferOracleType:
    """Testes defensivos para inferência de tipos Oracle SQL."""

    def test_coluna_data(self):
        s = pd.Series(["2026-01-01", "2026-01-02"], name="data_referencia")
        assert db.infer_oracle_type(s) == "DATE"

        s_dt = pd.Series(["2026-01-01", "2026-01-02"], name="dt_vencimento")
        assert db.infer_oracle_type(s_dt) == "DATE"

    def test_periodo_seis_ou_quatro_digitos_nao_e_date(self):
        s_mes = pd.Series(["202406", "202407"], name="data_mes")
        assert db.infer_oracle_type(s_mes) == "VARCHAR2(4000)"

        s_ano = pd.Series(["2024", "2025"], name="data_ano")
        assert db.infer_oracle_type(s_ano) == "VARCHAR2(4000)"

    def test_tipos_numericos_e_booleanos(self):
        s_bool = pd.Series([True, False, True], name="ativo")
        assert db.infer_oracle_type(s_bool) == "NUMBER(1)"

        s_int = pd.Series([10, 20, 30], dtype="int64", name="quantidade")
        assert db.infer_oracle_type(s_int) == "NUMBER(19)"

        s_float = pd.Series([10.5, 20.3, 30.1], dtype="float64", name="taxa")
        assert db.infer_oracle_type(s_float) == "NUMBER"

    def test_tipo_texto(self):
        s_str = pd.Series(["PETR4", "VALE3"], name="codigo_ativo")
        assert db.infer_oracle_type(s_str) == "VARCHAR2(4000)"


class TestStandardizeValues:
    """Testes defensivos para padronização e comparação de valores."""

    def test_valores_nulos(self):
        assert db.standardize_val(None) is None
        assert db.standardize_val(np.nan) is None
        assert db.standardize_val(pd.NA) is None

    def test_datas_e_timestamps(self):
        dt = datetime(2026, 6, 15, 12, 30, 0)
        assert db.standardize_val(dt) == "2026-06-15"
        assert db.standardize_val(date(2026, 6, 15)) == "2026-06-15"
        assert db.standardize_val(pd.Timestamp("2026-06-15")) == "2026-06-15"

    def test_strings_com_datas(self):
        assert db.standardize_val("15/06/2026") == "2026-06-15"
        assert db.standardize_val("2026-06-15") == "2026-06-15"
        assert db.standardize_val("2026/06/15") == "2026-06-15"
        assert db.standardize_val("  15/06/2026 00:00:00  ") == "2026-06-15"

    def test_numericos_e_decimais(self):
        assert db.standardize_val(100) == 100.0
        assert db.standardize_val(100.5) == 100.5
        assert db.standardize_val(decimal.Decimal("100.55")) == 100.55

    def test_standardize_tuple(self):
        tup = (" 15/06/2026 ", 10, " PETR4 ")
        expected = ("2026-06-15", 10.0, "PETR4")
        assert db.standardize_tuple(tup) == expected


class TestUploadDataFrameDefensive:
    """Testes de segurança e controle de fluxo para upload_dataframe."""

    def test_skip_oracle_db_environment(self, monkeypatch):
        monkeypatch.setenv("SKIP_ORACLE_DB", "1")
        df = pd.DataFrame({"col": [1, 2]})
        assert db.upload_dataframe(df, "TESTE") is False

    def test_dataframe_vazio_ou_none(self, monkeypatch):
        monkeypatch.delenv("SKIP_ORACLE_DB", raising=False)
        assert db.upload_dataframe(None, "TESTE") is False
        assert db.upload_dataframe(pd.DataFrame(), "TESTE") is False

    def test_sem_credenciais(self, monkeypatch):
        monkeypatch.delenv("SKIP_ORACLE_DB", raising=False)
        monkeypatch.delenv("ORACLE_DB_USER", raising=False)
        monkeypatch.delenv("ORACLE_DB_PASSWORD", raising=False)
        monkeypatch.delenv("ORACLE_DB_DSN", raising=False)
        df = pd.DataFrame({"col": [1, 2]})
        assert db.upload_dataframe(df, "TESTE") is False

    def test_get_engine_sem_credenciais_lanca_erro(self, monkeypatch):
        monkeypatch.delenv("ORACLE_DB_USER", raising=False)
        monkeypatch.delenv("ORACLE_DB_PASSWORD", raising=False)
        monkeypatch.delenv("ORACLE_DB_DSN", raising=False)
        db._engine = None
        with pytest.raises(ValueError, match="Credenciais do banco ausentes"):
            db.get_engine()
