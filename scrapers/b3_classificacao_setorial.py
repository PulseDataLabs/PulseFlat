"""
scrapers/b3_classificacao_setorial.py
---------------------------------------
Classificação setorial das empresas negociadas na B3.

Fonte: https://bvmf.bmfbovespa.com.br/InstDados/InformacoesEmpresas/ClassifSetorial.zip
"""

import io
import sys
import time
import zipfile
from pathlib import Path

import openpyxl
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, nova_session, salvar_csv
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_classificacao_setorial")

URL = "https://bvmf.bmfbovespa.com.br/InstDados/InformacoesEmpresas/ClassifSetorial.zip"
ARQUIVO = Path("data/b3_classificacao_setorial.csv")

CABECALHO = [
    "data_captura",
    "setor_economico",
    "subsetor",
    "segmento",
    "nome_empresa",
    "codigo",
    "segmento_listagem",
]


def capturar() -> list[dict]:
    session = nova_session()
    log.info(f"Baixando classificação setorial da B3 de {URL}...")

    resp = None
    for tentativa in range(1, 4):
        try:
            resp = session.get(URL, timeout=60)
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3 falhou: {e}")
            if tentativa == 3:
                log.error("Falha ao baixar classificação setorial da B3.")
                sys.exit(1)
            time.sleep(5)

    if not resp or not resp.content:
        log.error("Resposta vazia recebida do servidor B3.")
        sys.exit(1)

    log.info("Lendo arquivo ZIP...")
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        # Encontra o arquivo .xlsx correspondente
        xls_files = [n for n in zf.namelist() if n.lower().endswith(".xlsx")]
        if not xls_files:
            log.error("Nenhum arquivo .xlsx encontrado dentro do ZIP.")
            sys.exit(1)
        
        arquivo_nome = xls_files[0]
        log.info(f"Extraindo e processando {arquivo_nome}...")
        xlsx_bytes = zf.read(arquivo_nome)

    wb = openpyxl.load_workbook(io.BytesIO(xlsx_bytes), data_only=True)
    ws = wb.active

    data_captura, _ = agora_brt()
    companies = []
    
    current_setor = ""
    current_subsetor = ""
    current_segmento = ""

    # Itera a partir da linha 7 (onde se inicia o conteúdo do cabeçalho estrutural)
    for row in ws.iter_rows(min_row=7, values_only=True):
        # Ignora linhas totalmente vazias
        if all(val is None for val in row):
            continue

        # Coluna 0 (Setor Econômico)
        val_0 = limpar(row[0]) if len(row) > 0 and row[0] is not None else ""
        # Coluna 1 (Subsetor)
        val_1 = limpar(row[1]) if len(row) > 1 and row[1] is not None else ""
        # Coluna 2 (Segmento ou Nome da Empresa)
        val_2 = limpar(row[2]) if len(row) > 2 and row[2] is not None else ""
        # Coluna 3 (Código Ticker)
        val_3 = limpar(row[3]) if len(row) > 3 and row[3] is not None else ""
        # Coluna 4 (Segmento de Listagem)
        val_4 = limpar(row[4]) if len(row) > 4 and row[4] is not None else ""

        # Evita cabeçalhos repetidos e linhas informativas/legendas
        if val_0 == "SETOR ECONÔMICO" or val_3 == "CÓDIGO" or val_0.startswith("("):
            continue

        # Atualiza a hierarquia
        if val_0:
            current_setor = val_0
        if val_1:
            current_subsetor = val_1
        if val_2 and not val_3:
            current_segmento = val_2

        # Se houver um código de ticker válido, é uma empresa!
        if val_3:
            companies.append({
                "data_captura": data_captura,
                "setor_economico": current_setor,
                "subsetor": current_subsetor,
                "segmento": current_segmento,
                "nome_empresa": val_2,
                "codigo": val_3,
                "segmento_listagem": val_4,
            })

    wb.close()
    log.info(f"{len(companies)} empresas processadas da classificação setorial.")
    return companies

class B3ClassificacaoSetorialScraper(BaseScraper):
    name = "b3_classificacao_setorial"
    group = "b3"
    enabled = False
    phase = 1
    accumulate = False
    chaves_dedup = ['data_captura', 'codigo']
    
    # Catálogo de Metadados
    title = 'B3 Classificação Setorial'
    description = 'Classificação setorial completa das empresas listadas na B3 (setor econômico, subsetor e segmento de atuação).'
    icon = '🗂️'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['setor', 'subsetor', 'segmento']
    source = 'B3'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 — Classificação Setorial ===")
        registros = capturar()
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(registros)
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3ClassificacaoSetorialScraper().run()
