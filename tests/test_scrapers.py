"""
tests/test_scrapers.py
-----------------------
Testes unitários dos scrapers utilizando a biblioteca requests-mock
para simular respostas das APIs externas e garantir a resiliência do pipeline.
"""

import re
import sys
from pathlib import Path
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
                "dataHoraCotacao": "2026-06-01 13:15:00.000"
            }
        ]
    }

    # Mock de qualquer chamada para o domínio da PTAX Olinda
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
    assert reg["data_hora_cotacao"] == "2026-06-01 13:15:00.000"
    assert "data_captura" in reg


def test_bcb_ptax_erro_conexao(requests_mock):
    """Deve falhar e terminar com código de saída 1 se a API PTAX Olinda falhar em todas as tentativas."""
    requests_mock.get(
        re.compile(r"https://olinda\.bcb\.gov\.br/.*"),
        status_code=500
    )

    # O script bcb_ptax chama sys.exit(1) em caso de erro persistente
    with pytest.raises(SystemExit) as exc_info:
        bcb_ptax.capturar()

    assert exc_info.value.code == 1


def test_bcb_sgs_sucesso(requests_mock, monkeypatch):
    """Deve capturar as séries do SGS, realizar sleep e mapear campos corretamente."""
    # Como bcb_sgs faz time.sleep entre chamadas e em retries, vamos mockar para rodar rápido
    monkeypatch.setattr(bcb_sgs.time, "sleep", lambda x: None)

    mock_dados = [
        {"data": "01/06/2026", "valor": "10.50"},
        {"data": "02/06/2026", "valor": "10.75"}
    ]

    # Mock de todas as chamadas do SGS
    requests_mock.get(
        re.compile(r"https://api\.bcb\.gov\.br/.*"),
        json=mock_dados,
        status_code=200
    )

    registros = bcb_sgs.capturar()

    # Cada uma das séries mapeadas em SERIES deve retornar dados
    total_esperado = len(bcb_sgs.SERIES) * 2
    assert len(registros) == total_esperado

    for reg in registros:
        assert reg["data"] in ("01/06/2026", "02/06/2026")
        assert reg["valor"] in ("10.5", "10.75", "10.50")
        assert "codigo_serie" in reg
        assert "nome_serie" in reg
        assert "data_captura" in reg


def test_bcb_sgs_erro_parcial(requests_mock, monkeypatch):
    """Deve tolerar erros parciais nas séries do SGS e capturar apenas as que funcionarem."""
    monkeypatch.setattr(bcb_sgs.time, "sleep", lambda x: None)

    # Série 11 (SELIC) vai falhar, Série 1 (Dólar) e as demais vão funcionar
    mock_dados = [{"data": "01/06/2026", "valor": "5.25"}]

    def callback(request, context):
        if "sgs.11" in request.url:
            context.status_code = 500
            return {"error": "Internal Server Error"}
        context.status_code = 200
        return mock_dados


    # Registra o mock com callback dinâmico
    requests_mock.get(
        re.compile(r"https://api\.bcb\.gov\.br/.*"),
        json=callback
    )

    registros = bcb_sgs.capturar()

    # Deve conter registros de todas as séries exceto a série 11 que falhou
    codigos_capturados = {reg["codigo_serie"] for reg in registros}
    assert "11" not in codigos_capturados
    assert len(codigos_capturados) == len(bcb_sgs.SERIES) - 1


def test_generic_scraper_json(requests_mock, tmp_path, monkeypatch):
    """Deve baixar, processar e salvar corretamente dados de um recurso json genérico."""
    import yaml
    from scrapers.generic_scraper import run_resource

    mock_config = {
        "resources": [
            {
                "name": "teste_json",
                "url": "https://jsonplaceholder.typicode.com/posts/",
                "file_name": "teste_json.json",
                "type_response": "json"
            }
        ]
    }
    monkeypatch.setattr(yaml, "safe_load", lambda f: mock_config)

    mock_data = [
        {"id": 1, "title": "Post 1", "body": "Body 1", "userId": 10},
        {"id": 2, "title": "Post 2", "body": "Body 2", "userId": 20}
    ]

    requests_mock.get(
        "https://jsonplaceholder.typicode.com/posts/",
        json=mock_data,
        status_code=200
    )

    out_file = tmp_path / "teste_json.csv"
    run_resource("teste_json", output_file_override=out_file)

    assert out_file.exists()
    import csv
    with open(out_file, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert rows[0]["id"] == "1"
    assert rows[0]["title"] == "Post 1"
    assert rows[0]["body"] == "Body 1"
    assert rows[0]["userid"] == "10"


def test_b3_classificacao_setorial_sucesso(requests_mock):
    import openpyxl
    import zipfile
    import io
    import scrapers.b3_classificacao_setorial as bcs

    # Crie um arquivo Excel mock em memória
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Plan3"
    
    # Adiciona linhas no formato esperado (com 6 linhas de cabeçalho descritivo inicial)
    for _ in range(6):
        ws.append([None, None, None, None, None, None, None])
    ws.append(['SETOR ECONÔMICO', 'SUBSETOR', 'SEGMENTO', 'LISTAGEM', None, None, None])
    ws.append([None, None, None, 'CÓDIGO', 'SEGMENTO', None, None])
    ws.append(['Petróleo, Gás e Biocombustíveis', 'Petróleo, Gás e Biocombustíveis', 'Exploração, Refino e Distribuição', None, None, None, None])
    ws.append([None, None, 'PETROBRAS', 'PETR', 'N2', None, None])
    
    excel_io = io.BytesIO()
    wb.save(excel_io)
    excel_bytes = excel_io.getvalue()
    
    # Crie um arquivo ZIP mock em memória contendo o Excel
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, 'w') as zf:
        zf.writestr('Setorial B3.xlsx', excel_bytes)
    zip_bytes = zip_io.getvalue()
    
    # Mock do download
    requests_mock.get(
        bcs.URL,
        content=zip_bytes,
        status_code=200
    )
    
    empresas = bcs.capturar()
    assert len(empresas) == 1
    emp = empresas[0]
    assert emp["setor_economico"] == "Petróleo, Gás e Biocombustíveis"
    assert emp["subsetor"] == "Petróleo, Gás e Biocombustíveis"
    assert emp["segmento"] == "Exploração, Refino e Distribuição"
    assert emp["nome_empresa"] == "PETROBRAS"
    assert emp["codigo"] == "PETR"
    assert emp["segmento_listagem"] == "N2"


def test_anbima_ima_completo_sucesso(requests_mock, monkeypatch):
    """Deve capturar, validar D-1 e parsear com sucesso o arquivo IMA Completo da ANBIMA."""
    import scrapers.anbima_ima_completo as aic
    
    # Mock de obter_d1_util para retornar uma data fixa
    monkeypatch.setattr(aic, "obter_d1_util", lambda: "02/06/2026")
    
    # Mock do conteúdo do arquivo txt
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
    assert reg1["variacao_diaria"] == "0.0569"
    assert reg1["variacao_mensal"] == "0.0806"
    assert reg1["variacao_anual"] == "5.5163"
    
    reg2 = registros[1]
    assert reg2["data_referencia"] == "2026-06-02"
    assert reg2["indice"] == "IRF-M 1+"
    assert reg2["numero_indice"] == "24436.46503800"


def test_anbima_indicadores_sucesso(requests_mock):
    """Deve capturar, parsear e limpar corretamente os indicadores do HTML da ANBIMA."""
    import scrapers.anbima_indicadores as ai

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
        Euro Compra 2 02/06/2026 5,8379
        Euro Venda 2 02/06/2026 5,8396
        TR 2 01/06/2026 0,1709
        TBF 2 01/06/2026 1,0460
        FDS 4 02/06/2026 0,088624
        FDS 4 01/06/2026 0,088584
    </body>
    </html>
    """

    requests_mock.get(ai.URL, content=mock_html.encode("iso-8859-1"), status_code=200)

    registros = ai.capturar()
    
    assert len(registros) == 17
    
    # Valida IGP-M Número Índice
    igpm_idx = next(r for r in registros if r["indicador"] == "IGP-M Número Índice")
    assert igpm_idx["valor"] == "1229.904"
    assert igpm_idx["data_referencia"] == "2026-05-01"
    
    # Valida IPCA Número Índice
    ipca_idx = next(r for r in registros if r["indicador"] == "IPCA Número Índice")
    assert ipca_idx["valor"] == "7596.09"
    assert ipca_idx["data_referencia"] == "2026-04-01"

    # Valida Estimativa SELIC
    selic = next(r for r in registros if r["indicador"] == "Estimativa SELIC")
    assert selic["valor"] == "14.40"
    assert selic["data_referencia"] == "2026-06-03"

    # Valida Dólar Comercial Compra
    dolar = next(r for r in registros if r["indicador"] == "Dólar Comercial Compra")
    assert dolar["valor"] == "5.0154"
    assert dolar["data_referencia"] == "2026-06-02"






