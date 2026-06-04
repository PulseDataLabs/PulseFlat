#!/usr/bin/env python
# coding: utf-8
"""
Scraper: S&P Global – Ações de Rating (últimos 7 dias, Brasil)
Fonte:   https://www.spglobal.com/ratings/pt/regulatory/ratings-actions
Saída:   data/s_p_acoes_ratings.csv

A página filtra por período (últimos 7 dias) e país (Brasil).
O scraper extrai a tabela via requests + BeautifulSoup.
"""
import os
import sys
import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


BASE_URL = "https://www.spglobal.com/ratings/pt/regulatory/ratings-actions"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": "https://www.spglobal.com/ratings/pt/regulatory/",
}

# Parâmetros de filtro (últimos 7 dias, Brasil)
PARAMS = {
    "filterCriteria": "7",      # 7 = últimos 7 dias
    "countries": "BRA",
    "pageSize": 100,
}


def _parse_table(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")

    container = soup.find("div", id="listTableContainerId")
    if not container:
        return pd.DataFrame()

    header_ul = container.select_one(
        "ul.ratingsActions_filterable-list__header, ul.filterable-list__header"
    )
    col_names: List[str] = []
    if header_ul:
        col_names = [span.get_text(strip=True) for span in header_ul.find_all("span")]

    rows = container.select(
        "div.table-module__content div.table-module__row.ratingsActions-table-module__row"
    )
    data: List[List[str]] = []
    for row in rows:
        cols = row.find_all("div", class_="table-module__column")
        if not cols:
            continue
        values = []
        for col in cols[: len(col_names)]:
            texts = [p.get_text(strip=True) for p in col.find_all("p")]
            values.append(" ".join(t for t in texts if t))
        if len(values) < len(col_names):
            values += [""] * (len(col_names) - len(values))
        data.append(values)

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data, columns=col_names or None)


class SPAcoesRatingsScraper(BaseScraper):
    name = "s_p_acoes_ratings"

    def fetch(self) -> pd.DataFrame:
        session = requests.Session()
        cookie_str = os.environ.get("SP_GLOBAL_COOKIES", "")
        if cookie_str:
            self.logger.info("Utilizando cookies de sessão fornecidos em SP_GLOBAL_COOKIES...")
            cookies = {}
            for item in cookie_str.split(";"):
                if "=" in item:
                    k, v = item.split("=", 1)
                    cookies[k.strip()] = v.strip()
            session.cookies.update(cookies)
        self.logger.info(f"Acessando {BASE_URL}")

        resp = session.get(BASE_URL, params=PARAMS, headers=HEADERS, timeout=60)

        if resp.status_code == 403:
            self.logger.warning(
                "Acesso bloqueado (403 Forbidden) pela S&P Global. "
                "O site exige autenticação ou bloqueia bots. "
                "Configure USER_STANDARDPOORS / PASS_STANDARDPOORS ou "
                "utilize Playwright/Selenium."
            )
            return pd.DataFrame()

        resp.raise_for_status()

        df = _parse_table(resp.text)

        if df.empty:
            self.logger.warning(
                "Tabela de ações de rating vazia. "
                "A página pode exigir JavaScript para renderização. "
                "Considere integrar Playwright/Selenium para este scraper."
            )
            return pd.DataFrame()

        df.insert(0, "dt_captura", datetime.date.today())
        return df


if __name__ == "__main__":
    scraper = SPAcoesRatingsScraper()
    scraper.run()
