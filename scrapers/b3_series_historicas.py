#!/usr/bin/env python
# coding: utf-8
"""
Scraper: B3 – Séries Históricas de Renda Fixa (Negociação Consolidada)
Fonte:   https://arquivos.b3.com.br/bdi/tabelas
Saída:   data/b3_series_historicas.csv
"""
import datetime
import sys
import time
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.utils.base import BaseScraper
from scripts.utils.ux import print_warn

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
    group = "b3"
    enabled = True
    phase = 1
    accumulate = True

    # Catálogo de Metadados
    title = "B3 Séries Históricas"
    description = "Séries históricas de negociação consolidada de Renda Fixa da B3."
    icon = "📈"
    icon_class = "icon-b3"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = ["renda fixa", "bdi", "negociação consolidada", "B3"]
    source = "B3"

    def fetch(self) -> pd.DataFrame:
        data_final = datetime.date.today()
        session = requests.Session()
        resp = None

        try:
            for attempt in range(5):
                data_inicial = data_final - datetime.timedelta(days=7)
                dt_ini_str = data_inicial.strftime("%Y-%m-%d")
                dt_fim_str = data_final.strftime("%Y-%m-%d")

                params = {
                    "fileName": "ConsolidatedRecords",
                    "fileType": "true",  # indica Renda Fixa
                    "startDate": dt_ini_str,
                    "endDate": dt_fim_str,
                    "language": "pt-BR",
                }

                retries_429 = 0
                while True:
                    time.sleep(2)
                    resp = session.get(
                        REQUEST_URL, params=params, headers=HEADERS, timeout=60
                    )
                    if resp.status_code == 429 and retries_429 < 3:
                        retries_429 += 1
                        print_warn(f"limite 429 ({retries_429}/3), aguardando 5s")
                        time.sleep(5)
                        continue
                    break

                if resp.status_code == 404:
                    print_warn(
                        f"dados não disponíveis para {dt_fim_str}, retrocedendo 1 dia"
                    )
                    data_final -= datetime.timedelta(days=1)
                    time.sleep(1)
                    continue
                resp.raise_for_status()
                break
            else:
                print_warn("nenhum período disponível na B3")
                return pd.DataFrame()

            content_type = resp.headers.get("Content-Type", "")
            if "json" in content_type:
                data = resp.json()
                token = data.get("token")
                if not token:
                    print_warn("token de download não encontrado")
                    return pd.DataFrame()
                time.sleep(2)
                resp = session.get(
                    DOWNLOAD_URL, params={"token": token}, headers=HEADERS, timeout=60
                )
                resp.raise_for_status()
                content_type = resp.headers.get("Content-Type", "")

            encoding = "utf-8"
            if "latin" in content_type or "iso-8859" in content_type:
                encoding = "latin-1"

            text = resp.content.decode(encoding, errors="replace")
            sep = ";" if text.count(";") > text.count(",") else ","

            df = pd.read_csv(StringIO(text), sep=sep, encoding=encoding)
            df.columns = [str(c).strip() for c in df.columns]
            df.insert(0, "data_captura", data_final.strftime("%Y-%m-%d"))
            return df
        except Exception as e:
            print_warn(f"erro ao baixar: {e}")
            return pd.DataFrame()


if __name__ == "__main__":
    scraper = B3SeriesHistoricasScraper()
    scraper.run()
