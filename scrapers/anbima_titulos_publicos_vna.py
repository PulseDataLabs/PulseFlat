"""
scrapers/anbima_titulos_publicos_vna.py
---------------------------------------
Coleta oficial do Valor Nominal Atualizado (VNA) diário de títulos públicos federais
(NTN-B, NTN-C, LFT) apurados pela ANBIMA via API oficial ANBIMA Data.

Gera data/anbima_titulos_publicos_vna.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_titulos_publicos_vna")


class AnbimaTitulosPublicosVnaScraper(BaseAnbimaDataScraper):
    name = "anbima_titulos_publicos_vna"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia", "tipo_titulo"]

    title = "ANBIMA — Títulos Públicos Federais (VNA Oficial)"
    description = (
        "Série histórica oficial do Valor Nominal Atualizado (VNA) de títulos públicos federais "
        "(NTN-B, NTN-C e LFT) apurado e divulgado diariamente pela ANBIMA com base nos indexadores oficiais."
    )
    icon = "💵"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = ["anbima", "vna", "titulos_publicos", "ntnb", "lft", "ntnc", "ipca", "selic", "api"]
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
        dados_item = None
        data_str = None

        curr = data_ref
        for _ in range(4):
            data_str = curr.strftime("%Y-%m-%d")
            try:
                res = self.client.get(
                    "/feed/precos-indices/v1/titulos-publicos/vna",
                    params={"data": data_str},
                )
                if isinstance(res, list) and res:
                    dados_item = res[0]
                    break
                elif isinstance(res, dict) and res.get("titulos"):
                    dados_item = res
                    break
            except Exception:
                self.logger.info(
                    f"VNA ainda não disponível para {data_str}, tentando dia anterior..."
                )
            curr = _CAL.offset(curr, -1)

        if not dados_item or not dados_item.get("titulos"):
            self.logger.warning("Nenhum dado de VNA encontrado.")
            return pd.DataFrame()

        titulos_lista = dados_item.get("titulos", [])
        self.logger.info(
            f"Coleta de VNA para {data_str}: {len(titulos_lista)} títulos encontrados."
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

        for t in titulos_lista:
            tipo = clean_s(t.get("tipo_titulo"))
            if not tipo:
                continue

            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": data_str,
                "tipo_titulo": tipo,
                "codigo_selic": clean_s(t.get("codigo_selic")),
                "vna": clean_n(t.get("vna"), dec=6),
                "index": clean_n(t.get("index"), dec=4),
                "tipo_correcao": clean_s(t.get("tipo_correcao")),
                "data_validade": clean_s(t.get("data_validade")),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["tipo_titulo"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaTitulosPublicosVnaScraper().run()


if __name__ == "__main__":
    main()
