"""
tests/unit/test_schema_drift.py
--------------------------------
Testes unitários para o mecanismo de detecção e registro de Schema Drift em utils/base.py.
"""

import json

import pandas as pd
import pytest

from utils.base import DRIFTS, salvar_csv


@pytest.fixture(autouse=True)
def clear_drifts():
    """Limpa a lista global DRIFTS antes e depois de cada teste."""
    DRIFTS.clear()
    yield
    DRIFTS.clear()


class TestSchemaDriftDetection:
    """Testa a detecção de alterações na estrutura de colunas (Schema Drift)."""

    def test_drift_detected_when_column_is_added(self, tmp_path):
        """Quando uma nova coluna não declarada no schemas.json for fornecida, deve registrar como 'added'."""
        schemas_file = tmp_path / "schemas.json"
        target_csv = tmp_path / "anbima_dataset_teste.csv"

        # Cria schemas.json simulando a estrutura original
        initial_schema = [
            {
                "title": "Dataset Teste",
                "files": "anbima_dataset_teste.csv",
                "fields": [
                    {"name": "data_referencia", "type": "date"},
                    {"name": "codigo", "type": "str"},
                    {"name": "taxa", "type": "float"},
                ],
            }
        ]
        with schemas_file.open("w", encoding="utf-8") as f:
            json.dump(initial_schema, f)

        # DataFrame com uma coluna nova 'spread'
        df = pd.DataFrame(
            [
                {
                    "data_referencia": "2026-06-01",
                    "codigo": "PETR4",
                    "taxa": 14.5,
                    "spread": 1.25,
                }
            ]
        )

        salvar_csv(target_csv, df, cabecalho=["data_referencia", "codigo", "taxa", "spread"])

        # Deve ter registrado drift
        assert len(DRIFTS) == 1
        drift = DRIFTS[0]
        assert drift["file"] == "anbima_dataset_teste.csv"
        assert "spread" in drift["added"]
        assert len(drift["removed"]) == 0
        assert "timestamp" in drift

    def test_drift_detected_when_column_is_removed(self, tmp_path):
        """Quando uma coluna declarada no schemas.json deixa de existir no dataset, deve registrar como 'removed'."""
        schemas_file = tmp_path / "schemas.json"
        target_csv = tmp_path / "cvm_dataset_teste.csv"

        initial_schema = [
            {
                "title": "Dataset CVM Teste",
                "files": "cvm_dataset_teste.csv",
                "fields": [
                    {"name": "data_referencia", "type": "date"},
                    {"name": "cnpj", "type": "str"},
                    {"name": "patrimonio_liquido", "type": "float"},
                    {"name": "coluna_antiga_descontinuada", "type": "str"},
                ],
            }
        ]
        with schemas_file.open("w", encoding="utf-8") as f:
            json.dump(initial_schema, f)

        # DataFrame sem 'coluna_antiga_descontinuada'
        df = pd.DataFrame(
            [
                {
                    "data_referencia": "2026-06-01",
                    "cnpj": "00.000.000/0001-00",
                    "patrimonio_liquido": 5000000.0,
                }
            ]
        )

        salvar_csv(target_csv, df, cabecalho=["data_referencia", "cnpj", "patrimonio_liquido"])

        assert len(DRIFTS) == 1
        drift = DRIFTS[0]
        assert drift["file"] == "cvm_dataset_teste.csv"
        assert "coluna_antiga_descontinuada" in drift["removed"]
        assert len(drift["added"]) == 0

    def test_no_drift_when_schema_is_unchanged(self, tmp_path):
        """Não deve registrar drift quando as colunas corresponderem exatamente ao schema existente."""
        schemas_file = tmp_path / "schemas.json"
        target_csv = tmp_path / "b3_dataset_teste.csv"

        initial_schema = [
            {
                "title": "Dataset B3 Teste",
                "files": "b3_dataset_teste.csv",
                "fields": [
                    {"name": "data_referencia", "type": "date"},
                    {"name": "ticker", "type": "str"},
                    {"name": "preco", "type": "float"},
                ],
            }
        ]
        with schemas_file.open("w", encoding="utf-8") as f:
            json.dump(initial_schema, f)

        df = pd.DataFrame(
            [
                {
                    "data_referencia": "2026-06-01",
                    "ticker": "VALE3",
                    "preco": 65.40,
                }
            ]
        )

        salvar_csv(target_csv, df, cabecalho=["data_referencia", "ticker", "preco"])
        assert len(DRIFTS) == 0

    def test_drift_ignores_internal_metadata_columns(self, tmp_path):
        """Colunas internas de controle (conjunto, arquivo_origem, registro_hash, dt_captura) não devem gerar falso drift."""
        schemas_file = tmp_path / "schemas.json"
        target_csv = tmp_path / "bacen_dataset_teste.csv"

        initial_schema = [
            {
                "title": "Dataset BACEN Teste",
                "files": "bacen_dataset_teste.csv",
                "fields": [
                    {"name": "data_referencia", "type": "date"},
                    {"name": "valor", "type": "float"},
                ],
            }
        ]
        with schemas_file.open("w", encoding="utf-8") as f:
            json.dump(initial_schema, f)

        # DataFrame inclui registro_hash e dt_captura
        df = pd.DataFrame(
            [
                {
                    "data_referencia": "2026-06-01",
                    "valor": 10.0,
                    "registro_hash": "abc123hash",
                    "dt_captura": "2026-06-01 10:00:00",
                }
            ]
        )

        salvar_csv(
            target_csv,
            df,
            cabecalho=["data_referencia", "valor", "registro_hash", "dt_captura"],
        )
        assert len(DRIFTS) == 0
