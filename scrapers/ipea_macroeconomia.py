"""
Scraper: IPEADATA – Macroeconomia Geral
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/ipea_macroeconomia.csv
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper

SERIES = [
    {
        "code": "BM12_PIBAC12",
        "title": "PIB Acumulado 12m",
        "desc": "PIB acumulado em 12 meses (R$)",
        "icon": "📈",
        "tags": ["pib", "macroeconomia", "ipea"],
    },
    {
        "code": "PNADC12_TDESOC12",
        "title": "Taxa de Desocupação",
        "desc": "Taxa de desocupação da PNAD Contínua (%)",
        "icon": "👥",
        "tags": ["desemprego", "trabalho", "ipea"],
    },
    {
        "code": "GAC12_SALMINRE12",
        "title": "Salário Mínimo Real",
        "desc": "Salário mínimo real mensal (em R$ do último mês)",
        "icon": "💰",
        "tags": ["salario_minimo", "renda", "ipea"],
    },
    {
        "code": "MTE12_SALMIN12",
        "title": "Salário Mínimo Vigente",
        "desc": "Salário mínimo vigente nominal (R$)",
        "icon": "💰",
        "tags": ["salario_minimo", "renda", "ipea"],
    },
    {
        "code": "SGS12_7836",
        "title": "Saldo da Poupança",
        "desc": "Saldo total de depósitos em poupança SBPE e rural (R$ milhões)",
        "icon": "🏦",
        "tags": ["poupanca", "saldo", "ipea"],
    },
]
API_URL = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{code}')"


class IpeaMacroeconomiaScraper(BaseScraper):
    name = "ipea_macroeconomia"
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
    IpeaMacroeconomiaScraper().run()
