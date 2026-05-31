"""
B3 Carteiras Teóricas - Captura Automatizada
=============================================
Consome a API interna da B3 (sistemaswebb3-listados.b3.com.br)
que alimenta as páginas de composição de carteira de cada índice:
https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm

Endpoint utilizado:
  GET https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/<base64>

Parâmetros (antes do Base64):
  {"language":"pt-br","pageNumber":1,"pageSize":120,"index":"IBOV","segment":"1"}

O script captura todos os índices configurados em INDICES abaixo,
consolida em um único CSV com a coluna `indice` identificando cada carteira.

Dependências:
    pip install requests

Uso:
    python b3_carteiras.py
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
BASE_URL    = "https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/"
PAGE_SIZE   = 120          # valor usado pelo próprio site da B3
FUSO        = ZoneInfo("America/Sao_Paulo")
PASTA_SAIDA = Path("./data")
ARQUIVO_CSV = PASTA_SAIDA / "b3_carteiras_teoricas.csv"

# Índices B3 e seus segmentos (segment="1" para todos os ativos)
# Fonte: páginas de composição de carteira do site da B3
INDICES = [
    # Índices Amplos
    ("IBOV",  "1", "Ibovespa"),
    ("IBRA",  "1", "IBrA - Índice Brasil Amplo"),
    ("IBRX",  "1", "IBrX 100 - Índice Brasil 100"),
    ("IBXL",  "1", "IBrX 50 - Índice Brasil 50"),
    ("IGCX",  "1", "IGC - Índice de Ações com Governança Corporativa"),
    ("ITAG",  "1", "ITAG - Índice de Ações com Tag Along"),
    ("MLCX",  "1", "MLCX - Mid-Large Cap"),
    ("SMLL",  "1", "SMLL - Small Cap"),
    ("IVBX",  "1", "IVBX-2 - Índice Valor BM&F Bovespa"),
    # Índices de Segmentos e Setoriais
    ("IDIV",  "1", "IDIV - Índice Dividendos"),
    ("IFIX",  "1", "IFIX - Índice de Fundos Imobiliários"),
    ("IFNC",  "1", "IFNC - Índice Financeiro"),
    ("ICON",  "1", "ICON - Índice de Consumo"),
    ("IEEX",  "1", "IEEX - Índice de Energia Elétrica"),
    ("IMAT",  "1", "IMAT - Índice de Materiais Básicos"),
    ("IMOB",  "1", "IMOB - Índice Imobiliário"),
    ("INDX",  "1", "INDX - Índice do Setor Industrial"),
    ("UTIL",  "1", "UTIL - Índice Utilidade Pública"),
    # Índices de Sustentabilidade e Governança
    ("IGCT",  "1", "IGCT - Governança Corporativa Trade"),
    ("IGNM",  "1", "IGNM - Novo Mercado"),
    ("ISEE",  "1", "ISE - Sustentabilidade Empresarial"),
    ("ICO2",  "1", "ICO2 - Carbono Eficiente"),
]

CABECALHO_CSV = [
    "data_captura",
    "hora_captura",
    "indice",                 # código do índice (ex: IBOV)
    "indice_nome",            # nome completo do índice
    "codigo_ativo",           # ticker (ex: PETR4)
    "nome_ativo",             # nome da empresa/fundo
    "tipo_ativo",             # ON, PN, UNT, CI, etc.
    "quantidade_teorica",     # quantidade teórica na carteira
    "participacao_pct",       # peso no índice (%)
    "reducao_capital",        # flag de redução de capital
    "segmento",               # segmento de listagem
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

def montar_url(index: str, segment: str, page_number: int) -> str:
    """
    Monta URL com parâmetros em Base64, padrão da API da B3.
    Exemplo do JSON antes da codificação:
        {"language":"pt-br","pageNumber":1,"pageSize":120,"index":"IBOV","segment":"1"}
    """
    params = {
        "language":   "pt-br",
        "pageNumber": page_number,
        "pageSize":   PAGE_SIZE,
        "index":      index,
        "segment":    segment,
    }
    payload = json.dumps(params, separators=(",", ":"))
    encoded = b64encode(payload.encode("utf-8")).decode("utf-8")
    return BASE_URL + encoded


def limpar(valor) -> str:
    if valor is None:
        return ""
    return str(valor).strip()


# ─────────────────────────────────────────────
# Captura por índice
# ─────────────────────────────────────────────

def capturar_pagina(
    session: requests.Session, index: str, segment: str, page: int
) -> tuple[list[dict], int]:
    """Retorna (ativos_da_pagina, total_de_ativos)."""
    url = montar_url(index, segment, page)
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        log.error(f"[{index}] Erro na página {page}: {e}")
        return [], 0
    except ValueError:
        log.error(f"[{index}] Resposta não é JSON: {resp.text[:200]}")
        return [], 0

    # A API retorna {"results": [...], "total": N, "header": {...}}
    results = data.get("results", [])
    total   = data.get("total",   0)

    # Fallback: alguns índices retornam lista direta sem paginação
    if isinstance(data, list):
        return data, len(data)

    return results, total


def capturar_indice(
    session: requests.Session,
    index: str,
    segment: str,
    label: str,
    data_captura: str,
    hora_captura: str,
) -> list[dict]:
    """Percorre todas as páginas de um índice e retorna registros CSV."""
    log.info(f"[{index}] Capturando carteira teórica...")
    primeira_pagina, total = capturar_pagina(session, index, segment, page=1)

    if not primeira_pagina:
        log.warning(f"[{index}] Nenhum ativo retornado — índice pode não existir ou estar temporariamente indisponível.")
        return []

    # Se total não veio na resposta, usa o tamanho da primeira página
    if total == 0:
        total = len(primeira_pagina)

    total_paginas = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    log.info(f"[{index}] {total} ativos | {total_paginas} página(s)")

    todos = list(primeira_pagina)
    for page in range(2, total_paginas + 1):
        log.info(f"[{index}] Página {page}/{total_paginas}...")
        resultados, _ = capturar_pagina(session, index, segment, page)
        todos.extend(resultados)
        time.sleep(0.3)

    registros_csv = []
    for item in todos:
        registros_csv.append({
            "data_captura":      data_captura,
            "hora_captura":      hora_captura,
            "indice":            index,
            "indice_nome":       label,
            "codigo_ativo":      limpar(item.get("cod")          or item.get("ticker")       or item.get("code")),
            "nome_ativo":        limpar(item.get("asset")        or item.get("companyName")  or item.get("name")),
            "tipo_ativo":        limpar(item.get("type")         or item.get("typeStock")),
            "quantidade_teorica":limpar(item.get("theoricalQty") or item.get("quantity")     or item.get("qtyTheoretical")),
            "participacao_pct":  limpar(item.get("part")         or item.get("participation") or item.get("weight")),
            "reducao_capital":   limpar(item.get("reductionPct") or item.get("capitalReduction")),
            "segmento":          limpar(item.get("segment")      or item.get("setor")),
        })

    log.info(f"[{index}] {len(registros_csv)} ativos capturados.")
    return registros_csv


# ─────────────────────────────────────────────
# Captura principal — todos os índices
# ─────────────────────────────────────────────

def capturar_todas_carteiras() -> list[dict]:
    agora        = datetime.now(FUSO)
    data_captura = agora.strftime("%Y-%m-%d")
    hora_captura = agora.strftime("%H:%M:%S")

    session = requests.Session()
    session.headers.update(HEADERS_HTTP)

    todos_registros = []
    erros = []

    for index, segment, label in INDICES:
        registros = capturar_indice(session, index, segment, label, data_captura, hora_captura)
        if registros:
            todos_registros.extend(registros)
        else:
            erros.append(index)
        time.sleep(0.5)   # pausa entre índices

    log.info(f"Total geral: {len(todos_registros)} registros capturados em {len(INDICES) - len(erros)}/{len(INDICES)} índices.")
    if erros:
        log.warning(f"Índices sem dados: {', '.join(erros)}")

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

    log.info(f"CSV atualizado: {ARQUIVO_CSV} ({len(registros)} linhas adicionadas)")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    log.info("=== Iniciando captura das carteiras teóricas B3 ===")
    registros = capturar_todas_carteiras()
    salvar_csv(registros)
    log.info("=== Concluído com sucesso ===")
