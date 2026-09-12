"""
scrapers/anbima_letras_financeiras.py
-------------------------------------
Coleta oficial das matrizes de curvas e taxas de Letras Financeiras (LF)
por emissor bancário via API oficial ANBIMA Developers (ANBIMA Data).

Gera data/anbima_letras_financeiras.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_letras_financeiras")


class AnbimaLetrasFinanceirasScraper(BaseAnbimaDataScraper):
    name = "anbima_letras_financeiras"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia", "cnpj_emissor", "letra_financeira", "vertice_meses"]

    title = "ANBIMA — Letras Financeiras (Matrizes de Vértices por Emissor)"
    description = (
        "Matriz diária oficial de taxas indicativas, taxas de compra e venda de Letras Financeiras "
        "(LFs) por instituição bancária emissora e por vértices de prazos (em meses), apuradas pela ANBIMA."
    )
    icon = "🏦"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = ["anbima", "letras_financeiras", "bancos", "renda_fixa", "taxas", "curvas", "api"]
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
        data_str = data_ref.strftime("%Y-%m-%d")
        self.logger.info(f"Iniciando coleta de Letras Financeiras para: {data_str}")

        try:
            dados = self.client.get(
                "/feed/precos-indices/v1/letras-financeiras/matrizes-vertices-emissor",
                params={"data": data_str},
            )
        except Exception as e:
            self.logger.error(f"Erro na consulta de Letras Financeiras: {e}")
            return pd.DataFrame()

        if isinstance(dados, dict):
            dados = dados.get("content", [])
        if not isinstance(dados, list):
            dados = []

        self.logger.info(f"Retornados {len(dados)} emissores de Letras Financeiras.")
        if not dados:
            return pd.DataFrame()

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
            emissor = clean_s(item.get("emissor"))
            cnpj = clean_s(item.get("cnpj_emissor"))
            lf_tipo = clean_s(item.get("letra_financeira"))
            indexador = clean_s(item.get("indexador"))
            fluxo = clean_s(item.get("fluxo"))

            for v in item.get("vertices", []):
                vertice_m = clean_s(v.get("vertice"))
                if not vertice_m:
                    continue

                rec = {
                    "data_captura": data_captura_padrao,
                    "data_referencia": data_str,
                    "emissor": emissor,
                    "cnpj_emissor": cnpj,
                    "letra_financeira": lf_tipo,
                    "indexador": indexador,
                    "fluxo": fluxo,
                    "vertice_meses": vertice_m,
                    "taxa_indicativa": clean_n(v.get("taxa_indicativa"), dec=4),
                    "taxa_compra": clean_n(v.get("taxa_compra"), dec=4),
                    "taxa_venda": clean_n(v.get("taxa_venda"), dec=4),
                }
                registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["emissor", "letra_financeira", "vertice_meses"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaLetrasFinanceirasScraper().run()


if __name__ == "__main__":
    main()
