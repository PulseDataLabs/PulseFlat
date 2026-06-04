#!/usr/bin/env python
# coding: utf-8
"""
Scraper: Investing.com – Lista de ETFs brasileiros
Fonte:   https://br.investing.com/etfs/brazil-etfs
Saída:   data/investing_etf.csv

Captura a tabela de ETFs brasileiros do Investing.com.
A tabela HTML (id="etfs") contém colunas:
  [checkbox] | Nome | Código | Último | Var% | Vol. | Hora | [empty]
O ticker e link estão na coluna "Código" (cell index 2).
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
}


def _parse_html_table(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "etfs"})
    if not table:
        return pd.DataFrame()

    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all("td")
        if len(cells) < 6:
            continue

        # Cell 1 = Nome, Cell 2 = Código (com link), Cell 3 = Último,
        # Cell 4 = Var%, Cell 5 = Vol., Cell 6 = Hora
        nome = cells[1].get_text(strip=True)
        codigo_cell = cells[2]
        a = codigo_cell.find("a")
        ticker = a.get_text(strip=True) if a else codigo_cell.get_text(strip=True)
        href = ""
        if a and a.get("href"):
            href = a["href"]
            if not href.startswith("http"):
                href = "https://br.investing.com" + href

        ultimo = cells[3].get_text(strip=True) if len(cells) > 3 else ""
        variacao = cells[4].get_text(strip=True) if len(cells) > 4 else ""
        volume = cells[5].get_text(strip=True) if len(cells) > 5 else ""
        hora = cells[6].get_text(strip=True) if len(cells) > 6 else ""

        if not ticker:
            continue

        rows.append({
            "nome": nome,
            "ticker": ticker,
            "link": href,
            "vr_ultimo": ultimo,
            "vr_variacao_pct": variacao,
            "qt_volume": volume,
            "hr_atualizacao": hora,
        })

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
            return pd.DataFrame(columns=["nome", "ticker", "link"])

        self.logger.info(f"{len(df)} ETFs capturados.")
        return df


if __name__ == "__main__":
    scraper = InvestingEtfScraper()
    scraper.run()
