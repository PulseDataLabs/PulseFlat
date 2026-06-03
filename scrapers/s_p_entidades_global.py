#!/usr/bin/env python
# coding: utf-8
"""
Scraper: S&P Global – Entidades com rating (mercado global)
Fonte:   https://www.spglobal.com/ratings/pt/regulatory/entity-browse
Saída:   data/s_p_entidades_global.csv

NOTA: A página S&P utiliza JavaScript intensivo e requer autenticação.
O scraper tenta captura via requests puro. Caso a resposta seja bloqueada
(redirect de login ou página vazia), o arquivo de saída conterá apenas
os metadados de tentativa e um aviso no log.

Credenciais esperadas nas variáveis de ambiente (arquivo .env):
  USER_STANDARDPOORS=<email>
  PASS_STANDARDPOORS=<senha>
"""
import os
import sys
import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


BASE_URL = "https://www.spglobal.com/ratings/pt/regulatory"
BROWSE_URL = f"{BASE_URL}/entity-browse"
LOGIN_URL = "https://www.spglobal.com/ratings/pt/user-management/sign-in"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": BASE_URL,
}

# Filtro: apenas Brasil (BRA)
SEARCH_PARAMS = {
    "countries": "BRA",
    "pageSize": 100,
    "pageNumber": 1,
}


def _login(session: requests.Session, email: str, password: str) -> bool:
    """Tenta autenticação via POST no endpoint de login da S&P."""
    payload = {"username": email, "password": password}
    resp = session.post(LOGIN_URL, data=payload, headers=HEADERS, timeout=30, allow_redirects=True)
    return resp.status_code == 200


def _extract_entities(html: str) -> list[dict]:
    """Extrai nome e link das entidades do HTML renderizado."""
    soup = BeautifulSoup(html, "html.parser")
    entities = []
    container = soup.find("div", class_="table-module__content entity-browse-links")
    if not container:
        return entities
    for row in container.find_all("div", class_="table-module__row"):
        col = row.find("div", class_="table-module__column link")
        if not col:
            continue
        a = col.find("a", class_="link-black")
        if not a:
            continue
        nome = a.get_text(strip=True)
        href = a.get("href", "")
        if not href.startswith("http"):
            href = "https://www.spglobal.com" + href
        entities.append({"nome": nome, "link_completo": href})
    return entities


class SPEntidadesGlobalScraper(BaseScraper):
    name = "s_p_entidades_global"

    def fetch(self) -> pd.DataFrame:
        email = os.environ.get("USER_STANDARDPOORS", "")
        password = os.environ.get("PASS_STANDARDPOORS", "")

        session = requests.Session()

        if email and password:
            self.logger.info("Tentando autenticação na S&P Global...")
            _login(session, email, password)
        else:
            self.logger.warning(
                "Credenciais USER_STANDARDPOORS / PASS_STANDARDPOORS não definidas. "
                "A captura pode ser incompleta."
            )

        all_entities = []
        page = 1

        while True:
            SEARCH_PARAMS["pageNumber"] = page
            self.logger.info(f"Buscando página {page}...")
            resp = session.get(BROWSE_URL, params=SEARCH_PARAMS, headers=HEADERS, timeout=60)
            if resp.status_code != 200:
                self.logger.warning(f"Status {resp.status_code} na página {page}. Encerrando paginação.")
                break

            entities = _extract_entities(resp.text)
            if not entities:
                self.logger.info(f"Nenhuma entidade na página {page}. Fim da paginação.")
                break

            all_entities.extend(entities)
            page += 1

        if not all_entities:
            self.logger.warning(
                "Nenhuma entidade capturada. O site S&P pode exigir "
                "autenticação via browser ou bloqueio anti-bot."
            )
            return pd.DataFrame(columns=["nome", "link_completo"])

        df = pd.DataFrame(all_entities)
        df.insert(0, "dt_captura", datetime.date.today())
        return df


if __name__ == "__main__":
    scraper = SPEntidadesGlobalScraper()
    scraper.run()
