import utils.parsers as parsers


class TestDefensiveParsers:
    """Testes defensivos para tratamento de entradas malformadas ou corrompidas."""

    def test_decode_bytes_fallback_bytes_corrompidos(self):
        corrupted = b"\xff\xfe\x99\xaa\xbb\xcc"
        res = parsers.decode_bytes(corrupted)
        assert isinstance(res, str)
        assert len(res) > 0

    def test_csv_rows_corrompido_ou_vazio(self):
        assert parsers.csv_rows("") == []
        assert parsers.csv_rows("   \n\n  ") == []

        csv_irregular = "A;B\n1;2;3\n4"
        rows = parsers.csv_rows(csv_irregular)
        assert isinstance(rows, list)
        assert len(rows) > 0

    def test_json_rows_entradas_atipicas(self):
        assert parsers.json_rows("") == [{"valor": ""}]
        assert parsers.json_rows("{{invalid json") == [{"valor": "{{invalid json"}]
        assert parsers.json_rows([1, 2, 3]) == [
            {"valor": "1"},
            {"valor": "2"},
            {"valor": "3"},
        ]
        assert parsers.json_rows({"chave": "valor"}) == [{"chave": "valor"}]

    def test_xml_rows_xml_invalido(self):
        invalid_xml = b"<root><item><nome>Teste"
        res = parsers.xml_rows(invalid_xml)
        assert res == []

    def test_fwf_rows_linhas_curtas_ou_invalidas(self):
        fields = ["regtype", "codigo", "valor_indicador", "num_casas_decimais"]
        widths = [2, 10, 8, 1]

        # Linha válida
        valid_line = "01PETR4     000100002"
        rows = parsers.fwf_rows(valid_line, fields, widths, only_regtype_01=True)
        assert len(rows) == 1
        assert rows[0]["codigo"] == "PETR4"
        assert rows[0]["valor_indicador"] == "000100.00"

    def test_normalize_key_caracteres_raros(self):
        assert parsers.normalize_key("@#$%&*()_+") == "campo"
        assert parsers.normalize_key("123 Número de Série") in ("c_123_numero_de_serie", "123_numero_de_serie")
        assert parsers.normalize_key("emoji 🚀 indicador") == "emoji_indicador"
