"""
scrapers/anbima_projecoes_inflacao.py
------------------------------------
Coleta diária oficial das projeções de inflação (IPCA e IGP-M) apuradas pela ANBIMA
junto às instituições de mercado para o mês corrente e subsequentes.

Gera data/anbima_projecoes_inflacao.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_projecoes_inflacao")


class AnbimaProjecoesInflacaoScraper(BaseAnbimaDataScraper):
    name = "anbima_projecoes_inflacao"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_coleta", "indice", "mes_referencia"]

    title = "ANBIMA — Projeções Oficiais de Inflação (IPCA e IGP-M)"
    description = (
        "Projeções oficiais diárias apuradas pela ANBIMA para os índices de inflação IPCA e IGP-M "
        "(mês corrente e seguintes), utilizadas oficialmente pelo mercado para projeção de VNA e precificação de ativos."
    )
    icon = "📈"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "anbima",
        "inflacao",
        "ipca",
        "igpm",
        "projecoes",
        "macroeconomia",
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
                    "/feed/precos-indices/v1/debentures/projecoes",
                    params={"data": data_str},
                )
                if isinstance(res, dict):
                    res = res.get("content", [])
                if isinstance(res, list) and res:
                    dados = res
                    break
            except Exception:
                self.logger.info(
                    f"Projeções ainda não disponíveis para {data_str}, tentando dia anterior..."
                )
            curr = _CAL.offset(curr, -1)

        if not dados:
            self.logger.warning("Nenhuma projeção de inflação encontrada.")
            return pd.DataFrame()

        self.logger.info(
            f"Coleta de projeções de inflação para {data_str}: {len(dados)} projeções encontradas."
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
            indice = clean_s(item.get("indice"))
            mes_ref = clean_s(item.get("mes_referencia"))
            if not indice or not mes_ref:
                continue

            rec = {
                "data_captura": data_captura_padrao,
                "data_coleta": clean_s(item.get("data_coleta")) or data_str,
                "data_validade": clean_s(item.get("data_validade")),
                "indice": indice,
                "tipo_projecao": clean_s(item.get("tipo_projecao")),
                "mes_referencia": mes_ref,
                "variacao_projetada": clean_n(item.get("variacao_projetada"), dec=4),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["indice", "mes_referencia"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaProjecoesInflacaoScraper().run()


if __name__ == "__main__":
    main()
