"""
scrapers/fred_brazil_macro_fx_and_cycles.py
--------------------------------------------
Coleta séries internacionais do FRED focadas no Brasil e na dinâmica cambial e de ciclos:
- Câmbio Fed H.10 BRL/USD spot diário (DEXBZUS)
- Taxa de Câmbio Efetiva Real do BIS (RBBRBIS)
- Taxa de Câmbio Efetiva Nominal do BIS (NBBRBIS)
- Indicador Antecedente Composto OCDE CLI para o Brasil (BRALOLITOAASTSAM)
- Confiança do Consumidor OCDE para o Brasil (CSCICP03BRM665S)
- Confiança Empresarial OCDE para o Brasil (BSCICP03BRM665S)
- Spread de Crédito High Yield de Mercados Emergentes ICE BofA (BAMLEMHBHYCRPIOAS)

Gera data/fred_brazil_macro_fx_and_cycles.csv.gz com acumulação por data_referencia.
"""

import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.fred_base import BaseFredScraper
from utils.base import agora_brt, get_logger
from utils.parsers import hash_row

log = get_logger("fred_brazil_macro_fx_and_cycles")


class FredBrazilMacroFxAndCyclesScraper(BaseFredScraper):
    name = "fred_brazil_macro_fx_and_cycles"
    group = "fred"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia"]

    title = "FRED — Brasil: Câmbio Fed/BIS, Ciclos Econômicos OCDE e Risco Emergente"
    description = (
        "Consolidação de séries internacionais apuradas pelo Federal Reserve (H.10), "
        "Banco de Compensações Internacionais (BIS), OCDE e ICE BofA para o Brasil: "
        "câmbio comercial diário Fed, índices REER/NEER do BIS, indicador antecedente (CLI) "
        "e índices de confiança da OCDE, além de spreads de crédito de mercados emergentes."
    )
    icon = "🇧🇷"
    icon_class = "icon-fred"
    badge = "FRED API"
    badge_class = "badge-dynamic"
    tags = [
        "fred",
        "brasil",
        "cambio",
        "reer",
        "bis",
        "ocde",
        "cli",
        "confianca",
        "spread_emergente",
        "macroeconomia",
        "api",
    ]
    source = "Federal Reserve Economic Data — FRED (Fed, BIS, OCDE, ICE BofA)"

    SERIES_MAP = {
        "DEXBZUS": "cambio_brl_usd_fed",
        "RBBRBIS": "reer_bis_brasil",
        "NBBRBIS": "neer_bis_brasil",
        "BRALOLITOAASTSAM": "cli_ocde_brasil",
        "CSCICP03BRM665S": "confianca_consumidor_ocde",
        "BSCICP03BRM665S": "confianca_empresarial_ocde",
        "BAMLEMHBHYCRPIOAS": "spread_high_yield_emergentes_oas",
    }

    def _obter_janela_datas(self) -> tuple[str, str]:
        if self.target_date:
            dt_fim = self.target_date
            dt_inicio = dt_fim - timedelta(days=30)
        elif self.start_date and self.end_date:
            dt_inicio = self.start_date
            dt_fim = self.end_date
        else:
            dt_fim = date.today()
            # Padrão de 365 dias para cobrir séries diárias e mensais
            dt_inicio = dt_fim - timedelta(days=365)

        return dt_inicio.strftime("%Y-%m-%d"), dt_fim.strftime("%Y-%m-%d")

    def fetch(self) -> pd.DataFrame:
        if not self.check_credentials():
            self.logger.warning("Credenciais do FRED não configuradas (FRED_API_KEY).")
            return pd.DataFrame()

        start_str, end_str = self._obter_janela_datas()
        self.logger.info(
            f"Consultando séries internacionais para o Brasil no FRED de {start_str} a {end_str}..."
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
            self.logger.warning("Nenhuma observação retornada para as séries internacionais do Brasil.")
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
                "cambio_brl_usd_fed": clean_n(cols.get("cambio_brl_usd_fed")),
                "reer_bis_brasil": clean_n(cols.get("reer_bis_brasil")),
                "neer_bis_brasil": clean_n(cols.get("neer_bis_brasil")),
                "cli_ocde_brasil": clean_n(cols.get("cli_ocde_brasil")),
                "confianca_consumidor_ocde": clean_n(cols.get("confianca_consumidor_ocde")),
                "confianca_empresarial_ocde": clean_n(cols.get("confianca_empresarial_ocde")),
                "spread_high_yield_emergentes_oas": clean_n(
                    cols.get("spread_high_yield_emergentes_oas"), dec=2
                ),
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
            f"Coleta de séries de câmbio e ciclos do Brasil concluída: {len(df)} datas consolidadas."
        )
        return df


def main():
    FredBrazilMacroFxAndCyclesScraper().run()


if __name__ == "__main__":
    main()
