"""
scrapers/b3_indicadores_financeiros.py
----------------------------------------
Indicadores financeiros da B3 (SELIC, CDI, IPCA, IGP-M, câmbio, etc.)
via API interna dos sistemas de derivativos.

Fonte: https://sistemaswebb3-derivativos.b3.com.br/financialIndicatorsProxy/
       FinancialIndicators/GetFinancialIndicators/<base64>
Campos: security_identification_code, description, group_description,
        value, rate, last_update
"""

import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_indicadores_financeiros")

ARQUIVO = Path("data/b3_indicadores_financeiros.csv")

URL = (
    "https://sistemaswebb3-derivativos.b3.com.br/financialIndicatorsProxy/"
    "FinancialIndicators/GetFinancialIndicators/"
    "eyJsYW5ndWFnZSI6InB0LWJyIn0="
)

CABECALHO = [
    "data_captura",
    
    "security_identification_code",
    "description",
    "group_description",
    "value",
    "rate",
    "last_update",
]

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://www.b3.com.br/",
    "Origin": "https://www.b3.com.br",
}


def _camel_to_snake(name: str) -> str:
    """converte camelCase para snake_case simples."""
    import re
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def capturar() -> list[dict]:
    log.info(f"Buscando indicadores financeiros B3: {URL}")

    for tentativa in range(1, 4):
        try:
            resp = requests.get(URL, timeout=30, headers=HEADERS)
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error("Falha ao acessar indicadores B3.")
                sys.exit(1)
            time.sleep(5)

    dados = resp.json()
    if not dados:
        log.error("API B3 retornou lista vazia.")
        sys.exit(1)

    data_captura, _ = agora_brt()
    registros = []

    for item in dados:
        registros.append({
            "data_captura":                data_captura,
            "security_identification_code": limpar(item.get("securityIdentificationCode", "")),
            "description":                 limpar(item.get("description", "")),
            "group_description":           limpar(item.get("groupDescription", "")),
            "value":                       limpar(str(item.get("value", ""))),
            "rate":                        limpar(str(item.get("rate", ""))),
            "last_update":                 limpar(item.get("lastUpdate", "")),
        })

    log.info(f"{len(registros)} indicadores B3 capturados.")
    return registros

class B3IndicadoresFinanceirosScraper(BaseScraper):
    name = "b3_indicadores_financeiros"
    accumulate = True
    chaves_dedup = ['data_captura', 'security_identification_code']
    
    # Catálogo de Metadados
    title = 'B3 Indicadores Financeiros'
    description = 'Indicadores financeiros da B3 via API de derivativos: SELIC, CDI, IPCA, IGP-M, câmbio e taxas de juros.'
    icon = '📊'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['selic', 'cdi', 'ipca', 'igp-m', 'câmbio']
    source = 'B3 API'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 — Indicadores Financeiros ===")
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3IndicadoresFinanceirosScraper().run()
