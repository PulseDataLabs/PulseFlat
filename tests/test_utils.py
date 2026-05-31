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

from utils import agora_brt, limpar, b64_encode_params, salvar_csv
import json
from base64 import b64decode


def test_agora_brt_formato():
    data, hora = agora_brt()
    assert len(data) == 10 and data[4] == "-" and data[7] == "-", "Data deve ser YYYY-MM-DD"
    assert len(hora) == 8 and hora[2] == ":" and hora[5] == ":", "Hora deve ser HH:MM:SS"


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

CABECALHO_TESTE = ["data_captura", "hora_captura", "indicador", "valor"]


def _ler_csv(arquivo: Path) -> list[dict]:
    with arquivo.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_salvar_csv_primeira_escrita(tmp_path):
    """Deve criar o arquivo com cabeçalho na primeira execução."""
    arquivo = tmp_path / "test.csv"
    dados = [{"data_captura": "2025-06-01", "hora_captura": "09:30:00",
              "indicador": "SELIC", "valor": "13.75"}]

    salvar_csv(arquivo, dados, CABECALHO_TESTE, chaves_dedup=["data_captura", "indicador"])

    linhas = _ler_csv(arquivo)
    assert len(linhas) == 1
    assert linhas[0]["indicador"] == "SELIC"


def test_salvar_csv_acumula_dias_distintos(tmp_path):
    """Execuções em dias diferentes devem acumular o histórico."""
    arquivo = tmp_path / "test.csv"

    salvar_csv(arquivo,
               [{"data_captura": "2025-06-01", "hora_captura": "09:30:00",
                 "indicador": "SELIC", "valor": "13.75"}],
               CABECALHO_TESTE, chaves_dedup=["data_captura", "indicador"])

    salvar_csv(arquivo,
               [{"data_captura": "2025-06-02", "hora_captura": "09:30:00",
                 "indicador": "SELIC", "valor": "13.80"}],
               CABECALHO_TESTE, chaves_dedup=["data_captura", "indicador"])

    linhas = _ler_csv(arquivo)
    assert len(linhas) == 2, "Dias distintos devem ser preservados"
    datas = {l["data_captura"] for l in linhas}
    assert datas == {"2025-06-01", "2025-06-02"}


def test_salvar_csv_dedup_mesmo_dia_mesma_chave(tmp_path):
    """Re-execução no mesmo dia não deve duplicar — deve substituir."""
    arquivo = tmp_path / "test.csv"

    # Primeira execução
    salvar_csv(arquivo,
               [{"data_captura": "2025-06-01", "hora_captura": "09:30:00",
                 "indicador": "SELIC", "valor": "13.75"},
                {"data_captura": "2025-06-01", "hora_captura": "09:30:00",
                 "indicador": "DI", "valor": "13.65"}],
               CABECALHO_TESTE, chaves_dedup=["data_captura", "indicador"])

    # Segunda execução no mesmo dia
    salvar_csv(arquivo,
               [{"data_captura": "2025-06-01", "hora_captura": "14:00:00",
                 "indicador": "SELIC", "valor": "13.80"}],
               CABECALHO_TESTE, chaves_dedup=["data_captura", "indicador"])

    linhas = _ler_csv(arquivo)
    assert len(linhas) == 2, "Deve haver 2 linhas: DI (preservado) + SELIC (atualizado)"

    selic = next(l for l in linhas if l["indicador"] == "SELIC")
    assert selic["valor"] == "13.80", "Deve manter o valor mais recente"
    assert selic["hora_captura"] == "14:00:00", "Deve manter a hora mais recente"

    di = next(l for l in linhas if l["indicador"] == "DI")
    assert di["valor"] == "13.65", "DI não deve ter sido alterado"


def test_salvar_csv_dedup_simples_sem_chaves(tmp_path):
    """Sem chaves_dedup, remove todas as linhas do mesmo dia (dedup simples)."""
    arquivo = tmp_path / "test.csv"

    salvar_csv(arquivo,
               [{"data_captura": "2025-06-01", "hora_captura": "09:30:00",
                 "indicador": "SELIC", "valor": "13.75"}],
               CABECALHO_TESTE)

    salvar_csv(arquivo,
               [{"data_captura": "2025-06-01", "hora_captura": "14:00:00",
                 "indicador": "SELIC", "valor": "13.80"},
                {"data_captura": "2025-06-01", "hora_captura": "14:00:00",
                 "indicador": "DI", "valor": "13.65"}],
               CABECALHO_TESTE)

    linhas = _ler_csv(arquivo)
    assert len(linhas) == 2, "Deve substituir todas as linhas do mesmo dia"
    assert all(l["hora_captura"] == "14:00:00" for l in linhas)


def test_salvar_csv_preserva_historico_anterior(tmp_path):
    """Linhas de dias anteriores nunca devem ser apagadas."""
    arquivo = tmp_path / "test.csv"

    for dia in ["2025-05-28", "2025-05-29", "2025-05-30"]:
        salvar_csv(arquivo,
                   [{"data_captura": dia, "hora_captura": "09:30:00",
                     "indicador": "SELIC", "valor": "13.75"}],
                   CABECALHO_TESTE, chaves_dedup=["data_captura", "indicador"])

    # Re-execução apenas no último dia
    salvar_csv(arquivo,
               [{"data_captura": "2025-05-30", "hora_captura": "14:00:00",
                 "indicador": "SELIC", "valor": "13.80"}],
               CABECALHO_TESTE, chaves_dedup=["data_captura", "indicador"])

    linhas = _ler_csv(arquivo)
    assert len(linhas) == 3, "Histórico dos 3 dias deve ser preservado"

    por_data = {l["data_captura"]: l for l in linhas}
    assert por_data["2025-05-30"]["valor"] == "13.80", "Último dia deve ter valor atualizado"
    assert por_data["2025-05-28"]["valor"] == "13.75", "Dias anteriores não devem mudar"
    assert por_data["2025-05-29"]["valor"] == "13.75", "Dias anteriores não devem mudar"

