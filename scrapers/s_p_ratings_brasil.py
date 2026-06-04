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

# Colunas esperadas na tabela de ratings do site S&P Brasil
# (extraídas dos spans do header .table-module__ratings)
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
    """Extrai a tabela de ratings de uma página de entidade S&P Brasil.

    A estrutura HTML do site S&P Brasil usa:
      - div.table-module__ratings como container principal
      - div.table-module__header com spans contendo os nomes das colunas
      - div.table-module__content com div.table-module__row para cada linha
    """
    soup = BeautifulSoup(html, "html.parser")

    # Encontra o container de ratings (tem classe table-module__ratings)
    table_module = soup.find("div", class_="table-module__ratings")
    if not table_module:
        # Fallback: busca qualquer table-module__content
        table_module = soup.find("div", class_="table-module__content")
        if not table_module:
            return pd.DataFrame()

    # Extrai nomes das colunas do header
    col_names = []
    header_div = table_module.find("div", class_="table-module__header")
    if header_div:
        # Pega os spans de primeiro nível que contêm os nomes das colunas
        # Filtra spans que são títulos (não tooltips)
        for span in header_div.find_all("span", recursive=True):
            text = span.get_text(strip=True)
            # Pula tooltips e textos longos explicativos
            if text and len(text) < 60 and "indica a data" not in text:
                col_names.append(text)

    # Se não encontrou colunas, usa os padrões
    if not col_names:
        col_names = DEFAULT_COL_NAMES

    # Extrai dados das linhas
    content = table_module.find("div", class_="table-module__content")
    if not content:
        # Se o table_module já é o content
        content = table_module

    rows_data = []
    for row in content.find_all("div", class_="table-module__row"):
        cols = row.find_all("div", class_="table-module__column")
        values = [col.get_text(strip=True) for col in cols]
        if values:
            # Ajusta o número de valores para corresponder ao número de colunas
            if len(values) < len(col_names):
                values += [""] * (len(col_names) - len(values))
            elif len(values) > len(col_names):
                values = values[: len(col_names)]
            rows_data.append(values)

    if not rows_data:
        return pd.DataFrame()

    return pd.DataFrame(rows_data, columns=col_names[: len(rows_data[0])])


def _convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Converte colunas com 'data' no nome para formato YYYY-MM-DD."""
    date_cols = [c for c in df.columns if "data" in str(c).lower()]
    for col in date_cols:
        # Tenta formatos conhecidos do site S&P Brasil
        for fmt in ["%d-%b-%Y", "%d/%m/%Y", "%Y-%m-%d"]:
            try:
                parsed = pd.to_datetime(df[col], format=fmt, errors="coerce")
                if parsed.notna().any():
                    df[col] = parsed.dt.strftime("%Y-%m-%d")
                    break
            except (ValueError, TypeError):
                continue
    return df


class SPRatingsBrasilScraper(BaseScraper):
    name = "s_p_ratings_brasil"

    def fetch(self) -> pd.DataFrame:
        # Lê o arquivo de entidades gerado pelo scraper s_p_entidades_brasil
        entidades_csv = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "s_p_entidades_brasil.csv",
        )
        if not os.path.exists(entidades_csv):
            self.logger.warning(
                f"Arquivo de entidades não encontrado: {entidades_csv}. "
                "Execute s_p_entidades_brasil.py antes."
            )
            return pd.DataFrame()

        df_entidades = pd.read_csv(entidades_csv)
        if "link" not in df_entidades.columns:
            self.logger.warning(
                "Coluna 'link' não encontrada no CSV de entidades."
            )
            return pd.DataFrame()

        session = requests.Session()
        frames = []
        total = len(df_entidades)

        for i, row in df_entidades.iterrows():
            nome = row.get("nome", "")
            link = row.get("link", "")
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
                    self.logger.warning(
                        f"Tabela de ratings vazia para {nome}"
                    )
                    continue
                df_table["nome"] = nome
                df_table["link"] = link
                frames.append(df_table)
            except Exception as e:
                self.logger.warning(f"Erro em {link}: {e}")

        if not frames:
            self.logger.warning(
                "Nenhum rating capturado. Os sites S&P podem exigir "
                "autenticação ou usar JavaScript para renderização."
            )
            return pd.DataFrame()

        df = pd.concat(frames, ignore_index=True)
        df = _convert_dates(df)
        df.insert(0, "dt_captura", datetime.date.today())
        return df


if __name__ == "__main__":
    scraper = SPRatingsBrasilScraper()
    scraper.run()
