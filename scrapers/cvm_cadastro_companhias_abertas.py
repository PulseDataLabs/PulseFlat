"""
scrapers/cvm_cadastro_companhias_abertas.py
--------------------------------------------
Cadastro de companhias abertas registradas na CVM.

Fonte: https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import get_logger, nova_session, salvar_csv
from utils.parsers import decode_bytes, csv_rows, enriquecer, read_existing_header
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("cvm_cadastro_companhias_abertas")

URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv"
ARQUIVO = Path("data/cvm_cadastro_companhias_abertas.csv")


def capturar() -> tuple[list[dict], list[str]]:
    session = nova_session()
    log.info(f"Baixando {URL}")
    resp = session.get(URL, timeout=180)
    resp.raise_for_status()
    rows = csv_rows(decode_bytes(resp.content))
    enriched, header_novo = enriquecer("cvm_cadastro_companhias_abertas", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header

class CvmCadastroCompanhiasAbertasScraper(BaseScraper):
    name = "cvm_cadastro_companhias_abertas"
    group = "cvm"
    enabled = False
    phase = 1
    accumulate = False
    chaves_dedup = ['data_captura', 'conjunto', 'registro_hash']
    
    # Catálogo de Metadados
    title = 'CVM — Cadastro de Companhias Abertas'
    description = 'Cadastro completo de companhias abertas registradas na CVM: CNPJ, razão social, nome de pregão, situação cadastral e código CVM.'
    icon = '🏛️'
    icon_class = ''
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['cnpj', 'companhia aberta', 'cadastro cvm']
    source = 'CVM · Dados Abertos'

    def fetch(self) -> pd.DataFrame:
        log.info("=== CVM — Cadastro de Companhias Abertas ===")
        rows, header = capturar()
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    CvmCadastroCompanhiasAbertasScraper().run()
