"""
scrapers/bcb_ptax.py
--------------------
Cotação do dólar (USD/BRL) via API Olinda do Banco Central (PTAX).

Fonte: https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/
Campos: cotacao_compra, cotacao_venda, data_hora_cotacao
"""

import sys
import time
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, nova_session, salvar_csv
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("bcb_ptax")

ARQUIVO = Path("data/bcb_ptax.csv")

METADATA = {
    "title": "BCB PTAX",
    "description": "Cotações históricas diárias oficiais de compra e venda do dólar comercial (USD/BRL) publicadas pelo Banco Central do Brasil.",
    "icon": "💵",
    "icon_class": "icon-bcb",
    "badge": "Diário",
    "badge_class": "badge-daily",
    "tags": ["dólar", "ptax", "cotação", "compra", "venda", "bcb"],
    "source": "BCB",
    "file": "bcb_ptax.csv",
}

CABECALHO = [
    "data_captura",
    
    "data_referencia",
    "cotacao_compra",
    "cotacao_venda",
]

URL_TPL = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
    "?@dataInicial=%27{inicio}%27&@dataFinalCotacao=%27{fim}%27"
    "&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao"
)


def _url_hoje() -> str:
    hoje = date.today()
    inicio = date(2020, 1, 1)
    return URL_TPL.format(
        inicio=inicio.strftime("%m-%d-%Y"),
        fim=hoje.strftime("%m-%d-%Y"),
    )


def capturar() -> list[dict]:
    url = _url_hoje()
    log.info(f"Consultando PTAX: {url}")
    session = nova_session()

    dados = []
    proxima_url = url

    while proxima_url:
        log.info(f"Buscando página PTAX: {proxima_url}")
        for tentativa in range(1, 4):
            try:
                resp = session.get(proxima_url, timeout=30)
                resp.raise_for_status()
                break
            except requests.RequestException as e:
                log.warning(f"Tentativa {tentativa}/3: {e}")
                if tentativa == 3:
                    log.error("Falha ao acessar API PTAX.")
                    sys.exit(1)
                time.sleep(5)

        res_json = resp.json()
        pagina_dados = res_json.get("value", [])
        dados.extend(pagina_dados)
        proxima_url = res_json.get("@odata.nextLink")

    if not dados:
        log.error("Nenhum dado retornado pela API PTAX.")
        sys.exit(1)

    data_captura, _ = agora_brt()
    registros = []
    for item in dados:
        registros.append({
            "data_captura":      data_captura,
            "data_referencia":   limpar(item.get("dataHoraCotacao"))[:10],
            "cotacao_compra":    limpar(item.get("cotacaoCompra")),
            "cotacao_venda":     limpar(item.get("cotacaoVenda")),
        })

    log.info(f"{len(registros)} cotações PTAX capturadas.")
    return registros

class BcbPtaxScraper(BaseScraper):
    name = "bcb_ptax"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = False
    chaves_dedup = ['data_captura', 'data_referencia']
    
    # Catálogo de Metadados
    title = 'BCB PTAX'
    description = 'Cotações históricas diárias oficiais de compra e venda do dólar comercial (USD/BRL) publicadas pelo Banco Central do Brasil.'
    icon = '💵'
    icon_class = 'icon-bcb'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['dólar', 'ptax', 'cotação', 'compra', 'venda', 'bcb']
    source = 'BCB'

    def fetch(self) -> pd.DataFrame:
        log.info("=== BCB PTAX (USD/BRL) ===")
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    BcbPtaxScraper().run()
