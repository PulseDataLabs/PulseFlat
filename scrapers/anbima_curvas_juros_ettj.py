"""
scrapers/anbima_curvas_juros_ettj.py
------------------------------------
Coleta oficial da Estrutura a Termo das Taxas de Juros (ETTJ) - Curvas Zero-Cupom
de títulos públicos federais apuradas pela ANBIMA (Prefixadas, IPCA e Inflação Implícita).

Gera data/anbima_curvas_juros_ettj.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_curvas_juros_ettj")


class AnbimaCurvasJurosEttjScraper(BaseAnbimaDataScraper):
    name = "anbima_curvas_juros_ettj"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia", "vertice_du"]

    title = "ANBIMA — Curvas de Juros ETTJ (Taxas Zero-Cupom TPF)"
    description = (
        "Estrutura a Termo das Taxas de Juros (ETTJ) oficial da ANBIMA, contendo as curvas "
        "de juros zero-cupom ponto a ponto por vértice de dias úteis (DU) para taxas prefixadas, "
        "taxas reais (IPCA) e inflação implícita apuradas a partir de títulos públicos federais."
    )
    icon = "📉"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "anbima",
        "ettj",
        "curvas_juros",
        "zero_cupom",
        "titulos_publicos",
        "ipca",
        "prefixado",
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
        dados_item = None
        data_str = None

        curr = data_ref
        for _ in range(4):
            data_str = curr.strftime("%Y-%m-%d")
            try:
                res = self.client.get(
                    "/feed/precos-indices/v1/titulos-publicos/curvas-juros",
                    params={"data": data_str},
                )
                if isinstance(res, list) and res:
                    dados_item = res[0]
                    break
                elif isinstance(res, dict) and res.get("ettj"):
                    dados_item = res
                    break
            except Exception:
                self.logger.info(
                    f"ETTJ ainda não disponível para {data_str}, tentando dia anterior..."
                )
            curr = _CAL.offset(curr, -1)

        if not dados_item or not dados_item.get("ettj"):
            self.logger.warning("Nenhum dado de curva ETTJ encontrado.")
            return pd.DataFrame()

        pontos_ettj = dados_item.get("ettj", [])
        self.logger.info(
            f"Coleta de Curvas ETTJ para {data_str}: {len(pontos_ettj)} vértices encontrados."
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

        for p in pontos_ettj:
            vertice_du = p.get("vertice_du")
            if vertice_du is None:
                continue

            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": data_str,
                "vertice_du": str(int(vertice_du)),
                "taxa_prefixadas": clean_n(p.get("taxa_prefixadas"), dec=4),
                "taxa_ipca": clean_n(p.get("taxa_ipca"), dec=4),
                "taxa_implicita": clean_n(p.get("taxa_implicita"), dec=4),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df["vertice_du_int"] = df["vertice_du"].astype(int)
            df.sort_values(by=["vertice_du_int"], inplace=True)
            df.drop(columns=["vertice_du_int"], inplace=True)
            df.reset_index(drop=True, inplace=True)

            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaCurvasJurosEttjScraper().run()


if __name__ == "__main__":
    main()
