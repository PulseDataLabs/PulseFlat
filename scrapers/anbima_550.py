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
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, nova_session, salvar_csv
from utils.parsers import _CAL
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("anbima_550")

ARQUIVO = Path("data/anbima_550.csv")
URL_TPL = "https://www.anbima.com.br/informacoes/res-550/arqs/{yyyymmdd}_550.tex"

CABECALHO = [
    "data_captura",
    
    "titulo",
    "vencimento",
    "preco_unitario",
    "preco_retorno",
    "posicao_custodia",
]


def _url_referencia(session) -> tuple[str, date]:
    for delta in range(1, 6):
        ref = _CAL.offset(date.today(), -delta)
        url = URL_TPL.format(yyyymmdd=ref.strftime("%Y%m%d"))
        try:
            resp = session.head(url, timeout=15)
            if resp.status_code == 200:
                return url, ref
        except Exception:
            pass
    ref = _CAL.offset(date.today(), -1)
    return URL_TPL.format(yyyymmdd=ref.strftime("%Y%m%d")), ref


def capturar() -> list[dict]:
    session = nova_session()
    url, data_ref = _url_referencia(session)
    log.info(f"Buscando ANBIMA 550: {url}")

    for tentativa in range(1, 4):
        try:
            resp = session.get(url, timeout=30)
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

    data_captura, _ = agora_brt()
    registros = []

    for linha in linhas_dados:
        partes = linha.split()
        if len(partes) < 5:
            continue
        registros.append({
            "data_captura":    data_captura,
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

class Anbima550Scraper(BaseScraper):
    name = "anbima_550"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'titulo', 'vencimento']
    
    # Catálogo de Metadados
    title = 'ANBIMA Resolução 550'
    description = 'Ativos de renda fixa da Resolução ANBIMA 550: preço unitário, preço de retorno e posição em custódia.'
    icon = '📋'
    icon_class = 'icon-anbima'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['preço_unitário', 'preço_retorno', 'custódia']
    source = 'ANBIMA'

    def fetch(self) -> pd.DataFrame:
        log.info("=== ANBIMA 550 — Renda Fixa ===")
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    Anbima550Scraper().run()
