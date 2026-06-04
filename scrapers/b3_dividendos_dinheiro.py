"""
scrapers/b3_dividendos_dinheiro.py
-----------------------------------
Dividendos em dinheiro pagos por companhias listadas na B3.

Fonte: https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedCashDividends/
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import b64_encode_params, get_logger, nova_session, salvar_csv
from utils.b3_helpers import get_company_seeds
from utils.parsers import json_rows, enriquecer, read_existing_header
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_dividendos_dinheiro")

BASE_URL = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedCashDividends/"
ARQUIVO = Path("data/b3_dividendos_dinheiro.csv")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    seeds = get_company_seeds(session)
    log.info(f"{len(seeds)} empresas encontradas")

    todos = []
    for s in seeds:
        trading_name = s["tradingName"]
        if not trading_name:
            continue
        page = 1
        while True:
            params = {"tradingName": trading_name, "language": "pt-br", "pageNumber": page, "pageSize": 200}
            url = BASE_URL + b64_encode_params(params)
            try:
                resp = session.get(url, timeout=60)
                resp.raise_for_status()
                data = resp.json() or {}
                result = data.get("results") or []
                for item in result:
                    item["trading_name_consulta"] = trading_name
                todos.extend(result)
                total_pages = (data.get("page") or {}).get("totalPages") or 1
                if page >= int(total_pages or 1):
                    break
                page += 1
                time.sleep(0.2)
            except Exception as e:
                log.warning(f"tradingName {trading_name} (pág {page}) falhou: {e}")
                break
        time.sleep(0.1)

    rows = json_rows(todos)
    enriched, header_novo = enriquecer("b3_dividendos_dinheiro", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header

class B3DividendosDinheiroScraper(BaseScraper):
    name = "b3_dividendos_dinheiro"
    group = "b3"
    enabled = False
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'conjunto', 'registro_hash']
    
    # Catálogo de Metadados
    title = 'B3 Dividendos Dinheiro'
    description = 'Dados capturados.'
    icon = '📊'
    icon_class = 'icon-misc'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['b3']
    source = 'B3'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 — Dividendos em Dinheiro ===")
        rows, header = capturar()
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3DividendosDinheiroScraper().run()
