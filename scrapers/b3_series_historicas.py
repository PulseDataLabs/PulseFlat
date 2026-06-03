#!/usr/bin/env python
# coding: utf-8
"""
Scraper: B3 – Séries Históricas de Renda Fixa (Negociação Consolidada)
Fonte:   https://arquivos.b3.com.br/bdi/tabelas
Saída:   data/b3_series_historicas.csv

A B3 disponibiliza endpoint de download direto via POST/GET com parâmetros
de data. O scraper consulta o período dos últimos 7 dias úteis e retorna
o CSV consolidado.
"""
import os
import sys
import datetime
from io import StringIO

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


# Endpoint de download direto da B3 para tabelas BDI / séries históricas
DOWNLOAD_URL = "https://arquivos.b3.com.br/api/download/requestname"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://arquivos.b3.com.br",
    "Referer": "https://arquivos.b3.com.br/bdi/tabelas",
}


class B3SeriesHistoricasScraper(BaseScraper):
    name = "b3_series_historicas"

    def fetch(self) -> pd.DataFrame:
        data_final = datetime.date.today()
        data_inicial = data_final - datetime.timedelta(days=7)

        dt_ini_str = data_inicial.strftime("%Y-%m-%d")
        dt_fim_str = data_final.strftime("%Y-%m-%d")

        self.logger.info(f"Período: {dt_ini_str} → {dt_fim_str}")

        # Parâmetros para Renda Fixa / Negociação Consolidada
        params = {
            "fileName": "ConsolidatedRecords",
            "fileType": "true",  # indica Renda Fixa
            "startDate": dt_ini_str,
            "endDate": dt_fim_str,
            "language": "pt-BR",
        }

        session = requests.Session()
        resp = session.get(DOWNLOAD_URL, params=params, headers=HEADERS, timeout=120)
        resp.raise_for_status()

        # A resposta pode ser JSON com uma URL final ou o CSV diretamente
        content_type = resp.headers.get("Content-Type", "")
        if "json" in content_type:
            data = resp.json()
            file_url = data.get("url") or data.get("download_url")
            if not file_url:
                raise RuntimeError(f"URL de download não encontrada na resposta: {data}")
            resp = session.get(file_url, headers=HEADERS, timeout=120)
            resp.raise_for_status()

        # Detecta encoding
        encoding = "utf-8"
        if "latin" in content_type or "iso-8859" in content_type:
            encoding = "latin-1"

        text = resp.content.decode(encoding, errors="replace")
        sep = ";" if text.count(";") > text.count(",") else ","

        df = pd.read_csv(StringIO(text), sep=sep, encoding=encoding)
        df.columns = [str(c).strip() for c in df.columns]
        df.insert(0, "dt_captura", data_final)
        return df


if __name__ == "__main__":
    scraper = B3SeriesHistoricasScraper()
    scraper.run()
