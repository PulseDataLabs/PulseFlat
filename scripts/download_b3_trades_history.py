import argparse
import re
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

# Adiciona o diretório raiz ao sys.path para importar os módulos locais
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils import agora_brt, get_logger, limpar, salvar_csv

log = get_logger("download_b3_trades_history")

OUTPUT_FILE = ROOT_DIR / "data" / "b3_bdi_trades_acoes.csv.gz"
PAGE_SIZE = 1000
MAX_PAGES = 50

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
}


def _to_snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _buscar_pagina(url: str) -> list[dict]:
    for tentativa in range(1, 4):
        try:
            resp = requests.post(url, json={}, timeout=30, headers=HEADERS)
            resp.raise_for_status()
            table = resp.json().get("table", {})
            values = table.get("values", [])
            columns = [_to_snake(c["name"]) for c in table.get("columns", [])]
            if not values:
                return []
            return [dict(zip(columns, row)) for row in values]
        except Exception as e:
            log.warning(f"Erro {url} (tentativa {tentativa}/3): {e}")
            if tentativa < 3:
                time.sleep(2)
            else:
                return []
    return []


def run():
    parser = argparse.ArgumentParser(
        description="Importador de Histórico de Negócios de Ações da B3"
    )
    parser.add_argument(
        "--start-date", default="2026-01-01", help="Data de início (AAAA-MM-DD)"
    )
    parser.add_argument(
        "--end-date",
        default=date.today().strftime("%Y-%m-%d"),
        help="Data de término (AAAA-MM-DD)",
    )
    args = parser.parse_known_args()[0]

    start_date = date.fromisoformat(args.start_date)
    end_date = date.fromisoformat(args.end_date)

    print("=== B3 BDI — Negócios de Ações — Importador de Histórico ===")
    print(f"Período: {start_date} até {end_date}")

    data_captura, _ = agora_brt()

    curr = start_date
    datas_uteis = []

    while curr <= end_date:
        # Pula finais de semana
        if curr.weekday() < 5:
            datas_uteis.append(curr)
        curr += timedelta(days=1)

    print(f"Total de datas a tentar buscar: {len(datas_uteis)}")

    for i, dt in enumerate(datas_uteis, 1):
        str_data = dt.strftime("%Y-%m-%d")
        print(f"[{i}/{len(datas_uteis)}] Buscando trades para a data: {str_data}")

        todos_do_dia = []
        pagina = 1

        while pagina <= MAX_PAGES:
            url = (
                f"https://arquivos.b3.com.br/bdi/table/ConsolidatedTradesEquities/"
                f"{str_data}/{str_data}/{pagina}/{PAGE_SIZE}"
            )
            rows = _buscar_pagina(url)
            if not rows:
                break

            for item in rows:
                todos_do_dia.append(
                    {
                        "data_captura": data_captura,
                        "data_referencia": limpar(str(item.get("rpt_dt", ""))),
                        "codigo_ativo": limpar(item.get("tckr_symb", "")),
                        "isin": limpar(item.get("isin", "")),
                        "sgmt_nm": limpar(item.get("sgmt_nm", "")),
                        "mkt": limpar(item.get("mkt", "")),
                        "preco_abertura": limpar(str(item.get("open_pric", ""))),
                        "preco_minimo": limpar(str(item.get("min_pric", ""))),
                        "preco_maximo": limpar(str(item.get("max_pric", ""))),
                        "preco_medio": limpar(str(item.get("trad_avrg_pric", ""))),
                        "preco_ultimo": limpar(str(item.get("last_pric", ""))),
                        "osc": limpar(str(item.get("osc", ""))),
                        "trad_qty": limpar(str(item.get("trad_qty", ""))),
                        "fin_instrm_qty": limpar(str(item.get("fin_instrm_qty", ""))),
                        "ntl_fin_vol": limpar(str(item.get("ntl_fin_vol", ""))),
                    }
                )

            pagina += 1
            time.sleep(1.0)

        if todos_do_dia:
            print(f"  -> Salvando {len(todos_do_dia)} registros para {str_data}")
            df_day = pd.DataFrame(todos_do_dia)
            salvar_csv(
                arquivo=OUTPUT_FILE,
                registros=df_day,
                cabecalho=[
                    "data_captura",
                    "data_referencia",
                    "codigo_ativo",
                    "isin",
                    "sgmt_nm",
                    "mkt",
                    "preco_abertura",
                    "preco_minimo",
                    "preco_maximo",
                    "preco_medio",
                    "preco_ultimo",
                    "osc",
                    "trad_qty",
                    "fin_instrm_qty",
                    "ntl_fin_vol",
                ],
                chaves_dedup=["data_captura", "codigo_ativo", "data_referencia"],
                acumular=True,
            )
        else:
            print(f"  -> Nenhum dado retornado ou dia sem negócios para {str_data}")

        # Pequeno delay entre datas para ser amigável ao servidor
        time.sleep(1.5)

    print("\nImportação de histórico finalizada com sucesso!")


if __name__ == "__main__":
    run()
