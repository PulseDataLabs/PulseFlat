"""
B3 ETFs Listados - Captura Automatizada
=========================================
Consome a API interna da B3 (sistemaswebb3-listados.b3.com.br)
que alimenta o botão "Exportar lista completa de fundos" da página:
https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/etf/renda-variavel/etfs-listados/

A B3 divide os ETFs em duas categorias:
  - ETF    → ETFs de Renda Variável
  - ETF-RF → ETFs de Renda Fixa

O script captura AMBAS as categorias e consolida em um único CSV,
com a coluna `categoria_etf` identificando cada tipo.

Dependências:
    pip install requests

Uso:
    python b3_etfs.py          # execução direta
"""

import csv
import json
import logging
import sys
import time
from base64 import b64encode
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

# ─────────────────────────────────────────────
# Configurações
# ─────────────────────────────────────────────
BASE_URL    = "https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/GetListedFundsSupplement/"
PAGE_SIZE   = 100
FUSO        = ZoneInfo("America/Sao_Paulo")
PASTA_SAIDA = Path("./data")
ARQUIVO_CSV = PASTA_SAIDA / "b3_etfs_listados.csv"

# Categorias de ETF disponíveis na B3
CATEGORIAS_ETF = [
    ("ETF",    "ETF Renda Variável"),
    ("ETF-RF", "ETF Renda Fixa"),
]

CABECALHO_CSV = [
    "data_captura",
    "hora_captura",
    "categoria_etf",          # "ETF Renda Variável" ou "ETF Renda Fixa"
    "codigo_fundo",           # ticker (ex: BOVA11, IMAB11)
    "nome_fundo",
    "cnpj",
    "administrador",
    "gestor",
    "indice_referencia",      # índice que o ETF replica
    "segmento",
    "tipo",
    "prazo_duracao",
    "data_encerramento",
    "cotistas",
    "patrimonio_liquido",
]

# ─────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

HEADERS_HTTP = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept":  "application/json, text/plain, */*",
    "Referer": "https://www.b3.com.br/",
    "Origin":  "https://www.b3.com.br",
}


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def montar_url(funds_type: str, page_number: int) -> str:
    """
    Monta a URL com parâmetros codificados em Base64, padrão da API da B3.
    Exemplo do JSON antes da codificação:
        {"language":"pt-br","pageNumber":1,"pageSize":100,"fundsType":"ETF"}
    """
    params = {
        "language":   "pt-br",
        "pageNumber": page_number,
        "pageSize":   PAGE_SIZE,
        "fundsType":  funds_type,
    }
    payload = json.dumps(params, separators=(",", ":"))
    encoded = b64encode(payload.encode("utf-8")).decode("utf-8")
    return BASE_URL + encoded


def limpar(valor) -> str:
    if valor is None:
        return ""
    return str(valor).strip()


# ─────────────────────────────────────────────
# Captura por categoria
# ─────────────────────────────────────────────

def capturar_pagina(
    session: requests.Session, funds_type: str, page: int
) -> tuple[list[dict], int]:
    """Retorna (registros_da_pagina, total_de_registros)."""
    url = montar_url(funds_type, page)
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        log.error(f"[{funds_type}] Erro na página {page}: {e}")
        return [], 0
    except ValueError:
        log.error(f"[{funds_type}] Resposta não é JSON na página {page}: {resp.text[:200]}")
        return [], 0

    return data.get("results", []), data.get("total", 0)


def capturar_categoria(
    session: requests.Session,
    funds_type: str,
    label: str,
    data_captura: str,
    hora_captura: str,
) -> list[dict]:
    """Percorre todas as páginas de uma categoria e retorna registros CSV."""
    log.info(f"[{label}] Buscando página 1...")
    primeira_pagina, total = capturar_pagina(session, funds_type, page=1)

    if total == 0:
        log.warning(f"[{label}] Nenhum registro retornado.")
        return []

    total_paginas = (total + PAGE_SIZE - 1) // PAGE_SIZE
    log.info(f"[{label}] Total: {total} ETFs | Páginas: {total_paginas}")

    todos = list(primeira_pagina)
    for page in range(2, total_paginas + 1):
        log.info(f"[{label}] Buscando página {page}/{total_paginas}...")
        resultados, _ = capturar_pagina(session, funds_type, page)
        todos.extend(resultados)
        time.sleep(0.3)

    # Mapear campos da API → CSV
    registros_csv = []
    for item in todos:
        registros_csv.append({
            "data_captura":      data_captura,
            "hora_captura":      hora_captura,
            "categoria_etf":     label,
            "codigo_fundo":      limpar(item.get("fundTicker") or item.get("ticker") or item.get("code")),
            "nome_fundo":        limpar(item.get("fundName")   or item.get("companyName")),
            "cnpj":              limpar(item.get("cnpj")),
            "administrador":     limpar(item.get("administrator")),
            "gestor":            limpar(item.get("manager")    or item.get("managementCompany")),
            "indice_referencia": limpar(item.get("indexFund")  or item.get("benchmark") or item.get("referenceIndex")),
            "segmento":          limpar(item.get("fundSegment") or item.get("segment")),
            "tipo":              limpar(item.get("fundType")    or item.get("type")),
            "prazo_duracao":     limpar(item.get("term")),
            "data_encerramento": limpar(item.get("closingDate")),
            "cotistas":          limpar(item.get("quotaHolders")),
            "patrimonio_liquido": limpar(item.get("netEquity")),
        })

    log.info(f"[{label}] {len(registros_csv)} ETFs capturados.")
    return registros_csv


# ─────────────────────────────────────────────
# Captura principal
# ─────────────────────────────────────────────

def capturar_todos_etfs() -> list[dict]:
    agora        = datetime.now(FUSO)
    data_captura = agora.strftime("%Y-%m-%d")
    hora_captura = agora.strftime("%H:%M:%S")

    session = requests.Session()
    session.headers.update(HEADERS_HTTP)

    todos_registros = []
    for funds_type, label in CATEGORIAS_ETF:
        registros = capturar_categoria(session, funds_type, label, data_captura, hora_captura)
        todos_registros.extend(registros)

    log.info(f"Total geral: {len(todos_registros)} ETFs capturados (RV + RF).")
    return todos_registros


# ─────────────────────────────────────────────
# Persistência
# ─────────────────────────────────────────────

def salvar_csv(registros: list[dict]) -> None:
    if not registros:
        log.warning("Nenhum registro para salvar.")
        sys.exit(1)

    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
    novo = not ARQUIVO_CSV.exists()

    with open(ARQUIVO_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO_CSV)
        if novo:
            writer.writeheader()
        writer.writerows(registros)

    log.info(f"CSV atualizado: {ARQUIVO_CSV} ({len(registros)} ETFs registrados)")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    log.info("=== Iniciando captura de ETFs listados na B3 ===")
    registros = capturar_todos_etfs()
    salvar_csv(registros)
    log.info("=== Concluído com sucesso ===")
