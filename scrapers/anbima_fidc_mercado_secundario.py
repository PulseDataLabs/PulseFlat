"""
scrapers/anbima_fidc_mercado_secundario.py
------------------------------------------
Coleta oficial de preços e taxas indicativas de cotas seniores de FIDCs
(Fundos de Investimento em Direitos Creditórios) via API oficial ANBIMA Data.

Gera data/anbima_fidc_mercado_secundario.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_fidc_mercado_secundario")


class AnbimaFidcMercadoSecundarioScraper(BaseAnbimaDataScraper):
    name = "anbima_fidc_mercado_secundario"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia", "codigo_b3"]

    title = "ANBIMA — FIDC (Mercado Secundário e Preços)"
    description = (
        "Boletim oficial diário de preços unitários (PU), taxas indicativas, duration e "
        "parâmetros de negociação para cotas seniores de Fundos de Investimento em "
        "Direitos Creditórios (FIDC) apurados pela ANBIMA."
    )
    icon = "📑"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "anbima",
        "fidc",
        "direitos_creditorios",
        "mercado_secundario",
        "precos",
        "taxas",
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
        data_str = data_ref.strftime("%Y-%m-%d")
        self.logger.info(f"Iniciando coleta de FIDC para: {data_str}")

        try:
            dados = self.client.get(
                "/feed/precos-indices/v1/fidc/mercado-secundario",
                params={"data": data_str},
            )
        except Exception as e:
            self.logger.error(f"Erro na consulta de FIDC: {e}")
            return pd.DataFrame()

        if isinstance(dados, dict):
            dados = dados.get("content", [])
        if not isinstance(dados, list):
            dados = []

        self.logger.info(f"Retornados {len(dados)} ativos FIDC.")
        if not dados:
            return pd.DataFrame()

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
            codigo_b3 = clean_s(item.get("codigo_b3"))
            if not codigo_b3:
                continue

            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": data_str,
                "codigo_b3": codigo_b3,
                "nome": clean_s(item.get("nome")),
                "serie": clean_s(item.get("serie")),
                "emissor": clean_s(item.get("emissor")),
                "isin": clean_s(item.get("isin")),
                "data_vencimento": clean_s(item.get("data_vencimento")),
                "tipo_remuneracao": clean_s(item.get("tipo_remuneracao")),
                "taxa_correcao": clean_n(item.get("taxa_correcao"), dec=4),
                "taxa_indicativa": clean_n(item.get("taxa_indicativa"), dec=4),
                "taxa_compra": clean_n(item.get("taxa_compra"), dec=4),
                "taxa_venda": clean_n(item.get("taxa_venda"), dec=4),
                "pu": clean_n(item.get("pu"), dec=6),
                "percent_pu_par": clean_n(item.get("percent_pu_par"), dec=4),
                "duration": clean_n(item.get("duration"), dec=2),
                "desvio_padrao": clean_n(item.get("desvio_padrao"), dec=4),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["codigo_b3"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaFidcMercadoSecundarioScraper().run()


if __name__ == "__main__":
    main()
