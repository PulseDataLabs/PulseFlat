"""
scrapers/b3_fundos_listados.py
-------------------------------
Captura a lista completa de fundos listados na B3 via API interna (GetListFunds).

Cobre todos os tipos de fundo disponíveis no endpoint:
  FII, FIAGRO, FIDC, FIP, ETF, ETF-RF, Fundo Setorial

Endpoint: GET https://sistemaswebb3-listados.b3.com.br/fundsListedProxy/Search/
                GetListFunds/<base64>
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, b64_encode_params, nova_session
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_fundos_listados")

BASE_URL  = "https://sistemaswebb3-listados.b3.com.br/fundsListedProxy/Search/GetListFunds/"
PAGE_SIZE = 100
ARQUIVO   = Path("data/b3_fundos_listados.csv")

CATEGORIAS = [
    ("FII",      "FII"),
    ("FIAGRO",   "FIAGRO"),
    ("FIDC",     "FIDC"),
    ("FIP",      "FIP"),
    ("ETF",      "ETF Renda Variável"),
    ("ETF-RF",   "ETF Renda Fixa"),
    ("SETORIAL", "Fundo Setorial"),
]

CABECALHO = [
    "data_captura",
    "tipo_fundo",
    "codigo_fundo",
    "nome_fundo",
    "id_b3",
]


def _url(funds_type: str, page: int) -> str:
    return BASE_URL + b64_encode_params({
        "language": "pt-br", "pageNumber": page,
        "pageSize": PAGE_SIZE, "typeFund": funds_type,
    })


def _pagina(session, funds_type: str, page: int) -> tuple[list, int, int | None]:
    try:
        resp = session.get(_url(funds_type, page), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        resultados = data.get("results") or data.get("result") or data.get("data") or []
        page_info = data.get("page") or {}
        total = (
            data.get("total")
            or page_info.get("totalRecords")
            or page_info.get("totalResults")
            or page_info.get("total")
            or len(resultados)
        )
        total_pages = page_info.get("totalPages")
        return resultados, int(total or 0), int(total_pages) if total_pages else None
    except Exception as e:
        log.error(f"[{funds_type}] Página {page}: {e}")
        return [], 0, None


def _mapear(item: dict, data_captura: str, tipo_label: str) -> dict:
    codigo = limpar(item.get("acronym"))
    return {
        "data_captura":  data_captura,
        "tipo_fundo":    tipo_label,
        "codigo_fundo":  codigo,
        "nome_fundo":    limpar(item.get("fundName") or item.get("tradingName")),
        "id_b3":         str(item.get("id", "")),
    }


def _capturar_categoria(session, funds_type: str, label: str,
                         data_captura: str) -> list[dict]:
    log.info(f"[{label}] Buscando página 1...")
    primeira, total, total_pages = _pagina(session, funds_type, 1)
    if not primeira:
        log.warning(f"[{label}] Sem dados.")
        return []

    n_pag = total_pages or (total + PAGE_SIZE - 1) // PAGE_SIZE
    log.info(f"[{label}] {total} fundos | {n_pag} páginas")

    todos = list(primeira)
    for p in range(2, n_pag + 1):
        log.info(f"[{label}] Página {p}/{n_pag}...")
        resultados, *_ = _pagina(session, funds_type, p)
        todos.extend(resultados)
        time.sleep(0.3)

    return [_mapear(i, data_captura, label) for i in todos]


def capturar() -> list[dict]:
    data_captura, _ = agora_brt()
    session = nova_session()
    todos = []
    for funds_type, label in CATEGORIAS:
        todos.extend(_capturar_categoria(session, funds_type, label, data_captura))
        time.sleep(0.5)
    log.info(f"{len(todos)} fundos capturados ao total.")
    return todos


class B3FundosListadosScraper(BaseScraper):
    name = "b3_fundos_listados"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = False
    chaves_dedup = None

    title = 'B3 Fundos Listados'
    description = 'Lista completa de fundos listados na B3: FII, FIAGRO, FIDC, FIP, ETFs (RV e RF) e Fundos Setoriais.'
    icon = '🏢'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['ticker', 'fundos', 'fii', 'fiagro', 'fidc', 'fip', 'etf', 'setorial']
    source = 'B3 API'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 Fundos Listados ===")
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3FundosListadosScraper().run()
