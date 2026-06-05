#!/usr/bin/env python
# coding: utf-8
"""
scrapers/ibge_sidra.py
-----------------------
Metadados e datas de publicação de tabelas do IBGE SIDRA.

Tabelas capturadas por padrão:
  1737 — IPCA por item (IBGE)
  3065 — IPCA-15 por item (IBGE)
  1621 — INPC por item
  3066 — IPC-Br por item

Fonte: https://servicodados.ibge.gov.br/api/docs/
"""

import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv
import pandas as pd
from scrapers.utils.base import BaseScraper
from scripts.utils.ux import (
    banner, section, print_start, print_done, print_info, print_warn, print_fail,
    print_summary, ColorLogger, ICON,
)

log = ColorLogger("ibge_sidra")

ARQUIVO = Path("data/ibge_sidra.csv")

CABECALHO = [
    "data_captura",
    "serie_id",
    "nome_serie",
    "fonte",
    "periodo_referencia",
    "data_modificacao",
]

SERIES = {
    1737: "IPCA — Variação por item",
    3065: "IPCA-15 — Variação por item",
    1621: "INPC — Variação por item",
    # 3066 — IPC-Br removido: API retorna 500 consistentemente
}

URL_PERIODOS = "https://servicodados.ibge.gov.br/api/v3/agregados/{}/periodos"
URL_META = "https://sidra.ibge.gov.br/Ajax/JSon/Tabela/1/{}?versao=-1&_=0"


def _buscar_meta(serie_id: int) -> tuple[str, str]:
    """Retorna (nome, fonte) da tabela no SIDRA."""
    try:
        url = URL_META.format(serie_id)
        resp = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "*/*",
                "Referer": f"https://sidra.ibge.gov.br/tabela/{serie_id}",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return limpar(data.get("Nome", "")), limpar(data.get("Fonte", ""))
    except Exception:
        return SERIES.get(serie_id, f"Série {serie_id}"), "IBGE"


def _buscar_periodos(serie_id: int, data_captura: str) -> list[dict]:
    url = URL_PERIODOS.format(serie_id)
    for tentativa in range(1, 4):
        try:
            resp = requests.get(url, timeout=30,
                                headers={"Accept": "application/json"})
            resp.raise_for_status()
            dados = resp.json()
            break
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code >= 500:
                print_warn(f"[tabela {serie_id}] Erro {e.response.status_code} do servidor — ignorando.")
                return []
            print_warn(f"[tabela {serie_id}] Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                print_warn(f"[tabela {serie_id}] Falha definitiva — ignorando.")
                return []
            time.sleep(3)
        except requests.RequestException as e:
            print_warn(f"[tabela {serie_id}] Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                print_warn(f"[tabela {serie_id}] Falha definitiva — ignorando.")
                return []
            time.sleep(3)

    nome, fonte = _buscar_meta(serie_id)
    registros = []
    for item in dados:
        literals = item.get("literals", [])
        periodo = literals[1] if len(literals) > 1 else limpar(str(literals))
        registros.append({
            "data_captura":      data_captura,
            "serie_id":          str(serie_id),
            "nome_serie":        nome,
            "fonte":             fonte,
            "periodo_referencia": limpar(periodo),
            "data_modificacao":  limpar(item.get("modificacao", "")),
        })
    return registros


def capturar() -> list[dict]:
    data_captura, _ = agora_brt()
    todos = []
    total = len(SERIES)

    for idx, (serie_id, nome_serie) in enumerate(SERIES.items(), 1):
        print_start(f"[{idx}/{total}] tabela {serie_id} — {nome_serie}", icon="search")
        t0 = time.time()
        registros = _buscar_periodos(serie_id, data_captura)
        elapsed = time.time() - t0

        if not registros:
            print_warn(f"tabela {serie_id}: 0 períodos retornados.")
        else:
            print_done(f"tabela {serie_id}: {len(registros)} períodos", elapsed=elapsed)

        todos.extend(registros)

    if not todos:
        print_fail("Nenhum dado retornado do IBGE SIDRA.")
        sys.exit(1)

    print_done(f"Total: {len(todos)} registros capturados.")
    return todos


class IbgeSidraScraper(BaseScraper):
    name = "ibge_sidra"
    group = "ibge"
    enabled = True
    phase = 1
    accumulate = False
    chaves_dedup = ['data_captura', 'serie_id', 'periodo_referencia']

    # Catálogo de Metadados
    title = 'IBGE SIDRA — Metadados'
    description = 'Metadados das tabelas do IBGE SIDRA: IPCA, IPCA-15 e INPC — períodos disponíveis e datas de modificação.'
    icon = '📊'
    icon_class = 'icon-ibge'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['ipca', 'ipca-15', 'inpc']
    source = 'IBGE · SIDRA'

    def fetch(self) -> pd.DataFrame:
        # Mostra banner apenas quando executado standalone (não via run_all.py)
        is_pipeline = any("run_all" in str(getattr(m, "__file__", "")) for m in sys.modules.values())
        if not is_pipeline:
            banner("IBGE SIDRA — Metadados", "Captura períodos e datas de modificação")

        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    IbgeSidraScraper().run()
