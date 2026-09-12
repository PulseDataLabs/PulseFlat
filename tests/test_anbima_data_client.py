"""
tests/test_anbima_data_client.py
--------------------------------
Testes unitários para o AnbimaDataClient e BaseAnbimaDataScraper.
"""

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from scrapers.utils.anbima_data_client import (
    AnbimaAuthError,
    AnbimaDataClient,
    AnbimaMissingCredentialsError,
)


def test_client_missing_credentials():
    """Verifica comportamento quando as credenciais não são fornecidas."""
    client = AnbimaDataClient(client_id="", client_secret="")
    assert not client.has_credentials

    with pytest.raises(AnbimaMissingCredentialsError):
        client.get_access_token()

    diag = client.test_connection()
    assert diag["ok"] is False
    assert "Credenciais não encontradas" in diag["message"]


def test_client_get_access_token_success(requests_mock):
    """Testa obtenção bem-sucedida de token OAuth 2.0 via Client Credentials."""
    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    requests_mock.post(
        oauth_url,
        json={"access_token": "token_teste_12345", "expires_in": 3600, "token_type": "Bearer"},
        status_code=200,
    )

    client = AnbimaDataClient(
        client_id="meu_client_id",
        client_secret="meu_client_secret",
        oauth_url=oauth_url,
    )
    assert client.has_credentials

    token = client.get_access_token()
    assert token == "token_teste_12345"
    assert client._token == "token_teste_12345"

    history = requests_mock.request_history
    assert len(history) == 1
    assert "Basic " in history[0].headers["Authorization"]
    assert history[0].json() == {"grant_type": "client_credentials"}


def test_client_token_caching_and_expiration(requests_mock, monkeypatch):
    """Testa reutilização de token em cache e renovação após expiração."""
    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    requests_mock.post(
        oauth_url,
        json={"access_token": "token_valido", "expires_in": 3600},
        status_code=200,
    )

    client = AnbimaDataClient(client_id="id", client_secret="sec", oauth_url=oauth_url)

    # 1ª chamada -> faz POST no endpoint OAuth
    t1 = client.get_access_token()
    assert t1 == "token_valido"
    assert len(requests_mock.request_history) == 1

    # 2ª chamada logo em seguida -> deve usar cache sem nova requisição HTTP
    t2 = client.get_access_token()
    assert t2 == "token_valido"
    assert len(requests_mock.request_history) == 1

    # Simula o avanço do tempo para quando o token já estiver expirando
    client._token_expires_at = time.time() + 30  # Menos que o buffer de 60s
    requests_mock.post(
        oauth_url,
        json={"access_token": "novo_token_renovado", "expires_in": 3600},
        status_code=200,
    )

    t3 = client.get_access_token()
    assert t3 == "novo_token_renovado"
    assert len(requests_mock.request_history) == 2


def test_client_auth_error_on_invalid_credentials(requests_mock):
    """Testa tratamento de erro ao receber HTTP 401 ou 403 no endpoint OAuth."""
    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    requests_mock.post(
        oauth_url,
        text="Invalid client credentials",
        status_code=401,
    )

    client = AnbimaDataClient(client_id="errado", client_secret="errado", oauth_url=oauth_url)
    with pytest.raises(AnbimaAuthError) as exc_info:
        client.get_access_token()
    assert "Falha na autenticação ANBIMA (HTTP 401)" in str(exc_info.value)

    diag = client.test_connection()
    assert diag["ok"] is False
    assert "Falha na autenticação" in diag["message"]


def test_client_get_request(requests_mock):
    """Testa execução de GET autenticado com passagem correta de headers."""
    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    endpoint_url = "https://api.anbima.com.br/feed/precos-indices/v1/titulos"

    requests_mock.post(
        oauth_url,
        json={"access_token": "token_abc", "expires_in": 3600},
        status_code=200,
    )
    requests_mock.get(
        endpoint_url,
        json=[{"codigo": "LTN", "taxa": 12.5}],
        status_code=200,
    )

    client = AnbimaDataClient(
        client_id="id_123",
        client_secret="sec_123",
        oauth_url=oauth_url,
        base_url="https://api.anbima.com.br",
    )

    dados = client.get("/feed/precos-indices/v1/titulos")
    assert isinstance(dados, list)
    assert len(dados) == 1
    assert dados[0]["codigo"] == "LTN"

    req_history = requests_mock.request_history
    assert len(req_history) == 2
    api_req = req_history[1]
    assert api_req.headers["Authorization"] == "Bearer token_abc"
    assert api_req.headers["client_id"] == "id_123"


def test_client_rate_limit_retry(requests_mock, monkeypatch):
    """Testa retry automático em caso de rate-limiting HTTP 429."""
    monkeypatch.setattr(time, "sleep", lambda s: None)

    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    endpoint_url = "https://api.anbima.com.br/feed/test"

    requests_mock.post(
        oauth_url,
        json={"access_token": "tok", "expires_in": 3600},
        status_code=200,
    )
    # 1ª tentativa 429, 2ª tentativa 200
    requests_mock.get(
        endpoint_url,
        [
            {"text": "Rate limit exceeded", "status_code": 429},
            {"json": {"data": [{"id": 1}]}, "status_code": 200},
        ],
    )

    client = AnbimaDataClient(
        client_id="id", client_secret="sec", oauth_url=oauth_url, max_retries=2
    )
    resp = client.get("/feed/test")
    assert resp == {"data": [{"id": 1}]}


def test_base_anbima_scraper_extract_records():
    """Testa o extrator de registros em múltiplos envelopes da API ANBIMA."""
    scraper = BaseAnbimaDataScraper()

    # Formato lista direta
    assert scraper.extract_records([{"id": 1}, {"id": 2}]) == [{"id": 1}, {"id": 2}]

    # Formato envelopado com 'data'
    assert scraper.extract_records({"data": [{"id": 10}]}) == [{"id": 10}]

    # Formato envelopado com 'content'
    assert scraper.extract_records({"content": [{"id": 20}]}) == [{"id": 20}]

    # Formato envelopado com 'itens'
    assert scraper.extract_records({"itens": [{"id": 30}]}) == [{"id": 30}]

    # Dict único
    assert scraper.extract_records({"id": 40, "nome": "Item"}) == [{"id": 40, "nome": "Item"}]

    # Vazio / None
    assert scraper.extract_records(None) == []
    assert scraper.extract_records([]) == []


def test_base_anbima_scraper_fetch_endpoint(requests_mock):
    """Testa o fetch_endpoint do BaseAnbimaDataScraper."""
    oauth_url = "https://api.anbima.com.br/oauth/access-token"
    endpoint_url = "https://api.anbima.com.br/feed/exemplo"

    requests_mock.post(
        oauth_url,
        json={"access_token": "tok_base", "expires_in": 3600},
        status_code=200,
    )
    requests_mock.get(
        endpoint_url,
        json={"data": [{"codigo": "ABC", "valor": 100}]},
        status_code=200,
    )

    client = AnbimaDataClient(client_id="id", client_secret="sec", oauth_url=oauth_url)
    scraper = BaseAnbimaDataScraper(client=client)
    registros = scraper.fetch_endpoint("/feed/exemplo")

    assert len(registros) == 1
    assert registros[0]["codigo"] == "ABC"
