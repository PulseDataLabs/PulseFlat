#!/usr/bin/env python
# coding: utf-8
"""
tests/test_alerta_debentures.py
-------------------------------
Testes unitários e de integração para scripts/alerta_debentures.py.
"""

import json
import sys
from datetime import datetime as real_datetime
from pathlib import Path
from unittest.mock import patch

import pytest
import requests_mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scripts.alerta_debentures as ad

# Mocks de HTML que representam respostas reais do portal debentures.com.br

MOCK_HTML_EMPTY = """
<!DOCTYPE html>
<html>
<head><title>Preços de Negociação - Resultado</title></head>
<body>
  <table>
    <tr><td>Preços Unitários</td></tr>
  </table>
  <!-- Tabela 3: mensagem de sem dados e tabelas extras -->
  <table>
    <tr>
      <td>Preços Unitários</td>
      <td>Data</td>
      <td>Emissor</td>
      <td>Ativo</td>
      <td>ISIN</td>
      <td>Qtd.</td>
      <td>Neg.</td>
      <td>Mínimo</td>
      <td>Médio</td>
      <td>Máximo</td>
      <td>%PU</td>
      <td>da Curva</td>
      <td>Não existe resposta para os itens selecionados.</td>
      <td>Nova Consulta?</td>
    </tr>
  </table>
</body>
</html>
"""

MOCK_HTML_SUCCESS = """
<!DOCTYPE html>
<html>
<head><title>Preços de Negociação - Resultado</title></head>
<body>
  <table>
    <tr>
      <td>Data</td><td></td><td>Emissor</td><td></td><td>Ativo</td><td></td><td>ISIN</td>
      <td></td><td>Qtd.</td><td></td><td>Neg.</td><td></td><td>Mínimo</td><td></td>
      <td>Médio</td><td></td><td>Máximo</td><td></td><td>%PUda Curva</td><td></td>
    </tr>
    <tr>
      <td>02/06/2026</td><td></td><td>BRK AMBI_</td><td></td><td>ABRK11</td><td></td><td>BRABRKDBS008</td>
      <td></td><td>2.400</td><td></td><td>10</td><td></td><td>1.033,055045</td><td></td>
      <td>1.033,075707</td><td></td><td>1.033,096368</td><td></td><td>ND</td><td></td>
    </tr>
  </table>
</body>
</html>
"""

MOCK_HTML_FORM_ONLY = """
<!DOCTYPE html>
<html>
<head><title>Preços de Negociação - Consulta</title></head>
<body>
  <form method="post" action="precosdenegociacao_r.asp">
    <table>
      <tr>
        <td>Filtro de Consulta:</td>
      </tr>
      <tr>
        <td>Ativo: <input type="text" name="ativo" /></td>
      </tr>
      <tr>
        <td>Data Inicial: <input type="text" name="dt_ini" /></td>
      </tr>
    </table>
  </form>
</body>
</html>
"""


# Mock do datetime para congelar o fuso e a data
class MockDatetime:
    @classmethod
    def now(cls, tz=None):
        # Congela em 16/07/2026 às 09:30:00
        dt = real_datetime(2026, 7, 16, 9, 30, 0)
        if tz:
            return tz.localize(dt) if hasattr(tz, 'localize') else dt.replace(tzinfo=tz)
        return dt


# ── Testes Unitários de verificar_dados ──────────────────────────────────────

def test_verificar_dados_empty():
    """Deve identificar que não há dados no HTML com mensagem de erro clássica."""
    assert ad.verificar_dados(MOCK_HTML_EMPTY) is False


def test_verificar_dados_success():
    """Deve identificar que há dados quando houver uma linha de negociação válida."""
    assert ad.verificar_dados(MOCK_HTML_SUCCESS) is True


def test_verificar_dados_form_only():
    """Deve identificar que não há dados em um formulário vazio (sem mensagem de erro mas sem dados)."""
    assert ad.verificar_dados(MOCK_HTML_FORM_ONLY) is False


# ── Testes de Fluxo Principal (main) ─────────────────────────────────────────

def test_main_already_notified(tmp_path, monkeypatch):
    """Se a última notificação já foi enviada hoje, deve encerrar imediatamente sem chamadas HTTP."""
    # Redireciona o arquivo de estado para um arquivo temporário
    temp_state = tmp_path / "debentures_alert_state.json"
    temp_state.write_text(json.dumps({"ultima_notificacao": "2026-07-16"}), encoding="utf-8")
    monkeypatch.setattr(ad, "STATE_FILE_PATH", temp_state)
    
    # Congela a data do sistema para hoje (16/07/2026)
    monkeypatch.setattr(ad, "datetime", MockDatetime)
    
    # Executa main e verifica que encerra com sys.exit(0) sem erros
    with pytest.raises(SystemExit) as exc_info:
        ad.main()
    
    assert exc_info.value.code == 0


@patch("scripts.alerta_debentures.send_telegram")
@patch("scripts.alerta_debentures.send_email")
@patch("scripts.alerta_debentures.send_power_automate")
def test_main_not_available(mock_pa, mock_email, mock_tg, tmp_path, monkeypatch, requests_mock):
    """Se dados estiverem indisponíveis no site, encerra sem notificar e sem atualizar o arquivo de estado."""
    temp_state = tmp_path / "debentures_alert_state.json"
    monkeypatch.setattr(ad, "STATE_FILE_PATH", temp_state)
    monkeypatch.setattr(ad, "datetime", MockDatetime)
    
    # Moca as requisições HTTP para retornar o HTML sem dados
    requests_mock.get("https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_f.asp", status_code=200)
    requests_mock.post("https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_r.asp", text=MOCK_HTML_EMPTY, status_code=200)
    
    with pytest.raises(SystemExit) as exc_info:
        ad.main()
        
    assert exc_info.value.code == 0
    
    # Garante que nenhuma notificação foi disparada
    mock_tg.assert_not_called()
    mock_email.assert_not_called()
    mock_pa.assert_not_called()
    
    # Garante que o arquivo de estado não foi gravado ou está vazio
    assert not temp_state.exists()


@patch("scripts.alerta_debentures.send_telegram")
@patch("scripts.alerta_debentures.send_email")
@patch("scripts.alerta_debentures.send_power_automate")
def test_main_success(mock_pa, mock_email, mock_tg, tmp_path, monkeypatch, requests_mock):
    """Se dados estiverem disponíveis, envia notificações e atualiza arquivo de estado."""
    temp_state = tmp_path / "debentures_alert_state.json"
    monkeypatch.setattr(ad, "STATE_FILE_PATH", temp_state)
    monkeypatch.setattr(ad, "datetime", MockDatetime)
    
    # Define as variáveis de ambiente necessárias para habilitar o envio
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-tg-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "fake-tg-chat")
    monkeypatch.setenv("POWER_AUTOMATE_WEBHOOK_URL", "https://fake-pa-webhook")
    monkeypatch.setenv("SMTP_SERVER", "smtp.fake.com")
    monkeypatch.setenv("SMTP_USER", "user@fake.com")
    monkeypatch.setenv("SMTP_PASSWORD", "password123")
    
    # Moca as requisições HTTP para retornar o HTML de sucesso
    requests_mock.get("https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_f.asp", status_code=200)
    requests_mock.post("https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_r.asp", text=MOCK_HTML_SUCCESS, status_code=200)
    
    with pytest.raises(SystemExit) as exc_info:
        ad.main()
        
    assert exc_info.value.code == 0
    
    # Verifica se notificações foram enviadas
    mock_tg.assert_called_once()
    mock_pa.assert_called_once()
    mock_email.assert_called_once()
    
    # Verifica se o estado de notificações foi gravado indicando o dia de hoje
    assert temp_state.exists()
    with temp_state.open("r", encoding="utf-8") as f:
        state = json.load(f)
    assert state.get("ultima_notificacao") == "2026-07-16"


def test_verificar_dados_real_queries():
    """Teste de integração real que realiza consultas diretas ao portal debentures.com.br
    para validar o comportamento com dados históricos (passados) e dados futuros (vazio).
    """
    import requests
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    })
    
    f_url = "https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_f.asp"
    r_url = "https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_r.asp"
    
    try:
        session.get(f_url, timeout=30)
    except Exception as e:
        pytest.skip(f"Portal debentures.com.br indisponível no momento: {e}")
        
    # 1. Consulta com dados (data passada conhecida: 01/06/2026 a 02/06/2026)
    post_data_past = {
        "op_exc": "False",
        "emissor": "",
        "ativo": "",
        "ISIN": "",
        "dt_ini": "01/06/2026",
        "dt_fim": "02/06/2026",
        "Submit32.x": "38",
        "Submit32.y": "16"
    }
    try:
        resp_past = session.post(r_url, data=post_data_past, headers={"Referer": f_url}, timeout=30)
        assert resp_past.status_code == 200
        assert ad.verificar_dados(resp_past.text) is True
    except Exception as e:
        pytest.fail(f"Falha na consulta real com dados históricos: {e}")

    # 2. Consulta sem dados (domingo passado conhecido: 12/07/2026)
    post_data_sunday = {
        "op_exc": "False",
        "emissor": "",
        "ativo": "",
        "ISIN": "",
        "dt_ini": "12/07/2026",
        "dt_fim": "12/07/2026",
        "Submit32.x": "38",
        "Submit32.y": "16"
    }
    try:
        resp_sunday = session.post(r_url, data=post_data_sunday, headers={"Referer": f_url}, timeout=30)
        assert resp_sunday.status_code == 200
        assert ad.verificar_dados(resp_sunday.text) is False
    except Exception as e:
        pytest.fail(f"Falha na consulta real com domingo sem dados: {e}")


