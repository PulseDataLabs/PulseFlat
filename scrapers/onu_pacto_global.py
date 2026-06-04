#!/usr/bin/env python
# coding: utf-8
"""
Scraper: ONU Pacto Global – Participantes (Brasil)
Fonte:   https://unglobalcompact.org/what-is-gc/participants/
Saída:   data/onu_pacto_global.csv

Cria a lista de todos os participantes do Brasil no Pacto Global da ONU.
"""
import os
import sys
import datetime
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


BASE_URL = "https://unglobalcompact.org"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}


def parse_un_date(date_str: str) -> str:
    """Converte datas no formato 'DD-MMM-YYYY' para 'YYYY-MM-DD'."""
    if not date_str:
        return ""
    
    parts = date_str.strip().split("-")
    if len(parts) != 3:
        return date_str
        
    day, month_abbr, year = parts
    months = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    m = months.get(month_abbr.lower()[:3])
    if m:
        return f"{year}-{m}-{day.zfill(2)}"
        
    return date_str


class OnuPactoGlobalScraper(BaseScraper):
    name = "onu_pacto_global"
    group = "misc"
    enabled = True
    phase = 1
    accumulate = False  # Sobrescreve diariamente para manter a lista ativa atualizada

    def fetch(self) -> pd.DataFrame:
        session = requests.Session()
        page = 1
        data_rows = []

        self.logger.info("Iniciando captura de participantes do Pacto Global (Brasil)...")

        while True:
            url = f"{BASE_URL}/what-is-gc/participants/search?page={page}&search%5Bcountries%5D%5B%5D=24&search%5Bper_page%5D=50"
            self.logger.info(f"Processando página {page}: {url}")
            
            try:
                resp = session.get(url, headers=HEADERS, timeout=45)
                if resp.status_code != 200:
                    self.logger.error(f"Erro ao carregar página {page}: status {resp.status_code}")
                    break
                    
                soup = BeautifulSoup(resp.text, "html.parser")
                table = soup.find("table")
                if not table:
                    self.logger.warning(f"Nenhuma tabela encontrada na página {page}.")
                    break
                    
                tbody = table.find("tbody")
                if not tbody:
                    self.logger.warning(f"Corpo da tabela vazio na página {page}.")
                    break
                    
                rows = tbody.find_all("tr")
                if not rows:
                    self.logger.info("Fim dos dados encontrados.")
                    break
                    
                for tr in rows:
                    th_name = tr.find("th", class_="name")
                    if not th_name:
                        continue
                        
                    a_name = th_name.find("a")
                    if not a_name:
                        continue
                        
                    name = a_name.get_text(strip=True)
                    href = a_name.get("href", "")
                    profile_link = BASE_URL + href if href else ""
                    
                    td_type = tr.find("td", class_="type")
                    type_val = td_type.get_text(strip=True) if td_type else ""
                    
                    td_sector = tr.find("td", class_="sector")
                    sector_val = td_sector.get_text(strip=True) if td_sector else ""
                    
                    td_country = tr.find("td", class_="country")
                    country_val = td_country.get_text(strip=True) if td_country else ""
                    
                    td_joined = tr.find("td", class_="joined-on")
                    joined_val = td_joined.get_text(strip=True) if td_joined else ""
                    
                    data_rows.append({
                        "name": name,
                        "type": type_val,
                        "sector": sector_val,
                        "country": country_val,
                        "joined_on": parse_un_date(joined_val),
                        "link": profile_link
                    })
                
                # Verifica paginação
                next_el = soup.find(class_="next_page")
                if next_el and next_el.name == "a" and next_el.get("href"):
                    page += 1
                    time.sleep(0.2)  # Delay para respeitar o servidor
                else:
                    self.logger.info("Última página alcançada.")
                    break
            except Exception as e:
                self.logger.error(f"Exceção ao processar página {page}: {e}")
                break

        self.logger.info(f"Extração concluída. Total de {len(data_rows)} participantes capturados.")
        return pd.DataFrame(data_rows)


if __name__ == "__main__":
    scraper = OnuPactoGlobalScraper()
    scraper.run()
