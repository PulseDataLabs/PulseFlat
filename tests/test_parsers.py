"""
tests/test_parsers.py
---------------------
Testes unitários das funções utilitárias de parsing e normalização de dados
definidas em utils/parsers.py (CSV, JSON, XML, FWF, normalização de chaves e decodificação).
"""

import sys
from pathlib import Path
from datetime import datetime
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import utils.parsers as parsers


def test_decode_bytes():
    """Deve decodificar corretamente bytes com encodings variados, caindo de volta em latin1/cp1252."""
    utf8_sig_bytes = b"\xef\xbb\xbfOl\xc3\xa1 Mundo"
    assert parsers.decode_bytes(utf8_sig_bytes) == "Olá Mundo"

    latin1_bytes = "Cotação".encode("latin1")
    assert parsers.decode_bytes(latin1_bytes) == "Cotação"


def test_normalize_key():
    """Deve normalizar strings para formato snake_case limpo, removendo acentos e caracteres especiais."""
    assert parsers.normalize_key("  Nome da Companhia  ") == "nome_da_companhia"
    assert parsers.normalize_key("Código CVM / Cadastro") == "c_digo_cvm_cadastro"
    assert parsers.normalize_key("Data de Referência (2026)") == "data_de_refer_ncia_2026"
    assert parsers.normalize_key("Taxa % a.a.") == "taxa_a_a"
    assert parsers.normalize_key("___teste__multiplo__") == "teste_multiplo"
    assert parsers.normalize_key("") == "campo"


def test_csv_rows():
    """Deve identificar automaticamente o delimitador e extrair as linhas normalizando as chaves."""
    csv_semicolon = "Código;Nome;Valor\n123;Empresa A;10.50\n456;Empresa B;20.30"
    rows = parsers.csv_rows(csv_semicolon)
    assert len(rows) == 2
    assert rows[0]["c_digo"] == "123"
    assert rows[0]["nome"] == "Empresa A"
    assert rows[0]["valor"] == "10.50"

    csv_comma = "code,name,price\n99,Asset X,1.23"
    rows_comma = parsers.csv_rows(csv_comma)
    assert len(rows_comma) == 1
    assert rows_comma[0]["code"] == "99"
    assert rows_comma[0]["name"] == "Asset X"


def test_json_rows():
    """Deve parsear payloads JSON (listas e dicts) convertendo sub-estruturas em strings e normalizando chaves."""
    payload_list = [
        {"id": 1, "dados": {"sub_id": 100, "status": "ativo"}},
        {"id": 2, "dados": [1, 2, 3]}
    ]
    rows = parsers.json_rows(payload_list)
    assert len(rows) == 2
    assert rows[0]["id"] == "1"
    # Dicionários devem ser convertidos para string JSON
    assert "status" in rows[0]["dados"]
    assert "ativo" in rows[0]["dados"]
    # Listas devem ser convertidas para string JSON
    assert rows[1]["dados"] == "[1, 2, 3]"


def test_fwf_rows():
    """Deve fatiar linhas de largura fixa (FWF) e processar deslocamento de casas decimais."""
    # Definição dos campos
    fields = ["regtype", "codigo", "valor_indicador", "num_casas_decimais"]
    widths = [2, 10, 8, 1]

    # Exemplo 1: regtype = 01, valor_indicador = 00012345 (12345), casas = 2 -> 123.45
    line1 = "01PETR4     000123452\n"
    # Exemplo 2: regtype = 02, valor_indicador = 00005000 (5000), casas = 3 -> 5.000
    line2 = "02VALE3     000050003\n"

    text = line1 + line2

    # Rodando apenas para regtype 01
    rows_only_01 = parsers.fwf_rows(text, fields, widths, only_regtype_01=True)
    assert len(rows_only_01) == 1
    assert rows_only_01[0]["regtype"] == "01"
    assert rows_only_01[0]["codigo"] == "PETR4"
    assert rows_only_01[0]["valor_indicador"] == "000123.45"

    # Rodando para todos
    rows_all = parsers.fwf_rows(text, fields, widths, only_regtype_01=False)
    assert len(rows_all) == 2
    assert rows_all[1]["regtype"] == "02"
    assert rows_all[1]["codigo"] == "VALE3"
    assert rows_all[1]["valor_indicador"] == "00005.000"


def test_xml_rows():
    """Deve extrair elementos XML em formato de dicionários planos tratando namespaces."""
    xml_data = b"""<?xml version="1.0" encoding="UTF-8"?>
    <root xmlns:ns="http://example.org">
        <item>
            <ns:id>10</ns:id>
            <ns:nome>Teste XML</ns:nome>
        </item>
        <item>
            <ns:id>20</ns:id>
            <ns:nome>Outro Teste</ns:nome>
        </item>
    </root>
    """
    rows = parsers.xml_rows(xml_data)
    assert len(rows) == 2
    assert rows[0]["xml_tag"] == "item"
    assert rows[0]["id"] == "10"
    assert rows[0]["nome"] == "Teste XML"


def test_replace_date_vars():
    """Deve substituir placeholders de data em strings (URLs) por valores formatados."""
    dt = datetime(2026, 6, 4)
    url = "https://dados.com/YYYY-MM-DD/arquivo_YYYYMMDD.csv"
    formatted = parsers.replace_date_vars(url, dt)
    assert formatted == "https://dados.com/2026-06-04/arquivo_20260604.csv"

    url_br = "https://dados.com/DD/MM/YYYY"
    assert parsers.replace_date_vars(url_br, dt) == "https://dados.com/04/06/2026"


def test_hash_row():
    """Deve gerar um hash SHA256 de 24 caracteres estável para o conteúdo de um dicionário."""
    row1 = {"codigo": "PETR4", "preco": "42.50"}
    row2 = {"preco": "42.50", "codigo": "PETR4"}  # ordem diferente
    h1 = parsers.hash_row(row1)
    h2 = parsers.hash_row(row2)

    assert len(h1) == 24
    assert h1 == h2  # estável independente da ordem dos campos

    row3 = {"codigo": "VALE3", "preco": "42.50"}
    assert h1 != parsers.hash_row(row3)
