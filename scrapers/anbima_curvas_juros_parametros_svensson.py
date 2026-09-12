"""
scrapers/anbima_curvas_juros_parametros_svensson.py
--------------------------------------------------
Coleta oficial diária dos parâmetros dos modelos analíticos Nelson-Siegel-Svensson
(beta 1 a 4, lambda 1 e 2, erro de ajustamento) para as curvas soberanas
de juros Prefixadas e IPCA apuradas pela ANBIMA.

Gera data/anbima_curvas_juros_parametros_svensson.csv.gz com acumulação diária.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_curvas_juros_parametros_svensson")


class AnbimaCurvasJurosParametrosSvenssonScraper(BaseAnbimaDataScraper):
    name = "anbima_curvas_juros_parametros_svensson"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = ["data_referencia", "grupo_indexador"]

    title = "ANBIMA — Curvas de Juros: Parâmetros Svensson"
    description = (
        "Parâmetros analíticos diários dos modelos Nelson-Siegel-Svensson (b1, b2, b3, b4, l1, l2 e erro de ajuste) "
        "para as curvas de juros soberanas Prefixadas e IPCA, permitindo interpolação quantitativa contínua da ETTJ."
    )
    icon = "📐"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "anbima",
        "ettj",
        "svensson",
        "curva_juros",
        "modelos_quantitativos",
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
                    "/feed/precos-indices/v1/titulos-publicos/curvas-juros",
                    params={"data": data_str},
                )
                if isinstance(res, list) and res:
                    dados = res[0]
                    break
                elif isinstance(res, dict) and res:
                    dados = res
                    break
            except Exception:
                self.logger.info(
                    f"Parâmetros Svensson ainda não disponíveis para {data_str}, tentando dia anterior..."
                )
            curr = _CAL.offset(curr, -1)

        if not dados:
            self.logger.warning("Nenhum dado de curvas de juros Svensson encontrado.")
            return pd.DataFrame()

        parametros = dados.get("parametros", [])
        erros = {
            item.get("grupo_indexador"): item.get("valor_erro") for item in dados.get("erros", [])
        }

        self.logger.info(
            f"Coleta de parâmetros Svensson para {data_str}: {len(parametros)} indexadores encontrados."
        )

        data_captura_padrao, _ = agora_brt()
        registros = []

        def clean_s(val):
            if val is None:
                return ""
            s = str(val).strip()
            return "" if s in ("-", "--", "nan", "None") else s

        def clean_n(val, dec=8):
            if val is None:
                return ""
            try:
                f = float(val)
                return f"{f:.{dec}f}".rstrip("0").rstrip(".")
            except (ValueError, TypeError):
                return clean_s(val)

        for p in parametros:
            idx = clean_s(p.get("grupo_indexador"))
            if not idx:
                continue

            erro_val = erros.get(idx)

            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": data_str,
                "grupo_indexador": idx,
                "b1": clean_n(p.get("b1"), dec=8),
                "b2": clean_n(p.get("b2"), dec=8),
                "b3": clean_n(p.get("b3"), dec=8),
                "b4": clean_n(p.get("b4"), dec=8),
                "l1": clean_n(p.get("l1"), dec=8),
                "l2": clean_n(p.get("l2"), dec=8),
                "valor_erro": clean_n(erro_val, dec=8),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["grupo_indexador"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaCurvasJurosParametrosSvenssonScraper().run()


if __name__ == "__main__":
    main()
