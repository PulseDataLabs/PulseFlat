"""
scrapers/b3_valor_mercado_empresas.py
--------------------------------------
Valor de mercado (Market Capitalization) das companhias abertas listadas na B3.
Captura a posição mensal de capitalização em Reais (BRL) e Dólares (USD),
indicadores de participação nos índices IBOV e IBrX-100, e totalizadores gerais de mercado.

Fonte:
- B3 Market Data / Sistemas Web Listados
- Endpoint: GET https://sistemaswebb3-listados.b3.com.br/marketValueProxy/marketValueCall/GetStockExchangeMonthly/{b64}
Saída:
- data/b3_valor_mercado_empresas.csv (Acumulado mensal por empresa)
- data/b3_valor_mercado_totais.csv (Totais consolidados de mercado IBOV, IBXX e Total Geral)
"""

import base64
import json
import re
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.base import BaseScraper
from utils import agora_brt, get_logger, limpar, salvar_csv

log = get_logger("b3_valor_mercado_empresas")

ROOT_DIR = Path(__file__).resolve().parents[1]
ARQUIVO_EMPRESAS = ROOT_DIR / "data" / "b3_valor_mercado_empresas.csv"
ARQUIVO_TOTAIS = ROOT_DIR / "data" / "b3_valor_mercado_totais.csv"

CABECALHO_EMPRESAS = [
    "data_captura",
    "data_referencia",
    "empresa",
    "pertence_ibov",
    "pertence_ibrx100",
    "valor_mercado_brl",
    "valor_mercado_brl_anterior",
    "variacao_brl_pct",
    "valor_mercado_usd",
    "valor_mercado_usd_anterior",
    "variacao_usd_pct",
]

CABECALHO_TOTAIS = [
    "data_captura",
    "data_referencia",
    "segmento",
    "quantidade_empresas",
    "valor_mercado_brl",
    "valor_mercado_brl_anterior",
    "variacao_brl_pct",
    "valor_mercado_usd",
    "valor_mercado_usd_anterior",
    "variacao_usd_pct",
]

BASE_URL = (
    "https://sistemaswebb3-listados.b3.com.br/marketValueProxy/marketValueCall/GetStockExchangeMonthly/"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
}


def _parse_float_br(val) -> float | None:
    """Converte strings numéricas em formato brasileiro ('5.763.490.316,97' ou '-2,46%') para float."""
    if val is None:
        return None
    s = str(val).strip().replace("%", "").replace(".", "").replace(",", ".")
    if not s or s == "":
        return None
    try:
        return round(float(s), 2)
    except ValueError:
        return None


def _extrair_data_iso(texto: str) -> str:
    """Extrai 'DD/MM/YYYY' de títulos como 'Valor (R$) em 31/08/2026' e retorna 'YYYY-MM-DD'."""
    match = re.search(r"(\d{2})/(\d{2})/(\d{4})", str(texto or ""))
    if match:
        dia, mes, ano = match.groups()
        return f"{ano}-{mes}-{dia}"
    return ""


def capturar_dados_mensais() -> tuple[list[dict], list[dict], str]:
    """
    Executa a requisição ao serviço marketValueCall da B3 e retorna:
    (lista_empresas, lista_totais, data_referencia_iso).
    """
    payload = {"pageNumber": 1, "pageSize": 9999, "language": "pt-br"}
    b64_param = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
    url = BASE_URL + b64_param

    log.info(f"Requisitando valor de mercado mensal da B3: {url[:70]}...")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        dados_json = resp.json()
    except Exception as e:
        log.error(f"Erro ao acessar API de valor de mercado da B3: {e}")
        return [], [], ""

    header = dados_json.get("Header", {})
    body = dados_json.get("Body", [])
    footer = dados_json.get("Footer", [])

    data_captura, _ = agora_brt()
    str_data_ref = _extrair_data_iso(header.get("Column003", ""))
    if not str_data_ref:
        # Fallback para Date do Header
        date_raw = str(header.get("Date", "")).split("T")[0]
        str_data_ref = date_raw if date_raw else data_captura

    log.info(f"Data de referência identificada: {str_data_ref}")

    # 1. Parsing das Empresas
    empresas = []
    for item in body:
        nome_empresa = limpar(str(item.get("Column002") or ""))
        if not nome_empresa:
            continue

        col0 = str(item.get("Column000") or "").strip()
        col1 = str(item.get("Column001") or "").strip()

        pertence_ibov = "SIM" if "*" in col0 else "NAO"
        pertence_ibrx100 = "SIM" if "*" in col1 else "NAO"

        empresas.append(
            {
                "data_captura": data_captura,
                "data_referencia": str_data_ref,
                "empresa": nome_empresa,
                "pertence_ibov": pertence_ibov,
                "pertence_ibrx100": pertence_ibrx100,
                "valor_mercado_brl": _parse_float_br(item.get("Column003")),
                "valor_mercado_brl_anterior": _parse_float_br(item.get("Column004")),
                "variacao_brl_pct": _parse_float_br(item.get("Column005")),
                "valor_mercado_usd": _parse_float_br(item.get("Column006")),
                "valor_mercado_usd_anterior": _parse_float_br(item.get("Column007")),
                "variacao_usd_pct": _parse_float_br(item.get("Column008")),
            }
        )

    # 2. Parsing dos Totais do Rodapé
    totais = []
    for item in footer:
        desc = limpar(str(item.get("Column002") or ""))
        if not desc:
            continue

        # Extrai quantidade de empresas se houver (ex: 'TOTAL GERAL (343)')
        match_qtd = re.search(r"\((\d+)\)", desc)
        qtd_empresas = int(match_qtd.group(1)) if match_qtd else len(empresas)

        segmento = "TOTAL GERAL" if "TOTAL GERAL" in desc else desc

        totais.append(
            {
                "data_captura": data_captura,
                "data_referencia": str_data_ref,
                "segmento": segmento,
                "quantidade_empresas": qtd_empresas,
                "valor_mercado_brl": _parse_float_br(item.get("Column003")),
                "valor_mercado_brl_anterior": _parse_float_br(item.get("Column004")),
                "variacao_brl_pct": _parse_float_br(item.get("Column005")),
                "valor_mercado_usd": _parse_float_br(item.get("Column006")),
                "valor_mercado_usd_anterior": _parse_float_br(item.get("Column007")),
                "variacao_usd_pct": _parse_float_br(item.get("Column008")),
            }
        )

    return empresas, totais, str_data_ref


def atualizar_arquivo_totais(totais: list[dict]) -> None:
    """Salva e acumula os totais no arquivo data/b3_valor_mercado_totais.csv."""
    if not totais:
        return
    df_totais = pd.DataFrame(totais)
    salvar_csv(
        arquivo=ARQUIVO_TOTAIS,
        registros=df_totais,
        cabecalho=CABECALHO_TOTAIS,
        chaves_dedup=["data_referencia", "segmento"],
        acumular=True,
    )
    log.info(f"Totais agregados de valor de mercado salvos em {ARQUIVO_TOTAIS}.")


class B3ValorMercadoEmpresasScraper(BaseScraper):
    name = "b3_valor_mercado_empresas"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = True
    compress = False
    chaves_dedup = ["data_referencia", "empresa"]

    # Catálogo de Metadados
    title = "B3 — Valor de Mercado das Empresas Listadas (Market Cap)"
    description = (
        "Valor de mercado (Market Capitalization) em BRL e USD de todas as companhias abertas listadas na B3, "
        "com indicadores de participação no Ibovespa (IBOV) e IBrX-100 (IBRX100), variação mensal e totais de mercado."
    )
    icon = "🏢"
    icon_class = "icon-b3"
    badge = "Mensal"
    badge_class = "badge-monthly"
    tags = [
        "b3",
        "market cap",
        "valor de mercado",
        "empresas listadas",
        "ações",
        "ibov",
        "ibrx100",
        "capitalização",
    ]
    source = "B3"

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 — Valor de Mercado das Empresas Listadas ===")
        empresas, totais, str_ref = capturar_dados_mensais()
        if not empresas:
            return pd.DataFrame(columns=CABECALHO_EMPRESAS)

        # Atualiza o arquivo de totais em paralelo
        if totais:
            atualizar_arquivo_totais(totais)

        df = pd.DataFrame(empresas)
        df = df.sort_values(by="valor_mercado_brl", ascending=False)
        colunas = [c for c in CABECALHO_EMPRESAS if c in df.columns]
        return df[colunas]


if __name__ == "__main__":
    B3ValorMercadoEmpresasScraper().run()
