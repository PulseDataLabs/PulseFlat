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

log = get_logger("ibge_sidra")

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
                log.warning(f"[tabela {serie_id}] Erro {e.response.status_code} do servidor — ignorando.")
                return []
            log.warning(f"[tabela {serie_id}] Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error(f"[tabela {serie_id}] Falha definitiva — ignorando.")
                return []
            time.sleep(3)
        except requests.RequestException as e:
            log.warning(f"[tabela {serie_id}] Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error(f"[tabela {serie_id}] Falha definitiva — ignorando.")
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
    for serie_id in SERIES:
        log.info(f"Buscando metadados SIDRA tabela {serie_id}...")
        registros = _buscar_periodos(serie_id, data_captura)
        log.info(f"  → {len(registros)} períodos")
        todos.extend(registros)
        time.sleep(1)

    if not todos:
        log.error("Nenhum dado retornado do IBGE SIDRA.")
        sys.exit(1)

    log.info(f"Total IBGE SIDRA: {len(todos)} registros.")
    return todos


def main():
    log.info("=== IBGE SIDRA — Metadados ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "serie_id", "periodo_referencia"],
               acumular=False)


if __name__ == "__main__":
    main()
