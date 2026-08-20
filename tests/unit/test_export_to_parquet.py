import gzip

import pandas as pd

from scripts.export_to_parquet import exportar_dataset


class TestExportToParquet:
    """Testes defensivos para exportação de dados CSV/GZ para Parquet."""

    def test_exportar_csv_simples(self, tmp_path):
        csv_file = tmp_path / "teste_dados.csv"
        df_orig = pd.DataFrame(
            {
                "data_referencia": ["2026-01-01", "2026-01-02"],
                "valor": ["10.50", "20.30"],
                "codigo": ["PETR4", "VALE3"],
            }
        )
        df_orig.to_csv(csv_file, index=False)

        out_dir = tmp_path / "parquet"
        out_dir.mkdir()

        ok, linhas, tamanho, elapsed = exportar_dataset(
            caminho_csv=csv_file,
            output_dir=out_dir,
            compression="snappy",
            dry_run=False,
        )

        assert ok is True
        assert linhas == 2
        assert tamanho > 0
        assert elapsed >= 0.0

        parquet_file = out_dir / "teste_dados.parquet"
        assert parquet_file.exists()

        df_read = pd.read_parquet(parquet_file)
        assert len(df_read) == 2
        assert "data_referencia" in df_read.columns
        assert list(df_read["codigo"]) == ["PETR4", "VALE3"]

    def test_exportar_csv_gz(self, tmp_path):
        gz_file = tmp_path / "teste_historico.csv.gz"
        df_orig = pd.DataFrame(
            {
                "data_captura": ["2026-05-01", "2026-05-02"],
                "taxa": ["13.75", "13.65"],
            }
        )
        with gzip.open(gz_file, "wt", encoding="utf-8") as f:
            df_orig.to_csv(f, index=False)

        out_dir = tmp_path / "parquet_gz"
        out_dir.mkdir()

        ok, linhas, tamanho, _ = exportar_dataset(
            caminho_csv=gz_file,
            output_dir=out_dir,
            compression="zstd",
            dry_run=False,
        )

        assert ok is True
        assert linhas == 2
        parquet_file = out_dir / "teste_historico.parquet"
        assert parquet_file.exists()

    def test_exportar_csv_vazio(self, tmp_path):
        empty_csv = tmp_path / "vazio.csv"
        empty_csv.write_text("")

        out_dir = tmp_path / "out"
        out_dir.mkdir()

        ok, linhas, _, _ = exportar_dataset(
            caminho_csv=empty_csv,
            output_dir=out_dir,
            compression="snappy",
            dry_run=False,
        )

        assert ok is False
        assert linhas == 0

    def test_dry_run_nao_cria_arquivo(self, tmp_path):
        csv_file = tmp_path / "dry_run.csv"
        df_orig = pd.DataFrame({"col1": ["A", "B"]})
        df_orig.to_csv(csv_file, index=False)

        out_dir = tmp_path / "out_dry"
        out_dir.mkdir()

        ok, linhas, tamanho, _ = exportar_dataset(
            caminho_csv=csv_file,
            output_dir=out_dir,
            compression="snappy",
            dry_run=True,
        )

        assert ok is True
        assert not (out_dir / "dry_run.parquet").exists()
