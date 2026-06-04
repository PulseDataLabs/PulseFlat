#!/usr/bin/env python
# coding: utf-8
"""
Scraper: S&P Global – Ratings de emissores brasileiros
Fonte:   https://brazil.ratings.spglobal.com/
Saída:   data/s_p_ratings_brasil.csv

Para cada entidade listada em data/s_p_entidades_brasil.csv,
acessa a página de detalhes e extrai a tabela de ratings usando a estrutura Next.js (__NEXT_DATA__).
"""
import os
import sys
import datetime
import json
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}


def parse_sp_date(date_str: str) -> str:
    """Converte datas do formato S&P para YYYY-MM-DD."""
    if not date_str or date_str == "--":
        return ""
    
    date_str = date_str.strip()
    if "/" in date_str:
        parts = date_str.split("/")
        if len(parts) == 3:
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
            
    if "-" in date_str:
        parts = date_str.split("-")
        if len(parts) == 3:
            if len(parts[0]) == 4:
                return date_str
            
            day, month_abbr, year = parts
            months = {
                "jan": "01", "january": "01",
                "fev": "02", "feb": "02", "february": "02",
                "mar": "03", "march": "03",
                "abr": "04", "apr": "04", "april": "04",
                "mai": "05", "may": "05",
                "jun": "06", "june": "06",
                "jul": "07", "july": "07",
                "ago": "08", "aug": "08", "august": "08",
                "set": "09", "sep": "09", "september": "09",
                "out": "10", "oct": "10", "october": "10",
                "nov": "11", "november": "11",
                "dez": "12", "dec": "12", "december": "12"
            }
            m = months.get(month_abbr.lower())
            if m:
                return f"{year}-{m}-{day.zfill(2)}"
            if day.isdigit() and month_abbr.isdigit() and year.isdigit():
                return f"{year}-{month_abbr.zfill(2)}-{day.zfill(2)}"
                
    return date_str


def _parse_ratings_next_data(html: str) -> list[dict]:
    """Extrai os ratings do bloco __NEXT_DATA__ da página HTML."""
    soup = BeautifulSoup(html, "html.parser")
    next_data_el = soup.find("script", id="__NEXT_DATA__")
    if not next_data_el:
        return []

    try:
        data = json.loads(next_data_el.string)
        page_props = data.get("props", {}).get("pageProps", {})
        res = page_props.get("Res", {})
        if not res:
            return []
            
        rating_details = res.get("ratingDetails", {})
        if not rating_details:
            return []
            
        ratings_list = rating_details.get("Ratings", [])
        if not ratings_list:
            return []

        rows = []
        for r in ratings_list:
            tipo_rating = r.get("ratingTypeCode") or r.get("orgDebtTypeDesc") or ""
            rating_val = r.get("rating") or ""
            data_acao = parse_sp_date(r.get("ratingDate"))
            data_revisao = parse_sp_date(r.get("lastReviewDate"))
            identificadores = "--"
            cw_perspectiva = r.get("currentCwOl") or ""
            data_cw = parse_sp_date(r.get("currentCwOlDate"))

            rows.append({
                "Tipo de Rating": tipo_rating,
                "Rating": rating_val,
                "Data da Ação de Rating": data_acao,
                "Data da ÚltimaRevisão": data_revisao,
                "Identifica\xaddores Regulatórios": identificadores,
                "CreditWatch/ Perspectiva": cw_perspectiva,
                "Data do CreditWatch/ Perspectiva": data_cw
            })
        return rows
    except Exception:
        return []


class SPRatingsBrasilScraper(BaseScraper):
    name = "s_p_ratings_brasil"
    chaves_dedup = [
        "link",
        "Tipo de Rating",
        "Rating",
        "Data da Ação de Rating"
    ]
    accumulate = True

    def fetch(self) -> pd.DataFrame:
        entidades_csv = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "s_p_entidades_brasil.csv",
        )
        if not os.path.exists(entidades_csv):
            self.logger.warning(
                f"Arquivo de entidades não encontrado: {entidades_csv}. "
                "Execute s_p_entidades_brasil.py antes."
            )
            return pd.DataFrame()

        df_entidades = pd.read_csv(entidades_csv)
        if "link" not in df_entidades.columns:
            self.logger.warning(
                "Coluna 'link' não encontrada no CSV de entidades."
            )
            return pd.DataFrame()

        session = requests.Session()
        frames = []
        total = len(df_entidades)

        for i, row in df_entidades.iterrows():
            nome = row.get("nome", "")
            link = row.get("link", "")
            self.logger.info(f"[{i+1}/{total}] {nome}")

            try:
                resp = session.get(link, headers=HEADERS, timeout=30)
                if resp.status_code == 403:
                    self.logger.warning(
                        f"Acesso bloqueado (403) para {nome}."
                    )
                    continue
                if resp.status_code != 200:
                    self.logger.warning(
                        f"Status {resp.status_code} para {link}"
                    )
                    continue
                
                ratings_list = _parse_ratings_next_data(resp.text)
                if not ratings_list:
                    self.logger.warning(
                        f"Nenhum rating ou estrutura __NEXT_DATA__ encontrada para {nome}"
                    )
                    continue
                
                df_table = pd.DataFrame(ratings_list)
                df_table["nome"] = nome
                df_table["link"] = link
                frames.append(df_table)
                
                time.sleep(0.1)  # delay para não sobrecarregar
            except Exception as e:
                self.logger.warning(f"Erro em {link}: {e}")

        if not frames:
            self.logger.warning("Nenhum rating capturado.")
            return pd.DataFrame()

        df = pd.concat(frames, ignore_index=True)
        df.insert(0, "dt_captura", datetime.date.today().strftime("%Y-%m-%d"))
        return df


if __name__ == "__main__":
    scraper = SPRatingsBrasilScraper()
    scraper.run()

