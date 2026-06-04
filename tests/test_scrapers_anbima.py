"""
tests/test_scrapers_anbima.py
-----------------------------
Testes unitários específicos para os scrapers da ANBIMA.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scrapers.anbima_ima_completo as aic
import scrapers.anbima_indicadores as ai


def test_anbima_ima_completo_sucesso(requests_mock, monkeypatch):
    """Deve capturar, validar D-1 e parsear com sucesso o arquivo IMA Completo da ANBIMA."""
    monkeypatch.setattr(aic, "obter_d1_util", lambda: "02/06/2026")
    
    mock_txt = (
        "0@ANBIMA - Associação Brasileira das Entidades dos Mercados Financeiros e de Capitais\n"
        "1@TOTAIS\n"
        "1@Data de Referência@INDICE@Número Índice@Variação Diária(%)@Variação Mensal(%)@Variação Anual(%)\n"
        "1@02/06/2026@IRF-M 1@20154,43293200@0,0569@0,0806@5,5163\n"
        "1@02/06/2026@IRF-M 1+@24436,46503800@0,0386@0,0518@3,9291\n"
    )
    
    requests_mock.get(aic.URL, text=mock_txt, status_code=200)
    
    registros = aic.capturar()
    
    assert len(registros) == 2
    reg1 = registros[0]
    assert reg1["data_referencia"] == "2026-06-02"
    assert reg1["indice"] == "IRF-M 1"
    assert reg1["numero_indice"] == "20154.43293200"


def test_anbima_ima_completo_scraper_fetch(requests_mock, monkeypatch):
    """Deve testar o método fetch da classe AnbimaImaCompletoScraper."""
    monkeypatch.setattr(aic, "obter_d1_util", lambda: "02/06/2026")
    
    mock_txt = (
        "0@ANBIMA\n1@TOTAIS\n"
        "1@Data de Referência@INDICE@Número Índice@Variação Diária(%)@Variação Mensal(%)@Variação Anual(%)\n"
        "1@02/06/2026@IRF-M 1@20154,43293200@0,0569@0,0806@5,5163\n"
    )
    
    requests_mock.get(aic.URL, text=mock_txt, status_code=200)
    
    scraper = aic.AnbimaImaCompletoScraper()
    df = scraper.fetch()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "data_referencia" in df.columns
    assert "indice" in df.columns


def test_anbima_indicadores_sucesso(requests_mock):
    """Deve capturar, parsear e limpar corretamente os indicadores do HTML da ANBIMA."""
    mock_html = """
    <html>
    <body>
        Data e Hora da Última Atualização: 03/06/2026 - 09:30 h
        Estimativa SELIC 1 03/06/2026 14,40
        Taxa SELIC do BC 2 02/06/2026 14,40
        DI-B3 3 02/06/2026 14,40
        IGP-M (mai/26) 5 Número Índice 1.229,904 Var % no mês 0,84
        IGP-M 1 Projeção (jun/26) 0,40
        IPCA (abr/26) 6 Número Índice 7.596,09 Var % no mês 0,67
        IPCA 1 Projeção (mai/26) 0,50
        Dolar Comercial Compra 2 02/06/2026 5,0154
        Dólar Comercial Venda 2 02/06/2026 5,0160
    </body>
    </html>
    """

    requests_mock.get(ai.URL, content=mock_html.encode("iso-8859-1"), status_code=200)

    registros = ai.capturar()
    
    assert len(registros) == 11
    
    selic = next(r for r in registros if r["indicador"] == "Estimativa SELIC")
    assert selic["valor"] == "14.40"
    assert selic["data_referencia"] == "2026-06-03"


def test_anbima_indicadores_scraper_fetch(requests_mock):
    """Deve testar o método fetch da classe AnbimaIndicadoresScraper."""
    mock_html = """
    <html>
    <body>
        Data e Hora da Última Atualização: 03/06/2026 - 09:30 h
        Estimativa SELIC 1 03/06/2026 14,40
    </body>
    </html>
    """
    requests_mock.get(ai.URL, content=mock_html.encode("iso-8859-1"), status_code=200)
    
    scraper = ai.AnbimaIndicadoresScraper()
    df = scraper.fetch()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "indicador" in df.columns
    assert "valor" in df.columns
