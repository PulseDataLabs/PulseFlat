"""
scrapers/b3_carteiras_teoricas.py
------------------------
Captura a composição das carteiras teóricas dos principais índices da B3.

Endpoint: GET https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/
                GetPortfolioDay/<base64>
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, b64_encode_params, nova_session, salvar_csv
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_carteiras_teoricas")

BASE_URL  = "https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/"
PAGE_SIZE = 120
ARQUIVO   = Path("data/b3_carteiras_teoricas.csv")

# (código, segment, nome completo)
INDICES = [
    # Amplos
    ("IBOV", "1", "Ibovespa"),
    ("IBRA", "1", "IBrA - Índice Brasil Amplo"),
    ("IBRX", "1", "IBrX 100 - Índice Brasil 100"),
    ("IBXL", "1", "IBrX 50 - Índice Brasil 50"),
    ("IGCX", "1", "IGC - Governança Corporativa"),
    ("ITAG", "1", "ITAG - Tag Along"),
    ("MLCX", "1", "MLCX - Mid-Large Cap"),
    ("SMLL", "1", "SMLL - Small Cap"),
    ("IVBX", "1", "IVBX-2 - Valor BM&F Bovespa"),
    # Segmentos e Setoriais
    ("IDIV", "1", "IDIV - Índice Dividendos"),
    ("IFIX", "1", "IFIX - Índice de Fundos Imobiliários"),
    ("IFNC", "1", "IFNC - Índice Financeiro"),
    ("ICON", "1", "ICON - Índice de Consumo"),
    ("IEEX", "1", "IEEX - Índice de Energia Elétrica"),
    ("IMAT", "1", "IMAT - Índice de Materiais Básicos"),
    ("IMOB", "1", "IMOB - Índice Imobiliário"),
    ("INDX", "1", "INDX - Índice do Setor Industrial"),
    ("UTIL", "1", "UTIL - Índice Utilidade Pública"),
    # Sustentabilidade e Governança
    ("IGCT", "1", "IGCT - Governança Corporativa Trade"),
    ("IGNM", "1", "IGNM - Novo Mercado"),
    ("ISEE", "1", "ISE - Sustentabilidade Empresarial"),
    ("ICO2", "1", "ICO2 - Carbono Eficiente"),
]

CABECALHO = [
    "data_captura", 
    "indice", "indice_nome",
    "codigo_ativo", "nome_ativo", "tipo_ativo",
    "quantidade_teorica", "participacao_pct",
    "reducao_capital", "segmento",
]


def _url(index: str, segment: str, page: int) -> str:
    return BASE_URL + b64_encode_params({
        "language": "pt-br", "pageNumber": page,
        "pageSize": PAGE_SIZE, "index": index, "segment": segment,
    })


def _pagina(session, index: str, segment: str, page: int) -> tuple[list, int]:
    try:
        resp = session.get(_url(index, segment, page), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data, len(data)
        return data.get("results", []), data.get("total", 0)
    except Exception as e:
        log.error(f"[{index}] Página {page}: {e}")
        return [], 0


def _limpar_int(valor) -> str:
    if valor is None:
        return ""
    texto = str(valor).strip()
    clean = texto.replace(".", "").replace(" ", "")
    if "," in clean:
        clean = clean.split(",")[0]
    return clean


def _limpar_float(valor) -> str:
    if valor is None:
        return ""
    texto = str(valor).strip()
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    return texto.replace("%", "").strip()


def _mapear(item: dict, data_captura: str,
            index: str, label: str) -> dict:
    return {
        "data_captura":       data_captura,
        "indice":             index,
        "indice_nome":        label,
        "codigo_ativo":       limpar(item.get("cod")          or item.get("ticker")        or item.get("code")),
        "nome_ativo":         limpar(item.get("asset")        or item.get("companyName")   or item.get("name")),
        "tipo_ativo":         limpar(item.get("type")         or item.get("typeStock")),
        "quantidade_teorica": _limpar_int(limpar(item.get("theoricalQty") or item.get("quantity")      or item.get("qtyTheoretical"))),
        "participacao_pct":   _limpar_float(limpar(item.get("part")         or item.get("participation") or item.get("weight"))),
        "reducao_capital":    _limpar_float(limpar(item.get("reductionPct") or item.get("capitalReduction"))),
        "segmento":           limpar(item.get("segment")      or item.get("setor")),
    }


def _capturar_indice(session, index: str, segment: str, label: str,
                     data_captura: str) -> list[dict]:
    log.info(f"[{index}] Capturando...")
    primeira, total = _pagina(session, index, segment, 1)
    if not primeira:
        log.warning(f"[{index}] Sem dados.")
        return []

    total = total or len(primeira)
    n_pag = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    log.info(f"[{index}] {total} ativos | {n_pag} página(s)")

    todos = list(primeira)
    for p in range(2, n_pag + 1):
        log.info(f"[{index}] Página {p}/{n_pag}...")
        resultados, _ = _pagina(session, index, segment, p)
        todos.extend(resultados)
        time.sleep(0.3)

    return [_mapear(i, data_captura, index, label) for i in todos]


def capturar() -> list[dict]:
    data_captura, _ = agora_brt()
    session = nova_session()
    todos, erros = [], []

    for index, segment, label in INDICES:
        registros = _capturar_indice(session, index, segment, label, data_captura)
        if registros:
            todos.extend(registros)
        else:
            erros.append(index)
        time.sleep(0.5)

    log.info(f"{len(todos)} registros | {len(INDICES)-len(erros)}/{len(INDICES)} índices OK")
    if erros:
        log.warning(f"Sem dados: {', '.join(erros)}")
    return todos

class B3CarteirasTeoricasScraper(BaseScraper):
    name = "b3_carteiras_teoricas"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'indice', 'codigo_ativo']
    
    # Catálogo de Metadados
    title = 'B3 Carteiras Teóricas'
    description = 'Composição diária das carteiras teóricas dos 22 principais índices da B3. Permite acompanhar a evolução do peso de cada ativo ao longo do tempo e detectar entradas e saídas nas carteiras.'
    icon = '🗂️'
    icon_class = 'icon-b3'
    badge = 'Diário · 22 índices'
    badge_class = 'badge-daily'
    tags = ['IBOV', 'IBRA', 'IBrX 100', 'IBrX 50', 'SMLL', 'IDIV', 'IFIX', 'IFNC', 'ICON', 'IEEX', 'IMAT', 'IMOB', 'INDX', 'UTIL', 'IGC', 'ISE', 'ICO2', '+ 5 índices']
    source = 'B3 API · ~1.000 linhas/dia'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 Carteiras Teóricas ===")
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3CarteirasTeoricasScraper().run()
