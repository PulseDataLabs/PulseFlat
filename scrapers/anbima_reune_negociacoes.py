"""
scrapers/anbima_reune_negociacoes.py
------------------------------------
Coleta oficial das negociações secundárias registradas no sistema REUNE da ANBIMA
(Registro de Operações de Crédito Privado - Debêntures, CRI, CRA), trazendo
o tape analítico operação a operação com hora, quantidade, volume, PU e taxa.

Gera data/anbima_reune_negociacoes.csv.gz com acumulação diária.
"""

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("anbima_reune_negociacoes")


class AnbimaReuneNegociacoesScraper(BaseAnbimaDataScraper):
    name = "anbima_reune_negociacoes"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    chaves_dedup = [
        "data_operacao",
        "hora_operacao",
        "codigo_ativo",
        "qtd_negociada",
        "vl_pu_negociado",
        "taxa_negociada",
    ]

    title = "ANBIMA — REUNE Negociações (Tape de Crédito Privado)"
    description = (
        "Registro oficial individualizado das operações fechadas no mercado secundário de crédito privado "
        "(debêntures, CRI, CRA) apuradas no sistema REUNE da ANBIMA, com hora, emissor, volume, PU e taxa negociada."
    )
    icon = "⚡"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "anbima",
        "reune",
        "negociacoes",
        "trades",
        "credito_privado",
        "debentures",
        "cri",
        "cra",
        "liquidez",
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
        dados = []
        data_str = None

        curr = data_ref
        for _ in range(4):
            data_str = curr.strftime("%Y-%m-%d")
            try:
                primeira_pag = self.client.get(
                    "/feed/precos-indices/v1/reune/negociacoes",
                    params={"data": data_str, "page": 0},
                )
                if isinstance(primeira_pag, dict) and primeira_pag.get("content"):
                    total_pages = primeira_pag.get("total_pages", 1)
                    dados.extend(primeira_pag["content"])

                    if total_pages > 1:
                        self.logger.info(
                            f"REUNE para {data_str}: {total_pages} páginas ({primeira_pag.get('total_elements')} registros). Baixando páginas restantes em paralelo..."
                        )

                        def baixar_pagina(pg, dt=data_str):
                            res = self.client.get(
                                "/feed/precos-indices/v1/reune/negociacoes",
                                params={"data": dt, "page": pg},
                            )
                            return res.get("content", []) if isinstance(res, dict) else []

                        with ThreadPoolExecutor(max_workers=4) as executor:
                            futures = [
                                executor.submit(baixar_pagina, pg) for pg in range(1, total_pages)
                            ]
                            for fut in as_completed(futures):
                                try:
                                    items = fut.result()
                                    if items:
                                        dados.extend(items)
                                except Exception as e:
                                    self.logger.warning(f"Erro ao baixar página REUNE: {e}")

                    break
            except Exception:
                self.logger.info(
                    f"Negociações do REUNE ainda não disponíveis para {data_str}, tentando dia anterior..."
                )
            curr = _CAL.offset(curr, -1)

        if not dados:
            self.logger.warning("Nenhuma negociação do REUNE encontrada.")
            return pd.DataFrame()

        self.logger.info(
            f"Coleta de negociações do REUNE para {data_str}: {len(dados)} operações encontradas."
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
            dt_op = clean_s(item.get("data_operacao")) or data_str
            cod_ativo = clean_s(item.get("codigo_ativo"))
            if not cod_ativo:
                continue

            rec = {
                "data_captura": data_captura_padrao,
                "data_operacao": dt_op,
                "hora_operacao": clean_s(item.get("hora_operacao")),
                "tipo_ativo": clean_s(item.get("tipo_ativo")),
                "codigo_ativo": cod_ativo,
                "isin": clean_s(item.get("isin")),
                "emissor": clean_s(item.get("emissor")),
                "cnpj_emissor": clean_s(item.get("cnpj_emissor")),
                "emissao": clean_s(item.get("emissao")),
                "data_emissao": clean_s(item.get("data_emissao")),
                "data_vencimento": clean_s(item.get("data_vencimento")),
                "data_liquidacao": clean_s(item.get("data_liquidacao")),
                "tipo_liquidacao": clean_s(item.get("tipo_liquidacao")),
                "situacao_negociacao": clean_s(item.get("situacao_negociacao")),
                "qtd_negociada": clean_n(item.get("qtd_negociada"), dec=4),
                "vl_pu_negociado": clean_n(item.get("vl_pu_negociado"), dec=6),
                "vl_volume_negociado": clean_n(item.get("vl_volume_negociado"), dec=2),
                "taxa_negociada": clean_n(item.get("taxa_negociada"), dec=4),
                "data_atualizacao": clean_s(item.get("data_atualizacao")),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["data_operacao", "hora_operacao", "codigo_ativo"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]

        return df


def main():
    AnbimaReuneNegociacoesScraper().run()


if __name__ == "__main__":
    main()
