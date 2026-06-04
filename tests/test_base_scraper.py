"""
tests/test_base_scraper.py
---------------------------
Testes unitários da classe BaseScraper para garantir a correta sanitização de dados,
normalização de datas brasileiras e conversão de formatos decimais nacionais.
"""

import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.base import BaseScraper


def test_base_scraper_data_sanitization(tmp_path):
    """Deve normalizar datas no padrão brasileiro e converter números com vírgula para ponto."""
    class DummyScraper(BaseScraper):
        name = "dummy_test_scraper"
        accumulate = False
        chaves_dedup = None

        def fetch(self) -> pd.DataFrame:
            dados = [
                {
                    "data_br": "26/09/2016",
                    "data_br_curta": "26/09/16",
                    "numero_br": "5,3656",
                    "numero_br_grande": "1.234,56",
                    "valor_com_porcentagem": "12,5%",
                    "sem_alteracao": "texto normal",
                    "nulo": None,
                }
            ]
            return pd.DataFrame(dados)

    scraper = DummyScraper()
    # Redireciona o arquivo de saída para um diretório temporário de testes
    scraper.output_file = tmp_path / "dummy_test_scraper.csv"

    # Executa o scraper dummy
    scraper.run()

    # Verifica se o arquivo foi gerado
    assert scraper.output_file.exists()

    # Lê os dados do arquivo gerado para verificar a normalização
    import csv
    with scraper.output_file.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        registros = list(reader)

    assert len(registros) == 1
    reg = registros[0]

    # 1. Validação de datas
    assert reg["data_br"] == "2016-09-26"
    assert reg["data_br_curta"] == "2016-09-26"

    # 2. Validação de números BR
    assert reg["numero_br"] == "5.3656"
    assert reg["numero_br_grande"] == "1234.56"
    assert reg["valor_com_porcentagem"] == "12.5%"

    # 3. Validação de outros valores
    assert reg["sem_alteracao"] == "texto normal"
    assert reg["nulo"] == ""

    # 4. Inserção automática de data_captura
    assert "data_captura" in reg
    assert len(reg["data_captura"]) == 10  # formato YYYY-MM-DD


def test_base_scraper_datetime_conversion(tmp_path):
    """Deve converter colunas do tipo datetime64 do Pandas para string no formato YYYY-MM-DD."""
    class DatetimeDummyScraper(BaseScraper):
        name = "datetime_dummy_scraper"
        accumulate = False

        def fetch(self) -> pd.DataFrame:
            df = pd.DataFrame([{"data_referencia": pd.Timestamp("2026-06-04")}])
            # Força o tipo datetime64 na coluna
            df["data_referencia"] = pd.to_datetime(df["data_referencia"])
            return df

    scraper = DatetimeDummyScraper()
    scraper.output_file = tmp_path / "datetime_dummy.csv"
    scraper.run()

    import csv
    with scraper.output_file.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        registros = list(reader)

    assert registros[0]["data_referencia"] == "2026-06-04"


def test_base_scraper_run_empty_dataframe(tmp_path, caplog):
    """Deve registrar um alerta e não salvar arquivos caso o DataFrame retornado seja vazio."""
    class EmptyDummyScraper(BaseScraper):
        name = "empty_dummy_scraper"
        accumulate = False

        def fetch(self) -> pd.DataFrame:
            return pd.DataFrame()

    scraper = EmptyDummyScraper()
    scraper.output_file = tmp_path / "empty_dummy.csv"

    # Executa e verifica se não salvou arquivo
    scraper.run()
    assert not scraper.output_file.exists()
