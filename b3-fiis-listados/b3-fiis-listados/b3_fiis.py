"""
B3 FIIs Listados - Captura Automatizada
========================================
Consome a API interna da B3 (sistemaswebb3-listados.b3.com.br)
que alimenta o botão "Exportar lista completa de fundos" da página:
https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/fundos-de-investimentos/fii/fiis-listados/

A API usa paginação com parâmetros codificados em Base64.
O script percorre todas as páginas e salva o resultado em CSV acumulativo.

Dependências:
    pip install requests

Uso:
    python b3_fiis.py          # execução direta
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
FUNDS_TYPE  = "FII"
PAGE_SIZE   = 100          # máximo suportado pela API
FUSO        = ZoneInfo("America/Sao_Paulo")
PASTA_SAIDA = Path("./data")
ARQUIVO_CSV = PASTA_SAIDA / "b3_fiis_listados.csv"

CABECALHO_CSV = [
    "data_captura",
    "hora_captura",
    "codigo_fundo",          # ticker (ex: HGLG11)
    "nome_fundo",
    "cnpj",
    "administrador",
    "segmento",
    "tipo",
    "mandato",
    "prazo_duracao",
    "gestao",
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
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.b3.com.br/",
    "Origin":  "https://www.b3.com.br",
}


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def montar_url(page_number: int, page_size: int = PAGE_SIZE) -> str:
    """
    A API da B3 recebe os parâmetros como JSON codificado em Base64 na URL.
    Exemplo decodificado:
        {"language":"pt-br","pageNumber":1,"pageSize":100,"fundsType":"FII"}
    """
    params = {
        "language":   "pt-br",
        "pageNumber": page_number,
        "pageSize":   page_size,
        "fundsType":  FUNDS_TYPE,
    }
    # A B3 usa separadores sem espaço — importante para o Base64 bater
    payload = json.dumps(params, separators=(",", ":"))
    encoded = b64encode(payload.encode("utf-8")).decode("utf-8")
    return BASE_URL + encoded


def limpar(valor) -> str:
    """Normaliza valores None e strings vazias."""
    if valor is None:
        return ""
    return str(valor).strip()


# ─────────────────────────────────────────────
# Captura
# ─────────────────────────────────────────────

def capturar_pagina(session: requests.Session, page: int) -> tuple[list[dict], int]:
    """
    Retorna (registros_da_pagina, total_de_registros).
    total_de_registros = 0 em caso de erro.
    """
    url = montar_url(page)
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        log.error(f"Erro na página {page}: {e}")
        return [], 0
    except ValueError:
        log.error(f"Resposta não é JSON na página {page}: {resp.text[:200]}")
        return [], 0

    total    = data.get("total", 0)
    results  = data.get("results", [])
    return results, total


def capturar_todos_fiis() -> list[dict]:
    """Percorre todas as páginas da API e retorna a lista completa de FIIs."""
    agora        = datetime.now(FUSO)
    data_captura = agora.strftime("%Y-%m-%d")
    hora_captura = agora.strftime("%H:%M:%S")

    session = requests.Session()
    session.headers.update(HEADERS_HTTP)

    log.info("Buscando página 1 para descobrir o total de registros...")
    primeira_pagina, total = capturar_pagina(session, page=1)

    if total == 0:
        log.error("Nenhum registro retornado. Verifique a API.")
        sys.exit(1)

    total_paginas = (total + PAGE_SIZE - 1) // PAGE_SIZE
    log.info(f"Total de FIIs: {total} | Páginas: {total_paginas}")

    todos_resultados = list(primeira_pagina)

    for page in range(2, total_paginas + 1):
        log.info(f"Buscando página {page}/{total_paginas}...")
        resultados, _ = capturar_pagina(session, page)
        todos_resultados.extend(resultados)
        time.sleep(0.3)   # pausa gentil para não sobrecarregar a API

    log.info(f"Total de registros capturados: {len(todos_resultados)}")

    # Mapear campos da API para o CSV
    registros_csv = []
    for item in todos_resultados:
        registros_csv.append({
            "data_captura":    data_captura,
            "hora_captura":    hora_captura,
            "codigo_fundo":    limpar(item.get("fundTicker") or item.get("ticker") or item.get("code")),
            "nome_fundo":      limpar(item.get("fundName")   or item.get("companyName")),
            "cnpj":            limpar(item.get("cnpj")),
            "administrador":   limpar(item.get("administrator")),
            "segmento":        limpar(item.get("fundSegment") or item.get("segment")),
            "tipo":            limpar(item.get("fundType")    or item.get("type")),
            "mandato":         limpar(item.get("mandate")),
            "prazo_duracao":   limpar(item.get("term")),
            "gestao":          limpar(item.get("managementType") or item.get("management")),
            "data_encerramento": limpar(item.get("closingDate")),
            "cotistas":        limpar(item.get("quotaHolders")),
            "patrimonio_liquido": limpar(item.get("netEquity")),
        })

    return registros_csv


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

    log.info(f"CSV atualizado: {ARQUIVO_CSV} ({len(registros)} FIIs registrados)")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    log.info("=== Iniciando captura de FIIs listados na B3 ===")
    registros = capturar_todos_fiis()
    salvar_csv(registros)
    log.info("=== Concluído com sucesso ===")
