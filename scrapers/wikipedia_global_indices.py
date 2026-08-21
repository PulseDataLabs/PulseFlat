"""
scrapers/wikipedia_global_indices.py
------------------------------------
Captura a lista de ativos que compõem os principais índices de ações globais da Wikipedia.
Utilizado para alimentar dinamicamente os scrapers do Yahoo Finance de ações internacionais.
"""

import sys
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.utils.base import BaseScraper
from utils import agora_brt, get_logger

log = get_logger("wikipedia_global_indices")

CABECALHO = ["data_captura", "codigo_ativo", "nome_ativo", "indice_origem"]


def clean_us_ticker(ticker: str) -> str:
    # yfinance usa hífen para tickers de classe de ações nos EUA (ex: BRK.B -> BRK-B)
    return ticker.strip().replace(".", "-")


def scrape_sp500(session: requests.Session) -> list[dict]:
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    log.info("Buscando S&P 500...")
    r = session.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    if not table:
        raise ValueError("Tabela constituents do S&P 500 não encontrada")

    res = []
    for row in table.find_all("tr")[1:]:
        tds = row.find_all("td")
        if len(tds) >= 2:
            ticker = clean_us_ticker(tds[0].text.strip())
            name = tds[1].text.strip()
            res.append(
                {"codigo_ativo": ticker, "nome_ativo": name, "indice_origem": "S&P 500"}
            )
    return res


def scrape_nasdaq100(session: requests.Session) -> list[dict]:
    url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    log.info("Buscando NASDAQ-100...")
    r = session.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    if not table:
        raise ValueError("Tabela constituents do NASDAQ-100 não encontrada")

    res = []
    for row in table.find_all("tr")[1:]:
        tds = row.find_all("td")
        if len(tds) >= 2:
            ticker = clean_us_ticker(tds[0].text.strip())
            name = tds[1].text.strip()
            res.append(
                {
                    "codigo_ativo": ticker,
                    "nome_ativo": name,
                    "indice_origem": "NASDAQ-100",
                }
            )
    return res


def scrape_dowjones(session: requests.Session) -> list[dict]:
    url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
    log.info("Buscando Dow Jones...")
    r = session.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    if not table:
        raise ValueError("Tabela constituents do Dow Jones não encontrada")

    res = []
    for row in table.find_all("tr")[1:]:
        tds = row.find_all("td")
        if len(tds) >= 2:
            name = tds[0].text.strip()
            ticker = clean_us_ticker(tds[1].text.strip())
            res.append(
                {
                    "codigo_ativo": ticker,
                    "nome_ativo": name,
                    "indice_origem": "Dow Jones",
                }
            )
    return res


def scrape_ftse100(session: requests.Session) -> list[dict]:
    url = "https://en.wikipedia.org/wiki/FTSE_100_Index"
    log.info("Buscando FTSE 100...")
    r = session.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    if not table:
        raise ValueError("Tabela constituents do FTSE 100 não encontrada")

    res = []
    for row in table.find_all("tr")[1:]:
        tds = row.find_all("td")
        if len(tds) >= 2:
            name = tds[0].text.strip()
            ticker = tds[1].text.strip()
            # Adiciona sufixo .L do Yahoo para Londres
            if ticker and not ticker.endswith(".L"):
                ticker = f"{ticker}.L"
            res.append(
                {
                    "codigo_ativo": ticker,
                    "nome_ativo": name,
                    "indice_origem": "FTSE 100",
                }
            )
    return res


def scrape_dax40(session: requests.Session) -> list[dict]:
    url = "https://en.wikipedia.org/wiki/DAX"
    log.info("Buscando DAX 40...")
    r = session.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    if not table:
        raise ValueError("Tabela constituents do DAX 40 não encontrada")

    res = []
    for row in table.find_all("tr")[1:]:
        tds = row.find_all("td")
        if len(tds) >= 3:
            ticker = tds[0].text.strip()
            name = tds[2].text.strip()
            res.append(
                {"codigo_ativo": ticker, "nome_ativo": name, "indice_origem": "DAX 40"}
            )
    return res


def scrape_cac40(session: requests.Session) -> list[dict]:
    url = "https://en.wikipedia.org/wiki/CAC_40"
    log.info("Buscando CAC 40...")
    r = session.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    if not table:
        raise ValueError("Tabela constituents do CAC 40 não encontrada")

    res = []
    for row in table.find_all("tr")[1:]:
        tds = row.find_all("td")
        if len(tds) >= 4:
            name = tds[0].text.strip()
            ticker = tds[3].text.strip()
            res.append(
                {"codigo_ativo": ticker, "nome_ativo": name, "indice_origem": "CAC 40"}
            )
    return res


def scrape_eurostoxx50(session: requests.Session) -> list[dict]:
    url = "https://en.wikipedia.org/wiki/Euro_Stoxx_50"
    log.info("Buscando Euro Stoxx 50...")
    r = session.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    if not table:
        raise ValueError("Tabela constituents do Euro Stoxx 50 não encontrada")

    res = []
    for row in table.find_all("tr")[1:]:
        tds = row.find_all("td")
        if len(tds) >= 3:
            ticker = tds[0].text.strip()
            name = tds[2].text.strip()
            res.append(
                {
                    "codigo_ativo": ticker,
                    "nome_ativo": name,
                    "indice_origem": "Euro Stoxx 50",
                }
            )
    return res


class WikipediaGlobalIndicesScraper(BaseScraper):
    name = "wikipedia_global_indices"
    group = "global"
    enabled = True
    phase = 1
    accumulate = False
    chaves_dedup = None

    title = "Mercado Global — Índices Mundiais de Ações"
    description = "Principais índices mundiais de ações (S&P 500, Nasdaq, Dow Jones, FTSE, DAX, Nikkei)."
    icon = "🌐"
    icon_class = "icon-global"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = [
        "indices",
        "global",
        "wikipedia",
        "sp500",
        "nasdaq",
        "dowjones",
        "ftse",
        "dax",
        "cac",
    ]
    source = "Wikipedia"

    def fetch(self) -> pd.DataFrame:
        data_captura, _ = agora_brt()
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

        todos_ativos = []

        scrapers = [
            ("S&P 500", scrape_sp500),
            ("NASDAQ-100", scrape_nasdaq100),
            ("Dow Jones", scrape_dowjones),
            ("FTSE 100", scrape_ftse100),
            ("DAX 40", scrape_dax40),
            ("CAC 40", scrape_cac40),
            ("Euro Stoxx 50", scrape_eurostoxx50),
        ]

        for nome, func in scrapers:
            try:
                ativos = func(session)
                todos_ativos.extend(ativos)
                log.info(f"{nome}: {len(ativos)} ativos carregados.")
            except Exception as e:
                log.error(f"Erro ao raspar {nome}: {e}")

        if not todos_ativos:
            return pd.DataFrame(columns=CABECALHO)

        df = pd.DataFrame(todos_ativos)
        df["data_captura"] = data_captura
        return df[CABECALHO]


if __name__ == "__main__":
    WikipediaGlobalIndicesScraper().run()
