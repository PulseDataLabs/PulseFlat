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

log = get_logger("bcb_ptax")

ARQUIVO = Path("data/bcb_ptax.csv")

CABECALHO = [
    "data_captura",
    
    "data_hora_cotacao",
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
            "data_hora_cotacao": limpar(item.get("dataHoraCotacao")),
            "cotacao_compra":    limpar(item.get("cotacaoCompra")),
            "cotacao_venda":     limpar(item.get("cotacaoVenda")),
        })

    log.info(f"{len(registros)} cotações PTAX capturadas.")
    return registros


def main():
    log.info("=== BCB PTAX (USD/BRL) ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "data_hora_cotacao"],
               acumular=False)


if __name__ == "__main__":
    main()
