"""
scrapers/anbima_indices_carteira_teorica_ima.py
-----------------------------------------------
Coleta oficial da composição analítica e ponderação das carteiras teóricas
da família de índices IMA (Índice de Mercado ANBIMA - IMA-B, IRF-M, IMA-S, etc.),
detalhando cada título público federal componente, PU, quantidade e peso percentual.

Gera data/anbima_indices_carteira_teorica_ima.csv.gz com acumulação por vigência/mês.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_indices_carteira_teorica_ima")


class AnbimaIndicesCarteiraTeoricaImaScraper(BaseAnbimaDataScraper):
    name = "anbima_indices_carteira_teorica_ima"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_inicio", "indice", "codigo_isin"]

    title = "ANBIMA — Carteira Teórica do Índice IMA (Títulos Públicos)"
    description = (
        "Composição oficial e pesos dos títulos públicos federais integrantes de cada carteira teórica "
        "mensal da família do Índice de Mercado ANBIMA (IMA-B, IMA-B 5, IRF-M, IMA-S, etc.), com PU, peso e duration."
    )
    icon = "🏛️"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "anbima",
        "ima",
        "carteira_teorica",
        "composicao",
        "indices",
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
                    "/feed/precos-indices/v1/indices/carteira-teorica-ima",
                    params={"data": data_str},
                )
                if isinstance(res, dict):
                    res = res.get("content", [])
                if isinstance(res, list) and res:
                    dados = res
                    break
            except Exception:
                self.logger.info(
                    f"Carteira teórica IMA ainda não disponível para {data_str}, tentando dia anterior..."
                )
            curr = _CAL.offset(curr, -1)

        if not dados:
            self.logger.warning("Nenhuma carteira teórica do IMA encontrada.")
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

        for grupo in dados:
            indice = clean_s(grupo.get("indice"))
            dt_inicio = clean_s(grupo.get("data_inicio"))
            dt_fim = clean_s(grupo.get("data_fim"))
            referencias = grupo.get("referencias", [])

            for ref in referencias:
                isin = clean_s(ref.get("codigo_isin"))
                tipo_tit = clean_s(ref.get("tipo_titulo"))
                if not isin and not tipo_tit:
                    continue

                rec = {
                    "data_captura": data_captura_padrao,
                    "data_referencia": data_str,
                    "indice": indice,
                    "data_inicio": dt_inicio,
                    "data_fim": dt_fim,
                    "tipo_titulo": tipo_tit,
                    "codigo_selic_titulo": clean_s(ref.get("codigo_selic_titulo")),
                    "codigo_isin": isin,
                    "data_vencimento": clean_s(ref.get("data_vencimento")),
                    "pu": clean_n(ref.get("pu"), dec=6),
                    "quantidade_indice": clean_n(ref.get("quantidade_indice"), dec=4),
                    "peso": clean_n(ref.get("peso"), dec=4),
                    "duration": clean_n(ref.get("duration"), dec=2),
                }
                registros.append(rec)

        self.logger.info(
            f"Coleta de carteira teórica do IMA para {data_str}: {len(registros)} títulos componentes encontrados."
        )

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["indice", "tipo_titulo", "data_vencimento"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaIndicesCarteiraTeoricaImaScraper().run()


if __name__ == "__main__":
    main()
