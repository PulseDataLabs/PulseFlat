# coding: utf-8
"""
Scraper: IPEADATA – Taxas de Juros
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/ipea_taxas_juros.csv
"""

import os
import sys
import datetime
import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper

SERIES = [{'code': 'ANBIMA12_TJPOUP12', 'title': 'Poupança Rentabilidade Antiga', 'desc': 'Rentabilidade mensal da poupança para depósitos até 03/05/2012 (% a.m.)', 'icon': '💵', 'tags': ['juros', 'poupanca', 'ipea']}, {'code': 'BM12_RNDPO12', 'title': 'Poupança Rentabilidade Nova', 'desc': 'Rentabilidade mensal da poupança para depósitos a partir de 04/05/2012 (% a.m.)', 'icon': '💵', 'tags': ['juros', 'poupanca', 'ipea']}, {'code': 'ANBIMA12_TJTLN112', 'title': 'Taxa LTN 1m', 'desc': 'Taxa de juros prefixada - estrutura a termo - LTN - 1 mês (% a.m.)', 'icon': '🏛', 'tags': ['juros', 'ltn', 'ipea']}, {'code': 'ANBIMA12_TJTLN312', 'title': 'Taxa LTN 3m', 'desc': 'Taxa de juros prefixada - estrutura a termo - LTN - 3 meses (% a.m.)', 'icon': '🏛', 'tags': ['juros', 'ltn', 'ipea']}, {'code': 'ANBIMA12_TJTLN612', 'title': 'Taxa LTN 6m', 'desc': 'Taxa de juros prefixada - estrutura a termo - LTN - 6 meses (% a.m.)', 'icon': '🏛', 'tags': ['juros', 'ltn', 'ipea']}, {'code': 'ANBIMA12_TJTLN1212', 'title': 'Taxa LTN 12m', 'desc': 'Taxa de juros prefixada - estrutura a termo - LTN - 12 meses (% a.m.)', 'icon': '🏛', 'tags': ['juros', 'ltn', 'ipea']}, {'code': 'BM12_TJCDI12', 'title': 'Taxa CDI Mensal', 'desc': 'Taxa de juros - CDI / Over - acumulada no mês (% a.m.)', 'icon': '📊', 'tags': ['juros', 'cdi', 'ipea']}, {'code': 'BM12_TJLP12', 'title': 'Taxa TJLP', 'desc': 'Taxa de Juros de Longo Prazo (TJLP) (% a.m.)', 'icon': '🏭', 'tags': ['juros', 'tjlp', 'ipea']}, {'code': 'BM12_TJOVER12', 'title': 'Taxa Selic Mensal', 'desc': 'Taxa de juros - Over / Selic - acumulada no mês (% a.m.)', 'icon': '💰', 'tags': ['juros', 'selic', 'ipea']}, {'code': 'BM12_TJTBF12', 'title': 'Taxa TBF', 'desc': 'Taxa Básica Financeira (TBF) - 1º dia do mês (% a.m.)', 'icon': '📈', 'tags': ['juros', 'tbf', 'ipea']}, {'code': 'BM12_TJTR12', 'title': 'Taxa TR', 'desc': 'Taxa Referencial (TR) - 1º dia do mês (% a.m.)', 'icon': '🏠', 'tags': ['juros', 'tr', 'ipea']}]
API_URL = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{code}')"


class IpeaTaxasJurosScraper(BaseScraper):
    name = "ipea_taxas_juros"
    group = "misc"
    enabled = True
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

                records.append({
                    "data_referencia": date_ref,
                    "codigo_ativo": item["code"],
                    "label": item["title"],
                    "valor": float(val),
                })
            
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
    IpeaTaxasJurosScraper().run()
