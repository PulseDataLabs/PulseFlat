"""
tests/test_scrapers_bcb.py
--------------------------
Testes unitários específicos para os scrapers do Banco Central do Brasil (BCB / BACEN).
"""

import re
import sys
from pathlib import Path

import pandas as pd
import pytest

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
                "dataHoraCotacao": "2026-06-01 13:15:00.000",
            }
        ]
    }

    requests_mock.get(
        re.compile(r"https://olinda\.bcb\.gov\.br/.*"),
        json=mock_response,
        status_code=200,
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
    requests_mock.get(re.compile(r"https://olinda\.bcb\.gov\.br/.*"), status_code=500)

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
                "dataHoraCotacao": "2026-06-01 13:15:00.000",
            }
        ]
    }

    requests_mock.get(
        re.compile(r"https://olinda\.bcb\.gov\.br/.*"),
        json=mock_response,
        status_code=200,
    )

    scraper = bcb_ptax.BcbPtaxScraper()
    df = scraper.fetch()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == [
        "data_captura",
        "data_referencia",
        "cotacao_compra",
        "cotacao_venda",
    ]
    assert df.loc[0, "cotacao_compra"] == "5.253"


def test_bcb_sgs_sucesso(requests_mock, monkeypatch):
    """Deve capturar as séries do SGS, realizar sleep e mapear campos corretamente."""
    monkeypatch.setattr(bcb_sgs.time, "sleep", lambda x: None)

    mock_dados = [
        {"data": "01/06/2026", "valor": "10.50"},
        {"data": "02/06/2026", "valor": "10.75"},
    ]

    requests_mock.get(
        re.compile(r"https://api\.bcb\.gov\.br/.*"), json=mock_dados, status_code=200
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

    requests_mock.get(re.compile(r"https://api\.bcb\.gov\.br/.*"), json=callback)

    registros = bcb_sgs.capturar()

    codigos_capturados = {reg["codigo_serie"] for reg in registros}
    assert "11" not in codigos_capturados
    assert len(codigos_capturados) == len(bcb_sgs.SERIES) - 1


def test_bcb_sgs_scraper_fetch(requests_mock, monkeypatch):
    """Deve testar o método fetch do BcbSgsScraper instanciado."""
    monkeypatch.setattr(bcb_sgs.time, "sleep", lambda x: None)

    mock_dados = [{"data": "01/06/2026", "valor": "5.25"}]

    requests_mock.get(
        re.compile(r"https://api\.bcb\.gov\.br/.*"), json=mock_dados, status_code=200
    )

    scraper = bcb_sgs.BcbSgsScraper()
    df = scraper.fetch()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "codigo_serie" in df.columns
    assert "valor" in df.columns


def test_bacen_cadastro_instituicoes_metadata():
    """Verifica metadados e configuração do scraper BACEN Cadastro de Instituições."""
    from scrapers.bacen_cadastro_instituicoes import (
        CABECALHO,
        BacenCadastroInstituicoesScraper,
    )

    s = BacenCadastroInstituicoesScraper()
    assert s.name == "bacen_cadastro_instituicoes"
    assert s.group == "bcb"
    assert s.enabled is True
    assert s.accumulate is True
    assert s.compress is True
    assert s.output_file.name == "bacen_cadastro_instituicoes.csv.gz"
    assert "data_base" in s.chaves_dedup
    assert "codigo_instituicao" in s.chaves_dedup
    assert "instituições financeiras" in s.tags
    assert len(CABECALHO) == 20


def test_bacen_cadastro_instituicoes_captura_mock(requests_mock):
    """Testa captura e parsing da API Olinda IFData para o cadastro de IFs."""
    from scrapers.bacen_cadastro_instituicoes import capturar_cadastro_trimestre

    mock_odata = {
        "value": [
            {
                "CodInst": "00000000",
                "Data": "202606",
                "NomeInstituicao": "BCO DO BRASIL S.A.",
                "DataInicioAtividade": 180801,
                "Tcb": "B1",
                "Td": "C",
                "Tc": 1,
                "SegmentoTb": None,
                "Atividade": "Banco Comercial",
                "Uf": "DF",
                "Municipio": "Brasília",
                "Sr": "S1",
                "CodConglomeradoFinanceiro": "C0000001",
                "CodConglomeradoPrudencial": "C0000002",
                "CnpjInstituicaoLider": "00000000",
                "Situacao": "A",
            },
            {
                "CodInst": "5464-72-59",
                "Data": "202606",
                "NomeInstituicao": "321 SOCIEDADE DE CRÉDITO DIRETO S.A.",
                "DataInicioAtividade": 202407,
                "Tcb": "N1",
                "Td": "I",
                "Tc": 2,
                "SegmentoTb": None,
                "Atividade": "Sociedade de Crédito Direto",
                "Uf": "RS",
                "Municipio": "Porto Alegre",
                "Sr": "S4",
                "CodConglomeradoFinanceiro": None,
                "CodConglomeradoPrudencial": None,
                "CnpjInstituicaoLider": "15581638",
                "Situacao": "A",
            },
        ]
    }

    requests_mock.get(
        re.compile(r"https://olinda\.bcb\.gov\.br/olinda/servico/IFDATA/versao/v1/odata/IfDataCadastro.*"),
        json=mock_odata,
        status_code=200,
    )

    registros = capturar_cadastro_trimestre("202606")
    assert len(registros) == 2

    bb = registros[0]
    assert bb["codigo_instituicao"] == "00000000"
    assert bb["nome_instituicao"] == "BCO DO BRASIL S.A."
    assert bb["data_base"] == "2026-06-30"
    assert bb["segmento_prudencial"] == "S1"
    assert bb["tipo_consolidacao"] == "B1"
    assert "Carteira Comercial" in bb["tipo_consolidacao_desc"]
    assert bb["tipo_controle_desc"] == "Público"
    assert bb["situacao_desc"] == "Ativa"
    assert bb["cnpj_instituicao_lider"] == "00.000.000"
    assert bb["ano_mes_inicio_atividade"] == "1808-01"

    scd = registros[1]
    assert scd["codigo_instituicao"] == "5464-72-59"
    assert scd["segmento_prudencial"] == "S4"
    assert scd["tipo_controle_desc"] == "Privado Nacional"
    assert scd["cnpj_instituicao_lider"] == "15.581.638"
    assert scd["ano_mes_inicio_atividade"] == "2024-07"


def test_bacen_letras_financeiras_12_scrapers_metadata():
    """Valida metadados, cabeçalhos e chaves_dedup dos 12 scrapers de Letras Financeiras do BACEN."""
    from scrapers.bacen_lf_emissoes import BacenLfEmissoesScraper
    from scrapers.bacen_lf_estoque import BacenLfEstoqueScraper
    from scrapers.bacen_lf_estoque_emissor import BacenLfEstoqueEmissorScraper
    from scrapers.bacen_lf_estoque_indexador import BacenLfEstoqueIndexadorScraper
    from scrapers.bacen_lf_estoque_natureza_detentor import (
        BacenLfEstoqueNaturezaDetentorScraper,
    )
    from scrapers.bacen_lf_estoque_segmento import BacenLfEstoqueSegmentoScraper
    from scrapers.bacen_lf_mercado_secundario import BacenLfMercadoSecundarioScraper
    from scrapers.bacen_lf_prazo_emissoes import BacenLfPrazoEmissoesScraper
    from scrapers.bacen_lf_prazo_vencimento import BacenLfPrazoVencimentoScraper
    from scrapers.bacen_lf_prazo_vencimento_segmento import (
        BacenLfPrazoVencimentoSegmentoScraper,
    )
    from scrapers.bacen_lfs_estoque_segmento import BacenLfsEstoqueSegmentoScraper
    from scrapers.bacen_lfs_prazo_vencimento_segmento import (
        BacenLfsPrazoVencimentoSegmentoScraper,
    )

    classes = [
        BacenLfEmissoesScraper,
        BacenLfEstoqueScraper,
        BacenLfEstoqueNaturezaDetentorScraper,
        BacenLfEstoqueEmissorScraper,
        BacenLfEstoqueIndexadorScraper,
        BacenLfEstoqueSegmentoScraper,
        BacenLfPrazoVencimentoSegmentoScraper,
        BacenLfsEstoqueSegmentoScraper,
        BacenLfsPrazoVencimentoSegmentoScraper,
        BacenLfMercadoSecundarioScraper,
        BacenLfPrazoEmissoesScraper,
        BacenLfPrazoVencimentoScraper,
    ]

    assert len(classes) == 12
    for cls in classes:
        inst = cls()
        assert inst.group == "bcb"
        assert inst.enabled is True
        assert inst.accumulate is True
        assert inst.compress is True
        assert inst.output_file.name == f"{inst.name}.csv.gz"
        assert inst.chaves_dedup and "data_referencia" in inst.chaves_dedup
        assert inst.title.startswith("BACEN — Letras Financeiras")
        assert inst.badge in ("Mensal", "Anual")


def test_bacen_lf_helper_parsers_in_memory():
    """Testa os parsers de planilhas XLSX de Letras Financeiras do BACEN com workbooks em memória."""
    from io import BytesIO
    import openpyxl
    from scrapers.utils.bacen_lf_helper import (
        parse_annual_holder_nature,
        parse_annual_indexer,
        parse_annual_issuer,
        parse_monthly_lf_lfs,
        parse_monthly_secondary_market,
        parse_monthly_segments,
    )

    # 1. Teste mensal LF / LFS (com nota de rodapé 'LF 2/' no cabeçalho)
    wb1 = openpyxl.Workbook()
    ws1 = wb1.active
    ws1.title = "2021"
    ws1.cell(9, 1, "Mês")
    ws1.cell(9, 2, "LF 2/")
    ws1.cell(9, 3, "LFS")
    ws1.cell(10, 1, "jan")
    ws1.cell(10, 2, 36.7659)
    ws1.cell(10, 3, 97.3118)
    ws1.cell(11, 1, "Legenda: LF - Letra Financeira")
    buf1 = BytesIO()
    wb1.save(buf1)

    regs_lf = parse_monthly_lf_lfs(
        buf1.getvalue(),
        col_lf="prazo_medio_emissao_lf_meses",
        col_lfs="prazo_medio_emissao_lfs_meses",
    )
    assert len(regs_lf) == 1
    assert regs_lf[0]["data_referencia"] == "2021-01-01"
    assert regs_lf[0]["prazo_medio_emissao_lf_meses"] == "36.7659"
    assert regs_lf[0]["prazo_medio_emissao_lfs_meses"] == "97.3118"

    # 2. Teste mensal por segmento (wide format com evolução de colunas entre anos)
    wb2 = openpyxl.Workbook()
    ws2_2010 = wb2.active
    ws2_2010.title = "2010"
    ws2_2010.cell(9, 1, "Mês")
    ws2_2010.cell(9, 2, "Bancos Comerciais")
    ws2_2010.cell(9, 3, "Totais")
    ws2_2010.cell(10, 1, "abr")
    ws2_2010.cell(10, 2, 100.5)
    ws2_2010.cell(10, 3, 100.5)

    ws2_2025 = wb2.create_sheet("2025")
    ws2_2025.cell(9, 1, "Mês")
    ws2_2025.cell(9, 2, "Bancos Comerciais ")
    ws2_2025.cell(9, 3, "Cooperativas de Crédito ")
    ws2_2025.cell(9, 4, "Total Geral")
    ws2_2025.cell(10, 1, "dez")
    ws2_2025.cell(10, 2, 200.0)
    ws2_2025.cell(10, 3, 50.25)
    ws2_2025.cell(10, 4, 250.25)
    buf2 = BytesIO()
    wb2.save(buf2)

    expected_cols = ["bancos_comerciais", "cooperativas_credito", "total"]
    regs_seg = parse_monthly_segments(buf2.getvalue(), expected_segment_cols=expected_cols)
    assert len(regs_seg) == 2
    assert regs_seg[0]["data_referencia"] == "2010-04-01"
    assert regs_seg[0]["cooperativas_credito"] == ""
    assert regs_seg[1]["data_referencia"] == "2025-12-01"
    assert regs_seg[1]["cooperativas_credito"] == "50.25"
    assert regs_seg[1]["total"] == "250.25"

    # 3. Teste EstoquePorEmissor (coluna mesclada None em 2010 vs normal em 2025 e exclusão de Totais)
    wb3 = openpyxl.Workbook()
    ws3_2010 = wb3.active
    ws3_2010.title = "2010"
    ws3_2010.cell(8, 1, "Estoque por Emissor em 31/12/2010 (R$ Mi)")
    ws3_2010.cell(9, 1, "IF/Conglomerado")
    ws3_2010.cell(9, 2, None)
    ws3_2010.cell(9, 3, "LF")
    ws3_2010.cell(9, 4, "LFS")
    ws3_2010.cell(9, 5, "Totais")
    ws3_2010.cell(10, 1, "BRADESCO")
    ws3_2010.cell(10, 3, 1000.0)
    ws3_2010.cell(10, 4, 500.0)
    ws3_2010.cell(10, 5, 1500.0)
    ws3_2010.cell(11, 1, "Totais")
    ws3_2010.cell(11, 3, 1000.0)
    buf3 = BytesIO()
    wb3.save(buf3)

    regs_emissor = parse_annual_issuer(buf3.getvalue())
    assert len(regs_emissor) == 1
    assert regs_emissor[0]["instituicao_conglomerado"] == "BRADESCO"
    assert regs_emissor[0]["cnpj"] == "60746948000112"
    assert regs_emissor[0]["data_referencia"] == "2010-12-31"
    assert regs_emissor[0]["estoque_total"] == "1500.0"

    # 4. Teste EstoquePorIndexador (escala R$ Mi em 2010 vs R$ em 2025 + remoção de linha None de soma)
    wb4 = openpyxl.Workbook()
    ws4_2010 = wb4.active
    ws4_2010.title = "2010 "
    ws4_2010.cell(8, 1, "Estoque por indexador em 31/12/2010")
    ws4_2010.cell(9, 1, "Indexador")
    ws4_2010.cell(9, 2, "Valor (R$ Mi)")
    ws4_2010.cell(9, 3, "%")
    c_val_2010 = ws4_2010.cell(10, 2, 30056.5)
    c_val_2010.number_format = "#\\ #00\\ \\ "
    ws4_2010.cell(10, 1, "DI")
    ws4_2010.cell(10, 3, 0.97)
    ws4_2010.cell(11, 1, "Totais")
    ws4_2010.cell(11, 2, 30056.5)

    ws4_2025 = wb4.create_sheet("2025")
    ws4_2025.cell(8, 1, "Estoque por indexador em 31/12/2025")
    ws4_2025.cell(9, 1, "Indexador")
    ws4_2025.cell(9, 2, "Valor (R$ Mi)")
    ws4_2025.cell(9, 3, "%")
    ws4_2025.cell(10, 1, "DI   ")
    c_val_2025 = ws4_2025.cell(10, 2, 864168557823.23)
    c_val_2025.number_format = "#,##0,,_ ;\\-#,##0,,"
    ws4_2025.cell(10, 3, 0.8917)
    ws4_2025.cell(11, 1, None)
    ws4_2025.cell(11, 2, 969118118043.48)
    buf4 = BytesIO()
    wb4.save(buf4)

    regs_idx = parse_annual_indexer(buf4.getvalue())
    assert len(regs_idx) == 2
    assert regs_idx[0]["data_referencia"] == "2010-12-31"
    assert regs_idx[0]["valor"] == "30056500000.0"
    assert regs_idx[0]["participacao_perc"] == "97.0"
    assert regs_idx[1]["data_referencia"] == "2025-12-31"
    assert regs_idx[1]["indexador"] == "DI"
    assert regs_idx[1]["participacao_perc"] == "89.17"

    # 5. Teste Natureza do Detentor e Mercado Secundário
    wb5 = openpyxl.Workbook()
    ws5 = wb5.active
    ws5.title = "2023"
    ws5.cell(8, 1, "Estoque por Natureza dos Detentores em 29/12/2023 (R$ Mi)")
    ws5.cell(9, 1, "Natureza do Detentor")
    ws5.cell(9, 2, "LF")
    ws5.cell(9, 3, "LFS")
    ws5.cell(9, 4, "Totais")
    ws5.cell(9, 5, "%")
    ws5.cell(10, 1, "Fundos de investimento")
    ws5.cell(10, 2, 100.0)
    ws5.cell(10, 3, 50.0)
    ws5.cell(10, 4, 150.0)
    ws5.cell(10, 5, 0.75)
    ws5.cell(11, 1, "Total")
    ws5.cell(11, 4, 150.0)
    buf5 = BytesIO()
    wb5.save(buf5)

    regs_det = parse_annual_holder_nature(buf5.getvalue())
    assert len(regs_det) == 1
    assert regs_det[0]["data_referencia"] == "2023-12-29"
    assert regs_det[0]["participacao_perc"] == "75.0"

    wb6 = openpyxl.Workbook()
    ws6 = wb6.active
    ws6.title = "2025"
    ws6.cell(9, 1, "Mês")
    ws6.cell(9, 2, "Nº Negócios")
    ws6.cell(9, 3, "Valor (R$ Mi)")
    ws6.cell(10, 1, "jan")
    ws6.cell(10, 2, 9872)
    ws6.cell(10, 3, 32700659674.32)
    buf6 = BytesIO()
    wb6.save(buf6)

    regs_sec = parse_monthly_secondary_market(buf6.getvalue())
    assert len(regs_sec) == 1
    assert regs_sec[0]["numero_negocios"] == "9872"
    assert regs_sec[0]["valor"] == "32700659674.32"


