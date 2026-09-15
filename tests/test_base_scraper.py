"""
tests/test_base_scraper.py
---------------------------
Testes unitários da classe BaseScraper para garantir a correta sanitização de dados,
normalização de datas brasileiras e conversão de formatos decimais nacionais.
"""

import sys
from pathlib import Path

import pandas as pd

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


def test_large_datasets_compression_configured():
    """Garante que todos os datasets de grande porte (> 5 MB) estejam configurados com compress=True."""
    from scrapers.anbima_debentures import AnbimaDebenturesScraper
    from scrapers.b3_carteiras_teoricas import B3CarteirasTeoricasScraper
    from scrapers.b3_opcoes_posicoes_resumo import B3OpcoesPosicoesResumoScraper
    from scrapers.bacen_balancetes_bancos import BacenBalancetesBancosScraper
    from scrapers.bacen_cadastro_instituicoes import BacenCadastroInstituicoesScraper
    from scrapers.debentures_emissoes_caracteristicas import (
        DebenturesEmissoesCaracteristicasScraper,
    )
    from scrapers.yahoo_acoes_brasileiras import YahooAcoesBrasileirasScraper
    from scrapers.yahoo_etfs import YahooEtfsScraper
    from scrapers.yahoo_fiis_fiagros import YahooFiisFiagrosScraper

    scrapers = [
        AnbimaDebenturesScraper(),
        B3CarteirasTeoricasScraper(),
        B3OpcoesPosicoesResumoScraper(),
        BacenBalancetesBancosScraper(),
        BacenCadastroInstituicoesScraper(),
        DebenturesEmissoesCaracteristicasScraper(),
        YahooAcoesBrasileirasScraper(),
        YahooEtfsScraper(),
        YahooFiisFiagrosScraper(),
    ]

    for s in scrapers:
        assert s.compress is True, f"{s.name} deve possuir compress=True"
        assert s.output_file.name.endswith(".csv.gz"), f"{s.name} deve salvar em .csv.gz"
        assert s.output_file.exists(), f"Arquivo compactado {s.output_file} deve existir no disco"


def test_anbima_debentures_numeric_types_and_cleaning(monkeypatch):
    """Garante que campos numéricos de debêntures ANBIMA sejam convertidos para float e limpos de sentinelas como '--' e 'N/D'."""
    from datetime import date

    from scrapers.anbima_debentures import AnbimaDebenturesScraper

    raw_anbima_data = """HEADER LINE 1
HEADER LINE 2
HEADER LINE 3
AALM12@AURA ALMAS@2030-10-02@DI + 1.6%@0,8503@0,5404@0,6834@0,0541@0,6293@0,7376@1046,357089@102,0904@576,72@@
AALR13@CENTRO DIAG@2027-10-04@DI + 2.75%@--@--@--@--@--@--@N/D@N/D@N/D@@
"""

    class DummyResp:
        content = raw_anbima_data.encode("latin-1")
        status_code = 200
        def raise_for_status(self):
            pass

    class DummySession:
        def get(self, *args, **kwargs):
            return DummyResp()

    monkeypatch.setattr("scrapers.anbima_debentures.nova_session", lambda: DummySession())

    scraper = AnbimaDebenturesScraper()
    scraper.target_date = date(2026, 6, 3)
    df = scraper.fetch()

    assert not df.empty
    assert len(df) == 2

    # Verifica se as colunas numéricas foram convertidas para float
    numeric_cols = [
        "tx_compra",
        "tx_venda",
        "tx_indicativa",
        "desvio_padrao",
        "intervalo_indicativo_min",
        "intervalo_indicativo_max",
        "pu",
        "ratio_pu_par_vne",
        "duration",
    ]
    for col in numeric_cols:
        assert pd.api.types.is_float_dtype(df[col]), f"{col} deve ser float64"

    # Linha 0 deve ter valores float válidos
    assert df.loc[0, "tx_compra"] == 0.8503
    assert df.loc[0, "tx_venda"] == 0.5404
    assert df.loc[0, "tx_indicativa"] == 0.6834
    assert df.loc[0, "pu"] == 1046.357089
    assert df.loc[0, "ratio_pu_par_vne"] == 102.0904

    # Linha 1 (com '--' e 'N/D') deve ter virado NaN e não string literal
    assert pd.isna(df.loc[1, "tx_compra"])
    assert pd.isna(df.loc[1, "pu"])


def test_schema_generator_financial_type_inference(tmp_path):
    """Garante que salvar_csv infere corretamente tipos numéricos de métricas financeiras (taxas, variacao, peso, pmr, numero_indice)."""
    import json

    from utils.base import salvar_csv

    df = pd.DataFrame([
        {
            "data_referencia": "2026-06-01",
            "numero_indice": 11504.40986,
            "variacao_diaria": -0.0693,
            "peso_geral": 23.87,
            "pmr": 2943.0685,
            "convexidade": 78.3488,
            "tx_indicativa": 14.5669,
            "pu": 985.5354,
            "duration": 576.72,
            "codigo": "PETR4",
        }
    ])

    test_file = tmp_path / "test_metrics.csv"
    salvar_csv(
        test_file,
        df,
        cabecalho=list(df.columns),
        chaves_dedup=["data_referencia", "codigo"],
    )

    schemas_file = tmp_path / "schemas.json"
    assert schemas_file.exists()

    with schemas_file.open("r", encoding="utf-8") as f:
        schemas = json.load(f)

    fields = {f["name"]: f["type"] for f in schemas[0]["fields"]}

    assert fields["numero_indice"] == "float"
    assert fields["variacao_diaria"] == "float"
    assert fields["peso_geral"] == "float"
    assert fields["pmr"] == "float"
    assert fields["convexidade"] == "float"
    assert fields["tx_indicativa"] == "float"
    assert fields["pu"] == "float"
    assert fields["duration"] == "float"
    assert fields["codigo"] == "str"
    assert fields["data_referencia"] == "date"



