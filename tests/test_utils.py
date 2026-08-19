"""
tests/test_utils.py
-------------------
Testes básicos dos utilitários compartilhados.

Rodar: python -m pytest tests/ -v
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
from base64 import b64decode

from utils import agora_brt, b64_encode_params, limpar, salvar_csv


def test_agora_brt_formato():
    data, hora = agora_brt()
    assert (
        len(data) == 10 and data[4] == "-" and data[7] == "-"
    ), "Data deve ser YYYY-MM-DD"
    assert (
        len(hora) == 8 and hora[2] == ":" and hora[5] == ":"
    ), "Hora deve ser HH:MM:SS"


def test_limpar_none():
    assert limpar(None) == ""


def test_limpar_espacos():
    assert limpar("  PETR4  ") == "PETR4"


def test_limpar_numero():
    assert limpar(123) == "123"


def test_b64_encode_params_decodificavel():
    params = {"language": "pt-br", "pageNumber": 1, "pageSize": 100, "fundsType": "FII"}
    encoded = b64_encode_params(params)
    decoded = json.loads(b64decode(encoded).decode("utf-8"))
    assert decoded == params


def test_b64_encode_sem_espacos():
    """A B3 exige JSON sem espaços nos separadores."""
    params = {"a": 1, "b": 2}
    encoded = b64_encode_params(params)
    decoded_str = b64decode(encoded).decode("utf-8")
    assert " " not in decoded_str


# ─────────────────────────────────────────────
# Testes de deduplicação do salvar_csv
# ─────────────────────────────────────────────

CABECALHO_TESTE = ["data_captura", "indicador", "valor"]


def _ler_csv(arquivo: Path) -> list[dict]:
    with arquivo.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_salvar_csv_primeira_escrita(tmp_path):
    """Deve criar o arquivo com cabeçalho na primeira execução."""
    arquivo = tmp_path / "test.csv"
    dados = [{"data_captura": "2025-06-01", "indicador": "SELIC", "valor": "13.75"}]

    salvar_csv(
        arquivo, dados, CABECALHO_TESTE, chaves_dedup=["data_captura", "indicador"]
    )

    linhas = _ler_csv(arquivo)
    assert len(linhas) == 1
    assert linhas[0]["indicador"] == "SELIC"


def test_salvar_csv_acumula_dias_distintos(tmp_path):
    """Execuções em dias diferentes devem acumular o histórico."""
    arquivo = tmp_path / "test.csv"

    salvar_csv(
        arquivo,
        [{"data_captura": "2025-06-01", "indicador": "SELIC", "valor": "13.75"}],
        CABECALHO_TESTE,
        chaves_dedup=["data_captura", "indicador"],
    )

    salvar_csv(
        arquivo,
        [{"data_captura": "2025-06-02", "indicador": "SELIC", "valor": "13.80"}],
        CABECALHO_TESTE,
        chaves_dedup=["data_captura", "indicador"],
    )

    linhas = _ler_csv(arquivo)
    assert len(linhas) == 2, "Dias distintos devem ser preservados"
    datas = {l["data_captura"] for l in linhas}
    assert datas == {"2025-06-01", "2025-06-02"}


def test_salvar_csv_dedup_mesmo_dia_mesma_chave(tmp_path):
    """Re-execução no mesmo dia não deve duplicar — deve substituir."""
    arquivo = tmp_path / "test.csv"

    # Primeira execução
    salvar_csv(
        arquivo,
        [
            {"data_captura": "2025-06-01", "indicador": "SELIC", "valor": "13.75"},
            {"data_captura": "2025-06-01", "indicador": "DI", "valor": "13.65"},
        ],
        CABECALHO_TESTE,
        chaves_dedup=["data_captura", "indicador"],
    )

    # Segunda execução no mesmo dia
    salvar_csv(
        arquivo,
        [{"data_captura": "2025-06-01", "indicador": "SELIC", "valor": "13.80"}],
        CABECALHO_TESTE,
        chaves_dedup=["data_captura", "indicador"],
    )

    linhas = _ler_csv(arquivo)
    assert len(linhas) == 2, "Deve haver 2 linhas: DI (preservado) + SELIC (atualizado)"

    selic = next(l for l in linhas if l["indicador"] == "SELIC")
    assert selic["valor"] == "13.80", "Deve manter o valor mais recente"

    di = next(l for l in linhas if l["indicador"] == "DI")
    assert di["valor"] == "13.65", "DI não deve ter sido alterado"


def test_salvar_csv_dedup_simples_sem_chaves(tmp_path):
    """Sem chaves_dedup, remove todas as linhas do mesmo dia (dedup simples)."""
    arquivo = tmp_path / "test.csv"

    salvar_csv(
        arquivo,
        [{"data_captura": "2025-06-01", "indicador": "SELIC", "valor": "13.75"}],
        CABECALHO_TESTE,
    )

    salvar_csv(
        arquivo,
        [
            {"data_captura": "2025-06-01", "indicador": "SELIC", "valor": "13.80"},
            {"data_captura": "2025-06-01", "indicador": "DI", "valor": "13.65"},
        ],
        CABECALHO_TESTE,
    )

    linhas = _ler_csv(arquivo)
    assert len(linhas) == 2, "Deve substituir todas as linhas do mesmo dia"
    assert all(l["data_captura"] == "2025-06-01" for l in linhas)


def test_salvar_csv_preserva_historico_anterior(tmp_path):
    """Linhas de dias anteriores nunca devem ser apagadas."""
    arquivo = tmp_path / "test.csv"

    for dia in ["2025-05-28", "2025-05-29", "2025-05-30"]:
        salvar_csv(
            arquivo,
            [{"data_captura": dia, "indicador": "SELIC", "valor": "13.75"}],
            CABECALHO_TESTE,
            chaves_dedup=["data_captura", "indicador"],
        )

    # Re-execução apenas no último dia
    salvar_csv(
        arquivo,
        [{"data_captura": "2025-05-30", "indicador": "SELIC", "valor": "13.80"}],
        CABECALHO_TESTE,
        chaves_dedup=["data_captura", "indicador"],
    )

    linhas = _ler_csv(arquivo)
    assert len(linhas) == 3, "Histórico dos 3 dias deve ser preservado"

    por_data = {l["data_captura"]: l for l in linhas}
    assert (
        por_data["2025-05-30"]["valor"] == "13.80"
    ), "Último dia deve ter valor atualizado"
    assert por_data["2025-05-28"]["valor"] == "13.75", "Dias anteriores não devem mudar"
    assert por_data["2025-05-29"]["valor"] == "13.75", "Dias anteriores não devem mudar"


def test_salvar_csv_sem_acumular(tmp_path):
    """Quando acumular=False, deve sobrescrever completamente o arquivo contendo apenas os novos dados."""
    arquivo = tmp_path / "test.csv"

    # Primeira execução
    salvar_csv(
        arquivo,
        [{"data_captura": "2025-06-01", "indicador": "SELIC", "valor": "13.75"}],
        CABECALHO_TESTE,
    )

    # Segunda execução sem acúmulo
    salvar_csv(
        arquivo,
        [{"data_captura": "2025-06-02", "indicador": "DI", "valor": "13.65"}],
        CABECALHO_TESTE,
        acumular=False,
    )

    linhas = _ler_csv(arquivo)
    assert len(linhas) == 1, "Deve conter apenas o novo registro"
    assert linhas[0]["indicador"] == "DI"
    assert linhas[0]["valor"] == "13.65"
    assert linhas[0]["data_captura"] == "2025-06-02"


# ─────────────────────────────────────────────
# Testes do utilitário de Banco de Dados Oracle
# ─────────────────────────────────────────────


def test_sanitize_column_name():
    from utils.db import sanitize_column_name

    assert sanitize_column_name("data_captura") == "DATA_CAPTURA"
    assert sanitize_column_name("Preço Médio ($)") == "PRECO_MEDIO_"
    assert sanitize_column_name("123_ticker") == "C_123_TICKER"
    assert sanitize_column_name("DATE") == "DATE_VAL"
    assert sanitize_column_name("Ação e Opção") == "ACAO_E_OPCAO"
    assert sanitize_column_name("Muito_Longo_" * 20) == ("MUITO_LONGO_" * 20)[:128]


def test_infer_oracle_type():
    import pandas as pd

    from utils.db import infer_oracle_type

    s_int = pd.Series([1, 2, 3], name="id")
    s_float = pd.Series([1.5, 2.5], name="valor")
    s_bool = pd.Series([True, False], name="flag")
    s_str = pd.Series(["a", "b"], name="nome")
    s_date = pd.Series(["2025-06-01", "2025-06-02"], name="dt_captura")
    s_anomes = pd.Series(["202406", "202412"], name="AnoMes")

    assert infer_oracle_type(s_int) == "NUMBER(19)"
    assert infer_oracle_type(s_float) == "NUMBER"
    assert infer_oracle_type(s_bool) == "NUMBER(1)"
    assert infer_oracle_type(s_str) == "VARCHAR2(4000)"
    assert infer_oracle_type(s_date) == "DATE"
    assert infer_oracle_type(s_anomes) == "VARCHAR2(4000)"


def test_upload_dataframe_optimization(monkeypatch):
    monkeypatch.setenv("ORACLE_DB_USER", "test_user")
    monkeypatch.setenv("ORACLE_DB_PASSWORD", "test_pass")
    monkeypatch.setenv("ORACLE_DB_DSN", "test_dsn")

    from unittest.mock import MagicMock, patch

    import pandas as pd

    from utils.db import upload_dataframe

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    def mock_fetchone():
        args = mock_cursor.execute.call_args
        if args:
            sql = args[0][0]
            if "user_tables" in sql:
                return (1,)
            if "user_tab_columns" in sql:
                return ("DATE",)
        return None

    mock_cursor.fetchone.side_effect = mock_fetchone
    mock_cursor.fetchall.return_value = [("2026-06-28", "ABC")]

    df = pd.DataFrame(
        [
            {
                "data_referencia": "2026-06-28",
                "codigo_ativo": "ABC",
                "valor": 10.0,
            },  # duplicate
            {
                "data_referencia": "2026-06-29",
                "codigo_ativo": "DEF",
                "valor": 20.0,
            },  # new
        ]
    )

    with patch("utils.db.get_connection", return_value=mock_conn):
        with patch("utils.db.oracledb", new=MagicMock()):
            with patch("utils.db.create_engine", new=MagicMock()):
                success = upload_dataframe(
                    df, "TEST_TABLE", chaves_dedup=["data_referencia", "codigo_ativo"]
                )

    assert success is True
    assert mock_cursor.executemany.called
    insert_args = mock_cursor.executemany.call_args[0]
    batch = insert_args[1]
    assert len(batch) == 1
    assert "DEF" in batch[0]
    assert "ABC" not in batch[0]


def test_upload_dataframe_type_normalization(monkeypatch):
    monkeypatch.setenv("ORACLE_DB_USER", "test_user")
    monkeypatch.setenv("ORACLE_DB_PASSWORD", "test_pass")
    monkeypatch.setenv("ORACLE_DB_DSN", "test_dsn")

    from datetime import date
    from unittest.mock import MagicMock, patch

    import pandas as pd

    from utils.db import upload_dataframe

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    def mock_fetchone():
        args = mock_cursor.execute.call_args
        if args:
            sql = args[0][0]
            if "user_tables" in sql:
                return (1,)
            if "user_tab_columns" in sql:
                return ("DATE",)
        return None

    mock_cursor.fetchone.side_effect = mock_fetchone
    mock_cursor.fetchall.return_value = [(date(2026, 6, 28), "  ABC  ")]

    df = pd.DataFrame(
        [
            {
                "data_referencia": pd.Timestamp("2026-06-28"),
                "codigo_ativo": "ABC",
                "valor": 10.0,
            },  # duplicate
            {
                "data_referencia": "2026-06-29",
                "codigo_ativo": "DEF",
                "valor": 20.0,
            },  # new
        ]
    )

    with patch("utils.db.get_connection", return_value=mock_conn):
        with patch("utils.db.oracledb", new=MagicMock()):
            with patch("utils.db.create_engine", new=MagicMock()):
                success = upload_dataframe(
                    df, "TEST_TABLE", chaves_dedup=["data_referencia", "codigo_ativo"]
                )

    assert success is True
    assert mock_cursor.executemany.called
    batch = mock_cursor.executemany.call_args[0][1]
    assert len(batch) == 1
    assert "DEF" in batch[0]


def test_upload_dataframe_new_table(monkeypatch):
    monkeypatch.setenv("ORACLE_DB_USER", "test_user")
    monkeypatch.setenv("ORACLE_DB_PASSWORD", "test_pass")
    monkeypatch.setenv("ORACLE_DB_DSN", "test_dsn")

    from unittest.mock import MagicMock, patch

    import pandas as pd

    from utils.db import upload_dataframe

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (0,)

    df = pd.DataFrame(
        [
            {"data_referencia": "2026-06-29", "codigo_ativo": "ABC", "valor": 10.0},
        ]
    )

    with patch("utils.db.get_connection", return_value=mock_conn):
        with patch("utils.db.oracledb", new=MagicMock()):
            with patch("utils.db.create_engine", new=MagicMock()):
                success = upload_dataframe(
                    df, "TEST_TABLE", chaves_dedup=["data_referencia", "codigo_ativo"]
                )

    assert success is True
    create_executed = any(
        "CREATE TABLE" in args[0][0] for args in mock_cursor.execute.call_args_list
    )
    assert create_executed is True
    assert mock_cursor.executemany.called
    batch = mock_cursor.executemany.call_args[0][1]
    assert len(batch) == 1
