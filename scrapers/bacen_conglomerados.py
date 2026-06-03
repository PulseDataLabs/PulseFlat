#!/usr/bin/env python
# coding: utf-8
"""
Scraper: BACEN – Conglomerados Financeiros
Fonte:   https://www.bcb.gov.br/content/estabilidadefinanceira/relacao_instituicoes_funcionamento/
Saída:   data/bacen_conglomerados.csv

Baixa o arquivo ZIP mensal (YYYYMMCONGLOMERADO.zip), extrai o XLSX
e retorna o conteúdo normalizado.
"""
import os
import sys
import datetime
import zipfile
from io import BytesIO
from dateutil.relativedelta import relativedelta

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


BASE_URL = (
    "https://www.bcb.gov.br/content/estabilidadefinanceira/"
    "relacao_instituicoes_funcionamento/Conglomerados/"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}


def _try_download(session: requests.Session, yyyymm: str) -> bytes | None:
    file_name = f"{yyyymm}CONGLOMERADO.zip"
    url = BASE_URL + file_name
    resp = session.get(url, headers=HEADERS, timeout=120)
    if resp.status_code == 200:
        return resp.content
    return None


class BacenConglomeradosScraper(BaseScraper):
    name = "bacen_conglomerados"

    def fetch(self) -> pd.DataFrame:
        session = requests.Session()

        # Tenta o mês anterior; se não disponível, tenta mais um mês atrás
        hoje = datetime.date.today()
        for meses_atras in (1, 2, 3):
            ref = hoje - relativedelta(months=meses_atras)
            yyyymm = ref.strftime("%Y%m")
            self.logger.info(f"Tentando arquivo {yyyymm}CONGLOMERADO.zip")
            content = _try_download(session, yyyymm)
            if content:
                break
        else:
            raise RuntimeError("Nenhum arquivo de conglomerados disponível nos últimos 3 meses.")

        # Extrai XLSX do ZIP em memória
        with zipfile.ZipFile(BytesIO(content)) as zf:
            xlsx_names = [n for n in zf.namelist() if n.endswith(".xlsx")]
            if not xlsx_names:
                raise RuntimeError("Nenhum XLSX encontrado no arquivo ZIP.")
            xlsx_bytes = zf.read(xlsx_names[0])

        df = pd.read_excel(BytesIO(xlsx_bytes), engine="openpyxl")
        df.columns = [str(c).strip() for c in df.columns]
        df.insert(0, "dt_referencia", ref.replace(day=1))
        return df


if __name__ == "__main__":
    scraper = BacenConglomeradosScraper()
    scraper.run()
