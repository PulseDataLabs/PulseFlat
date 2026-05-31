"""
scrapers/b3_etfs.py
-------------------
Captura a lista completa de ETFs listados na B3 (Renda Variável + Renda Fixa).

Endpoint: GET https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/
                GetListedFundsSupplement/<base64>

fundsType: "ETF"    → ETFs de Renda Variável
           "ETF-RF" → ETFs de Renda Fixa
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, b64_encode_params, nova_session, salvar_csv

log = get_logger("b3_etfs")

BASE_URL  = "https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/GetListedFundsSupplement/"
PAGE_SIZE = 100
ARQUIVO   = Path("data/b3_etfs_listados.csv")

CATEGORIAS = [
    ("ETF",    "ETF Renda Variável"),
    ("ETF-RF", "ETF Renda Fixa"),
]

CABECALHO = [
    "data_captura", "hora_captura", "categoria_etf",
    "codigo_fundo", "nome_fundo", "cnpj",
    "administrador", "gestor", "indice_referencia",
    "segmento", "tipo", "prazo_duracao",
    "data_encerramento", "cotistas", "patrimonio_liquido",
]


def _url(funds_type: str, page: int) -> str:
    return BASE_URL + b64_encode_params({
        "language": "pt-br", "pageNumber": page,
        "pageSize": PAGE_SIZE, "fundsType": funds_type,
    })


def _pagina(session, funds_type: str, page: int) -> tuple[list, int]:
    try:
        resp = session.get(_url(funds_type, page), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("results", []), data.get("total", 0)
    except Exception as e:
        log.error(f"[{funds_type}] Página {page}: {e}")
        return [], 0


def _mapear(item: dict, data_captura: str, hora_captura: str, label: str) -> dict:
    return {
        "data_captura":       data_captura,
        "hora_captura":       hora_captura,
        "categoria_etf":      label,
        "codigo_fundo":       limpar(item.get("fundTicker") or item.get("ticker") or item.get("code")),
        "nome_fundo":         limpar(item.get("fundName")   or item.get("companyName")),
        "cnpj":               limpar(item.get("cnpj")),
        "administrador":      limpar(item.get("administrator")),
        "gestor":             limpar(item.get("manager")   or item.get("managementCompany")),
        "indice_referencia":  limpar(item.get("indexFund") or item.get("benchmark") or item.get("referenceIndex")),
        "segmento":           limpar(item.get("fundSegment") or item.get("segment")),
        "tipo":               limpar(item.get("fundType")  or item.get("type")),
        "prazo_duracao":      limpar(item.get("term")),
        "data_encerramento":  limpar(item.get("closingDate")),
        "cotistas":           limpar(item.get("quotaHolders")),
        "patrimonio_liquido": limpar(item.get("netEquity")),
    }


def _capturar_categoria(session, funds_type: str, label: str,
                         data_captura: str, hora_captura: str) -> list[dict]:
    log.info(f"[{label}] Buscando página 1...")
    primeira, total = _pagina(session, funds_type, 1)
    if total == 0:
        log.warning(f"[{label}] Sem dados.")
        return []

    n_pag = (total + PAGE_SIZE - 1) // PAGE_SIZE
    log.info(f"[{label}] {total} ETFs | {n_pag} páginas")

    todos = list(primeira)
    for p in range(2, n_pag + 1):
        log.info(f"[{label}] Página {p}/{n_pag}...")
        resultados, _ = _pagina(session, funds_type, p)
        todos.extend(resultados)
        time.sleep(0.3)

    return [_mapear(i, data_captura, hora_captura, label) for i in todos]


def capturar() -> list[dict]:
    data_captura, hora_captura = agora_brt()
    session = nova_session()
    todos = []
    for funds_type, label in CATEGORIAS:
        todos.extend(_capturar_categoria(session, funds_type, label, data_captura, hora_captura))
        time.sleep(0.5)
    log.info(f"{len(todos)} ETFs capturados (RV + RF).")
    return todos


def main():
    log.info("=== B3 ETFs Listados ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO)


if __name__ == "__main__":
    main()
