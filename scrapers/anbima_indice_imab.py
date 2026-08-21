"""
scrapers/anbima_indice_imab.py
-------------------------------
Índice IMA-B da ANBIMA — histórico completo de rentabilidade
do índice de Mercado ANBIMA (IMA-B).

Fonte: https://s3-data-prd-use1-precos.s3.us-east-1.amazonaws.com/arquivos/indices-historico/IMAGERAL-HISTORICO.xls
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd

from scrapers.utils.base import BaseScraper
from utils.base import get_logger, nova_session
from utils.parsers import enriquecer, read_existing_header, xls_rows

log = get_logger("anbima_indice_imab")

URL = "https://s3-data-prd-use1-precos.s3.us-east-1.amazonaws.com/arquivos/indices-historico/IMAGERAL-HISTORICO.xls"
ARQUIVO = Path("data/anbima_indice_imab.csv.gz")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    log.info(f"Baixando {URL}")
    resp = session.get(URL, timeout=180)
    resp.raise_for_status()
    rows = xls_rows(resp.content)
    enriched, header_novo = enriquecer("anbima_indice_imab", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header


class AnbimaIndiceImabScraper(BaseScraper):
    name = "anbima_indice_imab"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True
    chaves_dedup = ["data_captura", "conjunto", "registro_hash"]

    # Catálogo de Metadados
    title = "ANBIMA — Índice IMA-B"
    description = "Série histórica e composição de rentabilidade dos títulos públicos indexados ao IPCA (NTN-B)."
    icon = "📈"
    icon_class = "icon-anbima"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = ["ima-b", "índice", "rentabilidade"]
    source = "ANBIMA · S3"

    def fetch(self) -> pd.DataFrame:
        log.info("=== ANBIMA — Índice IMA-B ===")
        rows, header = capturar()
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in header if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    AnbimaIndiceImabScraper().run()
