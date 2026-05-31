"""
ANBIMA Indicadores - Captura para GitHub Actions
=================================================
Captura os indicadores da ANBIMA e salva em CSV acumulativo no repositório.
Roda via GitHub Actions diariamente às 09h30 (horário de Brasília).
"""

import csv
import os
import re
import sys
import logging
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────
# Configurações
# ─────────────────────────────────────────────
URL_ANBIMA  = "https://www.anbima.com.br/informacoes/indicadores/"
PASTA_SAIDA = Path("./data")
ARQUIVO_CSV = PASTA_SAIDA / "indicadores_anbima.csv"
FUSO        = ZoneInfo("America/Sao_Paulo")

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
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Funções de parsing
# ─────────────────────────────────────────────

def limpar_valor(texto: str) -> str:
    if not texto:
        return ""
    texto = texto.strip().replace("\xa0", "").replace(",", ".")
    texto = re.sub(r"[%\s]", "", texto)
    return texto


def extrair_data_referencia(soup: BeautifulSoup) -> str:
    texto = soup.get_text(" ", strip=True)
    match = re.search(r"(\d{2}/\d{2}/\d{4})\s*[-–]\s*(\d{2}:\d{2})", texto)
    return f"{match.group(1)} {match.group(2)}" if match else "N/A"


def capturar_indicadores() -> list[dict]:
    log.info(f"Acessando {URL_ANBIMA}")

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
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    agora = datetime.now(FUSO)
    data_captura    = agora.strftime("%Y-%m-%d")
    hora_captura    = agora.strftime("%H:%M:%S")
    data_referencia = extrair_data_referencia(soup)
    texto           = soup.get_text(" ", strip=True)

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

    # Taxas de Juros
    for nome, padrao in [
        ("Estimativa SELIC", r"Estimativa SELIC.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Taxa SELIC (BC)",  r"Taxa SELIC do BC.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("DI-B3",            r"DI-B3.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]:
        m = re.search(padrao, texto, re.DOTALL)
        if m:
            registros.append(reg(nome, "Taxa de Juros", m.group(2), "% a.a."))

    # Índices de Preços
    for nome, padrao, unidade in [
        ("IGP-M Número Índice", r"IGP-M.*?N.mero .ndice.*?(\d[\d\.,]+)",             "índice"),
        ("IGP-M Var % mês",     r"IGP-M.*?Var % no m[eê]s.*?(-?\d+[\.,]\d+)",       "%"),
        ("IGP-M Projeção",      r"Proje..o \(mar.*?\).*?(-?\d+[\.,]\d+)",            "%"),
        ("IPCA Número Índice",  r"IPCA.*?N.mero .ndice.*?(\d[\d\.,]+)",              "índice"),
        ("IPCA Var % mês",      r"IPCA.*?Var % no m[eê]s.*?(-?\d+[\.,]\d+)",        "%"),
        ("IPCA Projeção",       r"Proje..o \(mar.*?\).*?(-?\d+[\.,]\d+)",            "%"),
    ]:
        m = re.search(padrao, texto, re.DOTALL | re.IGNORECASE)
        if m:
            registros.append(reg(nome, "Índice de Preços", m.group(1), unidade))

    # Câmbio
    for nome, padrao in [
        ("Dólar Comercial Compra", r"Dolar Comercial Compra.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Dólar Comercial Venda",  r"D.lar Comercial Venda.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Euro Compra",            r"Euro Compra.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Euro Venda",             r"Euro Venda.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]:
        m = re.search(padrao, texto, re.DOTALL)
        if m:
            registros.append(reg(nome, "Câmbio", m.group(2), "R$"))

    # TR / TBF
    for nome, padrao in [
        ("TR",  r"\bTR\b.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("TBF", r"\bTBF\b.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]:
        m = re.search(padrao, texto, re.DOTALL)
        if m:
            registros.append(reg(nome, "Taxa de Referência", m.group(2), "% mês"))

    # FDS
    for i, m in enumerate(
        re.findall(r"FDS.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)", texto, re.DOTALL)[:2], 1
    ):
        registros.append(reg(f"FDS (registro {i})", "FDS", m[1], "R$ cota"))

    log.info(f"Indicadores capturados: {len(registros)}")
    return registros


# ─────────────────────────────────────────────
# Persistência em CSV
# ─────────────────────────────────────────────

def salvar_csv(registros: list[dict]) -> None:
    if not registros:
        log.warning("Nenhum registro para salvar.")
        sys.exit(1)

    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
    novo = not ARQUIVO_CSV.exists()

    with open(ARQUIVO_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO_CSV)
        if novo:
            writer.writeheader()
        writer.writerows(registros)

    log.info(f"CSV atualizado: {ARQUIVO_CSV} ({len(registros)} linhas adicionadas)")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    registros = capturar_indicadores()
    salvar_csv(registros)
    log.info("Concluído com sucesso.")
