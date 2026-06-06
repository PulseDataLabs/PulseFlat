#!/usr/bin/env python
# coding: utf-8
"""
Scraper: ANBIMA Matriz de Probabilidade de Resgate (FLIQ)
Fonte:   https://databricks-reports.anbima.com.br/fliq/
Saída:   data/anbima_matriz_probabilidade_resgate.csv

Os arquivos são mensais, nomeados report_fliq_YYYYMM.csv.
O scraper baixa o arquivo do mês anterior (última disponibilidade confirmada).
"""
import os
import sys
import datetime
import calendar

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


BASE_URL = "https://databricks-reports.anbima.com.br/fliq"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}


def _ultimo_dia_mes_anterior() -> datetime.date:
    hoje = datetime.date.today()
    mes = hoje.month - 1
    ano = hoje.year
    if mes == 0:
        mes = 12
        ano -= 1
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    return datetime.date(ano, mes, ultimo_dia)


class AnbimaMatrizProbabilidadeResgateScraper(BaseScraper):
    name = "anbima_matriz_probabilidade_resgate"
    group = "anbima"
    enabled = True
    phase = 1

    def fetch(self) -> pd.DataFrame:
        data_ref = _ultimo_dia_mes_anterior()
        file_name = f"report_fliq_{data_ref.strftime('%Y%m')}.csv"
        url = f"{BASE_URL}/{file_name}"

        resp = requests.get(url, headers=HEADERS, timeout=120)

        if resp.status_code == 404 or "NoSuchKey" in resp.text:
            mes = data_ref.month - 1
            ano = data_ref.year
            if mes == 0:
                mes = 12
                ano -= 1
            ultimo_dia = calendar.monthrange(ano, mes)[1]
            data_ref = datetime.date(ano, mes, ultimo_dia)
            file_name = f"report_fliq_{data_ref.strftime('%Y%m')}.csv"
            url = f"{BASE_URL}/{file_name}"
            from scripts.utils.ux import print_warn
            print_warn("arquivo não encontrado, tentando mês anterior")
            resp = requests.get(url, headers=HEADERS, timeout=120)

        resp.raise_for_status()

        from io import StringIO
        df = pd.read_csv(StringIO(resp.text), sep=",", encoding="utf-8")
        df.insert(0, "dt_referencia", data_ref)
        return df


if __name__ == "__main__":
    scraper = AnbimaMatrizProbabilidadeResgateScraper()
    scraper.run()
