"""
tests/unit/test_scrapers_sanitization.py
-----------------------------------------
Testes unitários para validar a sanitização de marcadores sentinelas (-- e N/D)
e a garantia de tipagem float em scrapers de títulos públicos e debêntures.
"""

from datetime import date
import pandas as pd
import pytest

from scrapers.anbima_titulos_publicos import AnbimaTitulosPublicosScraper
from scrapers.anbima_debentures import AnbimaDebenturesScraper


class TestAnbimaTitulosPublicosSanitization:
    """Valida a limpeza de sentinelas em ANBIMA Títulos Públicos."""

    def test_titulos_publicos_cleans_sentinels_and_casts_float(self, monkeypatch):
        # Simula resposta com dados válidos e dados com sentinelas '--' e 'N/D'
        raw_text = """CABECALHO 1
CABECALHO 2
CABECALHO 3
LTN@2026-06-05@100000@2024-01-01@2026-04-01@14.575@14.5537@14.5669@985.535409@0.00318369383421@14.5125@14.7984@14.5047@14.7973@D
NTN-B@2026-06-05@760199@2020-01-01@2030-08-15@--@--@--@N/D@--@--@--@--@--@D
"""

        class DummyResp:
            content = raw_text.encode("latin-1")
            status_code = 200
            def raise_for_status(self):
                pass

        class DummySession:
            def get(self, *args, **kwargs):
                return DummyResp()

        monkeypatch.setattr("scrapers.anbima_titulos_publicos.nova_session", lambda: DummySession())

        scraper = AnbimaTitulosPublicosScraper()
        scraper.target_date = date(2026, 6, 5)
        df = scraper.fetch()

        assert not df.empty
        assert len(df) == 2

        num_cols = [
            "tx_compra",
            "tx_venda",
            "tx_indicativa",
            "pu",
            "desvio_padrao",
            "interv_ind_inf_d0",
            "interv_ind_sup_d0",
            "interv_ind_inf_dma1",
            "interv_ind_sup_dma1",
        ]

        # Verifica tipo float em todas as colunas numéricas
        for col in num_cols:
            assert pd.api.types.is_float_dtype(df[col]), f"{col} deve ser float64"

        # Linha 0 deve ter valores numéricos corretos
        assert df.loc[0, "tx_indicativa"] == 14.5669
        assert df.loc[0, "pu"] == 985.535409
        assert df.loc[0, "interv_ind_inf_d0"] == 14.5125

        # Linha 1 (sentinelas) deve ter NaN e não strings '--'
        assert pd.isna(df.loc[1, "tx_indicativa"])
        assert pd.isna(df.loc[1, "pu"])
        assert pd.isna(df.loc[1, "interv_ind_inf_dma1"])


class TestAnbimaDebenturesSanitization:
    """Valida a limpeza de sentinelas em ANBIMA Debêntures."""

    def test_debentures_cleans_sentinels_and_casts_float(self, monkeypatch):
        raw_text = """CABECALHO 1
CABECALHO 2
CABECALHO 3
AALM12@AURA ALMAS@2030-10-02@DI + 1.6%@0.8503@0.5404@0.6834@0.0541@0.6293@0.7376@1046.357089@102.0904@576.72@5@2035-05-15
AALR13@CENTRO DIAG@2027-10-04@DI + 2.75%@--@--@--@--@--@--@N/D@N/D@N/D@@
"""

        class DummyResp:
            content = raw_text.encode("latin-1")
            status_code = 200
            def raise_for_status(self):
                pass

        class DummySession:
            def get(self, *args, **kwargs):
                return DummyResp()

        monkeypatch.setattr("scrapers.anbima_debentures.nova_session", lambda: DummySession())

        scraper = AnbimaDebenturesScraper()
        scraper.target_date = date(2026, 6, 5)
        df = scraper.fetch()

        assert not df.empty
        assert len(df) == 2

        num_cols = [
            "tx_compra",
            "tx_venda",
            "tx_indicativa",
            "desvio_padrao",
            "intervalo_indicativo_min",
            "intervalo_indicativo_max",
            "pu",
            "ratio_pu_par_vne",
            "duration",
            "pct_reune",
        ]

        for col in num_cols:
            assert pd.api.types.is_float_dtype(df[col]), f"{col} deve ser float64"

        assert df.loc[0, "pu"] == 1046.357089
        assert df.loc[0, "ratio_pu_par_vne"] == 102.0904
        assert df.loc[0, "duration"] == 576.72
        assert df.loc[0, "pct_reune"] == 5.0

        assert pd.isna(df.loc[1, "tx_compra"])
        assert pd.isna(df.loc[1, "pu"])
        assert pd.isna(df.loc[1, "duration"])


class TestDebenturesMercadoSecundarioSanitization:
    """Valida a higienização de sentinelas em Debêntures Mercado Secundário."""

    def test_clean_float_in_mercado_secundario(self):
        from scrapers.debentures_mercado_secundario_precos_negociacao import (
            DebenturesMercadoSecundarioPrecosNegociacaoScraper,
        )

        scraper = DebenturesMercadoSecundarioPrecosNegociacaoScraper()
        # Testa a conversão interna
        dummy_df = pd.DataFrame(
            [
                {
                    "data_referencia": "2026-06-01",
                    "codigo_ativo": "VALE12",
                    "pu_minimo": "1230,04",
                    "pu_medio": "1230,04",
                    "pu_maximo": "1230,04",
                    "pu_da_curva": "ND",
                    "quantidade": "100",
                    "numero_de_negocios": "1",
                },
                {
                    "data_referencia": "2026-06-01",
                    "codigo_ativo": "PETR15",
                    "pu_minimo": "--",
                    "pu_medio": "--",
                    "pu_maximo": "--",
                    "pu_da_curva": "101.66",
                    "quantidade": "-",
                    "numero_de_negocios": "--",
                },
            ]
        )

        # Mock super().fetch()
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "scrapers.generic_scraper.GenericScraper.fetch",
                lambda self: dummy_df.copy(),
            )
            df_cleaned = scraper.fetch()

        # 'ND' em pu_da_curva deve ter virado ''
        assert df_cleaned.loc[0, "pu_da_curva"] == ""
        assert df_cleaned.loc[0, "pu_minimo"] == "1230.04"

        # '--' e '-' devem ter virado ''
        assert df_cleaned.loc[1, "pu_minimo"] == ""
        assert df_cleaned.loc[1, "quantidade"] == ""
        assert df_cleaned.loc[1, "pu_da_curva"] == "101.66"
