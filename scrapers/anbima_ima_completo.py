"""
scrapers/anbima_ima_completo.py
-------------------------------
Índices de mercado ANBIMA (IMA, IDA, IDKA) — dados mark-to-market diários.

Fonte: https://www.anbima.com.br/informacoes/ima/arqs/ima_completo.txt
Campos: DATA_REFERENCIA, INDICE, NUMERO_INDICE, VARIACAO_DIARIA,
        VARIACAO_MENSAL, VARIACAO_ANUAL, VARIACAO_ULTIMOS_12_MESES,
        VARIACAO_ULTIMOS_24_MESES, DURATION_DU, PESO_GERAL,
        CARTEIRA_A_MERCADO_RS_MIL, NUMERO_OPERACOES,
        QUANT_NEGOCIADA_1000_TITULOS, VALOR_NEGOCIADO_RS_MIL,
        PMR, CONVEXIDADE, YIELD, REDEMPTION_YIELD
"""

import sys
import time
from datetime import datetime, date, timedelta
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, nova_session, salvar_csv
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("anbima_ima_completo")

ARQUIVO = Path("data/anbima_ima_completo.csv")
URL = "https://www.anbima.com.br/informacoes/ima/arqs/ima_completo.txt"

CABECALHO = [
    "data_captura",
    "data_referencia",
    "indice",
    "numero_indice",
    "variacao_diaria",
    "variacao_mensal",
    "variacao_anual",
    "variacao_ultimos_12_meses",
    "variacao_ultimos_24_meses",
    "duration_du",
    "peso_geral",
    "carteira_a_mercado_rs_mil",
    "numero_operacoes",
    "quant_negociada_1000_titulos",
    "valor_negociado_rs_mil",
    "pmr",
    "convexidade",
    "yield_",
    "redemption_yield",
]

COLUNAS_ARQUIVO = [
    "data_referencia", "indice", "numero_indice", "variacao_diaria",
    "variacao_mensal", "variacao_anual", "variacao_ultimos_12_meses",
    "variacao_ultimos_24_meses", "duration_du", "peso_geral",
    "carteira_a_mercado_rs_mil", "numero_operacoes",
    "quant_negociada_1000_titulos", "valor_negociado_rs_mil",
    "pmr", "convexidade", "yield_", "redemption_yield",
]


def obter_d1_util() -> str:
    """Retorna a data do dia útil anterior (D-1) no formato DD/MM/YYYY."""
    data_hoje_str, _ = agora_brt()
    hoje = datetime.strptime(data_hoje_str, "%Y-%m-%d").date()
    ref = hoje - timedelta(days=1)
    while ref.weekday() >= 5:  # Pula fins de semana (Sábado=5, Domingo=6)
        ref -= timedelta(days=1)
    return ref.strftime("%d/%m/%Y")


def _formatar_data_iso(data_str: str) -> str:
    parts = data_str.split("/")
    if len(parts) == 3:
        return f"{parts[2]}-{parts[1]}-{parts[0]}"
    return data_str


def capturar() -> list[dict]:
    log.info(f"Buscando IMA ANBIMA: {URL}")
    session = nova_session()

    for tentativa in range(1, 4):
        try:
            resp = session.get(URL, timeout=30)
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error("Falha ao baixar IMA ANBIMA.")
                sys.exit(1)
            time.sleep(5)

    for enc in ("latin-1", "utf-8", "cp1252"):
        try:
            texto = resp.content.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        texto = resp.content.decode("utf-8", errors="replace")

    linhas = texto.splitlines()
    # Remove comentários (##) e pega até linha em branco
    dados_linhas = []
    for linha in linhas:
        if linha.startswith("##"):
            continue
        if not linha.strip():
            break
        dados_linhas.append(linha)

    # As 3 primeiras linhas são cabeçalho do arquivo
    dados_linhas = dados_linhas[3:]

    # Validar que a data de referência no arquivo corresponde ao D-1 útil esperado
    d1_util_str = obter_d1_util()
    log.info(f"D-1 útil esperado: {d1_util_str}")
    
    primeira_linha_valida = next((l for l in dados_linhas if "@" in l), None)
    if primeira_linha_valida:
        p = primeira_linha_valida.split("@")
        if len(p) > 1:
            file_date = p[1].strip()
            if file_date != d1_util_str:
                log.error(f"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).")
                sys.exit(1)

    data_captura, _ = agora_brt()
    registros = []

    for linha in dados_linhas:
        if "@" not in linha:
            continue
        partes = linha.split("@")
        if len(partes) < len(COLUNAS_ARQUIVO) + 1:
            partes += [""] * (len(COLUNAS_ARQUIVO) + 1 - len(partes))
            
        registro = {"data_captura": data_captura}
        # Zipa pulando o primeiro elemento (partes[0]), que é o tipo de registro
        for col, val in zip(COLUNAS_ARQUIVO, partes[1:]):
            val_clean = limpar(val.replace(",", ".")).replace("--", "")
            if col == "data_referencia":
                val_clean = _formatar_data_iso(val_clean)
            registro[col] = val_clean
        registros.append(registro)

    if not registros:
        log.error("Nenhum dado IMA extraído.")
        sys.exit(1)

    log.info(f"{len(registros)} índices IMA capturados.")
    return registros

class AnbimaImaCompletoScraper(BaseScraper):
    name = "anbima_ima_completo"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'data_referencia', 'indice']
    
    # Catálogo de Metadados
    title = 'ANBIMA IMA / IDA'
    description = 'Índices de mercado ANBIMA (IMA, IRF-M, IDA, IDKA): variações diárias, mensais e anuais, duration e peso geral.'
    icon = '📊'
    icon_class = 'icon-anbima'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['ima-geral', 'irf-m', 'ida', 'idka', 'duration']
    source = 'ANBIMA'

    def fetch(self) -> pd.DataFrame:
        log.info("=== ANBIMA IMA Completo ===")
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    AnbimaImaCompletoScraper().run()
