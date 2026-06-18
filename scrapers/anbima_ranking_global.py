#!/usr/bin/env python
# coding: utf-8
"""
Scraper: ANBIMA Ranking Global de Administração de Recursos de Terceiros
Fonte:   https://www.anbima.com.br/pt_br/informar/ranking/fundos-de-investimento/global.htm
Saída:   data/anbima_ranking_global.csv

Nota: a página entrega um arquivo Excel (.xls/.xlsx). O scraper baixa via
requests seguindo os redirects, lê a aba "Pag 4 - Por Ativos RF" e
"Pag - 5 Por Ativos RV", e consolida ambas num único CSV.
"""
import os
import re
import sys
import time
import datetime
from io import BytesIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


STRAPI_HOST = "https://data-strapi.prd.anbima.com.br"
STRAPI_API_URL = f"{STRAPI_HOST}/api/ranking-global-de-adm-de-fundo?populate[template][populate][publication_document][populate]=*"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.anbima.com.br",
}


def _get_download_url(session: requests.Session) -> str:
    """Busca a URL do arquivo Excel via API do Strapi da ANBIMA."""
    resp = session.get(STRAPI_API_URL, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    try:
        template = data["data"]["attributes"]["template"]
        pub_docs = template["publication_document"]
        if not pub_docs:
            raise ValueError("publication_document está vazio.")

        pub_doc = pub_docs[0]
        files = pub_doc["file"]["data"]
        if not files:
            raise ValueError("Nenhum arquivo encontrado em publication_document.")

        url_path = files[0]["attributes"]["url"]
        return STRAPI_HOST + url_path
    except (KeyError, IndexError, TypeError, ValueError) as e:
        raise RuntimeError(f"Erro ao extrair URL de download da API do Strapi: {e}") from e


def _extract_date_from_filename(file_name: str) -> datetime.date:
    """Extrai a data de referência (YYYYMM) do nome do arquivo."""
    m = re.search(r"(\d{6})", file_name)
    if m:
        return datetime.datetime.strptime(m.group(1) + "01", "%Y%m%d").date()
    return datetime.date.today().replace(day=1)


def clean_header_name(name):
    if name is None:
        return ""
    return " ".join(str(name).replace("\n", " ").split()).strip()


def _read_sheet(content: bytes, sheet_name: str, data_referencia: datetime.date) -> pd.DataFrame:
    """Lê uma aba específica do Excel usando uma estratégia robusta para cabeçalhos e linhas de dados."""
    engine = "xlrd" if content.startswith(b"\xd0\xcf\x11\xe0") else "openpyxl"
    
    df_raw = pd.read_excel(
        BytesIO(content),
        sheet_name=sheet_name,
        header=None,
        engine=engine,
    )
    
    all_rows = df_raw.values.tolist()
    
    header_rows = []
    data_rows = []
    found_data = False
    
    for idx, row in enumerate(all_rows):
        if not any(str(v).strip() for v in row if v is not None):
            continue
            
        first_val = row[0]
        is_numeric = False
        try:
            val_f = float(first_val)
            if val_f > 0:
                is_numeric = True
        except (ValueError, TypeError):
            pass
            
        if is_numeric:
            found_data = True
            data_rows.append(row)
        else:
            if not found_data:
                if idx >= 6:
                    header_rows.append(row)
                    
    num_cols = len(all_rows[0]) if all_rows else 0
    col_names = []
    for col_idx in range(num_cols):
        parts = []
        for h_row in header_rows:
            if col_idx < len(h_row):
                val = clean_header_name(h_row[col_idx])
                if val and val not in parts:
                    parts.append(val)
        col_name = " - ".join(parts) if parts else f"col_{col_idx}"
        col_names.append(col_name)
        
    if col_names:
        col_names[0] = "Ordem"
    if len(col_names) > 1:
        col_names[1] = "Administrador"
        
    df = pd.DataFrame(data_rows, columns=col_names)
    df = df.loc[:, ~df.columns.str.startswith("col_")]
    
    df.insert(0, "data_referencia", data_referencia)
    df.insert(1, "tipo_ativo", sheet_name.strip())
    
    return df


class AnbimaRankingGlobalScraper(BaseScraper):
    name = "anbima_ranking_global"
    group = "anbima"
    enabled = True
    phase = 1

    def fetch(self) -> pd.DataFrame:
        from scripts.utils.ux import print_done, print_warn

        session = requests.Session()

        t0 = time.time()
        download_url = _get_download_url(session)
        resp = session.get(download_url, headers=HEADERS, timeout=120)
        resp.raise_for_status()
        content = resp.content
        print_done("arquivo baixado", elapsed=time.time() - t0)

        file_name = download_url.split("/")[-1].split("?")[0]
        data_referencia = _extract_date_from_filename(file_name)

        engine = "xlrd" if content.startswith(b"\xd0\xcf\x11\xe0") else "openpyxl"
        xl = pd.ExcelFile(BytesIO(content), engine=engine)
        sheets = [s for s in xl.sheet_names if "Pag" in s and "Índices" not in s and "Expediente" not in s]

        dfs = []
        for sheet_name in sheets:
            t0 = time.time()
            try:
                sheet_df = _read_sheet(content, sheet_name, data_referencia)
                dfs.append(sheet_df)
                print_done(f"aba: {sheet_name}", elapsed=time.time() - t0)
            except Exception as e:
                print_warn(f"aba {sheet_name}: {e}", elapsed=time.time() - t0)

        if not dfs:
            raise RuntimeError("Nenhuma aba pôde ser processada com sucesso.")

        return pd.concat(dfs, ignore_index=True)


if __name__ == "__main__":
    scraper = AnbimaRankingGlobalScraper()
    scraper.run()
