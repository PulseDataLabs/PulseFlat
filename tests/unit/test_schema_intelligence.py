"""
tests/unit/test_schema_intelligence.py
--------------------------------------
Testes unitários para o motor de reconciliação semântica de colunas,
auto-healing de schema e supressão inteligente de falsos schema drifts.
"""

import json

import pandas as pd
import pytest

from utils.base import DRIFTS, salvar_csv
from utils.schema_intelligence import (
    are_columns_equivalent,
    find_internal_duplicate_aliases,
    reconcile_columns,
    unify_dataframe_columns,
)


@pytest.fixture(autouse=True)
def clear_drifts():
    """Limpa a lista global DRIFTS antes e depois de cada teste."""
    DRIFTS.clear()
    yield
    DRIFTS.clear()


class TestSchemaIntelligenceEquivalence:
    """Valida a detecção inteligente de equivalência entre colunas."""

    @pytest.mark.parametrize(
        "col_a,col_b",
        [
            ("duration_d_u", "duration_du"),
            ("duration_du", "duration_d_u"),
            ("data_de_referencia", "data_referencia"),
            ("data_referencia", "data_de_referencia"),
            ("data_de_vencimento", "data_vencimento"),
            ("numero_de_negocios", "numero_negocios"),
            ("pu_m_dio", "pu_medio"),
            ("pu_medio", "pu_m_dio"),
            ("dt_referencia", "data_referencia"),
            ("tx_compra", "taxa_compra"),
            ("qtd_negociada", "quantidade_negociada"),
        ],
    )
    def test_equivalent_columns_detected(self, col_a, col_b):
        assert are_columns_equivalent(col_a, col_b) is True

    @pytest.mark.parametrize(
        "col_a,col_b",
        [
            ("variacao_12_meses", "variacao_24_meses"),
            ("intervalo_indicativo_min", "intervalo_indicativo_max"),
            ("interv_ind_inf_d0", "interv_ind_sup_d0"),
            ("taxa_compra", "taxa_venda"),
            ("posicao_coberta", "posicao_descoberta"),
            ("renda_variavel_acoes", "renda_variavel_opcoes"),
            ("valor_mercado_brl", "valor_mercado_usd"),
            ("ato_societario_1", "ato_societario_2"),
            ("credito_ig", "credito_hy"),
            ("retorno_ano", "retorno_mes"),
        ],
    )
    def test_guard_rails_prevent_false_positives(self, col_a, col_b):
        """Assegura que colunas com dimensões distintas ou números diferentes NUNCA sejam equivalentes."""
        assert are_columns_equivalent(col_a, col_b) is False


class TestSchemaIntelligenceHelpers:
    """Valida funções de mapeamento e unificação de DataFrames."""

    def test_reconcile_columns(self):
        incoming = ["data_captura", "data_de_referencia", "duration_d_u", "numero_indice"]
        canonical = ["data_captura", "data_referencia", "duration_du", "numero_indice"]
        mapping = reconcile_columns(incoming, canonical)
        assert mapping == {
            "data_de_referencia": "data_referencia",
            "duration_d_u": "duration_du",
        }

    def test_find_internal_duplicate_aliases(self):
        cols = ["data_captura", "data_referencia", "data_de_referencia", "duration_du", "duration_d_u"]
        mapping = find_internal_duplicate_aliases(cols)
        assert mapping["data_de_referencia"] == "data_referencia"
        assert mapping["duration_d_u"] == "duration_du"

    def test_unify_dataframe_columns_lossless_merge(self):
        df = pd.DataFrame(
            [
                {"codigo": "A", "duration_du": "10.5", "duration_d_u": ""},
                {"codigo": "B", "duration_du": "", "duration_d_u": "12.3"},
                {"codigo": "C", "duration_du": "15.0", "duration_d_u": "15.0"},
            ]
        )
        mapping = {"duration_d_u": "duration_du"}
        unified = unify_dataframe_columns(df, mapping)
        assert "duration_d_u" not in unified.columns
        assert list(unified["duration_du"]) == ["10.5", "12.3", "15.0"]


class TestSalvarCsvAutoHealingAndDriftSuppression:
    """Valida o auto-healing em salvar_csv durante as capturas."""

    def test_salvar_csv_auto_reconciles_variant_and_suppresses_drift(self, tmp_path):
        schemas_file = tmp_path / "schemas.json"
        target_csv = tmp_path / "anbima_dataset_teste.csv"

        initial_schema = [
            {
                "title": "Dataset Teste",
                "files": "anbima_dataset_teste.csv",
                "fields": [
                    {"name": "data_referencia", "type": "date"},
                    {"name": "duration_du", "type": "float"},
                    {"name": "taxa", "type": "float"},
                ],
            }
        ]
        with schemas_file.open("w", encoding="utf-8") as f:
            json.dump(initial_schema, f)

        # Scraper traz duration_d_u em vez de duration_du
        df_novo = pd.DataFrame(
            [
                {
                    "data_referencia": "2026-06-01",
                    "duration_d_u": "2.45",
                    "taxa": "13.5",
                }
            ]
        )

        salvar_csv(
            target_csv,
            df_novo,
            cabecalho=["data_referencia", "duration_d_u", "taxa"],
            acumular=True,
        )

        # 1. Não deve gerar Schema Drift (pois foi auto-resolvido)
        assert len(DRIFTS) == 0

        # 2. O arquivo gravado deve ter unificado duration_d_u -> duration_du
        df_gravado = pd.read_csv(target_csv, dtype=str)
        assert "duration_du" in df_gravado.columns
        assert "duration_d_u" not in df_gravado.columns
        assert df_gravado["duration_du"].iloc[0] == "2.45"

    def test_salvar_csv_auto_heals_polluted_historical_file(self, tmp_path):
        target_csv = tmp_path / "dataset_poluido.csv"

        # Simula arquivo histórico existente com colunas duplicadas
        df_antigo = pd.DataFrame(
            [
                {"data_captura": "2026-01-01", "duration_du": "1.0", "duration_d_u": ""},
                {"data_captura": "2026-02-01", "duration_du": "", "duration_d_u": "2.0"},
            ]
        )
        df_antigo.to_csv(target_csv, index=False)

        # Novo lote capturado com duration_du
        df_novo = pd.DataFrame(
            [
                {"data_captura": "2026-03-01", "duration_du": "3.0"}
            ]
        )

        salvar_csv(
            target_csv,
            df_novo,
            cabecalho=["data_captura", "duration_du"],
            acumular=True,
        )

        df_final = pd.read_csv(target_csv, dtype=str)
        assert "duration_d_u" not in df_final.columns
        assert list(df_final["duration_du"]) == ["1.0", "2.0", "3.0"]
