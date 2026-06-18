"""
tests/test_scrapers_bcb.py
--------------------------
Testes unitários específicos para os scrapers do Banco Central do Brasil (BCB / BACEN).
"""

import re
import sys
from pathlib import Path
import pytest
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scrapers.bcb_ptax as bcb_ptax
import scrapers.bcb_sgs as bcb_sgs


def test_bcb_ptax_sucesso(requests_mock):
    """Deve capturar e mapear corretamente as cotações da API PTAX Olinda em caso de sucesso."""
    mock_response = {
        "value": [
            {
                "cotacaoCompra": 5.2530,
                "cotacaoVenda": 5.2540,
                "dataHoraCotacao": "2026-06-01 13:15:00.000"
            }
        ]
    }

    requests_mock.get(
        re.compile(r"https://olinda\.bcb\.gov\.br/.*"),
        json=mock_response,
        status_code=200
    )

    registros = bcb_ptax.capturar()

    assert len(registros) == 1
    reg = registros[0]
    assert reg["cotacao_compra"] == "5.253"
    assert reg["cotacao_venda"] == "5.254"
    assert reg["data_referencia"] == "2026-06-01"
    assert "data_captura" in reg


def test_bcb_ptax_erro_conexao(requests_mock):
    """Deve falhar e terminar com código de saída 1 se a API PTAX Olinda falhar em todas as tentativas."""
    requests_mock.get(
        re.compile(r"https://olinda\.bcb\.gov\.br/.*"),
        status_code=500
    )

    with pytest.raises(SystemExit) as exc_info:
        bcb_ptax.capturar()

    assert exc_info.value.code == 1


def test_bcb_ptax_scraper_fetch(requests_mock):
    """Deve testar o método fetch do BcbPtaxScraper instanciado."""
    mock_response = {
        "value": [
            {
                "cotacaoCompra": 5.2530,
                "cotacaoVenda": 5.2540,
                "dataHoraCotacao": "2026-06-01 13:15:00.000"
            }
        ]
    }

    requests_mock.get(
        re.compile(r"https://olinda\.bcb\.gov\.br/.*"),
        json=mock_response,
        status_code=200
    )

    scraper = bcb_ptax.BcbPtaxScraper()
    df = scraper.fetch()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["data_captura", "data_referencia", "cotacao_compra", "cotacao_venda"]
    assert df.loc[0, "cotacao_compra"] == "5.253"


def test_bcb_sgs_sucesso(requests_mock, monkeypatch):
    """Deve capturar as séries do SGS, realizar sleep e mapear campos corretamente."""
    monkeypatch.setattr(bcb_sgs.time, "sleep", lambda x: None)

    mock_dados = [
        {"data": "01/06/2026", "valor": "10.50"},
        {"data": "02/06/2026", "valor": "10.75"}
    ]

    requests_mock.get(
        re.compile(r"https://api\.bcb\.gov\.br/.*"),
        json=mock_dados,
        status_code=200
    )

    registros = bcb_sgs.capturar()

    total_esperado = len(bcb_sgs.SERIES) * 2
    assert len(registros) == total_esperado

    for reg in registros:
        assert reg["data_referencia"] in ("01/06/2026", "02/06/2026")
        assert reg["valor"] in ("10.5", "10.75", "10.50")
        assert "codigo_serie" in reg
        assert "nome_serie" in reg
        assert "data_captura" in reg


def test_bcb_sgs_erro_parcial(requests_mock, monkeypatch):
    """Deve tolerar erros parciais nas séries do SGS e capturar apenas as que funcionarem."""
    monkeypatch.setattr(bcb_sgs.time, "sleep", lambda x: None)

    mock_dados = [{"data": "01/06/2026", "valor": "5.25"}]

    def callback(request, context):
        if "sgs.11" in request.url:
            context.status_code = 500
            return {"error": "Internal Server Error"}
        context.status_code = 200
        return mock_dados

    requests_mock.get(
        re.compile(r"https://api\.bcb\.gov\.br/.*"),
        json=callback
    )

    registros = bcb_sgs.capturar()

    codigos_capturados = {reg["codigo_serie"] for reg in registros}
    assert "11" not in codigos_capturados
    assert len(codigos_capturados) == len(bcb_sgs.SERIES) - 1


def test_bcb_sgs_scraper_fetch(requests_mock, monkeypatch):
    """Deve testar o método fetch do BcbSgsScraper instanciado."""
    monkeypatch.setattr(bcb_sgs.time, "sleep", lambda x: None)

    mock_dados = [{"data": "01/06/2026", "valor": "5.25"}]

    requests_mock.get(
        re.compile(r"https://api\.bcb\.gov\.br/.*"),
        json=mock_dados,
        status_code=200
    )

    scraper = bcb_sgs.BcbSgsScraper()
    df = scraper.fetch()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "codigo_serie" in df.columns
    assert "valor" in df.columns
