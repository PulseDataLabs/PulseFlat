"""
scrapers/b3_bdi_di_over.py
---------------------------
Taxa DI Over (depósito interbancário overnight) do BDI da B3.

Endpoint: POST https://arquivos.b3.com.br/bdi/table/DIover/{data}/{data}/{pagina}/{page_size}
Campos: RPT_DT, NUMBER_OF_OPERATIONS, FINANCIAL_VOLUME, AVERAGE, DAILY_FACTOR, SELIC_RATE
"""

import sys
import time
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv
from utils.parsers import _CAL
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_bdi_di_over")

ARQUIVO = Path("data/b3_bdi_di_over.csv")

CABECALHO = [
    "data_captura",
    
    "rpt_dt",
    "number_of_operations",
    "financial_volume",
    "average",
    "daily_factor",
    "selic_rate",
]

PAGE_SIZE = 1000
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
}


def _to_snake(name: str) -> str:
    import re
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _buscar_pagina(url: str) -> list[dict]:
    try:
        resp = requests.post(url, json={}, timeout=30, headers=HEADERS)
        resp.raise_for_status()
        table = resp.json().get("table", {})
        values = table.get("values", [])
        columns = [_to_snake(c["name"]) for c in table.get("columns", [])]
        if not values:
            return []
        return [dict(zip(columns, row)) for row in values]
    except Exception as e:
        log.warning(f"Erro página {url}: {e}")
        return []


def _data_referencia() -> date:
    return _CAL.offset(date.today(), -1)


def capturar() -> list[dict]:
    data_ref = _data_referencia()
    str_data = data_ref.strftime("%Y-%m-%d")
    log.info(f"Buscando DI Over B3 (ref: {str_data})...")

    data_captura, _ = agora_brt()
    todos = []
    pagina = 1

    while True:
        url = (
            f"https://arquivos.b3.com.br/bdi/table/DIover/"
            f"{str_data}/{str_data}/{pagina}/{PAGE_SIZE}"
        )
        log.info(f"  Página {pagina}...")
        rows = _buscar_pagina(url)
        if not rows:
            break

        for item in rows:
            # API retorna TCKR_SYMB no lugar de NUMBER_OF_OPERATIONS em alguns casos
            n_ops = item.get("tckr_symb") or item.get("number_of_operations", "")
            todos.append({
                "data_captura":       data_captura,
                "rpt_dt":             limpar(str(item.get("rpt_dt", ""))),
                "number_of_operations": limpar(str(n_ops)),
                "financial_volume":   limpar(str(item.get("financial_volume", ""))),
                "average":            limpar(str(item.get("average", ""))),
                "daily_factor":       limpar(str(item.get("daily_factor", ""))),
                "selic_rate":         limpar(str(item.get("selic_rate", ""))),
            })

        pagina += 1
        time.sleep(1)

    if not todos:
        log.error("Nenhum dado DI Over retornado.")
        sys.exit(1)

    log.info(f"{len(todos)} registros DI Over capturados.")
    return todos

class B3BdiDiOverScraper(BaseScraper):
    name = "b3_bdi_di_over"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'rpt_dt']
    
    # Catálogo de Metadados
    title = 'B3 BDI — DI Over'
    description = 'Taxa DI Over overnight: número de operações, volume financeiro, taxa média, fator diário e SELIC.'
    icon = '🏦'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['di over', 'taxa média', 'volume', 'selic']
    source = 'B3 · BDI'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 BDI — DI Over ===")
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3BdiDiOverScraper().run()
