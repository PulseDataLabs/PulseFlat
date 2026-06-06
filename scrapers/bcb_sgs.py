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
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, nova_session, salvar_csv
import pandas as pd
from scrapers.utils.base import BaseScraper

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


def capturar() -> list[dict]:
    from scripts.utils.ux import print_done, print_warn

    hoje = date.today()
    inicio = '01/01/2020'
    fim = hoje.strftime("%d/%m/%Y")
    data_captura, _ = agora_brt()

    session = nova_session()
    todos = []
    n = len(SERIES)
    for i, (codigo, nome) in enumerate(SERIES.items(), 1):
        t0 = time.time()
        url = URL_TPL.format(codigo=codigo, inicio=inicio, fim=fim)

        registros = []
        for tentativa in range(1, 4):
            try:
                resp = session.get(url, timeout=30)
                resp.raise_for_status()
                dados = resp.json()
                for item in dados:
                    registros.append({
                        "data_captura": data_captura,
                        "codigo_serie": str(codigo),
                        "nome_serie": nome,
                        "data": limpar(item.get("data")),
                        "valor": limpar(item.get("valor")),
                    })
                break
            except requests.RequestException as e:
                if tentativa == 3:
                    print_warn(f"({i}/{n}) série {codigo}: falha — ignorando")
                    break
                time.sleep(3)

        if registros:
            print_done(f"({i}/{n}) série {codigo}", elapsed=time.time() - t0)
            todos.extend(registros)
        time.sleep(0.5)

    if not todos:
        raise RuntimeError("Nenhum dado capturado do BCB SGS.")

    return todos

class BcbSgsScraper(BaseScraper):
    name = "bcb_sgs"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = False
    chaves_dedup = ['data_captura', 'codigo_serie', 'data']
    
    # Catálogo de Metadados
    title = 'BCB SGS — Séries Temporais'
    description = 'Séries históricas do Banco Central via SGS: SELIC, CDI, IPCA, IGP-M e Dólar. Snapshot com série histórica diária completa desde 01/01/2020 (não acumulativo).'
    icon = '📈'
    icon_class = 'icon-bcb'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['selic', 'cdi', 'ipca', 'igp-m', 'dólar']
    source = 'BCB · SGS'

    def fetch(self) -> pd.DataFrame:
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    BcbSgsScraper().run()
