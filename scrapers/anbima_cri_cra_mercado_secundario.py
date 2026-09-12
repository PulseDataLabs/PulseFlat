"""
scrapers/anbima_cri_cra_mercado_secundario.py
---------------------------------------------
Coleta oficial de preços e taxas indicativas do mercado secundário de
Certificados de Recebíveis Imobiliários (CRI) e do Agronegócio (CRA)
via API oficial ANBIMA Developers (ANBIMA Data).

Gera data/anbima_cri_cra_mercado_secundario.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_cri_cra_mercado_secundario")


class AnbimaCriCraMercadoSecundarioScraper(BaseAnbimaDataScraper):
    name = "anbima_cri_cra_mercado_secundario"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia", "codigo_ativo"]

    title = "ANBIMA — CRI e CRA (Mercado Secundário e Preços)"
    description = (
        "Boletim diário oficial de taxas indicativas, preços unitários (PU), duration, "
        "z-spread e percentual REUNE para Certificados de Recebíveis Imobiliários (CRI) "
        "e do Agronegócio (CRA) apurados pela ANBIMA, com identificação do emissor e originador."
    )
    icon = "🌾"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "anbima",
        "cri",
        "cra",
        "credito_privado",
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
        self.logger.info(f"Iniciando coleta de CRI/CRA para: {data_str}")

        try:
            dados = self.client.get(
                "/feed/precos-indices/v1/cri-cra/mercado-secundario",
                params={"data": data_str},
            )
        except Exception as e:
            self.logger.error(f"Erro na consulta de CRI/CRA: {e}")
            return pd.DataFrame()

        if isinstance(dados, dict):
            dados = dados.get("content", [])
        if not isinstance(dados, list):
            dados = []

        self.logger.info(f"Retornados {len(dados)} ativos CRI/CRA.")
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
            ticker = item.get("codigo_ativo")
            if not ticker:
                continue

            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": data_str,
                "codigo_ativo": clean_s(ticker),
                "emissor": clean_s(item.get("emissor")),
                "originador": clean_s(item.get("originador")),
                "originador_credito": clean_s(item.get("originador_credito")),
                "tipo_contrato": clean_s(item.get("tipo_contrato")),
                "serie": clean_s(item.get("serie")),
                "emissao": clean_s(item.get("emissao")),
                "data_vencimento": clean_s(item.get("data_vencimento")),
                "tipo_remuneracao": clean_s(item.get("tipo_remuneracao")),
                "taxa_correcao": clean_n(item.get("taxa_correcao"), dec=4),
                "taxa_indicativa": clean_n(item.get("taxa_indicativa"), dec=4),
                "taxa_compra": clean_n(item.get("taxa_compra"), dec=4),
                "taxa_venda": clean_n(item.get("taxa_venda"), dec=4),
                "pu": clean_n(item.get("pu"), dec=6),
                "duration": clean_n(item.get("duration"), dec=2),
                "z_spread": clean_n(item.get("z_spread"), dec=4),
                "percent_reune": clean_s(item.get("percent_reune")),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["codigo_ativo"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaCriCraMercadoSecundarioScraper().run()


if __name__ == "__main__":
    main()
