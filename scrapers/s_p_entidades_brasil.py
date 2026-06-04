#!/usr/bin/env python
# coding: utf-8
"""
Scraper: S&P Global – Entidades com rating no Brasil
Fonte:   https://brazil.ratings.spglobal.com/ratings/pt/regulatory/consolidated-search-entity/
Saída:   data/s_p_entidades_brasil.csv

Busca todos os emissores utilizando a API de busca da S&P Brasil.
"""
import os
import sys
import datetime
import string
import time

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


import re
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://brazil.ratings.spglobal.com"
TOKEN_URL = f"{BASE_URL}/api/tokenClient"

HEADERS_BASE = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": BASE_URL,
}

EMISSORES_FIXOS = [
    {"nome": "Banco Toyota do Brasil S.A.", "entity_id": "1000627", "sector_code": "FI"},
    {"nome": "Banco Mercantil", "entity_id": "1001476", "sector_code": "FI"},
]


class SPEntidadesBrasilScraper(BaseScraper):
    name = "s_p_entidades_brasil"
    group = "ratings"
    enabled = True
    phase = 1
    chaves_dedup = ["link"]
    accumulate = False

    def _get_api_key(self) -> str:
        """
        Recupera a API Key a partir do ambiente ou do HTML da página pública da S&P.
        Isso elimina chaves hardcodadas no código e protege contra vazamento de credenciais.
        """
        # 1. Tenta obter da variável de ambiente
        api_key = os.environ.get("SP_GLOBAL_API_KEY")
        if api_key:
            self.logger.info("Utilizando SP_GLOBAL_API_KEY da variável de ambiente.")
            return api_key

        # 2. Busca dinamicamente do HTML da página pública
        self.logger.info("Buscando API Key de forma dinâmica da página pública...")
        try:
            r = requests.get(
                BASE_URL,
                headers={
                    "User-Agent": HEADERS_BASE["User-Agent"]
                },
                timeout=30
            )
            if r.status_code == 200:
                match = re.search(r'"NEXT_PUBLIC_API_KEY"\s*:\s*"([^"]+)"', r.text)
                if match:
                    key = match.group(1)
                    self.logger.info("API Key obtida dinamicamente com sucesso.")
                    return key
        except Exception as e:
            self.logger.error(f"Erro ao obter API Key dinamicamente: {e}")

        # Se falhar, retorna string vazia
        self.logger.warning("Não foi possível carregar a API Key.")
        return ""

    def fetch(self) -> pd.DataFrame:
        session = requests.Session()
        
        api_key = self._get_api_key()
        if not api_key:
            self.logger.error("Abortando fetch: API Key não disponível.")
            return pd.DataFrame()

        api_url = f"https://api.use1.prod.ratings.spglobal.com/rbz-nsrbrazilapi/extoauthv2/brazilRatings/getEntitySearchRequest?apikey={api_key}"

        self.logger.info("Obtendo token de autorização da S&P...")
        try:
            token_resp = session.get(TOKEN_URL, headers=HEADERS_BASE, timeout=30)
            if token_resp.status_code != 200:
                self.logger.error(f"Falha ao obter token: status {token_resp.status_code}")
                return pd.DataFrame()
            token = token_resp.json().get("token")
        except Exception as e:
            self.logger.error(f"Erro ao obter token: {e}")
            return pd.DataFrame()

        if not token:
            self.logger.error("Token vazio retornado pela API.")
            return pd.DataFrame()

        api_headers = {
            "User-Agent": HEADERS_BASE["User-Agent"],
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}",
            "Access-Control-Allow-Origin": "*"
        }

        # Conjunto de termos de busca para garantir a cobertura completa
        search_terms = list(string.ascii_uppercase) + [str(i) for i in range(10)]
        resultados = {}

        self.logger.info(f"Iniciando busca abrangente por {len(search_terms)} termos...")
        
        for term in search_terms:
            page = 0
            page_length = 100
            
            while True:
                payload = {
                    "searchTerm": term,
                    "locale": "pt_LA",
                    "pageNumber": page,
                    "pageLength": page_length
                }
                
                try:
                    resp = session.post(api_url, json=payload, headers=api_headers, timeout=30)
                    if resp.status_code != 200:
                        self.logger.warning(f"Erro na busca do termo {term} página {page}: status {resp.status_code}")
                        break
                        
                    data = resp.json()
                    total_records = data.get("totalNumberOfRecords", 0)
                    details = data.get("entitySearchDetails", [])
                    
                    if not details:
                        break
                        
                    for entity in details:
                        org_id = entity.get("orgId")
                        org_name = entity.get("orgName")
                        sector_code = entity.get("sectorCode") or "CORP"
                        
                        if org_id and org_name:
                            # Constrói o link de detalhes de forma consistente
                            link = f"{BASE_URL}/ratings/pt/regulatory/org-details/sectorCode/{sector_code}/entityId/{org_id}"
                            resultados[link] = org_name
                            
                    if (page + 1) * page_length >= total_records:
                        break
                        
                    page += 1
                    time.sleep(0.1)
                except Exception as e:
                    self.logger.error(f"Erro ao processar termo {term} página {page}: {e}")
                    break

        # Mescla os emissores fixos como garantia
        for emissor in EMISSORES_FIXOS:
            link = f"{BASE_URL}/ratings/pt/regulatory/org-details/sectorCode/{emissor['sector_code']}/entityId/{emissor['entity_id']}"
            if link not in resultados:
                resultados[link] = emissor["nome"]

        self.logger.info(f"Busca finalizada. Total de entidades únicas encontradas: {len(resultados)}")

        # Converte para DataFrame no formato esperado
        rows = []
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        for link, nome in resultados.items():
            rows.append({
                "dt_captura": today_str,
                "nome": nome,
                "link": link
            })

        return pd.DataFrame(rows)


if __name__ == "__main__":
    scraper = SPEntidadesBrasilScraper()
    scraper.run()

