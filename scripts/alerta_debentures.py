#!/usr/bin/env python
# coding: utf-8
"""
PulseFlat – Script de monitoramento e alertas para debêntures do mercado secundário.
Busca dados de preços de negociação e notifica via E-mail, Telegram e Power Automate.
Usa um arquivo JSON de estado local para rastrear as notificações enviadas diariamente.
"""

import json
import os
import re
import sys
import smtplib
from datetime import date, datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests
from dotenv import load_dotenv

load_dotenv()

# Garante que o diretório raiz esteja no path para importar utils/scrapers
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, nova_session
from utils.parsers import _CAL
from utils.base import FUSO

log = get_logger("alerta_debentures")

STATE_FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "debentures_alert_state.json"


def send_telegram(token: str, chat_id: str, text: str):
    """Envia mensagem para o Telegram."""
    log.info("Disparando notificação via Telegram...")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        log.info("Telegram notificado com sucesso.")
    except Exception as e:
        log.error(f"Erro ao notificar Telegram: {e}")


def send_email(server: str, port: str, user: str, password: str, from_email: str, to_email: str, subject: str, html_content: str):
    """Envia e-mail via SMTP com suporte a STARTTLS e SSL."""
    log.info("Disparando notificação via E-mail...")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))

    try:
        p = int(port)
        if p == 465:
            with smtplib.SMTP_SSL(server, p, timeout=15) as s:
                s.login(user, password)
                s.sendmail(from_email, to_email, msg.as_string())
        else:
            with smtplib.SMTP(server, p, timeout=15) as s:
                s.starttls()
                s.login(user, password)
                s.sendmail(from_email, to_email, msg.as_string())
        log.info("E-mail enviado com sucesso.")
    except Exception as e:
        log.error(f"Erro ao enviar e-mail via SMTP: {e}")


def send_power_automate(url: str, title: str, message: str):
    """Envia card adaptativo para o Power Automate."""
    log.info("Disparando card adaptativo para o Power Automate...")
    adaptive_card = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": title,
                            "weight": "Bolder",
                            "size": "Medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": message,
                            "wrap": True
                        }
                    ],
                    "schema": "http://adaptivecards.io/schemas/adaptive-card.json"
                }
            }
        ]
    }
    try:
        r = requests.post(url, json=adaptive_card, timeout=15)
        r.raise_for_status()
        log.info("Power Automate notificado com sucesso.")
    except Exception as e:
        log.error(f"Erro ao enviar webhook para o Power Automate: {e}")


def verificar_dados(html: str) -> bool:
    """
    Avalia se existem dados disponíveis na página HTML do portal de debêntures.
    Retorna True se houver dados de negociação válidos, False caso contrário.
    """
    # 1. Verifica textos explícitos de ausência de dados
    texto_sem_dados = re.compile(
        r"nenhum\s+registro|"
        r"nenhuma\s+informa|"
        r"n[aã]o\s+foram\s+encontrados|"
        r"n[aã]o\s+existe\s+resposta",
        re.IGNORECASE
    )
    if texto_sem_dados.search(html):
        return False

    # 2. Verifica estrutura da tabela com BeautifulSoup
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all("tr")
        
        date_pattern = re.compile(r"^\d{2}/\d{2}/\d{4}$")
        isin_pattern = re.compile(r"^[A-Z]{2}[A-Z0-9]{10}$", re.IGNORECASE)
        
        for row in rows:
            cells = row.find_all(["td", "th"])
            # Remove células vazias/espaçadoras
            non_empty_texts = [text for c in cells if (text := c.get_text(strip=True))]
            if len(non_empty_texts) >= 4:
                # O primeiro campo deve ser uma data (Data) e o quarto deve ser o ISIN
                if date_pattern.match(non_empty_texts[0]) and isin_pattern.match(non_empty_texts[3]):
                    return True
    except Exception as e:
        log.warning(f"Erro ao analisar HTML com BeautifulSoup: {e}. Usando fallback.")

    # 3. Fallback heurístico simples caso falhe o parsing
    linhas_tabela = len(re.findall(r"<tr[^>]*>", html, re.IGNORECASE))
    return linhas_tabela > 3


def main():
    hoje = datetime.now(FUSO).date()
    hoje_iso = hoje.strftime("%Y-%m-%d")
    
    # 1. Determina a data de referência esperada (último dia útil)
    ref_date = _CAL.offset(hoje, -1)
    ref_date_str = ref_date.strftime("%d/%m/%Y")
    log.info(f"Hoje: {hoje.strftime('%d/%m/%Y')} (ISO: {hoje_iso}) | Data Ref Esperada: {ref_date_str}")

    # 2. Carrega o estado de notificações e verifica se já notificado hoje
    state_path = STATE_FILE_PATH
    state = {"ultima_notificacao": ""}
    
    if state_path.exists():
        try:
            with state_path.open("r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception as e:
            log.warning(f"Erro ao ler arquivo de estado: {e}. Criando novo estado.")

    if state.get("ultima_notificacao", "").startswith(hoje_iso):
        log.info(f"Notificação diária para {hoje_iso} já foi enviada hoje. Encerrando.")
        sys.exit(0)

    # 3. Consulta o site debentures.com.br
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    })

    f_url = "https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_f.asp"
    r_url = "https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_r.asp"

    try:
        log.info("Estabelecendo sessão no portal debentures.com.br...")
        session.get(f_url, timeout=30)
    except Exception as e:
        log.error(f"Erro ao obter sessão inicial: {e}")
        sys.exit(1)

    post_data = {
        "op_exc": "False",
        "emissor": "",
        "ativo": "",
        "ISIN": "",
        "dt_ini": ref_date_str,
        "dt_fim": hoje.strftime("%d/%m/%Y"),
        "Submit32.x": "38",
        "Submit32.y": "16"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f_url
    }

    try:
        log.info(f"Consultando dados de {ref_date_str} a {post_data['dt_fim']}...")
        resp = session.post(r_url, data=post_data, headers=headers, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        log.error(f"Erro ao realizar consulta POST: {e}")
        sys.exit(1)

    html = resp.text
    
    # 4. Avalia se existem dados disponíveis usando a heurística aprimorada
    tem_dados = verificar_dados(html)
    
    if not tem_dados:
        log.info("Dados ainda indisponíveis na ANBIMA. Encerrando e aguardando próxima checagem.")
        sys.exit(0)

    log.info("=== DADOS DISPONÍVEIS DETECTADOS! ===")

    # 5. Disparar notificações
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat = os.getenv("TELEGRAM_CHAT_ID", "8054664211")
    if telegram_token and telegram_chat:
        tg_text = f"<b>Debêntures - Disponível</b>\nArquivo de Negociação Disponível - Data de referência: {ref_date_str}"
        send_telegram(telegram_token, telegram_chat, tg_text)

    power_automate_url = os.getenv("POWER_AUTOMATE_WEBHOOK_URL")
    if power_automate_url:
        send_power_automate(
            url=power_automate_url,
            title="Debêntures.com.br - Preços de negociação",
            message=f"Dados disponíveis para captura. Data de referência: {ref_date_str}"
        )

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT", "587")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM", "royopa@gmail.com")
    smtp_to = os.getenv("SMTP_TO", "gerat05@caixa.gov.br")

    if smtp_server and smtp_user and smtp_pass:
        email_subject = os.getenv("SMTP_SUBJECT", "Debêntures - Disponível")
        email_subject = email_subject.replace("{data}", ref_date_str).replace("{dt_ini}", ref_date_str)
        
        download_date_str = hoje.strftime("%Y%m%d")
        download_url = f"https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_e.asp?op_exc=Nada&emissor=&isin=&ativo=&dt_ini=20250101&dt_fim={download_date_str}"
        page_url = "https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_f.asp"
        
        email_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; border-radius: 8px; padding: 24px; background-color: #ffffff; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <h2 style="color: #0078d4; margin-top: 0;">⚡ Debêntures — Arquivo Disponível</h2>
                <p>Os preços de negociação de debêntures no mercado secundário da ANBIMA já estão liberados para consulta e download.</p>
                
                <div style="background-color: #f3f2f1; padding: 12px 16px; border-radius: 4px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 14px;"><b>Data de Referência:</b> {ref_date_str}</p>
                </div>
                
                <p>Você pode baixar os dados consolidados (acumulados desde 01/01/2025) ou acessar a página de consulta:</p>
                
                <div style="margin: 24px 0; text-align: left;">
                    <a href="{download_url}" style="background-color: #0078d4; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 4px; font-weight: bold; font-size: 14px; display: inline-block; box-shadow: 0 2px 4px rgba(0, 120, 212, 0.2);">
                        Baixar Arquivo CSV
                    </a>
                    <a href="{page_url}" style="color: #0078d4; text-decoration: none; font-weight: 600; font-size: 14px; margin-left: 20px; display: inline-block; vertical-align: middle;">
                        Acessar Portal ANBIMA ↗
                    </a>
                </div>
                
                <hr style="border: none; border-top: 1px solid #eaeaea; margin: 24px 0;" />
                <p style="font-size: 11px; color: #888888; margin: 0;">Este é um alerta automático enviado pelo pipeline de dados PulseFlat.</p>
            </div>
        </body>
        </html>
        """
        send_email(smtp_server, smtp_port, smtp_user, smtp_pass, smtp_from, smtp_to, email_subject, email_html)
    else:
        log.warning("Credenciais de SMTP incompletas. Notificação por E-mail não enviada.")

    # 6. Grava a data de hoje no JSON de estado para evitar duplicidade de notificações
    log.info("Atualizando arquivo de estado...")
    state["ultima_notificacao"] = datetime.now(FUSO).strftime("%Y-%m-%d %H:%M:%S")
    try:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        with state_path.open("w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        log.info(f"Estado de notificações atualizado para {hoje_iso}.")
    except Exception as e:
        log.error(f"Erro ao salvar arquivo de estado: {e}")

    sys.exit(0)


if __name__ == "__main__":
    from utils.base import acquire_lock
    try:
        with acquire_lock("pulseflat", blocking=False):
            main()
    except RuntimeError as e:
        log.warning(f"Abortando alerta de debêntures: {e}")
        sys.exit(0)

