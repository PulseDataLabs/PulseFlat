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


BASE_URL = "https://brazil.ratings.spglobal.com/ratings/pt/regulatory/ratings-actions"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": "https://brazil.ratings.spglobal.com/ratings/pt/regulatory/",
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
        if len(col_names) == 10:
            col_names = [
                "descricao",
                "link_descricao",
                "classe",
                "data_vencimento",
                "tipo_rating",
                "data_acao",
                "rating_novo",
                "creditwatch_perspectiva_novo",
                "rating_anterior",
                "creditwatch_perspectiva_anterior",
                "acao"
            ]
        else:
            seen = {}
            new_names = []
            for name in col_names:
                clean_name = name.lower().replace(" ", "_").replace("/", "_").replace("ç", "c").replace("ã", "a").replace("ê", "e")
                if clean_name in seen:
                    seen[clean_name] += 1
                    new_names.append(f"{clean_name}_{seen[clean_name]}")
                else:
                    seen[clean_name] = 1
                    new_names.append(clean_name)
            col_names = new_names
            col_names.insert(1, "link_descricao")

    rows = container.select(
        "div.table-module__content div.table-module__row.ratingsActions-table-module__row"
    )
    data: List[List[str]] = []
    for row in rows:
        cols = row.find_all("div", class_="table-module__column")
        if not cols:
            continue
        values = []
        for i, col in enumerate(cols[: len(col_names) - 1]):
            texts = [p.get_text(strip=True) for p in col.find_all("p")]
            val = " ".join(t for t in texts if t)
            if i == 0:
                values.append(val)
                a_tag = col.find("a")
                link_val = ""
                if a_tag:
                    href = a_tag.get("href", "")
                    if href:
                        link_val = href if href.startswith("http") else f"https://brazil.ratings.spglobal.com{href}"
                values.append(link_val)
            else:
                values.append(val)
        if len(values) < len(col_names):
            values += [""] * (len(col_names) - len(values))
        data.append(values)

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data, columns=col_names or None)


class SPAcoesRatingsScraper(BaseScraper):
    name = "s_p_acoes_ratings"
    group = "ratings"
    enabled = True
    phase = 1
    chaves_dedup = ["descricao", "classe", "tipo_rating", "data_acao"]

    def fetch(self) -> pd.DataFrame:
        session = requests.Session()
        self.logger.info(f"Acessando {BASE_URL}")

        resp = session.get(BASE_URL, params=PARAMS, headers=HEADERS, timeout=60)
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
