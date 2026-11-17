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
import datetime
import os
import sys
import time
from io import StringIO

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper
from scripts.utils.ux import print_done, print_warn

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

# Tipos de instituição válidos para o Relatório 5 (compatível com PulseIFData):
# até 201412: tipo 2 (conglomerados_financeiros); a partir de 201503: tipo 1 (conglomerados_prudenciais)
TIPO_LABELS = {
    1: "conglomerados_prudenciais",
    2: "conglomerados_financeiros",
}

# Relatório: '5' = Informações de Capital
RELATORIO = "'5'"

# Períodos de referência trimestrais (março, junho, setembro, dezembro)
MESES_TRIMESTRAIS = [3, 6, 9, 12]


def _tipos_validos(periodo: int) -> list[dict]:
    codigo = 2 if periodo <= 201412 else 1
    return [{"codigo": codigo, "label": TIPO_LABELS[codigo]}]


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
    session: requests.Session,
    periodo: int,
    tipo_codigo: int,
    max_retries: int = 3,
    retry_delay: int = 5,
) -> tuple[pd.DataFrame, bool]:
    """Baixa relatório via OData com retries em erros 5xx/rede. Retorna (df, api_indisponivel)."""
    params = {
        "@AnoMes": str(periodo),
        "@TipoInstituicao": str(tipo_codigo),
        "@Relatorio": RELATORIO,
        "$format": "text/csv",
    }

    for tentativa in range(1, max_retries + 1):
        try:
            resp = session.get(ODATA_BASE, params=params, headers=HEADERS, timeout=120)
            if resp.status_code == 404:
                return pd.DataFrame(), False
            if resp.status_code == 200:
                content = resp.text.strip()
                if not content or "<!DOCTYPE" in content[:200]:
                    return pd.DataFrame(), False
                try:
                    return pd.read_csv(StringIO(content)), False
                except Exception as e:
                    print_warn(f"Erro ao ler CSV ({periodo} tipo={tipo_codigo}): {e}")
                    return pd.DataFrame(), False

            print_warn(
                f"HTTP {resp.status_code} IFData ({periodo} tipo={tipo_codigo}) "
                f"tentativa {tentativa}/{max_retries}"
            )
            if resp.status_code < 500 and resp.status_code != 429:
                return pd.DataFrame(), False
        except requests.RequestException as e:
            print_warn(
                f"Erro de rede IFData ({periodo} tipo={tipo_codigo}) "
                f"tentativa {tentativa}/{max_retries}: {e}"
            )

        if tentativa < max_retries:
            time.sleep(retry_delay)

    return pd.DataFrame(), True


class BacenParcelasCapitalBasileiaScraper(BaseScraper):
    name = "bacen_parcelas_capital_basileia"
    group = "bcb"
    enabled = True
    phase = 1
    compress = True
    chaves_dedup = ["AnoMes", "TipoInstituicao", "CodInst", "Conta", "Grupo"]
    title = "BACEN — Parcelas de Capital e Basileia"
    description = "Requerimentos de capital regulatório, Patrimônio de Referência (PR), ativos ponderados pelo risco (RWA) e Índice de Basileia de cada instituição bancária reportado ao BACEN."

    def fetch(self) -> pd.DataFrame:
        session = requests.Session()
        periodos = _get_periodos_recentes(4)

        frames = []
        api_indisponivel = False
        for periodo in periodos:
            for tipo in _tipos_validos(periodo):
                t0 = time.time()
                df, indisponivel = _download_relatorio_odata(
                    session,
                    periodo,
                    tipo["codigo"],
                )
                api_indisponivel = api_indisponivel or indisponivel
                if df.empty:
                    print_warn(f"sem dados: {tipo['label']} {periodo}")
                    continue

                df["tipo_instituicao_label"] = tipo["label"]
                frames.append(df)
                print_done(f"{tipo['label']} {periodo}", elapsed=time.time() - t0)

                time.sleep(1)

            if frames:
                break

        if not frames:
            if api_indisponivel:
                print_warn(
                    "API OData do BCB (IFData) indisponível no momento (HTTP 5xx/rede). "
                    "Mantendo dados existentes sem marcar falha no pipeline."
                )
            else:
                print_warn("Nenhum dado retornado da API OData do BCB (IFData).")
            return pd.DataFrame()

        return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    scraper = BacenParcelasCapitalBasileiaScraper()
    scraper.run()
