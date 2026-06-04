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
import time
from io import StringIO

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


# Endpoint de download direto da B3 para tabelas BDI / séries históricas
REQUEST_URL = "https://drp.b3.com.br/api/download/requestname"
DOWNLOAD_URL = "https://drp.b3.com.br/api/download"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://drp.b3.com.br",
    "Referer": "https://arquivos.b3.com.br/bdi/tabelas",
}


class B3SeriesHistoricasScraper(BaseScraper):
    name = "b3_series_historicas"

    def fetch(self) -> pd.DataFrame:
        data_final = datetime.date.today()
        session = requests.Session()
        resp = None

        try:
            for attempt in range(5):
                data_inicial = data_final - datetime.timedelta(days=7)
                dt_ini_str = data_inicial.strftime("%Y-%m-%d")
                dt_fim_str = data_final.strftime("%Y-%m-%d")

                self.logger.info(f"Tentativa {attempt + 1}: Período {dt_ini_str} → {dt_fim_str}")

                params = {
                    "fileName": "ConsolidatedRecords",
                    "fileType": "true",  # indica Renda Fixa
                    "startDate": dt_ini_str,
                    "endDate": dt_fim_str,
                    "language": "pt-BR",
                }

                retries_429 = 0
                while True:
                    time.sleep(6)  # Garante intervalo mínimo de 6s para evitar limite de taxa
                    resp = session.get(REQUEST_URL, params=params, headers=HEADERS, timeout=120)
                    if resp.status_code == 429 and retries_429 < 3:
                        retries_429 += 1
                        self.logger.warning(f"Limite de requisições atingido (429). Aguardando 11 segundos (tentativa {retries_429}/3)...")
                        time.sleep(11)
                        continue
                    break

                if resp.status_code == 404:
                    self.logger.warning(f"Dados não disponíveis para {dt_fim_str}. Retrocedendo 1 dia...")
                    data_final -= datetime.timedelta(days=1)
                    time.sleep(1)
                    continue
                resp.raise_for_status()
                break
            else:
                self.logger.warning("Não foi possível encontrar um período de dados disponível na B3.")
                return pd.DataFrame()

            content_type = resp.headers.get("Content-Type", "")
            if "json" in content_type:
                data = resp.json()
                token = data.get("token")
                if not token:
                    self.logger.warning(f"Token de download não encontrado na resposta: {data}")
                    return pd.DataFrame()
                time.sleep(6)  # Garante intervalo mínimo para o download
                resp = session.get(DOWNLOAD_URL, params={"token": token}, headers=HEADERS, timeout=120)
                resp.raise_for_status()
                content_type = resp.headers.get("Content-Type", "")

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
        except Exception as e:
            self.logger.warning(f"Erro ao baixar séries históricas da B3: {e}")
            return pd.DataFrame()


if __name__ == "__main__":
    scraper = B3SeriesHistoricasScraper()
    scraper.run()
