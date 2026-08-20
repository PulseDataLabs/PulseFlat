from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import pytest

from utils.base import FUSO, acquire_lock, agora_brt, limpar, nova_session, salvar_csv


class TestDefensiveBaseUtils:
    """Testes defensivos para utilitários fundamentais em utils/base.py."""

    def test_agora_brt_formato_e_timezone(self):
        data_str, hora_str = agora_brt()
        assert len(data_str) == 10
        assert data_str.count("-") == 2
        assert len(hora_str) == 8
        assert hora_str.count(":") == 2

        # Validação do fuso América/São Paulo
        dt_agora = datetime.now(FUSO)
        assert dt_agora.tzinfo == ZoneInfo("America/Sao_Paulo")

    def test_limpar_valores_extremos(self):
        assert limpar(None) == ""
        assert limpar("") == ""
        assert limpar("   ") == ""
        assert limpar("  Texto com  espaços múltiplos   ") == "Texto com  espaços múltiplos"
        assert limpar(12345) == "12345"
        assert limpar(12.34) == "12.34"
        assert limpar(True) == "True"
        assert limpar(float("nan")) == ""

    def test_nova_session_configuracao_segura(self):
        session = nova_session()
        assert "User-Agent" in session.headers
        assert "Mozilla" in session.headers["User-Agent"]
        assert callable(session.request)

    def test_acquire_lock_execucao_segura(self):
        with acquire_lock("teste_lock_seguro", blocking=True):
            pass

    def test_acquire_lock_non_blocking_concorrente(self):
        with acquire_lock("teste_lock_non_blocking", blocking=True):
            with pytest.raises(RuntimeError, match="já está em execução"):
                with acquire_lock("teste_lock_non_blocking", blocking=False):
                    pass

    def test_salvar_csv_criacao_diretorio_pai(self, tmp_path):
        arquivo_profundo = tmp_path / "sub1" / "sub2" / "teste_salvar.csv"
        dados = [
            {"data_captura": "2026-01-01", "hora_captura": "10:00:00", "indicador": "SELIC", "valor": "13.75"}
        ]
        salvar_csv(
            arquivo=arquivo_profundo,
            registros=dados,
            cabecalho=["data_captura", "hora_captura", "indicador", "valor"],
            chaves_dedup=["data_captura", "indicador"],
        )
        assert arquivo_profundo.exists()
        df_lido = pd.read_csv(arquivo_profundo)
        assert len(df_lido) == 1
        assert df_lido.loc[0, "indicador"] == "SELIC"
