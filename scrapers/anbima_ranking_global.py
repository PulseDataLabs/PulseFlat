#!/usr/bin/env python
# coding: utf-8
"""
Scraper: ANBIMA Ranking Global de Administração de Recursos de Terceiros
Fonte:   https://www.anbima.com.br/pt_br/informar/ranking/fundos-de-investimento/global.htm
Saída:   data/anbima_ranking_global.csv

Nota: a página entrega um arquivo Excel (.xls/.xlsx). O scraper baixa via
requests seguindo os redirects, lê a aba "Pag 4 - Por Ativos RF" e
"Pag - 5 Por Ativos RV", e consolida ambas num único CSV.
"""
import os
import re
import sys
import datetime
from io import BytesIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


STRAPI_HOST = "https://data-strapi.prd.anbima.com.br"
STRAPI_API_URL = f"{STRAPI_HOST}/api/ranking-global-de-adm-de-fundo?populate[template][populate][publication_document][populate]=*"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.anbima.com.br",
}


def _get_download_url(session: requests.Session) -> str:
    """Busca a URL do arquivo Excel via API do Strapi da ANBIMA."""
    resp = session.get(STRAPI_API_URL, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    try:
        template = data["data"]["attributes"]["template"]
        pub_docs = template["publication_document"]
        if not pub_docs:
            raise ValueError("publication_document está vazio.")

        pub_doc = pub_docs[0]
        files = pub_doc["file"]["data"]
        if not files:
            raise ValueError("Nenhum arquivo encontrado em publication_document.")

        url_path = files[0]["attributes"]["url"]
        return STRAPI_HOST + url_path
    except (KeyError, IndexError, TypeError, ValueError) as e:
        raise RuntimeError(f"Erro ao extrair URL de download da API do Strapi: {e}") from e


def _extract_date_from_filename(file_name: str) -> datetime.date:
    """Extrai a data de referência (YYYYMM) do nome do arquivo."""
    m = re.search(r"(\d{6})", file_name)
    if m:
        return datetime.datetime.strptime(m.group(1) + "01", "%Y%m%d").date()
    return datetime.date.today().replace(day=1)


def _read_sheet(content: bytes, sheet_name: str, data_referencia: datetime.date) -> pd.DataFrame:
    """Lê uma aba específica do Excel e retorna DataFrame normalizado."""
    engine = "xlrd" if content.startswith(b"\xd0\xcf\x11\xe0") else "openpyxl"
    df = pd.read_excel(
        BytesIO(content),
        sheet_name=sheet_name,
        skiprows=8,
        skipfooter=2,
        engine=engine,
    )
    df = df.dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]
    df.insert(0, "dt_referencia", data_referencia)
    df.insert(1, "tipo_ativo", sheet_name.strip())
    return df


class AnbimaRankingGlobalScraper(BaseScraper):
    name = "anbima_ranking_global"

    def fetch(self) -> pd.DataFrame:
        session = requests.Session()

        download_url = _get_download_url(session)
        self.logger.info(f"Baixando arquivo: {download_url}")

        resp = session.get(download_url, headers=HEADERS, timeout=120)
        resp.raise_for_status()
        content = resp.content

        file_name = download_url.split("/")[-1].split("?")[0]
        data_referencia = _extract_date_from_filename(file_name)
        self.logger.info(f"Data de referência: {data_referencia}")

        try:
            df_rf = _read_sheet(content, "Pag 4 - Por Ativos RF", data_referencia)
            df_rv = _read_sheet(content, "Pag - 5 Por Ativos RV", data_referencia)
        except Exception as e:
            raise RuntimeError(f"Erro ao ler abas do Excel: {e}") from e

        df = pd.concat([df_rf, df_rv], ignore_index=True)
        return df


if __name__ == "__main__":
    scraper = AnbimaRankingGlobalScraper()
    scraper.run()
