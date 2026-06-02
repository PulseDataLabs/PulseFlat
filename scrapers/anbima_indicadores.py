"""
scrapers/anbima_indicadores.py
-------------------------------
Captura o quadro de indicadores financeiros da ANBIMA:
  Taxa SELIC, DI-B3, IGP-M, IPCA, Dólar, Euro, TR, TBF, FDS.

Fonte: https://www.anbima.com.br/informacoes/indicadores/
"""

import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, nova_session, salvar_csv

log = get_logger("anbima_indicadores")

URL     = "https://www.anbima.com.br/informacoes/indicadores/"
ARQUIVO = Path("data/anbima_indicadores.csv")

CABECALHO = [
    "data_captura",
    
    "data_referencia_pagina",
    "indicador",
    "categoria",
    "valor",
    "unidade",
]


def _limpar_valor(texto: str) -> str:
    if not texto:
        return ""
    return re.sub(r"[%\s]", "", texto.strip().replace("\xa0", "").replace(",", "."))


def _extrair_data_ref(soup: BeautifulSoup) -> str:
    texto = soup.get_text(" ", strip=True)
    m = re.search(r"(\d{2}/\d{2}/\d{4})\s*[-–]\s*(\d{2}:\d{2})", texto)
    return f"{m.group(1)} {m.group(2)}" if m else "N/A"


def capturar() -> list[dict]:
    log.info(f"Acessando {URL}")
    session = nova_session()

    for tentativa in range(1, 4):
        try:
            resp = session.get(URL, timeout=30)
            resp.encoding = "iso-8859-1"
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error("Todas as tentativas falharam.")
                sys.exit(1)
            time.sleep(5)

    soup = BeautifulSoup(resp.text, "html.parser")
    data_captura, _ = agora_brt()
    data_ref = _extrair_data_ref(soup)
    texto    = soup.get_text(" ", strip=True)
    registros = []

    def add(indicador, categoria, valor, unidade=""):
        registros.append({
            "data_captura":           data_captura,
            "data_referencia_pagina": data_ref,
            "indicador":              indicador,
            "categoria":              categoria,
            "valor":                  _limpar_valor(valor),
            "unidade":                unidade,
        })

    # Taxas de Juros
    for nome, padrao in [
        ("Estimativa SELIC", r"Estimativa SELIC.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Taxa SELIC (BC)",  r"Taxa SELIC do BC.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("DI-B3",            r"DI-B3.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]:
        m = re.search(padrao, texto, re.DOTALL)
        if m:
            add(nome, "Taxa de Juros", m.group(2), "% a.a.")

    # Índices de Preços
    for nome, padrao, unidade in [
        ("IGP-M Número Índice", r"IGP-M.*?N.mero .ndice.*?(\d[\d\.,]+)",       "índice"),
        ("IGP-M Var % mês",     r"IGP-M.*?Var % no m[eê]s.*?(-?\d+[\.,]\d+)", "%"),
        ("IGP-M Projeção",      r"Proje..o.*?IGP.*?(-?\d+[\.,]\d+)",           "%"),
        ("IPCA Número Índice",  r"IPCA.*?N.mero .ndice.*?(\d[\d\.,]+)",        "índice"),
        ("IPCA Var % mês",      r"IPCA.*?Var % no m[eê]s.*?(-?\d+[\.,]\d+)",  "%"),
        ("IPCA Projeção",       r"Proje..o.*?IPCA.*?(-?\d+[\.,]\d+)",          "%"),
    ]:
        m = re.search(padrao, texto, re.DOTALL | re.IGNORECASE)
        if m:
            add(nome, "Índice de Preços", m.group(1), unidade)

    # Câmbio
    for nome, padrao in [
        ("Dólar Comercial Compra", r"Dolar Comercial Compra.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Dólar Comercial Venda",  r"D.lar Comercial Venda.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Euro Compra",            r"Euro Compra.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Euro Venda",             r"Euro Venda.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]:
        m = re.search(padrao, texto, re.DOTALL)
        if m:
            add(nome, "Câmbio", m.group(2), "R$")

    # TR / TBF
    for nome, padrao in [
        ("TR",  r"\bTR\b.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("TBF", r"\bTBF\b.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]:
        m = re.search(padrao, texto, re.DOTALL)
        if m:
            add(nome, "Taxa de Referência", m.group(2), "% mês")

    # FDS
    for i, m in enumerate(
        re.findall(r"FDS.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)", texto, re.DOTALL)[:2], 1
    ):
        add(f"FDS (registro {i})", "FDS", m[1], "R$ cota")

    log.info(f"{len(registros)} indicadores capturados (ref: {data_ref})")
    return registros


def main():
    log.info("=== ANBIMA Indicadores ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "indicador"])


if __name__ == "__main__":
    main()
