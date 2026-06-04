"""
tests/test_scrapers_cvm.py
--------------------------
Testes unitários específicos para os scrapers da CVM.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scrapers.cvm_cadastro_companhias_abertas as ccca


def test_cvm_cadastro_companhias_abertas_fetch(requests_mock):
    """Deve baixar e parsear com sucesso o cadastro de companhias abertas da CVM."""
    mock_csv = (
        "CNPJ_CIA;DENOM_SOCIAL;DENOM_COMERC;SIT;CD_CVM\n"
        "00.000.000/0001-91;EMPRESA TESTE S/A;EMPRESA TESTE;ATIVO;12345\n"
    )
    
    requests_mock.get(
        ccca.URL,
        content=mock_csv.encode("latin-1"),
        status_code=200
    )
    
    scraper = ccca.CvmCadastroCompanhiasAbertasScraper()
    df = scraper.fetch()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    
    # Valida presença das colunas originais do CSV mockado
    assert "cnpj_cia" in df.columns
    assert "denom_social" in df.columns
    assert df.loc[0, "cnpj_cia"] == "00.000.000/0001-91"
    assert df.loc[0, "denom_social"] == "EMPRESA TESTE S/A"
