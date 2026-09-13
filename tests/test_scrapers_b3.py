"""
tests/test_scrapers_b3.py
-------------------------
Testes unitários específicos para os scrapers da B3.
"""

import io
import sys
import zipfile
from pathlib import Path

import openpyxl
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scrapers.b3_classificacao_setorial as bcs
import scrapers.b3_limites_garantias as blg


def test_b3_classificacao_setorial_sucesso(requests_mock):
    """Deve capturar e extrair corretamente a classificação setorial B3 a partir de um ZIP mockado."""
    # Crie um arquivo Excel mock em memória
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Plan3"

    # Adiciona linhas no formato esperado
    for _ in range(6):
        ws.append([None, None, None, None, None, None, None])
    ws.append(["SETOR ECONÔMICO", "SUBSETOR", "SEGMENTO", "LISTAGEM", None, None, None])
    ws.append([None, None, None, "CÓDIGO", "SEGMENTO", None, None])
    ws.append(
        [
            "Petróleo, Gás e Biocombustíveis",
            "Petróleo, Gás e Biocombustíveis",
            "Exploração, Refino e Distribuição",
            None,
            None,
            None,
            None,
        ]
    )
    ws.append([None, None, "PETROBRAS", "PETR", "N2", None, None])

    excel_io = io.BytesIO()
    wb.save(excel_io)
    excel_bytes = excel_io.getvalue()

    # Crie um arquivo ZIP mock em memória contendo o Excel
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, "w") as zf:
        zf.writestr("Setorial B3.xlsx", excel_bytes)
    zip_bytes = zip_io.getvalue()

    # Mock do download
    requests_mock.get(bcs.URL, content=zip_bytes, status_code=200)

    empresas = bcs.capturar()
    assert len(empresas) == 1
    emp = empresas[0]
    assert emp["setor_economico"] == "Petróleo, Gás e Biocombustíveis"
    assert emp["nome_empresa"] == "PETROBRAS"
    assert emp["codigo"] == "PETR"


def test_b3_classificacao_setorial_scraper_fetch(requests_mock):
    """Deve testar o método fetch da classe B3ClassificacaoSetorialScraper."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Plan3"
    for _ in range(6):
        ws.append([None, None, None, None, None, None, None])
    ws.append(["SETOR ECONÔMICO", "SUBSETOR", "SEGMENTO", "LISTAGEM", None, None, None])
    ws.append([None, None, None, "CÓDIGO", "SEGMENTO", None, None])
    ws.append(["Petróleo", "Petróleo", "Exploração", None, None, None, None])
    ws.append([None, None, "PETROBRAS", "PETR", "N2", None, None])

    excel_io = io.BytesIO()
    wb.save(excel_io)
    excel_bytes = excel_io.getvalue()

    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, "w") as zf:
        zf.writestr("Setorial B3.xlsx", excel_bytes)
    zip_bytes = zip_io.getvalue()

    requests_mock.get(bcs.URL, content=zip_bytes, status_code=200)

    scraper = bcs.B3ClassificacaoSetorialScraper()
    df = scraper.fetch()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == [
        "data_captura",
        "setor_economico",
        "subsetor",
        "segmento",
        "nome_empresa",
        "codigo",
        "segmento_listagem",
    ]


def test_b3_limites_garantias_capturar(requests_mock):
    """Deve capturar limites de garantias B3 a partir de um ZIP mockado com 2 meses."""
    wb = openpyxl.Workbook()
    ws_acoes = wb.active
    ws_acoes.title = "Ações, BDRs, ETFs, FIIs e Units"
    ws_acoes.append(["Código", "ISIN", "Limite (quantidade)"])
    ws_acoes.append(["PETR4", "BRPETRACNPR6", 50000000])
    ws_acoes.append(["VALE3", "BRVALEACNPR3", 80000000])

    ws_adr = wb.create_sheet("ADR")
    ws_adr.append(["Código", "ISIN", "Limite (quantidade)"])
    ws_adr.append(["PETR4 BZ", "US71654V1017", 31339000])

    ws_deb = wb.create_sheet("DEB")
    ws_deb.append(["Código", "ISIN", "Limite (quantidade)"])
    ws_deb.append(["TIMS12", "BRTIMSDBS007", 63000])

    excel_io = io.BytesIO()
    wb.save(excel_io)
    excel_bytes = excel_io.getvalue()

    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, "w") as zf:
        zf.writestr(
            "Limites de Ações, BDRs, Units, ETFs, ADRs, FIIs e Debêntures_Junho_2026.xlsx",
            excel_bytes,
        )
    zip_bytes = zip_io.getvalue()

    pagina_html = """
    <html><body>
    <a href="/data/files/xxx/Limites%20de%20A%C3%A7%C3%B5es,%20BDRs,%20Units,%20ETFs,%20ADRs,%20FIIs%20e%20Deb%C3%AAntures.zip">
    Faça o download da planilha de limites do mês atual e do mês anterior</a>
    </body></html>
    """

    requests_mock.get(blg.URL_PAGINA, text=pagina_html, status_code=200)
    requests_mock.get(
        "https://www.b3.com.br/data/files/xxx/Limites%20de%20A%C3%A7%C3%B5es,%20BDRs,%20Units,%20ETFs,%20ADRs,%20FIIs%20e%20Deb%C3%AAntures.zip",
        content=zip_bytes,
        status_code=200,
    )

    registros = blg.capturar()
    df = registros if isinstance(registros, pd.DataFrame) else pd.DataFrame(registros)
    assert len(df) == 4
    assert not df.empty
    assert "data_captura" in df.columns
    assert "data_referencia" in df.columns
    assert df["data_referencia"].iloc[0] == "2026-06-01"
    assert "PETR4" in df["codigo"].values
    assert "VALE3" in df["codigo"].values
    assert "PETR4 BZ" in df["codigo"].values


def test_b3_limites_garantias_sheet_legacy(requests_mock):
    """Deve processar abas com nomenclatura antiga (sem FIIs)."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Ações, BDRs, ETFs e Units"
    ws.append(["Código", "ISIN", "Limite (quantidade)"])
    ws.append(["PETR4", "BRPETRACNPR6", 50000000])

    excel_io = io.BytesIO()
    wb.save(excel_io)
    excel_bytes = excel_io.getvalue()

    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, "w") as zf:
        zf.writestr(
            "Limites de Ações, BDRs, Units, ETFs, ADRs e Debêntures_Junho_2025.xlsx",
            excel_bytes,
        )
    zip_bytes = zip_io.getvalue()

    pagina_html = """
    <html><body>
    <a href="/data/files/xxx/Limites.zip">
    Faça o download da planilha de limites do mês atual e do mês anterior</a>
    </body></html>
    """

    requests_mock.get(blg.URL_PAGINA, text=pagina_html, status_code=200)
    requests_mock.get(
        "https://www.b3.com.br/data/files/xxx/Limites.zip",
        content=zip_bytes,
        status_code=200,
    )

    registros = blg.capturar()
    df = registros if isinstance(registros, pd.DataFrame) else pd.DataFrame(registros)
    assert not df.empty
    assert df["tipo_ativo"].iloc[0] == "Ações_BDRs_ETFs_Units"
    assert df["data_referencia"].iloc[0] == "2025-06-01"


def test_b3_bdi_derivativos_resumo_metadata():
    """Verifica metadados e configuração do scraper B3 BDI Derivativos."""
    from scrapers.b3_bdi_derivativos_resumo import CABECALHO, B3BdiDerivativosResumoScraper

    s = B3BdiDerivativosResumoScraper()
    assert s.name == "b3_bdi_derivativos_resumo"
    assert s.group == "b3"
    assert s.enabled is True
    assert s.accumulate is True
    assert "data_referencia" in s.chaves_dedup
    assert "ticker_simb" in s.chaves_dedup
    assert len(CABECALHO) == 11


def test_b3_bdi_derivativos_resumo_captura_mock(requests_mock):
    """Testa a captura e parsing dos contratos de derivativos com mock de resposta BDI."""
    import datetime

    from scrapers.b3_bdi_derivativos_resumo import capturar_dia

    mock_payload = {
        "table": {
            "columns": [
                {"name": "TckrSymb"},
                {"name": "Category"},
                {"name": "Market"},
                {"name": "Derivatives"},
                {"name": "Tipo"},
                {"name": "NmbrTradesDay"},
                {"name": "NmbrCntrctsDay"},
                {"name": "TotalVlmRS"},
                {"name": "TotalVlmUS"},
                {"name": "OrderCol"},
            ],
            "values": [
                [
                    "BGI: BOI GORDO - FUTURO",
                    "PREGÃO ELETRÔNICO",
                    "COMMODITIES",
                    "BGI: BOI GORDO",
                    "FUTURO",
                    5158,
                    8050,
                    997840254,
                    194529730,
                    1,
                    None,
                ],
                [
                    "DOL: DÓLAR COMERCIAL - FUTURO",
                    "PREGÃO ELETRÔNICO",
                    "MOEDAS",
                    "DOL: DÓLAR",
                    "FUTURO",
                    12000,
                    45000,
                    12500000000,
                    2400000000,
                    2,
                    None,
                ],
            ],
        }
    }

    url = "https://arquivos.b3.com.br/bdi/table/DerivativesOperation2/2026-09-11/2026-09-11/1/500"
    requests_mock.post(url, json=mock_payload, status_code=200)

    registros = capturar_dia(datetime.date(2026, 9, 11))
    assert len(registros) == 2
    assert registros[0]["ticker_simb"] == "BGI: BOI GORDO - FUTURO"
    assert registros[0]["mercado"] == "COMMODITIES"
    assert registros[0]["quantidade_negocios"] == 5158
    assert registros[0]["quantidade_contratos"] == 8050
    assert registros[0]["volume_financeiro_brl"] == 997840254
    assert registros[1]["ticker_simb"] == "DOL: DÓLAR COMERCIAL - FUTURO"
    assert registros[1]["mercado"] == "MOEDAS"


def test_b3_opcoes_posicoes_aberto_metadata():
    """Verifica metadados e configuração do scraper B3 Opções Posições em Aberto."""
    from scrapers.b3_opcoes_posicoes_aberto import (
        CABECALHO_GRANULAR,
        CABECALHO_RESUMO,
        B3OpcoesPosicoesAbertoScraper,
    )

    s = B3OpcoesPosicoesAbertoScraper()
    assert s.name == "b3_opcoes_posicoes_aberto"
    assert s.group == "b3"
    assert s.enabled is True
    assert s.accumulate is False
    assert s.compress is True
    assert "opções" in s.tags
    assert len(CABECALHO_GRANULAR) == 16
    assert len(CABECALHO_RESUMO) == 13


def test_b3_opcoes_posicoes_aberto_captura_mock(requests_mock):
    """Testa a captura de opções de empresas e índices e o cálculo do resumo com Put/Call Ratio."""
    import datetime
    from scrapers.b3_opcoes_posicoes_aberto import capturar_dia, gerar_resumo_por_ativo

    mock_emp = {
        "Empresa": {
            "P": [
                {
                    "ser": "PETRJ300",
                    "prEx": 30.50,
                    "nmEmp": "PETROBRAS",
                    "mer": "PETR",
                    "espPap": "PN",
                    "tMerc": "70",  # CALL
                    "dtVen": "20261016",
                    "poCob": 1000,
                    "posTr": 200,
                    "posDe": 300,
                    "posTo": 1500,
                    "qtdClTit": 50,
                    "qtdClLan": 30,
                },
                {
                    "ser": "PETRV300",
                    "prEx": 29.00,
                    "nmEmp": "PETROBRAS",
                    "mer": "PETR",
                    "espPap": "PN",
                    "tMerc": "80",  # PUT
                    "dtVen": "20261016",
                    "poCob": 500,
                    "posTr": 100,
                    "posDe": 400,
                    "posTo": 1000,
                    "qtdClTit": 40,
                    "qtdClLan": 20,
                },
            ]
        }
    }

    mock_ind = {
        "Indice": [
            {
                "ser": "IBOVJ130",
                "prEx": 130000.0,
                "nmEmp": "",
                "mer": "IBOV",
                "espPap": "",
                "tMerc": "70",  # CALL
                "dtVen": "20261014",
                "poCob": 0,
                "posTr": 50,
                "posDe": 50,
                "posTo": 100,
                "qtdClTit": 10,
                "qtdClLan": 5,
            }
        ]
    }

    url_emp = "https://www.b3.com.br/json/20260911/Posicoes/Empresa/SI_C_OPCPOSABEMP.json"
    url_ind = "https://www.b3.com.br/json/20260911/Posicoes/Indice/SI_C_OPCPOSABIND.json"

    requests_mock.get(url_emp, json=mock_emp, status_code=200)
    requests_mock.get(url_ind, json=mock_ind, status_code=200)

    registros, str_ref = capturar_dia(datetime.date(2026, 9, 11))
    assert str_ref == "2026-09-11"
    assert len(registros) == 3

    # Verifica empresa (PETR)
    petr_call = [r for r in registros if r["serie"] == "PETRJ300"][0]
    assert petr_call["tipo_mercado"] == "CALL"
    assert petr_call["codigo_ativo_objeto"] == "PETR"
    assert petr_call["data_vencimento"] == "2026-10-16"
    assert petr_call["preco_exercicio"] == 30.50
    assert petr_call["posicao_total"] == 1500

    # Verifica índice (IBOV)
    ibov_call = [r for r in registros if r["codigo_ativo_objeto"] == "IBOV"][0]
    assert ibov_call["categoria_ativo"] == "INDICE"
    assert ibov_call["posicao_total"] == 100

    # Testa cálculo de resumo e Put/Call Ratio
    df_granular = pd.DataFrame(registros)
    df_resumo = gerar_resumo_por_ativo(df_granular, str_ref)

    assert len(df_resumo) == 2  # PETR e IBOV
    row_petr = df_resumo[df_resumo["codigo_ativo_objeto"] == "PETR"].iloc[0]
    assert row_petr["posicao_aberta_call"] == 1500
    assert row_petr["posicao_aberta_put"] == 1000
    assert row_petr["posicao_aberta_total"] == 2500
    assert row_petr["put_call_ratio"] == round(1000 / 1500, 4)
    assert row_petr["strike_max_oi_call"] == 30.50
    assert row_petr["strike_max_oi_put"] == 29.00


def test_b3_opcoes_posicoes_resumo_metadata():
    """Verifica metadados do scraper B3 Opções Posições Resumo."""
    from scrapers.b3_opcoes_posicoes_resumo import B3OpcoesPosicoesResumoScraper

    s = B3OpcoesPosicoesResumoScraper()
    assert s.name == "b3_opcoes_posicoes_resumo"
    assert s.group == "b3"
    assert s.enabled is True
    assert s.accumulate is True
    assert "data_referencia" in s.chaves_dedup
    assert "codigo_ativo_objeto" in s.chaves_dedup
    assert "put call ratio" in s.tags



