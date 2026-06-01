"""
scrapers/b3_carteira_ibov.py
-----------------------------
Carteira teórica do índice IBOVESPA via API de listados da B3.

Fonte: https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/<base64>
Campos: codigo, acao, tipo, qtde_teorica, part_pct
"""

import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, b64_encode_params, nova_session, salvar_csv

log = get_logger("b3_carteira_ibov")

ARQUIVO = Path("data/b3_carteira_ibov.csv")

BASE_URL = "https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/"
INDICE = "IBOV"
PAGE_SIZE = 120

CABECALHO = [
    "data_captura",
    "hora_captura",
    "indice",
    "codigo",
    "acao",
    "tipo",
    "qtde_teorica",
    "part_pct",
]


def _url_pagina(page: int) -> str:
    return BASE_URL + b64_encode_params({
        "language": "pt-br",
        "pageNumber": page,
        "pageSize": PAGE_SIZE,
        "index": INDICE,
        "segment": "1",
    })


def capturar() -> list[dict]:
    session = nova_session()
    data_captura, hora_captura = agora_brt()
    todos = []
    pagina = 1

    while True:
        url = _url_pagina(pagina)
        log.info(f"Página {pagina} — {url}")
        try:
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            log.error(f"Erro página {pagina}: {e}")
            break

        resultados = data.get("results") or data.get("result") or data.get("data") or []
        if not resultados:
            break

        for item in resultados:
            todos.append({
                "data_captura": data_captura,
                "hora_captura": hora_captura,
                "indice":       INDICE,
                "codigo":       limpar(item.get("cod") or item.get("ticker") or item.get("code", "")),
                "acao":         limpar(item.get("asset") or item.get("name") or item.get("assetName", "")),
                "tipo":         limpar(item.get("type") or item.get("typeBDR", "")),
                "qtde_teorica": limpar(str(item.get("theoricalQty") or item.get("quantity", ""))),
                "part_pct":     limpar(str(item.get("part") or item.get("participation", ""))),
            })

        page_info = data.get("page", {})
        total_pages = page_info.get("totalPages")
        if total_pages and pagina >= int(total_pages):
            break
        pagina += 1
        time.sleep(0.5)

    if not todos:
        log.error("Nenhuma ação do IBOV capturada.")
        sys.exit(1)

    log.info(f"{len(todos)} ações na carteira teórica do {INDICE}.")
    return todos


def main():
    log.info("=== B3 — Carteira Teórica IBOV ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "indice", "codigo"])


if __name__ == "__main__":
    main()
