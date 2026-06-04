"""
scrapers/b3_cotahist_anual.py
-------------------------------
COTAHIST anual da B3 — cotações históricas do ano corrente.

Fonte: https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{year}.ZIP
"""

import io
import sys
import zipfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import FUSO, get_logger, nova_session, salvar_csv
from utils.parsers import decode_bytes, fwf_rows, enriquecer, read_existing_header
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_cotahist_anual")

URL_FORMAT = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{year}.ZIP"

COTAHIST_WIDTHS = [2, 8, 2, 12, 3, 12, 10, 3, 4, 13, 13, 13, 13, 13, 13, 13, 5, 18, 18, 13, 1, 8, 7, 13, 12, 3]
COTAHIST_FIELDS = [
    "regtype", "refdate", "bdi_code", "symbol", "instrument_market", "corporation_name", "specification_code",
    "days_to_settlement", "trading_currency", "open", "high", "low", "average", "close", "best_bid", "best_ask",
    "trade_quantity", "traded_contracts", "volume", "strike_price", "strike_price_adjustment_indicator",
    "maturity_date", "allocation_lot_size", "strike_price_in_points", "isin", "distribution_id",
]

ARQUIVO = Path("data/b3_cotahist_anual.csv")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    ano = datetime.now(FUSO).year
    url = URL_FORMAT.format(year=ano)
    log.info(f"Baixando {url}")
    resp = session.get(url, timeout=180)
    resp.raise_for_status()

    rows = []
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for info in zf.infolist():
            if info.is_dir() or info.file_size == 0:
                continue
            text = decode_bytes(zf.read(info.filename))
            parsed = fwf_rows(text, COTAHIST_FIELDS, COTAHIST_WIDTHS, only_regtype_01=True)
            for r in parsed:
                r["arquivo_origem"] = info.filename
                rows.append(r)

    enriched, header_novo = enriquecer("b3_cotahist_anual", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header

class B3CotahistAnualScraper(BaseScraper):
    name = "b3_cotahist_anual"
    group = "b3"
    enabled = False
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'conjunto', 'registro_hash']
    
    # Catálogo de Metadados
    title = 'B3 Cotahist Anual'
    description = 'Dados capturados.'
    icon = '📊'
    icon_class = 'icon-misc'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['b3']
    source = 'B3'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 — COTAHIST Anual ===")
        rows, header = capturar()
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3CotahistAnualScraper().run()
