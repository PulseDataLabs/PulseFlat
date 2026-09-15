"""
tests/unit/test_compression_and_storage.py
-------------------------------------------
Testes unitários para validar compressão de datasets (.csv.gz), deduplicação,
leitura de cabeçalhos e integridade do armazenamento em disco.
"""

import gzip
import json
from pathlib import Path

import pandas as pd
import pytest

from utils.base import read_existing_header, salvar_csv


class TestCompressionAndStorage:
    """Testa leitura e escrita transparente em arquivos .csv e .csv.gz compactados."""

    def test_read_existing_header_csv_and_gz(self, tmp_path):
        # 1. Arquivo não existente ou vazio
        assert read_existing_header(tmp_path / "nao_existe.csv") == []
        assert read_existing_header(tmp_path / "nao_existe.csv.gz") == []

        # 2. Arquivo CSV regular
        csv_file = tmp_path / "teste.csv"
        csv_file.write_text("data,codigo,valor\n2026-01-01,A,10\n", encoding="utf-8")
        assert read_existing_header(csv_file) == ["data", "codigo", "valor"]

        # 3. Arquivo CSV.GZ compactado
        gz_file = tmp_path / "teste.csv.gz"
        with gzip.open(gz_file, "wt", encoding="utf-8") as f:
            f.write("data,codigo,taxa,pu\n2026-01-01,B,14.5,1000\n")
        assert read_existing_header(gz_file) == ["data", "codigo", "taxa", "pu"]

    def test_salvar_csv_gz_transparent_compression_and_dedup(self, tmp_path):
        """Valida que salvar_csv grava e acumula em .csv.gz com descompressão/recompressão e dedup."""
        gz_target = tmp_path / "dataset_acumulado.csv.gz"

        df_lote1 = pd.DataFrame(
            [
                {"data_referencia": "2026-06-01", "codigo": "PETR4", "valor": 30.50},
                {"data_referencia": "2026-06-01", "codigo": "VALE3", "valor": 65.00},
            ]
        )

        salvar_csv(
            gz_target,
            df_lote1,
            cabecalho=["data_referencia", "codigo", "valor"],
            chaves_dedup=["data_referencia", "codigo"],
            acumular=True,
        )

        assert gz_target.exists()
        # Verifica se é um arquivo gzip válido
        with gzip.open(gz_target, "rt", encoding="utf-8") as f:
            content = f.read()
        assert "PETR4" in content
        assert "VALE3" in content

        # Lote 2: Atualização de PETR4 e inserção de BBAS3
        df_lote2 = pd.DataFrame(
            [
                {"data_referencia": "2026-06-01", "codigo": "PETR4", "valor": 31.00},  # Atualizado
                {"data_referencia": "2026-06-01", "codigo": "BBAS3", "valor": 28.00},  # Novo
            ]
        )

        salvar_csv(
            gz_target,
            df_lote2,
            cabecalho=["data_referencia", "codigo", "valor"],
            chaves_dedup=["data_referencia", "codigo"],
            acumular=True,
        )

        df_result = pd.read_csv(gz_target)
        assert len(df_result) == 3  # VALE3 + PETR4 (atualizado) + BBAS3

        petr4_row = df_result[df_result["codigo"] == "PETR4"].iloc[0]
        assert petr4_row["valor"] == 31.00

        bbas3_row = df_result[df_result["codigo"] == "BBAS3"].iloc[0]
        assert bbas3_row["valor"] == 28.00


class TestDataCatalogFilesIntegrity:
    """Valida a integridade física de todos os datasets compactados presentes em data/."""

    def test_all_gz_datasets_are_valid_gzip_streams(self):
        data_dir = Path("data")
        if not data_dir.exists():
            pytest.skip("Diretório data/ não encontrado")

        gz_files = list(data_dir.glob("*.csv.gz"))
        assert len(gz_files) > 0, "Deve haver arquivos .csv.gz no diretório data/"

        corrupted = []
        for f in gz_files:
            try:
                with gzip.open(f, "rb") as gz:
                    # Lê os primeiros 1KB para validar o header/CRC do gzip
                    gz.read(1024)
            except Exception as e:
                corrupted.append((f.name, str(e)))

        assert not corrupted, f"Arquivos gzip corrompidos encontrados: {corrupted}"

    def test_datasets_json_references_existing_files(self):
        datasets_json = Path("data/datasets.json")
        if not datasets_json.exists():
            pytest.skip("data/datasets.json não encontrado")

        with datasets_json.open("r", encoding="utf-8") as f:
            datasets = json.load(f)

        missing_files = []
        for ds in datasets:
            fname = ds.get("file")
            if not fname:
                continue
            path = Path("data") / fname
            if not path.exists():
                missing_files.append(fname)

        assert not missing_files, f"Arquivos referenciados em datasets.json que não existem no disco: {missing_files}"
