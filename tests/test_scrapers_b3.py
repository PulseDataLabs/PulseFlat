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
import pytest
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scrapers.b3_classificacao_setorial as bcs


def test_b3_classificacao_setorial_sucesso(requests_mock):
    """Deve capturar e extrair corretamente a classificação setorial B3 a partir de um ZIP mockado."""
    # Crie um arquivo Excel mock em memória
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Plan3"
    
    # Adiciona linhas no formato esperado
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
    assert emp["nome_empresa"] == "PETROBRAS"
    assert emp["codigo"] == "PETR"


def test_b3_classificacao_setorial_scraper_fetch(requests_mock):
    """Deve testar o método fetch da classe B3ClassificacaoSetorialScraper."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Plan3"
    for _ in range(6):
        ws.append([None, None, None, None, None, None, None])
    ws.append(['SETOR ECONÔMICO', 'SUBSETOR', 'SEGMENTO', 'LISTAGEM', None, None, None])
    ws.append([None, None, None, 'CÓDIGO', 'SEGMENTO', None, None])
    ws.append(['Petróleo', 'Petróleo', 'Exploração', None, None, None, None])
    ws.append([None, None, 'PETROBRAS', 'PETR', 'N2', None, None])
    
    excel_io = io.BytesIO()
    wb.save(excel_io)
    excel_bytes = excel_io.getvalue()
    
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, 'w') as zf:
        zf.writestr('Setorial B3.xlsx', excel_bytes)
    zip_bytes = zip_io.getvalue()
    
    requests_mock.get(
        bcs.URL,
        content=zip_bytes,
        status_code=200
    )
    
    scraper = bcs.B3ClassificacaoSetorialScraper()
    df = scraper.fetch()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["data_captura", "setor_economico", "subsetor", "segmento", "nome_empresa", "codigo", "segmento_listagem"]
