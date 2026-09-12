"""
scrapers/fred_us_treasuries_yield_curve.py
------------------------------------------
Coleta diária oficial da estrutura a termo da curva soberana dos EUA (US Treasuries),
taxas zero-cupom nominais (3M, 2Y, 5Y, 10Y, 30Y), spread de inclinação 10Y-2Y
e taxas de inflação implícita (Break-Even Inflation 5Y e 10Y via TIPS) do St. Louis Fed (FRED).

Gera data/fred_us_treasuries_yield_curve.csv.gz com acumulação diária.
"""

import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.fred_base import BaseFredScraper
from utils.base import agora_brt, get_logger
from utils.parsers import hash_row

log = get_logger("fred_us_treasuries_yield_curve")


class FredUsTreasuriesYieldCurveScraper(BaseFredScraper):
    name = "fred_us_treasuries_yield_curve"
    group = "fred"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia"]

    title = "FRED — Curva de Juros dos US Treasuries (Soberano EUA)"
    description = (
        "Estrutura a termo da curva soberana americana diária (Treasury Constant Maturity Rates de 3M, 2A, 5A, 10A, 30A), "
        "spread 10Y-2Y de inclinação e expectativas de inflação implícita (Break-even de 5 e 10 anos calculadas via TIPS)."
    )
    icon = "🇺🇸"
    icon_class = "icon-fred"
    badge = "FRED API"
    badge_class = "badge-dynamic"
    tags = [
        "fred",
        "treasuries",
        "curva_juros",
        "soberano_eua",
        "renda_fixa_global",
        "breakeven",
        "macroeconomia",
        "api",
    ]
    source = "Federal Reserve Economic Data — FRED (stlouisfed.org)"

    SERIES_MAP = {
        "DGS3MO": "dgs3mo",
        "DGS2": "dgs2",
        "DGS5": "dgs5",
        "DGS10": "dgs10",
        "DGS30": "dgs30",
        "T10Y2Y": "t10y2y_spread",
        "T5YIE": "t5y_breakeven",
        "T10YIE": "t10y_breakeven",
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
        self.logger.info(f"Consultando curvas do US Treasury no FRED de {start_str} a {end_str}...")

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
            self.logger.warning("Nenhuma observação retornada para a curva de Treasuries.")
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
                "dgs3mo": clean_n(cols.get("dgs3mo")),
                "dgs2": clean_n(cols.get("dgs2")),
                "dgs5": clean_n(cols.get("dgs5")),
                "dgs10": clean_n(cols.get("dgs10")),
                "dgs30": clean_n(cols.get("dgs30")),
                "t10y2y_spread": clean_n(cols.get("t10y2y_spread")),
                "t5y_breakeven": clean_n(cols.get("t5y_breakeven")),
                "t10y_breakeven": clean_n(cols.get("t10y_breakeven")),
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

        self.logger.info(f"Coleta de Treasuries concluída: {len(df)} datas consolidadas.")
        return df


def main():
    FredUsTreasuriesYieldCurveScraper().run()


if __name__ == "__main__":
    main()
