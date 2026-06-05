"""
B3 – Dados Financeiros de Companhias Listadas

Captura posição acionária, ações em circulação (free float) e composição
do capital social de todas as companhias listadas na B3.

Endpoint:
    https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedFinancial/<b64>

Fonte:
    https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/
"""

import sys
import time
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils import (
    get_logger,
    agora_brt,
    limpar,
    b64_encode_params,
    nova_session,
)

import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger(__name__)

BASE_URL = (
    "https://sistemaswebb3-listados.b3.com.br"
    "/listedCompaniesProxy/CompanyCall"
)

PAGE_SIZE = 9999
SLEEP_MIN = 0.4
SLEEP_MAX = 1.2

CABECALHO = [
    "data_captura",
    "secao",
    "codigo_cvm",
    "codigo_negociacao",
    "nome_empresa",
    "cnpj",
    "data_referencia",
    "descricao",
    "pct_on",
    "pct_pn",
    "pct_total",
    "quantidade",
    "percentual",
]


def _url(endpoint: str, params: dict) -> str:
    """Monta a URL completa com parâmetros em Base64."""
    return f"{BASE_URL}/{endpoint}/{b64_encode_params(params)}"


def _listar_empresas(session) -> list[dict]:
    """Busca todas as empresas listadas via GetInitialCompanies."""
    params = {
        "language": "pt-br",
        "pageNumber": 1,
        "pageSize": PAGE_SIZE,
    }
    url = _url("GetInitialCompanies", params)
    log.info("Buscando lista de empresas listadas na B3...")
    resp = session.get(url)
    resp.raise_for_status()
    dados = resp.json()
    empresas = dados.get("results", [])
    log.info(f"  {len(empresas)} empresas encontradas")
    return empresas


def _extrair_financeiro(dados: dict, empresa: dict, agora: str) -> list[dict]:
    """Extrai as 3 seções do JSON GetListedFinancial e retorna registros planos."""
    registros = []

    cvm  = empresa.get("codeCVM", "")
    code = empresa.get("issuingCompany", "")
    nome = empresa.get("tradingName", "")
    cnpj = empresa.get("cnpj", "")

    # 1) Posição acionária
    pos = dados.get("positionShareholders")
    if pos and isinstance(pos, dict):
        dt_ref = limpar(pos.get("informationReceived", ""))
        for r in pos.get("results", []):
            registros.append({
                "data_captura":    agora,
                "secao":           "posicao_acionaria",
                "codigo_cvm":      cvm,
                "codigo_negociacao": code,
                "nome_empresa":    nome,
                "cnpj":            cnpj,
                "data_referencia": dt_ref,
                "descricao":       limpar(r.get("describle", "")),
                "pct_on":          limpar(r.get("on", "")),
                "pct_pn":          limpar(r.get("pn", "")),
                "pct_total":       limpar(r.get("total", "")),
                "quantidade":      "",
                "percentual":      "",
            })

    # 2) Free float (ações em circulação)
    ff = dados.get("freeFloatResult")
    if ff and isinstance(ff, dict):
        dt_ref = limpar(ff.get("title", ""))
        for r in ff.get("results", []):
            registros.append({
                "data_captura":    agora,
                "secao":           "free_float",
                "codigo_cvm":      cvm,
                "codigo_negociacao": code,
                "nome_empresa":    nome,
                "cnpj":            cnpj,
                "data_referencia": dt_ref,
                "descricao":       limpar(r.get("describle", "")),
                "pct_on":          "",
                "pct_pn":          "",
                "pct_total":       "",
                "quantidade":      limpar(r.get("value", "")),
                "percentual":      limpar(r.get("value2", "")),
            })

    # 3) Composição do capital social
    cs = dados.get("capitalStockComposition")
    if cs and isinstance(cs, dict):
        dt_ref = limpar(cs.get("title", ""))
        for r in cs.get("results", []):
            registros.append({
                "data_captura":    agora,
                "secao":           "capital_social",
                "codigo_cvm":      cvm,
                "codigo_negociacao": code,
                "nome_empresa":    nome,
                "cnpj":            cnpj,
                "data_referencia": dt_ref,
                "descricao":       limpar(r.get("describle", "")),
                "pct_on":          "",
                "pct_pn":          "",
                "pct_total":       "",
                "quantidade":      limpar(r.get("value", "")),
                "percentual":      "",
            })

    return registros


def capturar() -> list[dict]:
    """
    Captura dados financeiros de todas as companhias listadas na B3.

    Para cada empresa, chama o endpoint GetListedFinancial que retorna
    em uma única resposta JSON:
      - positionShareholders  → Posição acionária
      - freeFloatResult       → Ações em circulação (free float)
      - capitalStockComposition → Composição do capital social

    Returns
    -------
    list[dict]
        Lista de registros planos prontos para DataFrame.
    """
    session = nova_session()
    agora   = agora_brt()
    todos   = []

    empresas = _listar_empresas(session)

    for i, emp in enumerate(empresas, 1):
        cvm  = emp.get("codeCVM", "")
        nome = emp.get("tradingName", "")

        if not cvm:
            continue

        log.info(f"[{i}/{len(empresas)}] {nome} (CVM: {cvm})")

        params = {"codeCVM": str(cvm), "language": "pt-br"}
        url    = _url("GetListedFinancial", params)

        try:
            resp = session.get(url)
            resp.raise_for_status()
            dados = resp.json()
        except Exception as e:
            log.warning(f"  Erro ao buscar {nome}: {e}")
            time.sleep(SLEEP_MAX)
            continue

        if not isinstance(dados, dict):
            time.sleep(SLEEP_MIN)
            continue

        novos = _extrair_financeiro(dados, emp, agora)
        todos.extend(novos)

        time.sleep(SLEEP_MIN + (SLEEP_MAX - SLEEP_MIN) * random.random())

    log.info(f"Total de registros capturados: {len(todos)}")
    session.close()
    return todos


class Scraper(BaseScraper):
    # ── Orquestração ──────────────────────────────────────────────────────────
    name        = "b3_companhias_financeiro"
    group       = "b3"
    enabled     = True
    phase       = 1

    # ── Persistência ──────────────────────────────────────────────────────────
    accumulate  = False                          # snapshot: substitui o arquivo a cada run
    output_file = ROOT / "data" / "b3_companhias_financeiro.csv"
    chaves_dedup = ["secao", "codigo_cvm", "descricao", "data_referencia"]

    # ── Catálogo / Dashboard ──────────────────────────────────────────────────
    title        = "B3 – Financeiro de Cias Listadas"
    description  = (
        "Posição acionária, free float e composição do capital social "
        "de todas as companhias listadas na B3."
    )
    icon         = "🏛️"
    icon_class   = "icon-b3"
    badge        = "Snapshot"
    badge_class  = "badge-snapshot"
    tags         = ["b3", "posicao-acionaria", "free-float", "capital-social"]
    source       = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/"

    def fetch(self) -> pd.DataFrame:
        """Captura os dados e devolve um DataFrame — salvamento é responsabilidade do BaseScraper."""
        rows = capturar()
        df   = pd.DataFrame(rows)
        if df.empty:
            return df
        return df.reindex(columns=CABECALHO)


if __name__ == "__main__":
    # Execução direta: usa o ciclo completo do BaseScraper (fetch → sanitize → save)
    Scraper().run()
