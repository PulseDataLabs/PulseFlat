"""
scrapers/anbima_indice_ida.py
-----------------------------
Coleta oficial dos resultados diários do Índice de Debêntures ANBIMA (IDA)
e de todos os seus subíndices (IDA-Geral, IDA-DI, IDA-IPCA, IDA-IPCA Infraestrutura,
IDA-IPCA Ex-Infraestrutura) via API oficial ANBIMA Data.

Gera data/anbima_indice_ida.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_indice_ida")


class AnbimaIndiceIdaScraper(BaseAnbimaDataScraper):
    name = "anbima_indice_ida"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia", "indice"]

    title = "ANBIMA — Índice IDA (Índice de Debêntures ANBIMA)"
    description = (
        "Resultados oficiais diários de fechamento da família do Índice de Debêntures ANBIMA (IDA), "
        "incluindo IDA-Geral, IDA-DI, IDA-IPCA, IDA-IPCA Infraestrutura e IDA-IPCA Ex-Infraestrutura, "
        "com número-índice, rentabilidade (diária, mensal, anual, 12M, 24M), duration e valor de mercado."
    )
    icon = "🏆"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "anbima",
        "ida",
        "indices",
        "debentures",
        "credito_privado",
        "benchmark",
        "rentabilidade",
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
                    "/feed/precos-indices/v1/indices/resultados-ida-fechado",
                    params={"data": data_str},
                )
                if isinstance(res, dict):
                    res = res.get("content", [])
                if isinstance(res, list) and res:
                    dados = res
                    break
            except Exception:
                self.logger.info(
                    f"Resultados IDA ainda não disponíveis para {data_str}, tentando dia anterior..."
                )
            curr = _CAL.offset(curr, -1)

        if not dados:
            self.logger.warning("Nenhum resultado do IDA encontrado.")
            return pd.DataFrame()

        self.logger.info(
            f"Coleta de resultados do IDA para {data_str}: {len(dados)} índices encontrados."
        )

        data_captura_padrao, _ = agora_brt()
        registros = []

        def clean_s(val):
            if val is None:
                return ""
            s = str(val).strip()
            return "" if s in ("-", "--", "nan", "None") else s

        def clean_n(val, dec=6):
            if val is None:
                return ""
            try:
                f = float(val)
                return f"{f:.{dec}f}".rstrip("0").rstrip(".")
            except (ValueError, TypeError):
                return clean_s(val)

        for item in dados:
            indice = clean_s(item.get("indice"))
            if not indice:
                continue

            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": data_str,
                "indice": indice,
                "numero_indice": clean_n(item.get("numero_indice"), dec=6),
                "variacao_diaria": clean_n(item.get("variacao_diaria"), dec=4),
                "variacao_mensal": clean_n(item.get("variacao_mensal"), dec=4),
                "variacao_anual": clean_n(item.get("variacao_anual"), dec=4),
                "variacao_ult12m": clean_n(item.get("variacao_ult12m"), dec=4),
                "variacao_ult24m": clean_n(item.get("variacao_ult24m"), dec=4),
                "duration": clean_n(item.get("duration"), dec=2),
                "peso": clean_n(item.get("peso"), dec=4),
                "valor_mercado": clean_n(item.get("valor_mercado"), dec=2),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["indice"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaIndiceIdaScraper().run()


if __name__ == "__main__":
    main()
