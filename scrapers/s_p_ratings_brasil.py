#!/usr/bin/env python
# coding: utf-8
"""
Scraper: S&P Global – Ratings de emissores brasileiros
Fonte:   https://brazil.ratings.spglobal.com/
Saída:   data/s_p_ratings_brasil.csv

Para cada entidade listada em data/s_p_entidades_brasil.csv,
acessa a página de detalhes e extrai a tabela de ratings.

Credenciais esperadas nas variáveis de ambiente:
  USER_STANDARDPOORS=<email>
  PASS_STANDARDPOORS=<senha>
"""
import os
import sys
import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}

# Mapeamento das colunas longas para nomes curtos
RENAME_MAP = {
    "Tipo de Rating": "tipo_rating",
    "Rating": "rating",
    "Data da Ação de Rating": "data_acao_rating",
    "CreditWatch/ Perspectiva": "creditwatch_perspectiva",
    "Data CreditWatch": "data_creditwatch_perspectiva",
    "Identificadores Regulatórios": "identificadores_regulatorios",
}


def _parse_ratings_table(html: str) -> pd.DataFrame:
    """Extrai a tabela de ratings de uma página de entidade S&P."""
    soup = BeautifulSoup(html, "html.parser")
    rows_data = []

    table = soup.find("div", class_="table-module__content")
    if not table:
        return pd.DataFrame()

    header_el = table.find("ul", class_=lambda c: c and "filterable-list__header" in c)
    col_names = []
    if header_el:
        col_names = [span.get_text(strip=True) for span in header_el.find_all("span")]

    for row in table.find_all("div", class_="table-module__row"):
        cols = row.find_all("div", class_="table-module__column")
        values = []
        for col in cols[: len(col_names)]:
            texts = [p.get_text(strip=True) for p in col.find_all("p")]
            values.append(" ".join(t for t in texts if t))
        if values:
            if len(values) < len(col_names):
                values += [""] * (len(col_names) - len(values))
            rows_data.append(values)

    if not rows_data:
        return pd.DataFrame()

    return pd.DataFrame(rows_data, columns=col_names or None)


def _convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    date_cols = [c for c in df.columns if "data" in str(c).lower()]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce").dt.strftime("%Y-%m-%d")
    return df


class SPRatingsBrasilScraper(BaseScraper):
    name = "s_p_ratings_brasil"

    def fetch(self) -> pd.DataFrame:
        # Lê o arquivo de entidades gerado pelo scraper s_p_entidades_brasil
        entidades_csv = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "s_p_entidades_brasil.csv"
        )
        if not os.path.exists(entidades_csv):
            raise FileNotFoundError(
                f"Arquivo de entidades não encontrado: {entidades_csv}. "
                "Execute s_p_entidades_brasil.py antes."
            )

        df_entidades = pd.read_csv(entidades_csv)
        if "link" not in df_entidades.columns:
            raise ValueError("Coluna 'link' não encontrada no CSV de entidades.")

        session = requests.Session()
        frames = []
        total = len(df_entidades)

        for i, row in df_entidades.iterrows():
            nome = row.get("nome", "")
            link = row.get("link", "")
            self.logger.info(f"[{i+1}/{total}] {nome}")

            try:
                resp = session.get(link, headers=HEADERS, timeout=30)
                if resp.status_code != 200:
                    self.logger.warning(f"Status {resp.status_code} para {link}")
                    continue
                df_table = _parse_ratings_table(resp.text)
                if df_table.empty:
                    continue
                df_table["nome"] = nome
                df_table["link"] = link
                frames.append(df_table)
            except Exception as e:
                self.logger.warning(f"Erro em {link}: {e}")

        if not frames:
            return pd.DataFrame()

        df = pd.concat(frames, ignore_index=True)
        df = _convert_dates(df)

        # Normaliza colunas mais comuns
        df.rename(columns=RENAME_MAP, inplace=True)

        df.insert(0, "dt_captura", datetime.date.today())
        return df


if __name__ == "__main__":
    scraper = SPRatingsBrasilScraper()
    scraper.run()
