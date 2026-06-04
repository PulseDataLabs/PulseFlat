"""
scrapers/b3_indices_precos_historicos.py
-----------------------------------------
Histórico de preços de índices da B3 (IBOV, IBRA, IFIX, IDIV, SMLL)
via API de carteiras teóricas.

Fonte: https://sistemaswebb3-listados.b3.com.br/indexStatisticsProxy/IndexCall/GetPortfolioDay/
"""

import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import FUSO, b64_encode_params, get_logger, nova_session, salvar_csv
from utils.parsers import json_rows, enriquecer, read_existing_header
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_indices_precos_historicos")

BASE_URL = "https://sistemaswebb3-listados.b3.com.br/indexStatisticsProxy/IndexCall/GetPortfolioDay/"
INDICES = ["IBOV", "IBRA", "IFIX", "IDIV", "SMLL"]
ARQUIVO = Path("data/b3_indices_precos_historicos.csv")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    ano_atual = datetime.now(FUSO).year
    anos = [ano_atual - 1, ano_atual]
    todos = []

    for idx in INDICES:
        for ano in anos:
            url = BASE_URL + b64_encode_params({"language": "pt-br", "year": ano, "index": idx})
            log.info(f"Índice {idx}/{ano}...")
            try:
                resp = session.get(url, timeout=60)
                resp.raise_for_status()
                data = resp.json() or {}
                result = data.get("results") or []
                for item in result:
                    item["indice"] = idx
                    item["ano"] = str(ano)
                todos.extend(result)
            except Exception as e:
                log.warning(f"Falha {idx}/{ano}: {e}")
            time.sleep(0.2)

    rows = json_rows(todos)
    enriched, header_novo = enriquecer("b3_indices_precos_historicos", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header

class B3IndicesPrecosHistoricosScraper(BaseScraper):
    name = "b3_indices_precos_historicos"
    group = "b3"
    enabled = False
    phase = 1
    accumulate = True
    chaves_dedup = ['indice', 'ano', 'day']
    
    # Catálogo de Metadados
    title = 'B3 — Índices de Preços Históricos'
    description = 'Composição histórica e pesos de índices B3 (IBOV, IBRA, IFIX, IDIV, SMLL) com dados dos últimos 2 anos.'
    icon = '📈'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['ibov', 'ibra', 'ifix', 'idiv', 'smll']
    source = 'B3 API'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 — Índices de Preços Históricos ===")
        rows, header = capturar()
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in header if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3IndicesPrecosHistoricosScraper().run()
