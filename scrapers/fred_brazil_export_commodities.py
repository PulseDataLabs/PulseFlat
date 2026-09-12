"""
scrapers/fred_brazil_export_commodities.py
-------------------------------------------
Coleta séries mensais oficiais de preços globais de commodities exportadas pelo Brasil
apuradas pelo FMI (Fundo Monetário Internacional) via FRED:
- Minério de Ferro (PIORECRUSDM) - USD por tonelada métrica
- Soja (PSOYBUSDM) - USD por tonelada métrica
- Petróleo Brent (POILBREUSDM) - USD por barril
- Açúcar Mercado Livre (PSUGAUSAUSDM) - USD por centavo/libra
- Café Arábica Suave (PCOFFOTMUSDM) - USD por centavo/libra

Gera data/fred_brazil_export_commodities.csv.gz com acumulação mensal.
"""

import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.fred_base import BaseFredScraper
from utils.base import agora_brt, get_logger
from utils.parsers import hash_row

log = get_logger("fred_brazil_export_commodities")


class FredBrazilExportCommoditiesScraper(BaseFredScraper):
    name = "fred_brazil_export_commodities"
    group = "fred"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia"]

    title = "FRED / FMI — Commodities Globais da Pauta Exportadora do Brasil"
    description = (
        "Preços globais mensais das 5 principais commodities que determinam a balança "
        "comercial brasileira e o fluxo cambial do Real: Minério de Ferro, Soja, "
        "Petróleo Brent, Açúcar e Café Arábica, apuradas pelo Fundo Monetário Internacional (FMI)."
    )
    icon = "🚢"
    icon_class = "icon-fred"
    badge = "FRED / IMF"
    badge_class = "badge-dynamic"
    tags = [
        "fred",
        "imf",
        "fmi",
        "commodities",
        "minerio_ferro",
        "soja",
        "petroleo",
        "acucar",
        "cafe",
        "exportacao",
        "balanca_comercial",
        "api",
    ]
    source = "Federal Reserve Economic Data — FRED / International Monetary Fund (IMF)"

    SERIES_MAP = {
        "PIORECRUSDM": "minerio_ferro_global_usd",
        "PSOYBUSDM": "soja_global_usd",
        "POILBREUSDM": "petroleo_brent_global_usd",
        "PSUGAUSAUSDM": "acucar_global_usd",
        "PCOFFOTMUSDM": "cafe_arabica_global_usd",
    }

    def _obter_janela_datas(self) -> tuple[str, str]:
        if self.target_date:
            dt_fim = self.target_date
            dt_inicio = dt_fim - timedelta(days=365)
        elif self.start_date and self.end_date:
            dt_inicio = self.start_date
            dt_fim = self.end_date
        else:
            dt_fim = date.today()
            # Padrão de 730 dias para cobrir 2 anos em execuções regulares
            dt_inicio = dt_fim - timedelta(days=730)

        return dt_inicio.strftime("%Y-%m-%d"), dt_fim.strftime("%Y-%m-%d")

    def fetch(self) -> pd.DataFrame:
        if not self.check_credentials():
            self.logger.warning("Credenciais do FRED não configuradas (FRED_API_KEY).")
            return pd.DataFrame()

        start_str, end_str = self._obter_janela_datas()
        self.logger.info(
            f"Consultando commodities da pauta brasileira no FRED/FMI de {start_str} a {end_str}..."
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
            self.logger.warning("Nenhuma observação retornada para commodities de exportação.")
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
                "minerio_ferro_global_usd": clean_n(cols.get("minerio_ferro_global_usd"), dec=2),
                "soja_global_usd": clean_n(cols.get("soja_global_usd"), dec=2),
                "petroleo_brent_global_usd": clean_n(cols.get("petroleo_brent_global_usd"), dec=2),
                "acucar_global_usd": clean_n(cols.get("acucar_global_usd"), dec=4),
                "cafe_arabica_global_usd": clean_n(cols.get("cafe_arabica_global_usd"), dec=4),
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

        self.logger.info(
            f"Coleta de commodities brasileiras concluída: {len(df)} meses consolidados."
        )
        return df


def main():
    FredBrazilExportCommoditiesScraper().run()


if __name__ == "__main__":
    main()
