#!/usr/bin/env python
# coding: utf-8
"""
Scraper: S&P Global – Ratings globais de emissores
Fonte:   https://www.spglobal.com/ratings/pt/regulatory/
Saída:   data/s_p_ratings_global.csv

Para cada entidade listada em data/s_p_entidades_global.csv,
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
from dotenv import load_dotenv

load_dotenv()

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

# Colunas padrão da tabela de ratings S&P Global
DEFAULT_COL_NAMES = [
    "tipo_rating",
    "rating",
    "data_acao_rating",
    "data_ultima_revisao",
    "identificadores_regulatorios",
    "creditwatch_perspectiva",
    "data_creditwatch_perspectiva",
]


def _parse_ratings_table(html: str) -> pd.DataFrame:
    """Extrai a tabela de ratings de uma página de entidade S&P Global."""
    soup = BeautifulSoup(html, "html.parser")

    # Encontra o container de ratings
    table_module = soup.find("div", class_="table-module__ratings")
    if not table_module:
        table_module = soup.find("div", class_="table-module__content")
        if not table_module:
            return pd.DataFrame()

    # Extrai nomes das colunas do header
    col_names = []
    header_div = table_module.find("div", class_="table-module__header")
    if header_div:
        for span in header_div.find_all("span", recursive=True):
            text = span.get_text(strip=True)
            if text and len(text) < 60 and "indica a data" not in text:
                col_names.append(text)

    if not col_names:
        col_names = DEFAULT_COL_NAMES

    # Extrai dados
    content = table_module.find("div", class_="table-module__content")
    if not content:
        content = table_module

    rows_data = []
    for row in content.find_all("div", class_="table-module__row"):
        cols = row.find_all("div", class_="table-module__column")
        values = [col.get_text(strip=True) for col in cols]
        if values:
            if len(values) < len(col_names):
                values += [""] * (len(col_names) - len(values))
            elif len(values) > len(col_names):
                values = values[: len(col_names)]
            rows_data.append(values)

    if not rows_data:
        return pd.DataFrame()

    return pd.DataFrame(rows_data, columns=col_names[: len(rows_data[0])])


def _convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    date_cols = [c for c in df.columns if "data" in str(c).lower()]
    for col in date_cols:
        df[col] = pd.to_datetime(
            df[col], dayfirst=True, errors="coerce"
        ).dt.strftime("%Y-%m-%d")
    return df


class SPRatingsGlobalScraper(BaseScraper):
    name = "s_p_ratings_global"

    def fetch(self) -> pd.DataFrame:
        # Lê o arquivo de entidades gerado pelo scraper s_p_entidades_global
        entidades_csv = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "s_p_entidades_global.csv",
        )
        if not os.path.exists(entidades_csv):
            self.logger.warning(
                f"Arquivo de entidades não encontrado: {entidades_csv}. "
                "Execute s_p_entidades_global.py antes. "
                "O site S&P Global requer autenticação."
            )
            return pd.DataFrame()

        df_entidades = pd.read_csv(entidades_csv)
        if "link_completo" not in df_entidades.columns:
            self.logger.warning(
                "Coluna 'link_completo' não encontrada no CSV de entidades."
            )
            return pd.DataFrame()

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

        frames = []
        total = len(df_entidades)

        for i, row in df_entidades.iterrows():
            nome = row.get("nome", "")
            link = row.get("link_completo", "")
            self.logger.info(f"[{i+1}/{total}] {nome}")

            try:
                resp = session.get(link, headers=HEADERS, timeout=30)
                if resp.status_code == 403:
                    self.logger.warning(
                        f"Acesso bloqueado (403) para {nome}. "
                        "O site pode exigir autenticação."
                    )
                    continue
                if resp.status_code != 200:
                    self.logger.warning(
                        f"Status {resp.status_code} para {link}"
                    )
                    continue
                df_table = _parse_ratings_table(resp.text)
                if df_table.empty:
                    continue
                df_table["nome"] = nome
                df_table["link_completo"] = link
                frames.append(df_table)
            except Exception as e:
                self.logger.warning(f"Erro em {link}: {e}")

        if not frames:
            self.logger.warning(
                "Nenhum rating capturado. O site S&P Global pode exigir "
                "autenticação via browser ou bloqueio anti-bot."
            )
            return pd.DataFrame()

        df = pd.concat(frames, ignore_index=True)
        df = _convert_dates(df)
        df.insert(0, "dt_captura", datetime.date.today())
        return df


if __name__ == "__main__":
    scraper = SPRatingsGlobalScraper()
    scraper.run()
