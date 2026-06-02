"""
scrapers/b3_bdi_trades_acoes.py
--------------------------------
Negócios consolidados de ações do Boletim Diário de Informações (BDI) da B3.

Endpoint: POST https://arquivos.b3.com.br/bdi/table/ConsolidatedTradesEquities/
          {data}/{data}/{pagina}/{page_size}
Campos: RPT_DT, TCKR_SYMB, ISIN, SGMT_NM, MKT, OPEN_PRIC, MIN_PRIC,
        MAX_PRIC, TRAD_AVRG_PRIC, LAST_PRIC, OSC, TRAD_QTY, NTL_FIN_VOL
"""

import sys
import time
from datetime import date, timedelta
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv

log = get_logger("b3_bdi_trades_acoes")

ARQUIVO = Path("data/b3_bdi_trades_acoes.csv")

CABECALHO = [
    "data_captura",
    
    "rpt_dt",
    "tckr_symb",
    "isin",
    "sgmt_nm",
    "mkt",
    "open_pric",
    "min_pric",
    "max_pric",
    "trad_avrg_pric",
    "last_pric",
    "osc",
    "trad_qty",
    "fin_instrm_qty",
    "ntl_fin_vol",
]

PAGE_SIZE = 1000
MAX_PAGES = 50  # Limite de segurança (~50k registros)

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
        log.warning(f"Erro {url}: {e}")
        return []


def _data_referencia() -> date:
    for delta in range(1, 6):
        ref = date.today() - timedelta(days=delta)
        if ref.weekday() < 5:
            return ref
    return date.today() - timedelta(days=1)


def capturar() -> list[dict]:
    data_ref = _data_referencia()
    str_data = data_ref.strftime("%Y-%m-%d")
    log.info(f"Buscando trades consolidados ações B3 (ref: {str_data})...")

    data_captura, _ = agora_brt()
    todos = []
    pagina = 1

    while pagina <= MAX_PAGES:
        url = (
            f"https://arquivos.b3.com.br/bdi/table/ConsolidatedTradesEquities/"
            f"{str_data}/{str_data}/{pagina}/{PAGE_SIZE}"
        )
        log.info(f"  Página {pagina}...")
        rows = _buscar_pagina(url)
        if not rows:
            break

        for item in rows:
            todos.append({
                "data_captura":  data_captura,
                "rpt_dt":        limpar(str(item.get("rpt_dt", ""))),
                "tckr_symb":     limpar(item.get("tckr_symb", "")),
                "isin":          limpar(item.get("isin", "")),
                "sgmt_nm":       limpar(item.get("sgmt_nm", "")),
                "mkt":           limpar(item.get("mkt", "")),
                "open_pric":     limpar(str(item.get("open_pric", ""))),
                "min_pric":      limpar(str(item.get("min_pric", ""))),
                "max_pric":      limpar(str(item.get("max_pric", ""))),
                "trad_avrg_pric": limpar(str(item.get("trad_avrg_pric", ""))),
                "last_pric":     limpar(str(item.get("last_pric", ""))),
                "osc":           limpar(str(item.get("osc", ""))),
                "trad_qty":      limpar(str(item.get("trad_qty", ""))),
                "fin_instrm_qty": limpar(str(item.get("fin_instrm_qty", ""))),
                "ntl_fin_vol":   limpar(str(item.get("ntl_fin_vol", ""))),
            })

        pagina += 1
        time.sleep(1.5)

    if not todos:
        log.error("Nenhum trade de ação retornado.")
        sys.exit(1)

    log.info(f"{len(todos)} trades consolidados capturados (ref: {data_ref}).")
    return todos


def main():
    log.info("=== B3 BDI — Trades Consolidados de Ações ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "tckr_symb", "rpt_dt"])


if __name__ == "__main__":
    main()
