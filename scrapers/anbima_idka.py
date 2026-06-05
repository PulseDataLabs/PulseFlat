#!/usr/bin/env python
# coding: utf-8
"""
Scraper: ANBIMA IDkA (Índice de Duração Constante ANBIMA)
Fonte:   https://www.anbima.com.br/informacoes/idka/
Saída:   data/anbima_idka.csv
"""
import os
import sys
import csv
import shutil
from datetime import date

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper
from utils.parsers import date_ref


COLUMNS = [
    "dt_referencia",
    "no_indexador",
    "no_indice",
    "nu_indice",
    "ret_dia_perc",
    "ret_mes_perc",
    "ret_ano_perc",
    "ret_12_meses_perc",
    "vol_aa_perc",
    "taxa_juros_aa_perc_compra_d1",
    "taxa_juros_aa_perc_venda_d0",
]

URL_TEMPLATE = (
    "https://www.anbima.com.br/informacoes/idka/IDkA-down.asp"
    "?Dt_Ref={dt}&DataIni={dt}&DataFim={dt}"
    "&indiceI=&indiceP=&saida=csv&Idioma=PT"
)


class AnbimaIdkaScraper(BaseScraper):
    name = "anbima_idka"
    group = "anbima"
    enabled = True
    phase = 1
    title = "ANBIMA IDkA"
    description = "Índice de Duração Constante ANBIMA (prefixado e inflação), apresentando retornos diários, mensais, anuais e volatilidade."
    icon = "📈"
    icon_class = "icon-anbima"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = ["idka", "prefixado", "inflação", "duracao constante", "anbima"]
    source = "ANBIMA"

    def fetch(self) -> pd.DataFrame:
        # Usa a data útil anterior (D-1) como referência
        dt = date_ref("dia_anterior")
        dt_ref = dt.strftime("%d/%m/%Y")
        url = URL_TEMPLATE.format(dt=dt_ref)

        self.logger.info(f"Baixando IDkA para {dt_ref}: {url}")

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": "https://www.anbima.com.br/",
        }

        resp = requests.get(url, headers=headers, timeout=60)
        resp.raise_for_status()

        # O arquivo vem em latin-1, com 2 linhas de cabeçalho e 3 de rodapé
        lines = resp.content.decode("latin-1").splitlines()

        # Primeira linha contém a data de referência: "Data de Referência: DD/MM/YYYY"
        data_line = lines[0].split(" ")[-1].strip()
        try:
            dt_referencia = date(*map(int, reversed(data_line.split("/"))))
        except ValueError:
            dt_referencia = dt.date()

        # Lê CSV pulando as 2 primeiras linhas e as 3 últimas (rodapé)
        from io import StringIO
        content = "\n".join(lines[2:-3])
        df_raw = pd.read_csv(
            StringIO(content),
            sep=";",
            encoding="latin-1",
            header=0,
        )

        if df_raw.empty:
            self.logger.warning("Nenhum dado retornado para o IDkA.")
            return pd.DataFrame(columns=COLUMNS)

        df = pd.DataFrame()
        df["dt_referencia"] = dt_referencia
        df["no_indexador"] = df_raw.get("Indexador", pd.Series(dtype=str))
        df["no_indice"] = df_raw.get("Índices", pd.Series(dtype=str))
        df["nu_indice"] = df_raw.get("Nº Índice", pd.Series(dtype=str))
        df["ret_dia_perc"] = df_raw.get("Retorno (% Dia)", pd.Series(dtype=str))
        df["ret_mes_perc"] = df_raw.get("Retorno (% Mês)", pd.Series(dtype=str))
        df["ret_ano_perc"] = df_raw.get("Retorno (% Ano)", pd.Series(dtype=str))
        df["ret_12_meses_perc"] = df_raw.get("Retorno (% 12 Meses)", pd.Series(dtype=str))
        df["vol_aa_perc"] = df_raw.get("Volatilidade (% a.a.) *", pd.Series(dtype=str))
        df["taxa_juros_aa_perc_compra_d1"] = df_raw.get(
            "Taxa de Juros (% a.a.) [Compra (D-1)]", pd.Series(dtype=str)
        )
        df["taxa_juros_aa_perc_venda_d0"] = df_raw.get(
            "Taxa de Juros (% a.a.) [Venda (D-0)]", pd.Series(dtype=str)
        )

        return df[COLUMNS]


if __name__ == "__main__":
    scraper = AnbimaIdkaScraper()
    scraper.run()
