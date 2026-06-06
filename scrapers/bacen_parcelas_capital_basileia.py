#!/usr/bin/env python
# coding: utf-8
"""
Scraper: BACEN – Parcelas de Capital (Basileia) via IFData / OData
Fonte:   https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/
Saída:   data/bacen_parcelas_capital_basileia.csv

Usa a API pública OData do BCB (Olinda) para obter dados do relatório
"Informações de Capital" (Relatório 5) do IFData.

Dois conjuntos são capturados:
  - Conglomerados Prudenciais (TipoInstituicao=1)
  - Instituições Individuais   (TipoInstituicao=3)
"""
import os
import sys
import datetime
import time
from io import StringIO

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


# API OData do BCB (Olinda) – IFData
ODATA_BASE = (
    "https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/"
    "IfDataValores(AnoMes=@AnoMes,TipoInstituicao=@TipoInstituicao,"
    "Relatorio=@Relatorio)"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/csv, application/json, */*",
}

# Tipos de instituição: código OData → label descritivo
TIPOS_INST = [
    {"codigo": 1, "label": "conglomerados_prudenciais"},
    {"codigo": 3, "label": "instituicoes_individuais"},
]

# Relatório: '5' = Informações de Capital
RELATORIO = "'5'"

# Períodos de referência trimestrais (março, junho, setembro, dezembro)
MESES_TRIMESTRAIS = [3, 6, 9, 12]


def _get_periodos_recentes(n_trimestres: int = 4) -> list[int]:
    """Gera os últimos n_trimestres períodos trimestrais no formato YYYYMM."""
    hoje = datetime.date.today()
    periodos = []
    for i in range(n_trimestres):
        # Anda para trás mês a mês procurando trimestral
        dt = hoje.replace(day=1)
        months_back = i * 3
        year = dt.year
        month = dt.month - months_back
        while month <= 0:
            month += 12
            year -= 1
        # Encontra o trimestre mais próximo para trás
        while month not in MESES_TRIMESTRAIS:
            month -= 1
            if month <= 0:
                month = 12
                year -= 1
        periodos.append(year * 100 + month)
    return sorted(set(periodos), reverse=True)


def _download_relatorio_odata(
    session: requests.Session, periodo: int, tipo_codigo: int,
) -> pd.DataFrame:
    params = {
        "@AnoMes": str(periodo),
        "@TipoInstituicao": str(tipo_codigo),
        "@Relatorio": RELATORIO,
        "$format": "text/csv",
    }
    url = ODATA_BASE
    resp = session.get(url, params=params, headers=HEADERS, timeout=120)

    if resp.status_code == 404:
        return pd.DataFrame()
    if resp.status_code != 200:
        return pd.DataFrame()

    content = resp.text.strip()
    if not content or "<!DOCTYPE" in content[:100]:
        return pd.DataFrame()

    try:
        return pd.read_csv(StringIO(content))
    except Exception:
        return pd.DataFrame()


class BacenParcelasCapitalBasileiaScraper(BaseScraper):
    name = "bacen_parcelas_capital_basileia"
    group = "bcb"
    enabled = True
    phase = 1

    def fetch(self) -> pd.DataFrame:
        from scripts.utils.ux import print_done, print_warn

        session = requests.Session()

        periodos = _get_periodos_recentes(4)

        frames = []
        for periodo in periodos:
            for tipo in TIPOS_INST:
                t0 = time.time()
                df = _download_relatorio_odata(
                    session, periodo, tipo["codigo"],
                )
                if df.empty:
                    print_warn(f"sem dados: {tipo['label']} {periodo}", elapsed=time.time() - t0)
                    continue

                df["tipo_instituicao_label"] = tipo["label"]
                frames.append(df)
                print_done(f"{tipo['label']} {periodo}", elapsed=time.time() - t0)

                time.sleep(1)

            if frames:
                break

        if not frames:
            raise RuntimeError(
                "Nenhum dado retornado da API OData do BCB (IFData). "
                "Verifique se a API está disponível."
            )

        return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    scraper = BacenParcelasCapitalBasileiaScraper()
    scraper.run()
