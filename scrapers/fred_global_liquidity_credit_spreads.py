"""
scrapers/fred_global_liquidity_credit_spreads.py
------------------------------------------------
Coleta diária oficial dos indicadores de liquidez monetária do Federal Reserve
(Fed Funds Effective Rate, SOFR), spreads de crédito corporativo globais da ICE BofA
(Investment Grade, High Yield e Mercados Emergentes), VIX e índice DXY do St. Louis Fed (FRED).

Gera data/fred_global_liquidity_credit_spreads.csv.gz com acumulação diária.
"""

import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.fred_base import BaseFredScraper
from utils.base import agora_brt, get_logger
from utils.parsers import hash_row

log = get_logger("fred_global_liquidity_credit_spreads")


class FredGlobalLiquidityCreditSpreadsScraper(BaseFredScraper):
    name = "fred_global_liquidity_credit_spreads"
    group = "fred"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia"]

    title = "FRED — Liquidez Global e Spreads de Crédito Corporativo"
    description = (
        "Indicadores diários de política monetária global (Effective Fed Funds, SOFR), apetite a risco "
        "e spreads de crédito corporativo globais (ICE BofA US Corp IG, US High Yield, Emerging Markets High Yield), "
        "índice VIX e DXY Broad U.S. Dollar Index apurados via FRED."
    )
    icon = "🌐"
    icon_class = "icon-fred"
    badge = "FRED API"
    badge_class = "badge-dynamic"
    tags = [
        "fred",
        "liquidez_global",
        "sofr",
        "fed_funds",
        "spreads_credito",
        "high_yield",
        "vix",
        "dolar",
        "api",
    ]
    source = "Federal Reserve Economic Data — FRED (stlouisfed.org)"

    SERIES_MAP = {
        "DFF": "fed_funds_rate",
        "SOFR": "sofr_rate",
        "BAMLC0A0CM": "credit_spread_corp_ig",
        "BAMLH0A0HYM2": "credit_spread_corp_hy",
        "BAMLEMHBHYCRPIEY": "credit_spread_em_hy",
        "VIXCLS": "vix",
        "DTWEXBGS": "dxy_broad",
    }

    def _obter_janela_datas(self) -> tuple[str, str]:
        if self.target_date:
            dt_fim = self.target_date
            dt_inicio = dt_fim - timedelta(days=7)
        elif self.start_date and self.end_date:
            dt_inicio = self.start_date
            dt_fim = self.end_date
        else:
            dt_fim = date.today()
            dt_inicio = dt_fim - timedelta(days=30)

        return dt_inicio.strftime("%Y-%m-%d"), dt_fim.strftime("%Y-%m-%d")

    def fetch(self) -> pd.DataFrame:
        if not self.check_credentials():
            self.logger.warning("Credenciais do FRED não configuradas (FRED_API_KEY).")
            return pd.DataFrame()

        start_str, end_str = self._obter_janela_datas()
        self.logger.info(
            f"Consultando liquidez e spreads globais no FRED de {start_str} a {end_str}..."
        )

        dados_por_data: dict[str, dict[str, str]] = {}

        for sid, col_name in self.SERIES_MAP.items():
            try:
                obs_list = self.fetch_series(sid, start_date=start_str, end_date=end_str)
                for obs in obs_list:
                    dt = obs.get("date")
                    val = obs.get("value", "").strip()
                    if not dt or val in (".", "", "nan", "None"):
                        continue
                    if dt not in dados_por_data:
                        dados_por_data[dt] = {}
                    dados_por_data[dt][col_name] = val
            except Exception as e:
                self.logger.warning(f"Erro ao consultar série {sid} no FRED: {e}")

        if not dados_por_data:
            self.logger.warning("Nenhuma observação retornada para liquidez e spreads globais.")
            return pd.DataFrame()

        data_captura_padrao, _ = agora_brt()
        registros = []

        def clean_n(val, dec=4):
            if not val:
                return ""
            try:
                f = float(val)
                return f"{f:.{dec}f}".rstrip("0").rstrip(".")
            except (ValueError, TypeError):
                return str(val).strip()

        for dt, cols in sorted(dados_por_data.items()):
            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": dt,
                "fed_funds_rate": clean_n(cols.get("fed_funds_rate")),
                "sofr_rate": clean_n(cols.get("sofr_rate")),
                "credit_spread_corp_ig": clean_n(cols.get("credit_spread_corp_ig")),
                "credit_spread_corp_hy": clean_n(cols.get("credit_spread_corp_hy")),
                "credit_spread_em_hy": clean_n(cols.get("credit_spread_em_hy")),
                "vix": clean_n(cols.get("vix")),
                "dxy_broad": clean_n(cols.get("dxy_broad")),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["data_referencia"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        self.logger.info(f"Coleta de liquidez e spreads concluída: {len(df)} datas consolidadas.")
        return df


def main():
    FredGlobalLiquidityCreditSpreadsScraper().run()


if __name__ == "__main__":
    main()
