"""
ANBIMA Indicadores - Captura Automatizada
==========================================
Captura diariamente os indicadores da ANBIMA às 09h30
e salva em CSV para importação em base de dados.

Dependências:
    pip install requests beautifulsoup4 schedule

Uso:
    python anbima_indicadores.py                  # Roda o agendador contínuo
    python anbima_indicadores.py --agora          # Captura imediatamente (teste)
"""

import csv
import os
import re
import sys
import logging
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import schedule
import time

# ─────────────────────────────────────────────
# Configurações
# ─────────────────────────────────────────────
URL_ANBIMA       = "https://www.anbima.com.br/informacoes/indicadores/"
HORARIO_CAPTURA  = "09:30"
PASTA_SAIDA      = Path("./dados_anbima")
ARQUIVO_CSV      = PASTA_SAIDA / "indicadores_anbima.csv"
ARQUIVO_LOG      = PASTA_SAIDA / "anbima_captura.log"

CABECALHO_CSV = [
    "data_captura",
    "hora_captura",
    "data_referencia_pagina",
    "indicador",
    "categoria",
    "valor",
    "unidade",
]

# ─────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(ARQUIVO_LOG, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Funções de parsing
# ─────────────────────────────────────────────

def limpar_valor(texto: str) -> str:
    """Remove espaços, caracteres invisíveis e normaliza separadores."""
    if not texto:
        return ""
    texto = texto.strip().replace("\xa0", "").replace(",", ".")
    # Remove sufixos como "% a.a." que já ficam na coluna unidade
    texto = re.sub(r"[%\s]", "", texto)
    return texto


def extrair_data_referencia(soup: BeautifulSoup) -> str:
    """Extrai a data/hora da última atualização exibida na página."""
    texto = soup.get_text(" ", strip=True)
    match = re.search(r"(\d{2}/\d{2}/\d{4})\s*[-–]\s*(\d{2}:\d{2})", texto)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return "N/A"


def capturar_indicadores() -> list[dict]:
    """
    Acessa a página da ANBIMA e extrai todos os indicadores.
    Retorna uma lista de dicionários prontos para CSV.
    """
    log.info(f"Iniciando captura em {URL_ANBIMA}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        )
    }

    try:
        resp = requests.get(URL_ANBIMA, headers=headers, timeout=30)
        resp.encoding = "iso-8859-1"
        resp.raise_for_status()
    except requests.RequestException as e:
        log.error(f"Falha ao acessar a página: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    agora = datetime.now()
    data_captura     = agora.strftime("%Y-%m-%d")
    hora_captura     = agora.strftime("%H:%M:%S")
    data_referencia  = extrair_data_referencia(soup)

    texto_completo = soup.get_text(" ", strip=True)
    registros = []

    def reg(indicador, categoria, valor, unidade=""):
        return {
            "data_captura":           data_captura,
            "hora_captura":           hora_captura,
            "data_referencia_pagina": data_referencia,
            "indicador":              indicador,
            "categoria":              categoria,
            "valor":                  limpar_valor(valor),
            "unidade":                unidade,
        }

    # ── Taxas de Juros ──────────────────────────────────────────
    padroes_juros = [
        ("Estimativa SELIC",  r"Estimativa SELIC.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Taxa SELIC (BC)",   r"Taxa SELIC do BC.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("DI-B3",             r"DI-B3.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]
    for nome, padrao in padroes_juros:
        m = re.search(padrao, texto_completo, re.DOTALL)
        if m:
            registros.append(reg(nome, "Taxa de Juros", m.group(2), "% a.a."))

    # ── Índices de Preços ────────────────────────────────────────
    padroes_indices = [
        ("IGP-M Número Índice", r"IGP-M.*?Número Índice.*?(\d[\d\.,]+)"),
        ("IGP-M Var % mês",     r"IGP-M.*?Var % no m[eê]s.*?(-?\d+[\.,]\d+)"),
        ("IGP-M Projeção",      r"Projeção \(mar.*?\).*?(-?\d+[\.,]\d+)"),
        ("IPCA Número Índice",  r"IPCA.*?Número Índice.*?(\d[\d\.,]+)"),
        ("IPCA Var % mês",      r"IPCA.*?Var % no m[eê]s.*?(-?\d+[\.,]\d+)"),
        ("IPCA Projeção",       r"Projeção \(mar.*?\).*?(-?\d+[\.,]\d+)"),
    ]
    for nome, padrao in padroes_indices:
        m = re.search(padrao, texto_completo, re.DOTALL | re.IGNORECASE)
        if m:
            unidade = "%" if "Var" in nome or "Projeção" in nome else "índice"
            registros.append(reg(nome, "Índice de Preços", m.group(1), unidade))

    # ── Câmbio ───────────────────────────────────────────────────
    padroes_cambio = [
        ("Dólar Comercial Compra", r"Dolar Comercial Compra.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Dólar Comercial Venda",  r"Dólar Comercial Venda.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Euro Compra",            r"Euro Compra.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Euro Venda",             r"Euro Venda.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]
    for nome, padrao in padroes_cambio:
        m = re.search(padrao, texto_completo, re.DOTALL)
        if m:
            registros.append(reg(nome, "Câmbio", m.group(2), "R$"))

    # ── TR / TBF ─────────────────────────────────────────────────
    padroes_tr = [
        ("TR",  r"\bTR\b.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("TBF", r"\bTBF\b.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]
    for nome, padrao in padroes_tr:
        m = re.search(padrao, texto_completo, re.DOTALL)
        if m:
            registros.append(reg(nome, "Taxa de Referência", m.group(2), "% mês"))

    # ── FDS ──────────────────────────────────────────────────────
    fds_matches = re.findall(
        r"FDS.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)", texto_completo, re.DOTALL
    )
    for i, m in enumerate(fds_matches[:2], 1):
        registros.append(reg(f"FDS (registro {i})", "FDS", m[1], "R$ cota"))

    log.info(f"Total de indicadores capturados: {len(registros)}")
    return registros


# ─────────────────────────────────────────────
# Persistência em CSV
# ─────────────────────────────────────────────

def salvar_csv(registros: list[dict]) -> None:
    """
    Acrescenta os registros ao CSV acumulativo (append).
    Cria o arquivo com cabeçalho se ainda não existir.
    """
    if not registros:
        log.warning("Nenhum registro para salvar.")
        return

    novo_arquivo = not ARQUIVO_CSV.exists()

    with open(ARQUIVO_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO_CSV)
        if novo_arquivo:
            writer.writeheader()
        writer.writerows(registros)

    log.info(f"Dados salvos em: {ARQUIVO_CSV.resolve()}")


# ─────────────────────────────────────────────
# Rotina principal
# ─────────────────────────────────────────────

def executar_captura() -> None:
    log.info("=" * 50)
    log.info("Iniciando rotina de captura ANBIMA")
    registros = capturar_indicadores()
    salvar_csv(registros)
    log.info("Rotina concluída.")
    log.info("=" * 50)


def main() -> None:
    # Modo de teste: captura imediata
    if "--agora" in sys.argv:
        log.info("Modo --agora: executando captura imediata.")
        executar_captura()
        return

    # Modo agendado: roda todos os dias às 09h30
    log.info(f"Agendador iniciado. Captura programada para {HORARIO_CAPTURA} diariamente.")
    schedule.every().day.at(HORARIO_CAPTURA).do(executar_captura)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
