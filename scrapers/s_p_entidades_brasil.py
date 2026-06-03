#!/usr/bin/env python
# coding: utf-8
"""
Scraper: S&P Global – Entidades com rating no Brasil
Fonte:   https://brazil.ratings.spglobal.com/ratings/pt/regulatory/consolidated-search-entity/
Saída:   data/s_p_entidades_brasil.csv

Busca cada emissor na API de busca da S&P Brasil e retorna nome + link.
A lista de emissores é lida de EMISSORES_BASE abaixo (ajuste conforme necessário)
ou pode ser passada via arquivo CSV com coluna 'nome'.

Credenciais esperadas nas variáveis de ambiente:
  USER_STANDARDPOORS=<email>
  PASS_STANDARDPOORS=<senha>
"""
import os
import sys
import datetime
from urllib.parse import quote

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


BASE_URL = "https://brazil.ratings.spglobal.com"
SEARCH_URL = f"{BASE_URL}/ratings/pt/regulatory/consolidated-search-entity/searchTerm"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": BASE_URL,
}

# Emissores mapeados manualmente (fallback / complemento)
EMISSORES_FIXOS = [
    {"nome": "Banco Toyota do Brasil S.A.", "entity_id": "1000627"},
    {"nome": "Banco Mercantil", "entity_id": "1001476"},
]

ENTITY_BASE_URL = f"{BASE_URL}/ratings/pt/regulatory/org-details/sectorCode/FI/entityId/"


def _buscar_emissor(session: requests.Session, nome: str) -> dict | None:
    url = f"{SEARCH_URL}/{quote(nome.strip())}"
    resp = session.get(url, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Verifica mensagem "sem resultado"
    msg_sem_resultado = soup.select_one("div#maindiv.results-header h3.text-red")
    if msg_sem_resultado and "Não foram encontrados" in msg_sem_resultado.get_text():
        return None

    # Extrai primeira linha de resultado
    linha = soup.select_one("div.table-module__row")
    if not linha:
        return None

    link_el = linha.select_one("a.entity-results-table-content-font")
    if not link_el:
        return None

    nome_encontrado = link_el.get_text(strip=True)
    href = link_el.get("href", "")
    if not href.startswith("http"):
        href = BASE_URL + href

    return {"nome": nome_encontrado, "link": href}


class SPEntidadesBrasilScraper(BaseScraper):
    name = "s_p_entidades_brasil"

    def fetch(self) -> pd.DataFrame:
        session = requests.Session()

        # Carrega lista de emissores de arquivo externo (se existir)
        emissores_path = os.path.join(
            os.path.dirname(__file__), "config", "s_p_emissores_brasil.txt"
        )
        if os.path.exists(emissores_path):
            with open(emissores_path, encoding="utf-8") as f:
                nomes = [line.strip() for line in f if line.strip()]
        else:
            self.logger.warning(
                f"Arquivo {emissores_path} não encontrado. "
                "Usando apenas os emissores fixos mapeados."
            )
            nomes = []

        resultados = []

        for nome in nomes:
            self.logger.info(f"Buscando: {nome}")
            res = _buscar_emissor(session, nome)
            if res:
                resultados.append(res)
            else:
                self.logger.warning(f"Emissor não encontrado: {nome}")

        # Adiciona emissores fixos (sem duplicar por link)
        links_existentes = {r["link"] for r in resultados}
        for e in EMISSORES_FIXOS:
            link = f"{ENTITY_BASE_URL}{e['entity_id']}"
            if link not in links_existentes:
                resultados.append({"nome": e["nome"], "link": link})

        if not resultados:
            return pd.DataFrame(columns=["dt_captura", "nome", "link"])

        df = pd.DataFrame(resultados).drop_duplicates("link")
        df.insert(0, "dt_captura", datetime.date.today())
        return df


if __name__ == "__main__":
    scraper = SPEntidadesBrasilScraper()
    scraper.run()
