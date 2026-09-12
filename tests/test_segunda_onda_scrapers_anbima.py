"""
tests/test_segunda_onda_scrapers_anbima.py
------------------------------------------
Testes unitários para os 7 novos scrapers da 2ª onda da API ANBIMA Data:
- IDKA Resultados
- Projeções de Inflação
- Carteira Teórica IMA
- Carteira Teórica IDA
- Curvas de Juros Parâmetros Svensson
- Estimativa Selic Oficial
- REUNE Negociações
"""

import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.anbima_curvas_juros_parametros_svensson import (
    AnbimaCurvasJurosParametrosSvenssonScraper,
)
from scrapers.anbima_indices_carteira_teorica_ida import AnbimaIndicesCarteiraTeoricaIdaScraper
from scrapers.anbima_indices_carteira_teorica_ima import AnbimaIndicesCarteiraTeoricaImaScraper
from scrapers.anbima_indices_idka_resultados import AnbimaIndicesIdkaResultadosScraper
from scrapers.anbima_projecoes_inflacao import AnbimaProjecoesInflacaoScraper
from scrapers.anbima_reune_negociacoes import AnbimaReuneNegociacoesScraper
from scrapers.anbima_titulos_publicos_estimativa_selic import (
    AnbimaTitulosPublicosEstimativaSelicScraper,
)

SEGUNDA_ONDA_SCRAPERS = [
    (AnbimaIndicesIdkaResultadosScraper, "anbima_indices_idka_resultados"),
    (AnbimaProjecoesInflacaoScraper, "anbima_projecoes_inflacao"),
    (AnbimaIndicesCarteiraTeoricaImaScraper, "anbima_indices_carteira_teorica_ima"),
    (AnbimaIndicesCarteiraTeoricaIdaScraper, "anbima_indices_carteira_teorica_ida"),
    (AnbimaCurvasJurosParametrosSvenssonScraper, "anbima_curvas_juros_parametros_svensson"),
    (AnbimaTitulosPublicosEstimativaSelicScraper, "anbima_titulos_publicos_estimativa_selic"),
    (AnbimaReuneNegociacoesScraper, "anbima_reune_negociacoes"),
]


@pytest.mark.parametrize("cls,expected_name", SEGUNDA_ONDA_SCRAPERS)
def test_metadata_segunda_onda(cls, expected_name):
    inst = cls()
    assert inst.name == expected_name
    assert inst.group == "anbima"
    assert inst.enabled is True
    assert inst.accumulate is True
    assert inst.compress is True
    assert len(inst.chaves_dedup) >= 1
    assert "ANBIMA" in inst.title


def test_idka_fetch_mock(requests_mock):
    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    api_url = "https://api.anbima.com.br/feed/precos-indices/v1/indices/resultados-idka"

    requests_mock.post(
        oauth_url, json={"access_token": "mock_token", "expires_in": 3600}, status_code=200
    )
    requests_mock.get(
        api_url,
        json=[
            {
                "data_referencia": "2026-09-11",
                "nome": "IDkA Pré 2A",
                "numero_indice": 7500.123456,
                "tx_compra": 13.5,
                "tx_venda": 13.4,
                "variacao_diaria": 0.05,
                "variacao_mensal": 0.45,
                "variacao_anual": 9.8,
                "variacao_ult12m": 14.2,
                "volatilidade": 0.05,
            }
        ],
        status_code=200,
    )

    scraper = AnbimaIndicesIdkaResultadosScraper()
    scraper.target_date = date(2026, 9, 11)
    df = scraper.fetch()

    assert not df.empty
    assert len(df) == 1
    assert df.iloc[0]["nome"] == "IDkA Pré 2A"
    assert "registro_hash" in df.columns


def test_projecoes_fetch_mock(requests_mock):
    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    api_url = "https://api.anbima.com.br/feed/precos-indices/v1/debentures/projecoes"

    requests_mock.post(
        oauth_url, json={"access_token": "mock_token", "expires_in": 3600}, status_code=200
    )
    requests_mock.get(
        api_url,
        json=[
            {
                "indice": "IPCA",
                "tipo_projecao": "PROJEÇÕES PARA O MÊS CORRENTE",
                "data_coleta": "2026-09-11",
                "mes_referencia": "09/2026",
                "variacao_projetada": 0.42,
                "data_validade": "2026-09-12",
            }
        ],
        status_code=200,
    )

    scraper = AnbimaProjecoesInflacaoScraper()
    scraper.target_date = date(2026, 9, 11)
    df = scraper.fetch()

    assert not df.empty
    assert len(df) == 1
    assert df.iloc[0]["indice"] == "IPCA"
    assert df.iloc[0]["mes_referencia"] == "09/2026"
    assert "registro_hash" in df.columns


def test_selic_fetch_mock(requests_mock):
    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    api_url = "https://api.anbima.com.br/feed/precos-indices/v1/titulos-publicos/estimativa-selic"

    requests_mock.post(
        oauth_url, json={"access_token": "mock_token", "expires_in": 3600}, status_code=200
    )
    requests_mock.get(
        api_url,
        json=[
            {
                "data_referencia": "2026-09-11",
                "estimativa_taxa_selic": 13.9,
            }
        ],
        status_code=200,
    )

    scraper = AnbimaTitulosPublicosEstimativaSelicScraper()
    scraper.target_date = date(2026, 9, 11)
    df = scraper.fetch()

    assert not df.empty
    assert len(df) == 1
    assert df.iloc[0]["estimativa_taxa_selic"] == "13.9"
    assert "registro_hash" in df.columns
