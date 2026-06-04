"""
scrapers/b3_bmf_taxas_juros.py
--------------------------------
Taxas de mercado para swaps (ex-Taxas Referenciais BM&F) via BDI da B3.

A fonte legada (www2.bmf.com.br/…/TxRef1.asp) foi descontinuada em dez/2025.
Os dados agora estão no Hub de Dados Públicos da B3 (arquivos.b3.com.br/bdi).

Endpoint: POST https://arquivos.b3.com.br/bdi/table/{TABELA}/{data}/{data}/{pag}/{size}
"""

import sys
import time
from datetime import date, timedelta
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_bmf_taxas_juros")

ARQUIVO = Path("data/b3_bmf_taxas_juros.csv")

# Candidatos em ordem de probabilidade — o script para no primeiro que retornar dados
TABELAS_CANDIDATAS = [
    "DerivativesMarketSwapRates",
    "SwapRates",
    "ReferenceRates",
    "DerivativesSwapRates",
    "MarketRatesSwap",
    "TaxasSwap",
    "TaxasReferenciaisBMF",
    "DerivativesMarketRates",
]

CABECALHO = [
    "data_captura",
    
    "tabela_origem",
    "data_referencia",
    "curva",
    "prazo_dias",
    "taxa",
    "base",
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


def _buscar_pagina(url: str) -> tuple[list[dict], list[str]]:
    """Retorna (rows, column_names). rows vazio = sem dados ou erro."""
    try:
        resp = requests.post(url, json={}, timeout=30, headers=HEADERS)
        resp.raise_for_status()
        raw = resp.json()
        table = raw.get("table") or {}
        columns_raw = table.get("columns") or []
        values = table.get("values") or []
        columns = [_to_snake(c["name"]) for c in columns_raw if isinstance(c, dict)]
        if not values or not columns:
            return [], columns
        return [dict(zip(columns, row)) for row in values], columns
    except Exception as e:
        log.warning(f"Erro em {url}: {e}")
        return [], []


def _descobrir_tabela(str_data: str) -> str | None:
    """Tenta cada candidato e retorna o nome da primeira tabela com dados."""
    for nome in TABELAS_CANDIDATAS:
        url = (
            f"https://arquivos.b3.com.br/bdi/table/{nome}/"
            f"{str_data}/{str_data}/1/5"
        )
        log.info(f"Testando tabela: {nome}")
        rows, cols = _buscar_pagina(url)
        if rows:
            log.info(f"  ✓ Tabela encontrada: {nome} | colunas: {cols}")
            return nome
        log.info(f"  ✗ Sem dados")
        time.sleep(0.3)
    return None


def _data_referencia() -> date:
    for delta in range(1, 6):
        ref = date.today() - timedelta(days=delta)
        if ref.weekday() < 5:
            return ref
    return date.today() - timedelta(days=1)


def capturar() -> list[dict]:
    data_ref = _data_referencia()
    str_data = data_ref.strftime("%Y-%m-%d")
    log.info(f"Buscando taxas swap B3 (ref: {str_data})...")

    tabela = _descobrir_tabela(str_data)
    if not tabela:
        log.error(
            "Nenhuma tabela de swap encontrada. Candidatos testados:\n  "
            + "\n  ".join(TABELAS_CANDIDATAS)
            + "\nAbra https://arquivos.b3.com.br/bdi/tabelas no browser, "
            "procure por 'swap' ou 'taxa' e adicione o nome correto a TABELAS_CANDIDATAS."
        )
        sys.exit(1)

    data_captura, _ = agora_brt()
    todos = []
    pagina = 1

    while True:
        url = (
            f"https://arquivos.b3.com.br/bdi/table/{tabela}/"
            f"{str_data}/{str_data}/{pagina}/{PAGE_SIZE}"
        )
        log.info(f"  Página {pagina}...")
        rows, _ = _buscar_pagina(url)
        if not rows:
            break

        for item in rows:
            curva  = item.get("curve_name") or item.get("curve") or item.get("index_name") or item.get("description") or item.get("nm_indic") or ""
            prazo  = item.get("business_days") or item.get("term_days") or item.get("days") or item.get("prazo") or ""
            taxa   = item.get("rate") or item.get("yield_") or item.get("value") or item.get("taxa") or ""
            base   = item.get("base") or item.get("day_count") or item.get("base_calc") or ""

            todos.append({
                "data_captura":    data_captura,
                "tabela_origem":   tabela,
                "data_referencia": limpar(str(item.get("rpt_dt", str_data))),
                "curva":           limpar(str(curva)),
                "prazo_dias":      limpar(str(prazo)),
                "taxa":            limpar(str(taxa)),
                "base":            limpar(str(base)),
            })

        pagina += 1
        time.sleep(1)

    if not todos:
        log.error("Tabela encontrada mas sem registros.")
        sys.exit(1)

    log.info(f"{len(todos)} taxas swap capturadas via tabela '{tabela}' (ref: {data_ref}).")
    return todos

class B3BmfTaxasJurosScraper(BaseScraper):
    name = "b3_bmf_taxas_juros"
    accumulate = True
    chaves_dedup = ['data_captura', 'data_referencia', 'curva', 'prazo_dias']
    
    # Catálogo de Metadados
    title = 'B3 BDI — Taxas de Swap'
    description = 'Taxas de mercado e de referência para swaps e taxas referenciais da BM&F por prazo em dias corridos e úteis.'
    icon = '📊'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['taxas', 'swap', 'juros', 'bm&f', 'curva']
    source = 'B3 BDI'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 BM&F — Taxas de Mercado para Swaps ===")
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3BmfTaxasJurosScraper().run()
