"""
scrapers/anbima_titulos_publicos_mercado_secundario.py
------------------------------------------------------
Coleta oficial de preços e taxas indicativas do mercado secundário
de Títulos Públicos Federais (TPF) apurados pela ANBIMA (LTN, LFT, NTN-B, NTN-F).

Gera data/anbima_titulos_publicos_mercado_secundario.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_titulos_publicos_mercado_secundario")


class AnbimaTitulosPublicosMercadoSecundarioScraper(BaseAnbimaDataScraper):
    name = "anbima_titulos_publicos_mercado_secundario"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia", "codigo_selic", "data_vencimento"]

    title = "ANBIMA — Títulos Públicos Federais (Mercado Secundário e Preços)"
    description = (
        "Boletim diário oficial de preços unitários (PU), taxas indicativas, taxas de compra/venda "
        "e intervalos estatísticos de negociação no mercado secundário de títulos públicos federais "
        "(LTN, LFT, NTN-B e NTN-F) apurados pela ANBIMA junto aos dealers de mercado."
    )
    icon = "🏛️"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "anbima",
        "titulos_publicos",
        "tpf",
        "mercado_secundario",
        "precos",
        "taxas",
        "tesouro",
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
                    "/feed/precos-indices/v1/titulos-publicos/mercado-secundario-TPF",
                    params={"data": data_str},
                )
                if isinstance(res, dict):
                    res = res.get("content", [])
                if isinstance(res, list) and res:
                    dados = res
                    break
            except Exception:
                self.logger.info(
                    f"Mercado secundário TPF ainda não disponível para {data_str}, tentando dia anterior..."
                )
            curr = _CAL.offset(curr, -1)

        if not dados:
            self.logger.warning("Nenhum dado de TPF mercado secundário encontrado.")
            return pd.DataFrame()

        self.logger.info(
            f"Coleta de TPF mercado secundário para {data_str}: {len(dados)} títulos encontrados."
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
            tipo = clean_s(item.get("tipo_titulo"))
            selic = clean_s(item.get("codigo_selic"))
            venc = clean_s(item.get("data_vencimento"))
            if not tipo or not selic:
                continue

            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": data_str,
                "tipo_titulo": tipo,
                "codigo_selic": selic,
                "codigo_isin": clean_s(item.get("codigo_isin")),
                "data_vencimento": venc,
                "data_base": clean_s(item.get("data_base")),
                "expressao": clean_s(item.get("expressao")),
                "taxa_indicativa": clean_n(item.get("taxa_indicativa"), dec=4),
                "taxa_compra": clean_n(item.get("taxa_compra"), dec=4),
                "taxa_venda": clean_n(item.get("taxa_venda"), dec=4),
                "pu": clean_n(item.get("pu"), dec=6),
                "desvio_padrao": clean_n(item.get("desvio_padrao"), dec=6),
                "intervalo_min_d0": clean_n(item.get("intervalo_min_d0"), dec=4),
                "intervalo_max_d0": clean_n(item.get("intervalo_max_d0"), dec=4),
                "intervalo_min_d1": clean_n(item.get("intervalo_min_d1"), dec=4),
                "intervalo_max_d1": clean_n(item.get("intervalo_max_d1"), dec=4),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["tipo_titulo", "data_vencimento"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaTitulosPublicosMercadoSecundarioScraper().run()


if __name__ == "__main__":
    main()
