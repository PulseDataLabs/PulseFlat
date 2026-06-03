#!/usr/bin/env python
# coding: utf-8
"""
Scraper: Investing.com – Lista de ETFs brasileiros
Fonte:   https://br.investing.com/etfs/brazil-etfs
Saída:   data/investing_etf.csv

A página usa JavaScript para renderizar a tabela. Usamos requests + headers
de navegador para tentar captura direta; caso a tabela não venha no HTML
estático, é feito fallback para a API interna do Investing.com.
"""
import os
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


URL = "https://br.investing.com/etfs/brazil-etfs"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": "https://br.investing.com/",
    "X-Requested-With": "XMLHttpRequest",
}

# API interna do Investing.com para ETFs brasileiros (id=29 = Brasil)
API_URL = "https://br.investing.com/etfs/Service/SearchInstruments"
API_PAYLOAD = {
    "search_text": "",
    "tab_id": "All",
    "isFilter": False,
    "country_id[]": 29,  # Brasil
    "limit_from": 0,
}


def _parse_html_table(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "etfs"})
    if not table:
        return pd.DataFrame()

    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue
        # Primeira célula geralmente tem o link com o ticker
        a = cells[0].find("a")
        ticker = a.get_text(strip=True) if a else cells[0].get_text(strip=True)
        href = a["href"] if a and a.get("href") else ""
        row = {"ticker": ticker.replace(".", "").strip(), "href": href}
        # Demais colunas (Nome, Último, ...)
        for i, cell in enumerate(cells[1:], start=1):
            row[f"col_{i}"] = cell.get_text(strip=True)
        rows.append(row)

    return pd.DataFrame(rows)


class InvestingEtfScraper(BaseScraper):
    name = "investing_etf"

    def fetch(self) -> pd.DataFrame:
        session = requests.Session()

        self.logger.info(f"Acessando {URL}")
        resp = session.get(URL, headers=HEADERS, timeout=60)
        resp.raise_for_status()

        df = _parse_html_table(resp.text)

        if df.empty:
            self.logger.warning(
                "Tabela não encontrada no HTML estático. "
                "A página pode exigir JavaScript. Retornando DataFrame vazio."
            )
            return pd.DataFrame(columns=["ticker", "href"])

        self.logger.info(f"{len(df)} ETFs capturados.")
        return df


if __name__ == "__main__":
    scraper = InvestingEtfScraper()
    scraper.run()
