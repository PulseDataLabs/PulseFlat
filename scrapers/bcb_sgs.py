"""
scrapers/bcb_sgs.py
-------------------
Séries temporais do Banco Central via Sistema Gerenciador de Séries (SGS).

Séries capturadas por padrão:
  11    — Taxa SELIC diária (% a.d.)
  4390  — SELIC acumulada no mês (% a.m.)
  432   — CDI diário (% a.d.)
  4391  — CDI acumulado no mês (% a.m.)
  3695  — IPCA variação mensal (% a.m.)
  433   — IPCA acumulado 12 meses (% a.a.)
  189   — IGP-M variação mensal (% a.m.)
  190   — IGP-M acumulado 12 meses (% a.a.)
  1     — Dólar americano venda (R$/US$)

Fonte: https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados
"""

import sys
import time
from datetime import date, timedelta
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, nova_session, salvar_csv

log = get_logger("bcb_sgs")

ARQUIVO = Path("data/bcb_sgs.csv")

CABECALHO = [
    "data_captura",
    
    "codigo_serie",
    "nome_serie",
    "data",
    "valor",
]

# Séries com nome amigável
SERIES = {
    11:   "Taxa SELIC diária (% a.d.)",
    4390: "SELIC acumulada no mês (% a.m.)",
    432:  "CDI diário (% a.d.)",
    4391: "CDI acumulado no mês (% a.m.)",
    3695: "IPCA - variação mensal (% a.m.)",
    433:  "IPCA - acumulado 12 meses (% a.a.)",
    189:  "IGP-M - variação mensal (% a.m.)",
    190:  "IGP-M - acumulado 12 meses (% a.a.)",
    1:    "Dólar americano - venda (R$/US$)",
}

URL_TPL = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}"
    "/dados?formato=json&dataInicial={inicio}&dataFinal={fim}"
)


def _buscar_serie(session, codigo: int, nome: str, inicio: str, fim: str,
                  data_captura: str) -> list[dict]:
    url = URL_TPL.format(codigo=codigo, inicio=inicio, fim=fim)
    for tentativa in range(1, 4):
        try:
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            dados = resp.json()
            break
        except requests.RequestException as e:
            log.warning(f"[série {codigo}] Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error(f"[série {codigo}] Falha definitiva — ignorando.")
                return []
            time.sleep(3)

    registros = []
    for item in dados:
        registros.append({
            "data_captura":  data_captura,
            "codigo_serie":  str(codigo),
            "nome_serie":    nome,
            "data":          limpar(item.get("data")),
            "valor":         limpar(item.get("valor")),
        })
    return registros


def capturar() -> list[dict]:
    hoje = date.today()
    inicio = (hoje - timedelta(days=40)).strftime("%d/%m/%Y")
    fim = hoje.strftime("%d/%m/%Y")
    data_captura, _ = agora_brt()
    session = nova_session()

    todos = []
    for codigo, nome in SERIES.items():
        log.info(f"Buscando série {codigo} — {nome}")
        registros = _buscar_serie(session, codigo, nome, inicio, fim,
                                  data_captura)
        log.info(f"  → {len(registros)} pontos")
        todos.extend(registros)
        time.sleep(0.5)

    if not todos:
        log.error("Nenhum dado capturado do BCB SGS.")
        sys.exit(1)

    log.info(f"Total BCB SGS: {len(todos)} registros.")
    return todos


def main():
    log.info("=== BCB SGS — Séries Temporais ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "codigo_serie", "data"])


if __name__ == "__main__":
    main()
