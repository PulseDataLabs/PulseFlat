"""
scrapers/anbima_debentures.py
------------------------------
Preços e taxas indicativas de debêntures publicadas diariamente pela ANBIMA.

Formato do arquivo: delimitado por @, skiprows=3
Fonte: https://www.anbima.com.br/informacoes/merc-sec-debentures/arqs/db{YYMMDD}.txt
"""

import sys
import time
from datetime import date, timedelta
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv

log = get_logger("anbima_debentures")

ARQUIVO = Path("data/anbima_debentures.csv")

CABECALHO = [
    "data_captura",
    "hora_captura",
    "codigo",
    "nome_emissor",
    "dt_repactuacao_vencimento",
    "indice_correcao",
    "tx_compra",
    "tx_venda",
    "tx_indicativa",
    "desvio_padrao",
    "intervalo_indicativo_min",
    "intervalo_indicativo_max",
    "pu",
    "ratio_pu_par_vne",
    "duration",
    "pct_reune",
    "ref_ntnb",
]

URL_TPL = "https://www.anbima.com.br/informacoes/merc-sec-debentures/arqs/db{yymmdd}.txt"


def _url_referencia() -> tuple[str, date]:
    for delta in range(1, 6):
        ref = date.today() - timedelta(days=delta)
        if ref.weekday() >= 5:
            continue
        url = URL_TPL.format(yymmdd=ref.strftime("%y%m%d"))
        try:
            resp = requests.head(url, timeout=15)
            if resp.status_code == 200:
                return url, ref
        except Exception:
            pass
    ref = date.today() - timedelta(days=1)
    return URL_TPL.format(yymmdd=ref.strftime("%y%m%d")), ref


def capturar() -> list[dict]:
    url, data_ref = _url_referencia()
    log.info(f"Buscando debêntures ANBIMA: {url}")

    for tentativa in range(1, 4):
        try:
            resp = requests.get(url, timeout=30,
                                headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error("Falha ao baixar arquivo ANBIMA debêntures.")
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
    dados_linhas = [l for l in linhas[3:] if l.strip() and "@" in l]

    data_captura, hora_captura = agora_brt()
    registros = []

    COLUNAS = [
        "codigo", "nome_emissor", "dt_repactuacao_vencimento", "indice_correcao",
        "tx_compra", "tx_venda", "tx_indicativa", "desvio_padrao",
        "intervalo_indicativo_min", "intervalo_indicativo_max", "pu",
        "ratio_pu_par_vne", "duration", "pct_reune", "ref_ntnb",
    ]

    for linha in dados_linhas:
        partes = linha.split("@")
        if len(partes) < len(COLUNAS):
            partes += [""] * (len(COLUNAS) - len(partes))
        registro = {"data_captura": data_captura, "hora_captura": hora_captura}
        for col, val in zip(COLUNAS, partes):
            registro[col] = limpar(val.replace(",", "."))
        registros.append(registro)

    if not registros:
        log.error("Nenhuma debênture extraída.")
        sys.exit(1)

    log.info(f"{len(registros)} debêntures capturadas (ref: {data_ref}).")
    return registros


def main():
    log.info("=== ANBIMA — Debêntures ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "codigo"])


if __name__ == "__main__":
    main()
