#!/usr/bin/env python
# coding: utf-8
"""
Scraper: BACEN – Parcelas de Capital (Basileia) via IFData
Fonte:   https://www3.bcb.gov.br/ifdata
Saída:   data/bacen_parcelas_capital_basileia.csv

O site IFData não disponibiliza endpoint REST público para download direto.
A estratégia é consultar a API interna que o próprio site usa para popular
as tabelas de dados, filtrando pelo relatório "Resumo" (parcelas de capital).

Dois conjuntos são capturados:
  - Conglomerados Prudenciais e Instituições Independentes
  - Instituições Individuais
"""
import os
import sys
import datetime
import re
from dateutil.relativedelta import relativedelta

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


# API interna do IFData (descoberta via DevTools)
IFDATA_API = "https://www3.bcb.gov.br/ifdata/rest"
PERIODOS_URL = f"{IFDATA_API}/periodos"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www3.bcb.gov.br/ifdata/",
}

# Tipos de instituição: código usado na API → label descritivo
TIPOS_INST = [
    {"codigo": "b", "label": "conglomerados_prudenciais"},
    {"codigo": "n", "label": "instituicoes_individuais"},
]

# Relatório de interesse: Resumo das parcelas de capital
RELATORIO_CODIGO = "c"  # código "c" = Capital (Resumo) na API do IFData


def _get_ultimo_periodo(session: requests.Session) -> str:
    """Retorna o código do período mais recente disponível no IFData."""
    resp = session.get(PERIODOS_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    periodos = resp.json()
    # A lista vem ordenada do mais recente para o mais antigo
    return periodos[0] if periodos else None


def _download_relatorio(
    session: requests.Session, periodo: str, tipo_codigo: str
) -> pd.DataFrame:
    """Baixa o CSV de um relatório específico via endpoint de exportação."""
    url = (
        f"{IFDATA_API}/dados/{periodo}/{tipo_codigo}/{RELATORIO_CODIGO}"
        f"?formato=csv"
    )
    resp = session.get(url, headers=HEADERS, timeout=60)
    if resp.status_code != 200:
        return pd.DataFrame()

    from io import StringIO
    try:
        df = pd.read_csv(StringIO(resp.text), sep=";", encoding="utf-8")
    except Exception:
        df = pd.read_csv(StringIO(resp.text), sep=",", encoding="utf-8")
    return df


class BacenParcelasCapitalBasileiaScraper(BaseScraper):
    name = "bacen_parcelas_capital_basileia"

    def fetch(self) -> pd.DataFrame:
        session = requests.Session()

        periodo = _get_ultimo_periodo(session)
        if not periodo:
            raise RuntimeError("Não foi possível obter o período mais recente do IFData.")

        self.logger.info(f"Período IFData: {periodo}")

        # Converte o período (ex.: "202312") para date
        try:
            dt_ref = datetime.datetime.strptime(str(periodo), "%Y%m").date()
        except ValueError:
            dt_ref = datetime.date.today().replace(day=1)

        frames = []
        for tipo in TIPOS_INST:
            self.logger.info(f"Baixando tipo: {tipo['label']}")
            df = _download_relatorio(session, periodo, tipo["codigo"])
            if df.empty:
                self.logger.warning(f"Sem dados para {tipo['label']}")
                continue
            df.insert(0, "dt_referencia", dt_ref)
            df.insert(1, "tipo_instituicao", tipo["label"])
            frames.append(df)

        if not frames:
            raise RuntimeError("Nenhum dado retornado do IFData.")

        return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    scraper = BacenParcelasCapitalBasileiaScraper()
    scraper.run()
