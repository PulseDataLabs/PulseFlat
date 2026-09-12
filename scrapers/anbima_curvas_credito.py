"""
scrapers/anbima_curvas_credito.py
---------------------------------
Coleta oficial das curvas de crédito corporativo da ANBIMA,
apresentando spreads médios de debêntures por nota de rating (AAA, AA, A, etc.)
e vértices de prazo em anos.

Gera data/anbima_curvas_credito.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_curvas_credito")


class AnbimaCurvasCreditoScraper(BaseAnbimaDataScraper):
    name = "anbima_curvas_credito"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia", "vertice_anos"]

    title = "ANBIMA — Curvas de Crédito Corporativo por Rating"
    description = (
        "Spreads médios oficiais de crédito corporativo (em % sobre a taxa soberana) "
        "apurados pela ANBIMA para debêntures, organizados por classificação de rating "
        "(AAA, AA, A) ao longo de vértices de prazos (em anos)."
    )
    icon = "📈"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = ["anbima", "curvas_credito", "spreads", "ratings", "debentures", "modelagem", "api"]
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

        # Tenta data_ref e, se ainda não divulgada (HTTP 404), tenta até 3 dias úteis anteriores
        curr = data_ref
        for _ in range(4):
            data_str = curr.strftime("%Y-%m-%d")
            try:
                res = self.client.get(
                    "/feed/precos-indices/v1/debentures/curvas-credito",
                    params={"data": data_str},
                )
                if isinstance(res, dict):
                    res = res.get("content", [])
                if isinstance(res, list) and res:
                    dados = res
                    break
            except Exception:
                self.logger.info(
                    f"Curvas de crédito ainda não disponíveis para {data_str}, buscando data anterior..."
                )
            curr = _CAL.offset(curr, -1)

        if not dados:
            self.logger.warning("Nenhum dado de Curvas de Crédito encontrado.")
            return pd.DataFrame()

        self.logger.info(
            f"Coleta de Curvas de Crédito para {data_str}: {len(dados)} vértices encontrados."
        )

        data_captura_padrao, _ = agora_brt()
        registros = []

        def clean_n(val, dec=4):
            if val is None:
                return ""
            try:
                f = float(val)
                return f"{f:.{dec}f}".rstrip("0").rstrip(".")
            except (ValueError, TypeError):
                return str(val) if val is not None else ""

        for item in dados:
            v_anos = item.get("vertice_anos")
            if v_anos is None:
                continue

            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": data_str,
                "vertice_anos": clean_n(v_anos, dec=2),
                "aaa": clean_n(item.get("aaa"), dec=4),
                "aa": clean_n(item.get("aa"), dec=4),
                "a": clean_n(item.get("a"), dec=4),
            }
            for k, v in item.items():
                if k not in ("data_referencia", "vertice_anos", "aaa", "aa", "a"):
                    rec[k] = clean_n(v, dec=4)

            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["vertice_anos"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaCurvasCreditoScraper().run()


if __name__ == "__main__":
    main()
