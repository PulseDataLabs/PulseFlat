"""
scrapers/b3_futuros_ajustes.py
-------------------------------
⚠ DESATIVADO — A fonte legada (www2.bmf.com.br) foi descontinuada pela B3 em
dez/2025. Os dados de ajustes de futuros não estão disponíveis em API pública
conhecida. Mantido apenas como referência.

Ajustes de fechamento de contratos futuros (pregão) da B3/BM&F (fonte legada).

Fonte: https://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-ajustes-do-pregao-ptBR.asp (OFFLINE)
Campos: mercadoria, vencimento, preco_ajuste_anterior,
        preco_ajuste_atual, variacao, valor_ajuste_por_contrato_brl
"""

import sys
import time
from datetime import date, timedelta
from pathlib import Path

import requests
from lxml import html

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_futuros_ajustes")

ARQUIVO = Path("data/b3_futuros_ajustes.csv")

CABECALHO = [
    "data_captura",
    
    "data_referencia",
    "mercadoria",
    "vencimento",
    "preco_ajuste_anterior",
    "preco_ajuste_atual",
    "variacao",
    "valor_ajuste_por_contrato_brl",
]

URL_TPL = (
    "https://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/"
    "lum-ajustes-do-pregao-ptBR.asp?dData1={data}"
)

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-ajustes-do-pregao-ptBR.asp",
}


def _url_referencia() -> tuple[str, date]:
    for delta in range(1, 6):
        ref = date.today() - timedelta(days=delta)
        if ref.weekday() >= 5:
            continue
        return URL_TPL.format(data=ref.strftime("%d%%2F%m%%2F%Y")), ref
    ref = date.today() - timedelta(days=1)
    return URL_TPL.format(data=ref.strftime("%d%%2F%m%%2F%Y")), ref


def _limpar_num(val: str) -> str:
    return val.replace("\xa0", "").replace(".", "").replace(",", ".").strip()


def capturar() -> list[dict]:
    url, data_ref = _url_referencia()
    log.info(f"Buscando ajustes B3 futuros: {url}")

    for tentativa in range(1, 4):
        try:
            resp = requests.get(url, timeout=30, headers=HEADERS)
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error("Falha ao acessar ajustes B3 futuros.")
                sys.exit(1)
            time.sleep(5)

    if not resp.content.strip():
        log.error(
            "Fonte legada descontinuada (www2.bmf.com.br). "
            "A página de ajustes de futuros não está mais disponível. "
            "Desative este scraper em run_all.py."
        )
        sys.exit(1)

    try:
        tree = html.fromstring(resp.content)
    except Exception:
        log.error("HTML inválido da fonte legada (www2.bmf.com.br).")
        sys.exit(1)

    xpath_td = '//*[@id="tblDadosAjustes"]/tbody/tr/td'
    celulas = tree.xpath(xpath_td)

    if not celulas:
        log.error("Tabela de ajustes não encontrada no HTML.")
        sys.exit(1)

    vals = [
        "" if c.text is None
        else _limpar_num(c.text)
        for c in celulas
    ]

    NCOLS = 6
    COLUNAS = [
        "mercadoria", "vencimento", "preco_ajuste_anterior",
        "preco_ajuste_atual", "variacao", "valor_ajuste_por_contrato_brl",
    ]

    data_captura, _ = agora_brt()
    registros = []
    mercadoria_atual = ""

    for i in range(0, len(vals) - NCOLS + 1, NCOLS):
        linha = vals[i:i + NCOLS]
        if len(linha) < NCOLS:
            break
        if linha[0]:
            mercadoria_atual = linha[0]
        registro = {
            "data_captura": data_captura,
            "data_referencia": data_ref.strftime("%Y-%m-%d"),
            "mercadoria": mercadoria_atual
        }
        for col, val in zip(COLUNAS[1:], linha[1:]):
            registro[col] = val
        registros.append(registro)

    if not registros:
        log.error("Nenhum ajuste de futuro extraído.")
        sys.exit(1)

    log.info(f"{len(registros)} ajustes capturados (ref: {data_ref}).")
    return registros

class B3FuturosAjustesScraper(BaseScraper):
    name = "b3_futuros_ajustes"
    accumulate = True
    chaves_dedup = ['data_captura', 'mercadoria', 'vencimento']
    
    # Catálogo de Metadados
    title = 'B3 Futuros — Ajustes de Fechamento'
    description = 'Preços de ajuste de fechamento diários para contratos futuros de juros (DI), dólar, índice Ibovespa e commodities.'
    icon = '📉'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['futuros', 'ajustes', 'commodities', 'b3', 'bm&f']
    source = 'B3'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 Futuros — Ajustes de Fechamento ===")
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3FuturosAjustesScraper().run()
