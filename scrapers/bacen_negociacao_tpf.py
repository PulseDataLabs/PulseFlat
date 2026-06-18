"""
scrapers/bacen_negociacao_tpf.py
---------------------------------
Captura dados de negociacao de Titulos Publicos Federais (TPF)
Extra-grupo do Banco Central (BCB/DEMAB).

Fontes:
  - https://www4.bcb.gov.br/pom/demab/negociacoes/download/NegEYYYYMM.ZIP
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import get_logger, nova_session, salvar_csv
from utils.parsers import date_ref, replace_date_vars, rows_from_zip, enriquecer, read_existing_header
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("bacen_negociacao_tpf")

URL_TPLT = "https://www4.bcb.gov.br/pom/demab/negociacoes/download/NegEYYYYMM.ZIP"
OUTPUT_FILE = Path("data/bacen_negociacao_tpf_extragrupo.csv")
DATASET_ID = "bacen_negociacao_tpf_extragrupo"

ARQUIVOS_CONFIG = [
    {"tipo": "corrente", "ref": None},
    {"tipo": "anterior", "ref": "mes_anterior"},
]


def capturar() -> list[dict]:
    session = nova_session()
    registros = []

    for cfg in ARQUIVOS_CONFIG:
        tipo = cfg["tipo"]
        ref = cfg["ref"]
        dt = date_ref(ref)

        url = replace_date_vars(URL_TPLT, dt)
        log.info(f"[{DATASET_ID}][{tipo}] Baixando {url}")

        try:
            resp = session.get(url, timeout=120)
            resp.raise_for_status()
            rows = rows_from_zip(resp.content)
            if not rows:
                raise RuntimeError("Sem linhas apos processamento")

            enriched, header_novo = enriquecer(DATASET_ID, rows)
            header_existente = read_existing_header(OUTPUT_FILE)
            header = []
            for col in header_existente + header_novo:
                if col and col not in header:
                    header.append(col)

            salvar_csv(OUTPUT_FILE, enriched, header, chaves_dedup=["data_captura", "conjunto", "registro_hash"])
            log.info(f"[{DATASET_ID}][{tipo}] {len(enriched)} linha(s) salvas")
            registros.extend(enriched)
        except Exception as e:
            log.error(f"[{DATASET_ID}][{tipo}] Falha: {e}")

    return registros

class BacenNegociacaoTpfScraper(BaseScraper):
    name = "bacen_negociacao_tpf"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'conjunto', 'registro_hash']
    
    # Catálogo de Metadados
    title = 'BCB — Negociação TPF Extra-grupo'
    description = 'Operações de compra e venda de Títulos Públicos Federais extra-grupo realizadas no mercado aberto (BCB/DEMAB).'
    icon = '📋'
    icon_class = 'icon-bcb'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['título público', 'compra/venda', 'quantidade', 'preço']
    source = 'BCB · DEMAB'

    def fetch(self) -> pd.DataFrame:
        log.info("=== BCB — Negociacao TPF Extra-grupo ===")
        capturar()


if __name__ == "__main__":
    BacenNegociacaoTpfScraper().run()
