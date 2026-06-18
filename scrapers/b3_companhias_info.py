"""
scrapers/b3_companhias_info.py
-------------------------------
Informações complementares de companhias listadas na B3, incluindo
proventos (dividendos, juros, subscrições).

Fonte: https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedSupplementCompany/
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

log = get_logger("b3_companhias_info")

BASE_URL = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedSupplementCompany/"
ARQUIVO = Path("data/b3_companhias_info.csv")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    seeds = get_company_seeds(session)
    log.info(f"{len(seeds)} empresas encontradas")

    todos = []
    for s in seeds:
        issuing = s["issuingCompany"]
        if not issuing:
            continue
        url = BASE_URL + b64_encode_params({"issuingCompany": issuing, "language": "pt-br"})
        try:
            resp = session.get(url, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            payload = data if isinstance(data, dict) else {}
            base_row = payload.get("info") if isinstance(payload.get("info"), dict) else payload
            if isinstance(base_row, dict):
                base_row["issuingcompany_consulta"] = issuing
                todos.append(base_row)
            for sub_key in ("cashDividends", "stockDividends", "subscriptions"):
                for item in payload.get(sub_key, []) or []:
                    item["tipo_bloco"] = sub_key
                    item["issuingcompany_consulta"] = issuing
                    todos.append(item)
        except Exception as e:
            log.warning(f"issuingCompany {issuing} falhou: {e}")
        time.sleep(0.2)

    rows = json_rows(todos)
    enriched, header_novo = enriquecer("b3_companhias_info", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header

class B3CompanhiasInfoScraper(BaseScraper):
    name = "b3_companhias_info"
    group = "b3"
    enabled = False
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'conjunto', 'registro_hash']
    
    # Catálogo de Metadados
    title = 'B3 — Informações de Companhias'
    description = 'Informações complementares e proventos (dividendos em dinheiro, bonificações em ações, subscrições) de todas as companhias listadas na B3.'
    icon = '📋'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['proventos', 'dividendos', 'subscrições', 'b3']
    source = 'B3 API'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 — Informações de Companhias Listadas ===")
        rows, header = capturar()
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in header if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3CompanhiasInfoScraper().run()
