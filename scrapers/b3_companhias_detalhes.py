"""
scrapers/b3_companhias_detalhes.py
-----------------------------------
Detalhes cadastrais de companhias listadas na B3.

Fonte: https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetDetail/
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

log = get_logger("b3_companhias_detalhes")

BASE_URL = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetDetail/"
ARQUIVO = Path("data/b3_companhias_detalhes.csv")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    seeds = get_company_seeds(session)
    log.info(f"{len(seeds)} empresas encontradas")

    todos = []
    for s in seeds:
        code_cvm = s["codeCVM"]
        if not code_cvm:
            continue
        url = BASE_URL + b64_encode_params({"codeCVM": code_cvm, "language": "pt-br"})
        try:
            resp = session.get(url, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            payload = data if isinstance(data, dict) else {}
            if isinstance(payload, dict):
                payload["codecvm_consulta"] = code_cvm
                todos.append(payload)
        except Exception as e:
            log.warning(f"codeCVM {code_cvm} falhou: {e}")
        time.sleep(0.2)

    rows = json_rows(todos)
    enriched, header_novo = enriquecer("b3_companhias_detalhes", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header

class B3CompanhiasDetalhesScraper(BaseScraper):
    name = "b3_companhias_detalhes"
    group = "b3"
    enabled = False
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'conjunto', 'registro_hash']
    
    # Catálogo de Metadados
    title = 'B3 Companhias Detalhes'
    description = 'Dados capturados.'
    icon = '📊'
    icon_class = 'icon-misc'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['b3']
    source = 'B3'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 — Detalhes de Companhias Listadas ===")
        rows, header = capturar()
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3CompanhiasDetalhesScraper().run()
