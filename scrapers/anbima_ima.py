"""
scrapers/anbima_ima.py
-----------------------
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
from io import StringIO
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv

log = get_logger("anbima_ima")

ARQUIVO = Path("data/anbima_ima.csv")
URL = "https://www.anbima.com.br/informacoes/ima/arqs/ima_completo.txt"

CABECALHO = [
    "data_captura",
    "hora_captura",
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


def capturar() -> list[dict]:
    log.info(f"Buscando IMA ANBIMA: {URL}")

    for tentativa in range(1, 4):
        try:
            resp = requests.get(URL, timeout=30,
                                headers={"User-Agent": "Mozilla/5.0"})
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

    data_captura, hora_captura = agora_brt()
    registros = []

    for linha in dados_linhas:
        if "@" not in linha:
            continue
        partes = linha.split("@")
        if len(partes) < len(COLUNAS_ARQUIVO):
            partes += [""] * (len(COLUNAS_ARQUIVO) - len(partes))
        registro = {"data_captura": data_captura, "hora_captura": hora_captura}
        for col, val in zip(COLUNAS_ARQUIVO, partes):
            registro[col] = limpar(val.replace(",", ".")).replace("--", "")
        registros.append(registro)

    if not registros:
        log.error("Nenhum dado IMA extraído.")
        sys.exit(1)

    log.info(f"{len(registros)} índices IMA capturados.")
    return registros


def main():
    log.info("=== ANBIMA IMA/IDA — Índices de Renda Fixa ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "data_referencia", "indice"])


if __name__ == "__main__":
    main()
