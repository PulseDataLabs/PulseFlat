"""
scrapers/anbima_550.py
-----------------------
Listagem de ativos de renda fixa da Resolução ANBIMA 550.

Formato: espaços múltiplos, skiprows=2, skipfooter=4
Campos: TITULO, VENCIMENTO, PRECO_UNITARIO, PRECO_RETORNO, POSICAO_CUSTODIA
Fonte: https://www.anbima.com.br/informacoes/res-550/arqs/{YYYYMMDD}_550.tex
"""

import sys
import time
from datetime import date, timedelta
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv

log = get_logger("anbima_550")

ARQUIVO = Path("data/anbima_550.csv")
URL_TPL = "https://www.anbima.com.br/informacoes/res-550/arqs/{yyyymmdd}_550.tex"

CABECALHO = [
    "data_captura",
    "hora_captura",
    "titulo",
    "vencimento",
    "preco_unitario",
    "preco_retorno",
    "posicao_custodia",
]


def _url_referencia() -> tuple[str, date]:
    for delta in range(1, 6):
        ref = date.today() - timedelta(days=delta)
        if ref.weekday() >= 5:
            continue
        url = URL_TPL.format(yyyymmdd=ref.strftime("%Y%m%d"))
        try:
            resp = requests.head(url, timeout=15)
            if resp.status_code == 200:
                return url, ref
        except Exception:
            pass
    ref = date.today() - timedelta(days=1)
    return URL_TPL.format(yyyymmdd=ref.strftime("%Y%m%d")), ref


def capturar() -> list[dict]:
    url, data_ref = _url_referencia()
    log.info(f"Buscando ANBIMA 550: {url}")

    for tentativa in range(1, 4):
        try:
            resp = requests.get(url, timeout=30,
                                headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error("Falha ao baixar arquivo ANBIMA 550.")
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
    # Skiprows=2, skipfooter=4
    linhas_dados = linhas[2:-4] if len(linhas) > 6 else linhas[2:]

    data_captura, hora_captura = agora_brt()
    registros = []

    for linha in linhas_dados:
        partes = linha.split()
        if len(partes) < 5:
            continue
        registros.append({
            "data_captura":    data_captura,
            "hora_captura":    hora_captura,
            "titulo":          limpar(partes[0]),
            "vencimento":      limpar(partes[1]),
            "preco_unitario":  limpar(partes[2].replace(".", "").replace(",", ".")),
            "preco_retorno":   limpar(partes[3].replace(".", "").replace(",", ".")),
            "posicao_custodia": limpar(partes[4].replace(".", "").replace(",", ".")),
        })

    if not registros:
        log.error("Nenhum ativo 550 extraído.")
        sys.exit(1)

    log.info(f"{len(registros)} ativos ANBIMA 550 capturados (ref: {data_ref}).")
    return registros


def main():
    log.info("=== ANBIMA 550 — Renda Fixa ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "titulo", "vencimento"])


if __name__ == "__main__":
    main()
