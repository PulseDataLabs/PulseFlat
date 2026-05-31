"""
scrapers/b3_fiis.py
-------------------
Captura a lista completa de FIIs listados na B3 via API interna.

Fonte:    https://www.b3.com.br/.../fii/fiis-listados/
Endpoint: GET https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/
                GetListedFundsSupplement/<base64>
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, b64_encode_params, nova_session, salvar_csv

log = get_logger("b3_fiis")

BASE_URL   = "https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/GetListedFundsSupplement/"
FUNDS_TYPE = "FII"
PAGE_SIZE  = 100
ARQUIVO    = Path("data/b3_fiis_listados.csv")

CABECALHO = [
    "data_captura", "hora_captura",
    "codigo_fundo", "nome_fundo", "cnpj",
    "administrador", "segmento", "tipo",
    "mandato", "prazo_duracao", "gestao",
    "data_encerramento", "cotistas", "patrimonio_liquido",
]


def _url(page: int) -> str:
    return BASE_URL + b64_encode_params({
        "language": "pt-br", "pageNumber": page,
        "pageSize": PAGE_SIZE, "fundsType": FUNDS_TYPE,
    })


def _pagina(session, page: int) -> tuple[list, int]:
    try:
        resp = session.get(_url(page), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("results", []), data.get("total", 0)
    except Exception as e:
        log.error(f"Página {page}: {e}")
        return [], 0


def _mapear(item: dict, data_captura: str, hora_captura: str) -> dict:
    return {
        "data_captura":       data_captura,
        "hora_captura":       hora_captura,
        "codigo_fundo":       limpar(item.get("fundTicker") or item.get("ticker") or item.get("code")),
        "nome_fundo":         limpar(item.get("fundName")   or item.get("companyName")),
        "cnpj":               limpar(item.get("cnpj")),
        "administrador":      limpar(item.get("administrator")),
        "segmento":           limpar(item.get("fundSegment") or item.get("segment")),
        "tipo":               limpar(item.get("fundType")    or item.get("type")),
        "mandato":            limpar(item.get("mandate")),
        "prazo_duracao":      limpar(item.get("term")),
        "gestao":             limpar(item.get("managementType") or item.get("management")),
        "data_encerramento":  limpar(item.get("closingDate")),
        "cotistas":           limpar(item.get("quotaHolders")),
        "patrimonio_liquido": limpar(item.get("netEquity")),
    }


def capturar() -> list[dict]:
    data_captura, hora_captura = agora_brt()
    session = nova_session()

    log.info("Buscando página 1...")
    primeira, total = _pagina(session, 1)
    if total == 0:
        log.error("Nenhum FII retornado.")
        sys.exit(1)

    n_pag = (total + PAGE_SIZE - 1) // PAGE_SIZE
    log.info(f"Total: {total} FIIs | {n_pag} páginas")

    todos = list(primeira)
    for p in range(2, n_pag + 1):
        log.info(f"Página {p}/{n_pag}...")
        resultados, _ = _pagina(session, p)
        todos.extend(resultados)
        time.sleep(0.3)

    registros = [_mapear(i, data_captura, hora_captura) for i in todos]
    log.info(f"{len(registros)} FIIs capturados.")
    return registros


def main():
    log.info("=== B3 FIIs Listados ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO)


if __name__ == "__main__":
    main()
