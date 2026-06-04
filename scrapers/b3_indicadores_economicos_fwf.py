"""
scrapers/b3_indicadores_economicos_fwf.py
-----------------------------------------
Indicadores econômicos da B3 — arquivo ID com dados macroeconômicos
em formato de largura fixa.

Fonte: https://www.b3.com.br/pesquisapregao/download?filelist=ID%y%m%d.ex_
"""

import io
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import get_logger, nova_session, salvar_csv
from utils.parsers import date_ref, replace_date_vars, decode_bytes, fwf_rows, enriquecer, read_existing_header
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_indicadores_economicos_fwf")

URL = "https://www.b3.com.br/pesquisapregao/download?filelist=ID%y%m%d.ex_"

INDICADORES_WIDTHS = [6, 3, 2, 8, 2, 25, 25, 2, 36]
INDICADORES_FIELDS = [
    "id_transacao", "compl_transacao", "tipo_registro", "data_geracao_arquivo", "grupo_indicador",
    "cod_indicador", "valor_indicador", "num_casas_decimais", "reserva",
]

ARQUIVO = Path("data/b3_indicadores_economicos_fwf.csv")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    dt = date_ref("dia_anterior")
    url = replace_date_vars(URL, dt)
    log.info(f"Baixando {url}")
    resp = session.get(url, timeout=180)
    resp.raise_for_status()

    rows = []
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for info in zf.infolist():
            if info.is_dir() or info.file_size == 0:
                continue
            text = decode_bytes(zf.read(info.filename))
            parsed = fwf_rows(text, INDICADORES_FIELDS, INDICADORES_WIDTHS)
            for r in parsed:
                r["arquivo_origem"] = info.filename
                rows.append(r)

    enriched, header_novo = enriquecer("b3_indicadores_economicos_fwf", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header

class B3IndicadoresEconomicosFwfScraper(BaseScraper):
    name = "b3_indicadores_economicos_fwf"
    group = "b3"
    enabled = False
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'conjunto', 'registro_hash']
    
    # Catálogo de Metadados
    title = 'B3 Indicadores Economicos Fwf'
    description = 'Dados capturados.'
    icon = '📊'
    icon_class = 'icon-misc'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['b3']
    source = 'B3'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 — Indicadores Econômicos (FWF) ===")
        rows, header = capturar()
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3IndicadoresEconomicosFwfScraper().run()
