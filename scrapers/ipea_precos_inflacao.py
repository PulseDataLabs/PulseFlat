"""
Scraper: IPEADATA – Preços e Inflação
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/ipea_precos_inflacao.csv
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper

SERIES = [
    {
        "code": "IGP12_IGPDI12",
        "title": "IGP-DI Índice Geral",
        "desc": "Índice Geral de Preços - Disponibilidade Interna (IGP-DI) - índice (ago 1994 = 100)",
        "icon": "📊",
        "tags": ["igp_di", "inflacao", "ipea"],
    },
    {
        "code": "IGP12_INCC12",
        "title": "INCC-DI Índice Geral",
        "desc": "Índice Nacional de Custo da Construção - Disponibilidade Interna (INCC-DI) - índice (ago 1994 = 100)",
        "icon": "🏗",
        "tags": ["incc_di", "construcao", "ipea"],
    },
    {
        "code": "PRECOS12_INPC12",
        "title": "INPC Índice Geral",
        "desc": "Índice Nacional de Preços ao Consumidor (INPC) - geral - índice (dez 1993 = 100)",
        "icon": "📊",
        "tags": ["inpc", "inflacao", "ipea"],
    },
    {
        "code": "PRECOS12_INPCBR12",
        "title": "INPC Taxa de Variação",
        "desc": "Índice Nacional de Preços ao Consumidor (INPC) - geral - taxa de variação (% a.m.)",
        "icon": "📈",
        "tags": ["inpc", "inflacao", "ipea"],
    },
]
API_URL = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{code}')"


class IpeaPrecosInflacaoScraper(BaseScraper):
    name = "ipea_precos_inflacao"
    group = "misc"
    enabled = False
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    def fetch(self) -> pd.DataFrame:
        session = self.get_session()
        frames = []

        for item in SERIES:
            url = API_URL.format(code=item["code"])
            resp = session.get(url, timeout=60)
            resp.raise_for_status()
            data = resp.json()

            values = data.get("value", [])
            if not values:
                continue

            records = []
            for val_item in values:
                raw_date = val_item.get("VALDATA", "")
                if "T" in raw_date:
                    date_ref = raw_date.split("T")[0]
                else:
                    date_ref = raw_date[:10]

                val = val_item.get("VALVALOR")
                if val is None:
                    continue

                records.append(
                    {
                        "data_referencia": date_ref,
                        "codigo_ativo": item["code"],
                        "label": item["title"],
                        "valor": float(val),
                    }
                )

            if records:
                frames.append(pd.DataFrame(records))

        session.close()

        if not frames:
            raise RuntimeError("Nenhum dado retornado para as séries do Ipea.")

        df = pd.concat(frames, ignore_index=True)

        # Filtros de data em memória se target_date ou start/end_date estiverem definidos
        if self.target_date:
            target_str = self.target_date.strftime("%Y-%m-%d")
            df = df[df["data_referencia"] == target_str]
        elif self.start_date or self.end_date:
            if self.start_date:
                df = df[df["data_referencia"] >= self.start_date.strftime("%Y-%m-%d")]
            if self.end_date:
                df = df[df["data_referencia"] <= self.end_date.strftime("%Y-%m-%d")]

        return df


if __name__ == "__main__":
    IpeaPrecosInflacaoScraper().run()
