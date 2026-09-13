"""
scrapers/b3_bdi_derivativos_resumo.py
--------------------------------------
Boletim Diário do Mercado (BDI) da B3: Derivativos — Resumo das Operações.
Consolida contratos futuros, opções e rolagens negociados no pregão eletrônico da B3
(Commodities, Taxas de Juros, Moedas/Câmbio e Índices), com número de negócios,
contratos negociados e volume financeiro em BRL e USD.

Fonte: https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/boletim-diario-do-mercado/
Endpoint: POST https://arquivos.b3.com.br/bdi/table/DerivativesOperation2/{data}/{data}/{pagina}/{page_size}
"""

import sys
import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.base import BaseScraper
from utils import agora_brt, get_logger, limpar
from utils.parsers import _CAL

log = get_logger("b3_bdi_derivativos_resumo")

ARQUIVO = Path("data/b3_bdi_derivativos_resumo.csv")

CABECALHO = [
    "data_captura",
    "data_referencia",
    "categoria",
    "mercado",
    "derivativo",
    "tipo_contrato",
    "ticker_simb",
    "quantidade_negocios",
    "quantidade_contratos",
    "volume_financeiro_brl",
    "volume_financeiro_usd",
]

PAGE_SIZE = 500
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json",
}


def _buscar_pagina_derivativos(url: str) -> list[dict]:
    """Requisita uma página da tabela DerivativesOperation2 na API BDI da B3."""
    try:
        resp = requests.post(url, json={}, timeout=30, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        table = data.get("table", {})
        values = table.get("values", [])
        raw_cols = [c.get("name") for c in table.get("columns", [])]

        if not values or not raw_cols:
            return []

        col_count = len(raw_cols)
        results = []
        for row in values:
            row_dict = dict(zip(raw_cols, row[:col_count]))
            results.append(row_dict)
        return results
    except Exception as e:
        log.warning(f"Erro ao requisitar {url}: {e}")
        return []


def _data_referencia() -> date:
    """Retorna o dia útil anterior conforme o calendário financeiro da B3."""
    return _CAL.offset(date.today(), -1)


def capturar_dia(data_alvo: date) -> list[dict]:
    """Captura os registros de resumo de derivativos para um dia de pregão específico."""
    str_data = data_alvo.strftime("%Y-%m-%d")
    data_captura, _ = agora_brt()
    todos = []
    pagina = 1

    while True:
        url = (
            f"https://arquivos.b3.com.br/bdi/table/DerivativesOperation2/"
            f"{str_data}/{str_data}/{pagina}/{PAGE_SIZE}"
        )
        rows = _buscar_pagina_derivativos(url)
        if not rows:
            break

        for item in rows:
            ticker = limpar(str(item.get("TckrSymb", "")))
            categoria = limpar(str(item.get("Category", "")))
            mercado = limpar(str(item.get("Market", "")))
            derivativo = limpar(str(item.get("Derivatives", "")))
            tipo = limpar(str(item.get("Tipo", "")))

            # Sanitização numérica
            n_trades = item.get("NmbrTradesDay")
            n_cntrcts = item.get("NmbrCntrctsDay")
            vlm_rs = item.get("TotalVlmRS")
            vlm_us = item.get("TotalVlmUS")

            todos.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": str_data,
                    "categoria": categoria,
                    "mercado": mercado,
                    "derivativo": derivativo,
                    "tipo_contrato": tipo,
                    "ticker_simb": ticker,
                    "quantidade_negocios": n_trades if n_trades is not None else "",
                    "quantidade_contratos": n_cntrcts if n_cntrcts is not None else "",
                    "volume_financeiro_brl": vlm_rs if vlm_rs is not None else "",
                    "volume_financeiro_usd": vlm_us if vlm_us is not None else "",
                }
            )

        # Se retornou menos que o tamanho da página ou paginação zerada, concluído
        if len(rows) < PAGE_SIZE:
            break
        pagina += 1
        time.sleep(0.5)

    return todos


def capturar(target_date: date | None = None) -> list[dict]:
    """
    Captura dados da sessão mais recente. Se target_date não for informado,
    testa os últimos dias úteis até encontrar a sessão mais recente publicada.
    """
    if target_date:
        return capturar_dia(target_date)

    data_base = _data_referencia()
    # Tenta até 5 dias úteis retroativos (para fins de semana, feriados ou D+1 da virada)
    for delta in range(5):
        d = _CAL.offset(data_base, -delta)
        log.info(f"Tentando capturar derivativos B3 para {d}...")
        registros = capturar_dia(d)
        if registros:
            log.info(f"{len(registros)} registros de derivativos encontrados para {d}.")
            return registros
        time.sleep(0.3)

    log.warning("Nenhum registro retornado da API da B3 nos últimos 5 dias úteis.")
    return []


class B3BdiDerivativosResumoScraper(BaseScraper):
    name = "b3_bdi_derivativos_resumo"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = True
    chaves_dedup = [
        "data_referencia",
        "ticker_simb",
        "categoria",
        "mercado",
        "derivativo",
        "tipo_contrato",
    ]

    # Catálogo de Metadados
    title = "B3 BDI — Derivativos (Resumo das Operações)"
    description = (
        "Resumo oficial das operações de derivativos do Boletim Diário do Mercado (BDI) da B3, "
        "abrangendo contratos futuros, opções e rolagens de commodities, juros, câmbio e índices, "
        "com contagem de negócios, contratos e volumes financeiros em R$ e US$."
    )
    icon = "⚡"
    icon_class = "icon-b3"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = ["derivativos", "futuros", "opções", "bdi", "commodities", "juros", "dólar", "B3"]
    source = "B3 · BDI"

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 BDI — Derivativos (Resumo das Operações) ===")
        dados = capturar(self.target_date)
        df = pd.DataFrame(dados)
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return pd.DataFrame(columns=CABECALHO)


if __name__ == "__main__":
    B3BdiDerivativosResumoScraper().run()
