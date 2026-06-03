#!/usr/bin/env python
# coding: utf-8
"""
Scraper: BACEN – Última data disponível dos balancetes de bancos
Fonte:   https://www.bcb.gov.br/api/servico/sitebcb/Documentos/byListGuid
Saída:   data/bacen_balancetes_bancos.csv

O endpoint JSON retorna a lista de documentos; capturamos apenas
a data mais recente disponível.
"""
import os
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


URL = (
    "https://www.bcb.gov.br/api/servico/sitebcb/Documentos/byListGuid"
    "?tronco=estabilidadefinanceira"
    "&guidLista=a11917e4-c729-4259-bd4e-0266827b6acd"
    "&ordem=DataDocumento%20desc"
    "&pasta=/Bancos"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


class BacenBalancetesBancosScraper(BaseScraper):
    name = "bacen_balancetes_bancos"

    def fetch(self) -> pd.DataFrame:
        self.logger.info(f"Consultando: {URL}")
        resp = requests.get(URL, headers=HEADERS, timeout=60)
        resp.raise_for_status()

        data = resp.json()
        df_docs = pd.DataFrame(data.get("conteudo", []))

        if df_docs.empty:
            raise RuntimeError("Nenhum documento retornado pela API do BCB.")

        df_docs["DataDocumento"] = pd.to_datetime(df_docs["DataDocumento"])
        ultima_data = df_docs["DataDocumento"].max().date()
        self.logger.info(f"Última data disponível: {ultima_data}")

        df = pd.DataFrame([{"data": ultima_data}])
        return df


if __name__ == "__main__":
    scraper = BacenBalancetesBancosScraper()
    scraper.run()
