from pathlib import Path

# coding: utf-8
"""
Scraper: Yahoo Finance – FIIs e Fiagros B3
Fonte:   https://finance.yahoo.com
Saída:   data/yahoo_fiis_fiagros.csv
"""

import datetime
import os
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper

DYNAMIC_CSV = "b3_fundos_listados.csv"
DYNAMIC_FILTERS = ["FII", "FIAGRO"]
DYNAMIC_SUFFIX = ".SA"
YAHOO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
    "Referer": "https://finance.yahoo.com/",
    "Origin": "https://finance.yahoo.com",
}
API_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
DAYS_BACK = 30


def _fetch_ticker(
    session: requests.Session, ticker: str, label: str, dt_ini: int, dt_fim: int
) -> pd.DataFrame:
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
    df["data_referencia"] = (
        pd.to_datetime(df["timestamp"], unit="s").dt.normalize().dt.date
    )
    df["codigo_ativo"] = ticker
    df["label"] = label
    df["preco_fechamento"] = pd.to_numeric(df["close"], errors="coerce")
    df["preco_fechamento"] = df["preco_fechamento"].ffill()

    return df[["data_referencia", "codigo_ativo", "label", "preco_fechamento"]]


class YahooFiisFiagrosScraper(BaseScraper):
    name = "yahoo_fiis_fiagros"
    group = "misc"
    enabled = True
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]
    title = "Yahoo Finance — FIIs e FIAGROs"
    description = "Cotações diárias, volume e histórico dos principais Fundos de Investimento Imobiliário (FIIs) e FIAGROs de maior liquidez negociados na B3 (HGLG11, KNIP11, MXRF11, XPLG11, etc.)."

    def fetch(self) -> pd.DataFrame:

        dt_ini_date = self.start_date
        dt_fim_date = self.end_date

        if dt_ini_date is None:
            hoje = datetime.date.today()
            dt_ini_date = hoje - datetime.timedelta(days=DAYS_BACK)
        if dt_fim_date is None:
            dt_fim_date = datetime.date.today()

        dt_fim = int(
            datetime.datetime.combine(dt_fim_date, datetime.time()).timestamp()
        )
        dt_ini = int(
            datetime.datetime.combine(dt_ini_date, datetime.time()).timestamp()
        )

        # Resolve tickers list
        tickers_list = []
        root_dir = Path(__file__).resolve().parents[1]
        custom_csv = root_dir / "data" / "custom_tickers.csv"
        if custom_csv.exists():
            try:
                df_custom = pd.read_csv(custom_csv)
                df_filtered = df_custom[df_custom["category"] == "yahoo_fiis_fiagros"]
                for _, row in df_filtered.iterrows():
                    tickers_list.append(
                        (str(row["ticker"]).strip(), str(row["label"]).strip())
                    )
            except Exception as e:
                self.logger.warning(f"Erro ao carregar custom_tickers.csv: {e}")

        if DYNAMIC_CSV:
            csv_path = root_dir / "data" / DYNAMIC_CSV
            if csv_path.exists():
                try:
                    df_b3 = pd.read_csv(csv_path)
                    if DYNAMIC_FILTERS and "tipo_fundo" in df_b3.columns:
                        df_b3 = df_b3[df_b3["tipo_fundo"].isin(DYNAMIC_FILTERS)]
                    col = (
                        "codigo_fundo"
                        if "codigo_fundo" in df_b3.columns
                        else "codigo_ativo"
                    )
                    if col in df_b3.columns:
                        codes = df_b3[col].dropna().unique()
                        for code in codes:
                            code_str = str(code).strip()
                            if code_str:
                                ticker_yahoo = (
                                    f"{code_str}{DYNAMIC_SUFFIX}"
                                    if DYNAMIC_SUFFIX
                                    else code_str
                                )
                                tickers_list.append((ticker_yahoo, code_str))
                except Exception as e:
                    self.logger.warning(f"Erro ao carregar B3 tickers dinâmicos: {e}")

        # Deduplicate tickers_list based on first element (ticker)
        seen = set()
        dedup_tickers = []
        for t, l in tickers_list:
            if t not in seen:
                seen.add(t)
                dedup_tickers.append((t, l))

        session = requests.Session()
        frames = []

        for i, (ticker, label) in enumerate(dedup_tickers, 1):
            try:
                df = _fetch_ticker(session, ticker, label, dt_ini, dt_fim)
                if not df.empty:
                    frames.append(df)
            except Exception:
                pass

        session.close()

        if not frames:
            raise RuntimeError("Nenhuma série baixada do Yahoo Finance.")

        return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    YahooFiisFiagrosScraper().run()
