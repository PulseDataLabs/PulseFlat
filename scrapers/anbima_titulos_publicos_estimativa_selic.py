"""
scrapers/anbima_titulos_publicos_estimativa_selic.py
---------------------------------------------------
Coleta oficial diária da estimativa da taxa Selic apurada pela ANBIMA
para fins de fechamento e precificação de mercado.

Gera data/anbima_titulos_publicos_estimativa_selic.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_titulos_publicos_estimativa_selic")


class AnbimaTitulosPublicosEstimativaSelicScraper(BaseAnbimaDataScraper):
    name = "anbima_titulos_publicos_estimativa_selic"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia"]

    title = "ANBIMA — Estimativa Oficial da Taxa Selic"
    description = (
        "Estimativa diária da taxa Selic oficial apurada pela ANBIMA para o fechamento de mercado, "
        "utilizada na precificação de títulos públicos federais e ativos de crédito privado."
    )
    icon = "🎯"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "anbima",
        "selic",
        "taxa_juros",
        "macroeconomia",
        "titulos_publicos",
        "renda_fixa",
        "api",
    ]
    source = "ANBIMA Data (developers.anbima.com.br)"

    def _obter_data_referencia(self) -> date:
        if self.target_date:
            return self.target_date
        return _CAL.offset(date.today(), -1)

    def fetch(self) -> pd.DataFrame:
        if not self.check_credentials():
            self.logger.warning("Credenciais da ANBIMA não configuradas.")
            return pd.DataFrame()

        data_ref = self._obter_data_referencia()
        dados = None
        data_str = None

        curr = data_ref
        for _ in range(4):
            data_str = curr.strftime("%Y-%m-%d")
            try:
                res = self.client.get(
                    "/feed/precos-indices/v1/titulos-publicos/estimativa-selic",
                    params={"data": data_str},
                )
                if isinstance(res, dict):
                    res = res.get("content", [])
                if isinstance(res, list) and res:
                    dados = res
                    break
            except Exception:
                self.logger.info(
                    f"Estimativa Selic ainda não disponível para {data_str}, tentando dia anterior..."
                )
            curr = _CAL.offset(curr, -1)

        if not dados:
            self.logger.warning("Nenhum dado de estimativa Selic encontrado.")
            return pd.DataFrame()

        self.logger.info(
            f"Coleta de estimativa Selic para {data_str}: {len(dados)} registros encontrados."
        )

        data_captura_padrao, _ = agora_brt()
        registros = []

        def clean_s(val):
            if val is None:
                return ""
            s = str(val).strip()
            return "" if s in ("-", "--", "nan", "None") else s

        def clean_n(val, dec=4):
            if val is None:
                return ""
            try:
                f = float(val)
                return f"{f:.{dec}f}".rstrip("0").rstrip(".")
            except (ValueError, TypeError):
                return clean_s(val)

        for item in dados:
            dt_item = clean_s(item.get("data_referencia")) or data_str
            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": dt_item,
                "estimativa_taxa_selic": clean_n(item.get("estimativa_taxa_selic"), dec=4),
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

        return df


def main():
    AnbimaTitulosPublicosEstimativaSelicScraper().run()


if __name__ == "__main__":
    main()
