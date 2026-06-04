"""
scrapers/b3_capital_social_empresas.py
---------------------------------------
Captura dados de capital social de empresas listadas na B3.

Fonte: https://sistemaswebb3-listados.b3.com.br/shareCapitalProxy/
       ShareCapitalCall/GetList/<base64>
"""

import sys
import time
from base64 import b64encode
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import get_logger, nova_session, salvar_csv
from utils.parsers import json_rows, enriquecer, read_existing_header
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_capital_social_empresas")

BASE_URL = (
    "https://sistemaswebb3-listados.b3.com.br/"
    "shareCapitalProxy/ShareCapitalCall/"
    "GetList/"
)
PAGE_SIZE = 120
ARQUIVO = Path("data/b3_capital_social_empresas.csv")


def _url(page: int) -> str:
    params = {"name": "", "pageNumber": page, "pageSize": PAGE_SIZE}
    payload = json.dumps(params, separators=(",", ":"))
    return BASE_URL + b64encode(payload.encode("utf-8")).decode("utf-8")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    todos = []

    for page in range(1, 20):
        url = _url(page)
        log.info(f"Pagina {page}...")
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        items = data if isinstance(data, list) else data.get("results", [])
        if not items:
            break
        todos.extend(items)

        total_items = len(items)
        if total_items < PAGE_SIZE:
            break

        time.sleep(0.3)

    log.info(f"{len(todos)} registros brutos capturados")
    rows = json_rows(todos)
    enriched, header_novo = enriquecer("b3_capital_social_empresas", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header

class B3CapitalSocialEmpresasScraper(BaseScraper):
    name = "b3_capital_social_empresas"
    accumulate = True
    chaves_dedup = ['data_captura', 'conjunto', 'registro_hash']
    
    # Catálogo de Metadados
    title = 'B3 — Capital Social de Empresas'
    description = 'Capital social de empresas listadas na B3: CNPJ, valor do capital e data de referência.'
    icon = '🏢'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['cnpj', 'empresa', 'capital social']
    source = 'B3 API'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 — Capital Social de Empresas Listadas ===")
        rows, header = capturar()
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3CapitalSocialEmpresasScraper().run()
