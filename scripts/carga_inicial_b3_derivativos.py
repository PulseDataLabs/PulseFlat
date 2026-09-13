#!/usr/bin/env python
# coding: utf-8
"""
scripts/carga_inicial_b3_derivativos.py
----------------------------------------
Carga inicial retroativa do dataset B3 BDI Derivativos — Resumo das Operações.
Varre a janela máxima disponível na API da B3 (D-21 até o pregão mais recente),
captura todos os pregões e grava a base consolidada em data/b3_bdi_derivativos_resumo.csv.

Uso:
    python scripts/carga_inicial_b3_derivativos.py
    python scripts/carga_inicial_b3_derivativos.py --dias 25
"""

import argparse
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.b3_bdi_derivativos_resumo import (
    CABECALHO,
    capturar_dia,
)
from scripts.utils.ux import (
    ColorLogger,
    banner,
    print_done,
    print_info,
    print_start,
    print_summary,
    print_warn,
    section,
)
from utils.parsers import _CAL

log = ColorLogger("carga_b3_derivativos")
ARQUIVO_DESTINO = Path(__file__).resolve().parents[1] / "data" / "b3_bdi_derivativos_resumo.csv"
CHAVES_DEDUP = [
    "data_referencia",
    "ticker_simb",
    "categoria",
    "mercado",
    "derivativo",
    "tipo_contrato",
]


def executar_carga_inicial(max_dias_uteis: int = 25) -> None:
    t0 = time.time()
    banner(
        "Carga Inicial — B3 Derivativos BDI",
        f"Captura histórica retroativa da janela máxima disponível (~{max_dias_uteis} dias úteis)",
    )

    section("Calculando calendário de pregões", "clock")
    hoje = date.today()
    # Coleta os últimos dias úteis
    dias_uteis: list[date] = []
    d = hoje
    while len(dias_uteis) < max_dias_uteis:
        d = _CAL.offset(d, -1)
        dias_uteis.append(d)

    dias_uteis.reverse()  # Ordena do mais antigo para o mais recente
    print_info(f"Período selecionado: {dias_uteis[0]} até {dias_uteis[-1]} ({len(dias_uteis)} dias úteis)")

    section("Coletando dados via API B3 BDI", "search")
    todos_registros = []
    dias_com_dados = 0
    dias_sem_dados = 0

    for idx, d_alvo in enumerate(dias_uteis, 1):
        str_d = d_alvo.strftime("%Y-%m-%d")
        print_start(f"[{idx}/{len(dias_uteis)}] Pregão {str_d}...")
        try:
            regs = capturar_dia(d_alvo)
            if regs:
                todos_registros.extend(regs)
                dias_com_dados += 1
                print_done(f"Pregão {str_d}: {len(regs)} contratos capturados.")
            else:
                dias_sem_dados += 1
                print_warn(f"Pregão {str_d}: 0 registros (fora da janela D-21 ou sem negociação).")
            time.sleep(0.4)
        except Exception as e:
            dias_sem_dados += 1
            print_warn(f"Pregão {str_d}: falha na captura ({e}).")

    if not todos_registros:
        print_warn("Nenhum registro capturado. Verifique a conectividade com a B3.")
        return

    section("Consolidando e Deduplicando", "chart")
    df_novo = pd.DataFrame(todos_registros)

    # Se já existir arquivo prévio, mescla
    if ARQUIVO_DESTINO.exists():
        try:
            df_antigo = pd.read_csv(ARQUIVO_DESTINO, dtype=str)
            print_info(f"Arquivo existente com {len(df_antigo)} linhas encontrado.")
            df_combinado = pd.concat([df_antigo, df_novo], ignore_index=True)
        except Exception as e:
            print_warn(f"Erro ao ler arquivo anterior ({e}), sobrescrevendo.")
            df_combinado = df_novo
    else:
        df_combinado = df_novo

    # Deduplicação
    cols_dedup = [c for c in CHAVES_DEDUP if c in df_combinado.columns]
    df_final = df_combinado.drop_duplicates(subset=cols_dedup, keep="last")

    # Ordenação por data e ticker
    if "data_referencia" in df_final.columns:
        df_final = df_final.sort_values(by=["data_referencia", "ticker_simb"])

    # Reordena colunas padrão
    colunas = [c for c in CABECALHO if c in df_final.columns]
    df_final = df_final[colunas]

    ARQUIVO_DESTINO.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(ARQUIVO_DESTINO, index=False, encoding="utf-8")
    print_done(f"Dataset salvo em {ARQUIVO_DESTINO} com {len(df_final)} registros.")

    elapsed = time.time() - t0
    print_summary(
        title="Carga Inicial Concluída",
        total=len(dias_uteis),
        success=dias_com_dados,
        failed=dias_sem_dados,
        elapsed=elapsed,
        details=[
            ("chart", "Registros únicos", str(len(df_final))),
            ("clock", "Dias com pregão", str(dias_com_dados)),
            ("file", "Arquivo gerado", ARQUIVO_DESTINO.name),
        ],
    )


def main():
    parser = argparse.ArgumentParser(description="Carga inicial B3 BDI Derivativos")
    parser.add_argument(
        "--dias",
        type=int,
        default=25,
        help="Quantidade de dias úteis retroativos para varredura (padrão: 25)",
    )
    args = parser.parse_args()
    executar_carga_inicial(max_dias_uteis=args.dias)


if __name__ == "__main__":
    main()
