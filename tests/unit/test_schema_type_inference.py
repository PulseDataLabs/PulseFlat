"""
tests/unit/test_schema_type_inference.py
-----------------------------------------
Suíte de testes para validar o motor de inferência de tipos de campos (get_type_badge)
e a geração de governança de esquemas em schemas.json.
"""

import json
from pathlib import Path
import pandas as pd
import pytest

from utils import get_type_badge, salvar_csv


class TestGetTypeBadgeNameHeuristics:
    """Testa a inferência léxica de tipos quando não há Series disponível."""

    @pytest.mark.parametrize(
        "col_name",
        [
            "tx_compra",
            "tx_venda",
            "tx_indicativa",
            "numero_indice",
            "cota",
            "variacao_diaria",
            "variacao_mensal",
            "variacao_anual",
            "variacao_ultimos_12_meses",
            "variacao_ultimos_24_meses",
            "pu",
            "pu_minimo",
            "pu_medio",
            "pu_maximo",
            "pu_da_curva",
            "pu_indicativo",
            "pu_par",
            "ratio_pu_par_vne",
            "duration",
            "duration_du",
            "duration_d_u",
            "desvio_padrao",
            "intervalo_indicativo_min",
            "intervalo_indicativo_max",
            "interv_ind_inf_d0",
            "interv_ind_sup_d0",
            "interv_ind_inf_dma1",
            "interv_ind_sup_dma1",
            "pmr",
            "convexidade",
            "yield_",
            "redemption_yield",
            "spread_incentivado_sem_gross_up",
            "z_spread",
            "credit_spread_corp_ig",
            "t10y2y_spread",
            "peso_geral",
            "peso_indice",
            "patrimonio_liquido",
            "saldo_devedor",
            "valor_mercado",
            "pct_reune",
            "vol_aa_perc",
            "ret_dia_perc",
        ],
    )
    def test_financial_float_metrics(self, col_name):
        assert get_type_badge(col_name) == "float", f"{col_name} deve ser inferido como float"

    @pytest.mark.parametrize(
        "col_name",
        [
            "data_captura",
            "data_referencia",
            "dt_vencimento",
            "data_base_emissao",
            "dt_repactuacao_vencimento",
            "data_patrimonio_liquido",
            "valid_from_date",
        ],
    )
    def test_date_fields(self, col_name):
        assert get_type_badge(col_name) == "date", f"{col_name} deve ser inferido como date"

    @pytest.mark.parametrize(
        "col_name",
        [
            "quantidade",
            "numero_de_negocios",
            "prazo_dias",
            "nr_seq",
            "page_number",
            "id_registro_fundo",
        ],
    )
    def test_integer_fields(self, col_name):
        assert get_type_badge(col_name) == "int", f"{col_name} deve ser inferido como int"

    @pytest.mark.parametrize(
        "col_name",
        [
            "codigo",
            "nome_emissor",
            "indice_correcao",
            "criterio",
            "publico_alvo",
            "emissor",
            "isin",
        ],
    )
    def test_text_fields(self, col_name):
        assert get_type_badge(col_name) == "str", f"{col_name} deve ser inferido como str"


class TestGetTypeBadgeWithSeriesInspection:
    """Testa a inferência dinâmica com inspeção de dados em tempo de execução."""

    def test_native_float_series(self):
        s = pd.Series([10.5, 20.3, None], dtype=float)
        assert get_type_badge("coluna_qualquer", s) == "float"

    def test_native_int_series(self):
        s = pd.Series([10, 20, 30], dtype="int64")
        assert get_type_badge("coluna_qualquer", s) == "int"

    def test_native_datetime_series(self):
        s = pd.to_datetime(["2026-06-01", "2026-06-02"])
        assert get_type_badge("coluna_qualquer", s) == "date"

    def test_string_series_with_decimals_and_sentinels(self):
        """Simula coluna lida como object com sentinelas textuais (-- e N/D) e decimais."""
        s = pd.Series(["1046.357089", "1022.08", "--", "N/D", "", "ND", "null"])
        assert get_type_badge("campo_generico", s) == "float"

    def test_string_series_with_dates(self):
        s = pd.Series(["2026-06-01", "2026-06-02", ""])
        assert get_type_badge("campo_generico", s) == "date"

    def test_string_series_with_leading_zeros(self):
        """Códigos com zero à esquerda (ex: contas, agências, códigos B3) devem permanecer str."""
        s = pd.Series(["010100", "020200", "005000"])
        assert get_type_badge("codigo_conta", s) == "str"

    def test_string_series_with_alpha_text(self):
        s = pd.Series(["PETR4", "VALE3", "AALM12"])
        assert get_type_badge("ativo", s) == "str"


class TestSalvarCsvSchemaGeneration:
    """Testa a geração e atualização de schemas.json através de salvar_csv."""

    def test_salvar_csv_generates_correct_types_and_examples(self, tmp_path):
        df = pd.DataFrame(
            [
                {
                    "data_referencia": "2026-06-01",
                    "codigo": "AALM12",
                    "tx_compra": 0.8503,
                    "pu": 1046.357089,
                    "numero_indice": 11504.40986,
                    "variacao_diaria": -0.0693,
                    "quantidade": 1500,
                    "publico_alvo": "Geral",
                },
                {
                    "data_referencia": "2026-06-01",
                    "codigo": "VALE3",
                    "tx_compra": None,
                    "pu": None,
                    "numero_indice": 11500.0,
                    "variacao_diaria": 0.05,
                    "quantidade": 2000,
                    "publico_alvo": "Qualificado",
                },
            ]
        )

        test_file = tmp_path / "teste_pipeline.csv"
        salvar_csv(
            test_file,
            df,
            cabecalho=list(df.columns),
            chaves_dedup=["data_referencia", "codigo"],
        )

        schemas_path = tmp_path / "schemas.json"
        assert schemas_path.exists()

        with schemas_path.open("r", encoding="utf-8") as f:
            schemas = json.load(f)

        assert len(schemas) == 1
        fields = {f["name"]: f for f in schemas[0]["fields"]}

        assert fields["data_referencia"]["type"] == "date"
        assert fields["codigo"]["type"] == "str"
        assert fields["tx_compra"]["type"] == "float"
        assert fields["pu"]["type"] == "float"
        assert fields["numero_indice"]["type"] == "float"
        assert fields["variacao_diaria"]["type"] == "float"
        assert fields["quantidade"]["type"] == "int"
        assert fields["publico_alvo"]["type"] == "str"


class TestExistingSchemasIntegrity:
    """Testa a integridade do catálogo oficial data/schemas.json."""

    def test_no_financial_metrics_classified_as_str_in_schemas_json(self):
        schemas_file = Path("data/schemas.json")
        if not schemas_file.exists():
            pytest.skip("data/schemas.json não encontrado")

        with schemas_file.open("r", encoding="utf-8") as f:
            schemas = json.load(f)

        violating_fields = []
        forbidden_as_str = {
            "tx_compra",
            "tx_venda",
            "tx_indicativa",
            "numero_indice",
            "pu",
            "pu_minimo",
            "pu_medio",
            "pu_maximo",
            "pu_da_curva",
            "pu_indicativo",
            "pu_par",
            "duration",
            "duration_du",
            "desvio_padrao",
            "intervalo_indicativo_min",
            "intervalo_indicativo_max",
            "pmr",
            "convexidade",
            "yield_",
            "variacao_diaria",
            "variacao_mensal",
            "variacao_anual",
        }

        for s in schemas:
            fname = s.get("files", "")
            for fld in s.get("fields", []):
                name = fld.get("name", "")
                ftype = fld.get("type", "")
                if name in forbidden_as_str and ftype == "str":
                    violating_fields.append((fname, name, ftype))

        assert not violating_fields, f"Campos financeiros tipados como str em schemas.json: {violating_fields}"
