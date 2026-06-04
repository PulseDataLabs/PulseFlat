#!/usr/bin/env python
# coding: utf-8
"""
Scraper: Moody's Local – Lista de Classificações Vigentes (Brasil)
Fonte:   https://moodyslocal.com.br/
Saída:   data/moodys_local_ratings.csv

A página disponibiliza um link direto para download do Excel de ratings.
O scraper faz parse do HTML para encontrar o link e baixa via requests.
"""
import os
import sys
import re
from io import BytesIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


BASE_URL = "https://moodyslocal.com.br"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": BASE_URL,
}

RENAME_MAP = {
    "Setor": "no_setor",
    "Emissor": "no_entidade",
    "Produto": "no_tipo_rating",
    "Instrumento": "de_instrumento",
    "Objeto": "de_objeto",
    "Rating / Avaliação": "de_rating_br",
    "Perspectiva": "de_outlook",
    "Última data de atualização": "dt_rating",
}


def _find_download_url(session: requests.Session) -> str:
    resp = session.get(BASE_URL, headers=HEADERS, timeout=60)
    if resp.status_code == 403:
        raise RuntimeError(
            "Acesso bloqueado (403 Forbidden) pela Moody's Local. "
            "O site bloqueia requisições automatizadas. "
            "Considere usar Playwright/Selenium para este scraper."
        )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]
        if "Lista de Classificações Vigentes" in text or re.search(r"MOODYS.*\.xlsx?", href, re.IGNORECASE):
            return href if href.startswith("http") else BASE_URL.rstrip("/") + "/" + href.lstrip("/")

    raise RuntimeError("Link de download da Moody's Local não encontrado.")


class MoodysLocalRatingsScraper(BaseScraper):
    name = "moodys_local_ratings"

    def fetch(self) -> pd.DataFrame:
        session = requests.Session()

        try:
            download_url = _find_download_url(session)
        except RuntimeError as e:
            self.logger.warning(str(e))
            return pd.DataFrame()

        self.logger.info(f"Baixando: {download_url}")

        resp = session.get(download_url, headers=HEADERS, timeout=120)
        resp.raise_for_status()

        xlsx_bytes = BytesIO(resp.content)

        # Linha 0: metadados (data de atualização está no cabeçalho das colunas)
        df_meta = pd.read_excel(xlsx_bytes, engine="openpyxl", nrows=1)
        xlsx_bytes.seek(0)

        # Dados reais a partir da linha 3 (skiprows=3)
        df = pd.read_excel(xlsx_bytes, engine="openpyxl", skiprows=3)

        # Extrai a data de atualização da linha de metadados
        try:
            data_atualizacao = df_meta.columns[7]
            if hasattr(data_atualizacao, "date"):
                data_atualizacao = data_atualizacao.date()
        except (IndexError, AttributeError):
            import datetime
            data_atualizacao = datetime.date.today()

        df["dh_atu_arquivo"] = data_atualizacao
        df.rename(columns=RENAME_MAP, inplace=True)
        df.dropna(how="all", inplace=True)

        return df


if __name__ == "__main__":
    scraper = MoodysLocalRatingsScraper()
    scraper.run()
