"""
scrapers/anbima_indices_idka_resultados.py
------------------------------------------
Coleta oficial dos resultados diários dos Índices de Duração Constante ANBIMA (IDKA),
incluindo IDkA Pré (3M, 1A, 2A, 3A, 5A) e IDkA IPCA (2A, 3A, 5A, 10A, 15A, 20A, 30A),
com número-índice, taxas indicativas e variações diárias, mensais e anuais.

Gera data/anbima_indices_idka_resultados.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_indices_idka_resultados")


class AnbimaIndicesIdkaResultadosScraper(BaseAnbimaDataScraper):
    name = "anbima_indices_idka_resultados"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia", "nome"]

    title = "ANBIMA — Resultados do Índice IDKA (Duração Constante)"
    description = (
        "Resultados e variações oficiais diárias da família dos Índices de Duração Constante da ANBIMA (IDKA), "
        "cobrindo prazos fixos em vértices Prefixados e IPCA (3M até 30A), com número-índice, taxas e volatilidade."
    )
    icon = "⏱️"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "anbima",
        "idka",
        "indices",
        "duracao_constante",
        "renda_fixa",
        "titulos_publicos",
        "benchmark",
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
                    "/feed/precos-indices/v1/indices/resultados-idka",
                    params={"data": data_str},
                )
                if isinstance(res, dict):
                    res = res.get("content", [])
                if isinstance(res, list) and res:
                    dados = res
                    break
            except Exception:
                self.logger.info(
                    f"Resultados IDKA ainda não disponíveis para {data_str}, tentando dia anterior..."
                )
            curr = _CAL.offset(curr, -1)

        if not dados:
            self.logger.warning("Nenhum resultado do IDKA encontrado.")
            return pd.DataFrame()

        self.logger.info(
            f"Coleta de resultados do IDKA para {data_str}: {len(dados)} índices encontrados."
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
            nome = clean_s(item.get("nome") or item.get("indice"))
            if not nome:
                continue

            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": data_str,
                "nome": nome,
                "numero_indice": clean_n(item.get("numero_indice"), dec=6),
                "tx_compra": clean_n(item.get("tx_compra"), dec=4),
                "tx_venda": clean_n(item.get("tx_venda"), dec=4),
                "variacao_diaria": clean_n(item.get("variacao_diaria"), dec=4),
                "variacao_mensal": clean_n(item.get("variacao_mensal"), dec=4),
                "variacao_anual": clean_n(item.get("variacao_anual"), dec=4),
                "variacao_ult12m": clean_n(item.get("variacao_ult12m"), dec=4),
                "volatilidade": clean_n(item.get("volatilidade"), dec=4),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["nome"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaIndicesIdkaResultadosScraper().run()


if __name__ == "__main__":
    main()
