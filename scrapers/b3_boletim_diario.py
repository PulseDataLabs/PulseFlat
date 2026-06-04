"""
scrapers/b3_boletim_diario.py
-----------------------------
Baixa arquivos diários do Boletim Diário B3 via API de download.

Fonte: https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/arquivos-para-download/
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, nova_session
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_boletim_diario")

BASE_URL = "https://arquivos.b3.com.br/api/download"
REQUEST_URL = f"{BASE_URL}/requestname"
DOWNLOAD_URL = f"{BASE_URL}/"

OUTPUT_DIR = Path("data/b3_boletim_diario")

ARQUIVOS_PADRAO = [
    "LendingOpenPosition",
    "OTCInstrumentsConsolidated",
    "InstrumentsConsolidated",
    "MarginScenarioLiquidAssets",
    "EconomicIndicatorPrice",
    "OTCTradeInformationConsolidated",
    "TradeInformationConsolidated",
    "TradeInformationConsolidatedAfterHours",
    "DerivativesOpenPosition",
    "LoanBalance",
]


def _data_referencia() -> str:
    data_env = os.getenv("B3_BOLETIM_DATE", "").strip()
    if data_env:
        return data_env
    return agora_brt()[0]


def _arquivos_configurados() -> list[str]:
    raw = os.getenv("B3_BOLETIM_FILES", "").strip()
    if raw:
        nomes = [nome.strip() for nome in raw.split(",") if nome.strip()]
        if nomes:
            return nomes
    return ARQUIVOS_PADRAO


def _solicitar_token(session, file_name: str, date: str, recaptcha_token: str) -> tuple[str, dict]:
    resp = session.get(
        REQUEST_URL,
        params={
            "fileName": file_name,
            "date": date,
            "recaptchaToken": recaptcha_token or "",
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    token = data.get("token") or ""
    file_info = data.get("file") or {}
    return token, file_info


def _nome_arquivo(file_name: str, date: str, file_info: dict) -> str:
    name = file_info.get("name") or f"{file_name}_{date.replace('-', '')}"
    ext = file_info.get("extension") or ""
    if ext and name.endswith(ext):
        return name
    return f"{name}{ext}" if ext else name


def _salvar_bytes(caminho: Path, conteudo: bytes) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(conteudo)


def capturar() -> tuple[int, int]:
    data_ref = _data_referencia()
    arquivos = _arquivos_configurados()
    recaptcha_token = os.getenv("B3_RECAPTCHA_TOKEN", "")
    session = nova_session()

    if not recaptcha_token:
        log.warning("B3_RECAPTCHA_TOKEN não definido; tentando request sem token.")

    ok, erro = 0, 0
    for file_name in arquivos:
        log.info(f"[{file_name}] Solicitando token ({data_ref})...")
        try:
            token, file_info = _solicitar_token(session, file_name, data_ref, recaptcha_token)
            if not token:
                log.error(f"[{file_name}] Token vazio na resposta.")
                erro += 1
                continue

            resp = session.get(DOWNLOAD_URL, params={"token": token}, timeout=60)
            resp.raise_for_status()
            nome_arquivo = _nome_arquivo(file_name, data_ref, file_info)
            caminho = OUTPUT_DIR / nome_arquivo
            _salvar_bytes(caminho, resp.content)
            log.info(f"[{file_name}] Salvo em {caminho}")
            ok += 1
            time.sleep(0.4)
        except Exception as e:
            log.error(f"[{file_name}] Erro ao baixar: {e}")
            erro += 1

    return ok, erro

class B3BoletimDiarioScraper(BaseScraper):
    name = "b3_boletim_diario"
    accumulate = True
    chaves_dedup = None
    
    # Catálogo de Metadados
    title = 'B3 Boletim Diário'
    description = 'Downloads dos arquivos consolidados do boletim diário de derivativos e posições em aberto da B3.'
    icon = '📂'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['boletim', 'derivativos', 'posição em aberto', 'B3']
    source = 'B3'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 Boletim Diário (arquivos para download) ===")
        ok, erro = capturar()
        log.info(f"{ok} arquivo(s) baixado(s) | {erro} erro(s)")
        if erro or ok == 0:
            raise RuntimeError('Execução do scraper falhou')


if __name__ == "__main__":
    B3BoletimDiarioScraper().run()
