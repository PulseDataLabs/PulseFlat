#!/usr/bin/env python
# coding: utf-8
"""
Scraper: Yahoo Finance – Séries de preços/cotações
Fonte:   https://query2.finance.yahoo.com/v8/finance/chart/
Saída:   data/yahoo_finance_series.csv

Baixa séries históricas de fechamento para todos os tickers configurados
em TICKERS abaixo. Adicione ou remova conforme a necessidade do projeto.
"""
import os
import sys
import time
import datetime

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


# Tickers a capturar: (ticker_yahoo, label)
# Ajuste conforme os benchmarks de interesse do PulseFlat
TICKERS = [
    ("^BVSP", "IBOVESPA"),
    ("BRL=X", "USD_BRL"),
    ("GLD", "OURO_GLD"),
    ("^TNX", "TREASURY_10Y"),
]

YAHOO_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://finance.yahoo.com/",
    "Origin": "https://finance.yahoo.com",
}

API_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"

# Período de captura: últimos 30 dias (ajustável)
DAYS_BACK = 30


def _fetch_ticker(session: requests.Session, ticker: str, label: str, dt_ini: int, dt_fim: int) -> pd.DataFrame:
    url = API_URL.format(ticker=ticker)
    params = {
        "period1": dt_ini,
        "period2": dt_fim,
        "interval": "1d",
        "events": "history",
        "includeAdjustedClose": "true",
    }
    resp = session.get(url, params=params, headers=YAHOO_HEADERS, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    result = data.get("chart", {}).get("result", [])
    if not result:
        return pd.DataFrame()

    timestamps = result[0].get("timestamp", [])
    closes = result[0].get("indicators", {}).get("quote", [{}])[0].get("close", [])

    df = pd.DataFrame({"timestamp": timestamps, "close": closes})
    df["data_referencia"] = pd.to_datetime(df["timestamp"], unit="s").dt.normalize().dt.date
    df["codigo_ativo"] = ticker
    df["label"] = label
    df["preco_fechamento"] = pd.to_numeric(df["close"], errors="coerce")
    df["preco_fechamento"] = df["preco_fechamento"].ffill()

    return df[["data_referencia", "codigo_ativo", "label", "preco_fechamento"]]


class YahooFinanceSeriesScraper(BaseScraper):
    name = "yahoo_finance_series"
    group = "misc"
    enabled = True
    phase = 1

    def fetch(self) -> pd.DataFrame:
        from scripts.utils.ux import print_done, print_warn

        hoje = datetime.date.today()
        dt_fim = int(datetime.datetime.combine(hoje, datetime.time()).timestamp())
        dt_ini = int(
            datetime.datetime.combine(
                hoje - datetime.timedelta(days=DAYS_BACK), datetime.time()
            ).timestamp()
        )

        session = requests.Session()
        frames = []
        n = len(TICKERS)

        for i, (ticker, label) in enumerate(TICKERS, 1):
            t0 = time.time()
            try:
                df = _fetch_ticker(session, ticker, label, dt_ini, dt_fim)
                if not df.empty:
                    frames.append(df)
                print_done(f"({i}/{n}) {ticker} ({label})", elapsed=time.time() - t0)
            except Exception as e:
                print_warn(f"({i}/{n}) {ticker}: {e}")

        session.close()

        if not frames:
            raise RuntimeError("Nenhuma série baixada do Yahoo Finance.")

        return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    scraper = YahooFinanceSeriesScraper()
    scraper.run()
