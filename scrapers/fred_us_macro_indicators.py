"""
scrapers/fred_us_macro_indicators.py
------------------------------------
Coleta mensal oficial dos principais indicadores macroeconômicos dos Estados Unidos:
inflação cheia e núcleo (CPI e Core CPI), índice preferido do Fed (PCE e Core PCE),
geração de empregos líquidos (Nonfarm Payroll) e Taxa de Desemprego do St. Louis Fed (FRED).

Gera data/fred_us_macro_indicators.csv.gz com acumulação mensal.
"""

import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.fred_base import BaseFredScraper
from utils.base import agora_brt, get_logger
from utils.parsers import hash_row

log = get_logger("fred_us_macro_indicators")


class FredUsMacroIndicatorsScraper(BaseFredScraper):
    name = "fred_us_macro_indicators"
    group = "fred"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia"]

    title = "FRED — Indicadores Macroeconômicos dos EUA (Inflação e Emprego)"
    description = (
        "Série mensal dos principais indicadores da economia americana apurados via FRED: "
        "CPI Headline e Core, PCE Headline e Core (medidor oficial da meta do Fed), "
        "Nonfarm Payroll (criação de vagas líquidas) e taxa de desemprego (Unemployment Rate)."
    )
    icon = "📊"
    icon_class = "icon-fred"
    badge = "FRED API"
    badge_class = "badge-dynamic"
    tags = [
        "fred",
        "macroeconomia",
        "inflacao_eua",
        "cpi",
        "pce",
        "payroll",
        "desemprego",
        "fed",
        "api",
    ]
    source = "Federal Reserve Economic Data — FRED (stlouisfed.org)"

    SERIES_MAP = {
        "CPIAUCSL": "cpi_headline",
        "CPILFESL": "cpi_core",
        "PCEPI": "pce_headline",
        "PCEPILFE": "pce_core",
        "PAYEMS": "nonfarm_payroll",
        "UNRATE": "unemployment_rate",
    }

    def _obter_janela_datas(self) -> tuple[str, str]:
        if self.start_date and self.end_date:
            dt_inicio = self.start_date
            dt_fim = self.end_date
        else:
            dt_fim = date.today()
            # Janela padrão de 12 meses para dados mensais
            dt_inicio = dt_fim - timedelta(days=365)

        return dt_inicio.strftime("%Y-%m-%d"), dt_fim.strftime("%Y-%m-%d")

    def fetch(self) -> pd.DataFrame:
        if not self.check_credentials():
            self.logger.warning("Credenciais do FRED não configuradas (FRED_API_KEY).")
            return pd.DataFrame()

        start_str, end_str = self._obter_janela_datas()
        self.logger.info(
            f"Consultando indicadores macro dos EUA no FRED de {start_str} a {end_str}..."
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
            self.logger.warning("Nenhuma observação retornada para indicadores macroeconômicos.")
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
                "cpi_headline": clean_n(cols.get("cpi_headline")),
                "cpi_core": clean_n(cols.get("cpi_core")),
                "pce_headline": clean_n(cols.get("pce_headline")),
                "pce_core": clean_n(cols.get("pce_core")),
                "nonfarm_payroll": clean_n(cols.get("nonfarm_payroll"), dec=1),
                "unemployment_rate": clean_n(cols.get("unemployment_rate"), dec=2),
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

        self.logger.info(f"Coleta de macroeconômicos concluída: {len(df)} meses consolidados.")
        return df


def main():
    FredUsMacroIndicatorsScraper().run()


if __name__ == "__main__":
    main()
