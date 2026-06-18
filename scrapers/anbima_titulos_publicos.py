"""
scrapers/anbima_titulos_publicos.py
------------------------------------
Preços e taxas indicativas de títulos públicos (Tesouro Direto e LFT/NTN/LTN)
publicados diariamente pela ANBIMA.

Formato do arquivo: delimitado por @, skiprows=3
Fonte: https://www.anbima.com.br/informacoes/merc-sec/arqs/ms{YYMMDD}.txt
"""

import sys
import time
from datetime import date
from io import StringIO
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, nova_session, salvar_csv
from utils.parsers import _CAL
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("anbima_titulos_publicos")

ARQUIVO = Path("data/anbima_titulos_publicos.csv")

CABECALHO = [
    "data_captura",
    
    "titulo",
    "data_referencia",
    "codigo_selic",
    "data_base_emissao",
    "data_vencimento",
    "tx_compra",
    "tx_venda",
    "tx_indicativa",
    "pu",
    "desvio_padrao",
    "interv_ind_inf_d0",
    "interv_ind_sup_d0",
    "interv_ind_inf_dma1",
    "interv_ind_sup_dma1",
    "criterio",
]

URL_TPL = "https://www.anbima.com.br/informacoes/merc-sec/arqs/ms{yymmdd}.txt"


def _url_referencia(session) -> tuple[str, date]:
    """Tenta o dia útil anterior; recua até encontrar arquivo disponível (máx 5 dias)."""
    for delta in range(1, 6):
        ref = _CAL.offset(date.today(), -delta)
        url = URL_TPL.format(yymmdd=ref.strftime("%y%m%d"))
        try:
            resp = session.head(url, timeout=15)
            if resp.status_code == 200:
                return url, ref
        except Exception:
            pass
    ref = _CAL.offset(date.today(), -1)
    return URL_TPL.format(yymmdd=ref.strftime("%y%m%d")), ref


def capturar() -> list[dict]:
    session = nova_session()
    url, data_ref = _url_referencia(session)
    log.info(f"Buscando títulos públicos ANBIMA: {url}")

    for tentativa in range(1, 4):
        try:
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error("Falha ao baixar arquivo ANBIMA títulos públicos.")
                sys.exit(1)
            time.sleep(5)

    # Detecta encoding
    for enc in ("latin-1", "utf-8", "cp1252"):
        try:
            texto = resp.content.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        texto = resp.content.decode("utf-8", errors="replace")

    linhas = texto.splitlines()
    # Pula cabeçalho (3 linhas) e remove rodapé vazio
    dados_linhas = [l for l in linhas[3:] if l.strip() and "@" in l]

    data_captura, _ = agora_brt()
    registros = []

    COLUNAS = [
        "titulo", "data_referencia", "codigo_selic", "data_base_emissao",
        "data_vencimento", "tx_compra", "tx_venda", "tx_indicativa", "pu",
        "desvio_padrao", "interv_ind_inf_d0", "interv_ind_sup_d0",
        "interv_ind_inf_dma1", "interv_ind_sup_dma1", "criterio",
    ]

    for linha in dados_linhas:
        partes = linha.split("@")
        if len(partes) < len(COLUNAS):
            partes += [""] * (len(COLUNAS) - len(partes))
        registro = {"data_captura": data_captura}
        for col, val in zip(COLUNAS, partes):
            registro[col] = limpar(val.replace(",", "."))
        registros.append(registro)

    if not registros:
        log.error("Nenhum título público extraído.")
        sys.exit(1)

    log.info(f"{len(registros)} títulos públicos capturados (ref: {data_ref}).")
    return registros

class AnbimaTitulosPublicosScraper(BaseScraper):
    name = "anbima_titulos_publicos"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    chaves_dedup = ['data_captura', 'titulo', 'data_vencimento']
    
    # Catálogo de Metadados
    title = 'ANBIMA Títulos Públicos'
    description = 'Preços e taxas indicativas de títulos públicos federais (LTN, NTN, LFT), incluindo PU, duration e desvio padrão.'
    icon = '🏛️'
    icon_class = 'icon-anbima'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['ltn', 'ntn', 'lft', 'pu', 'tx_indicativa']
    source = 'ANBIMA'

    def fetch(self) -> pd.DataFrame:
        log.info("=== ANBIMA — Títulos Públicos ===")
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    AnbimaTitulosPublicosScraper().run()
