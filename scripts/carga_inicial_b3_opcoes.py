#!/usr/bin/env python
# coding: utf-8
"""
scripts/carga_inicial_b3_opcoes.py
----------------------------------
Carga inicial retroativa do dataset B3 Opções — Resumo de Posições em Aberto e Put/Call Ratio.
Varre os últimos pregões úteis na B3, computa as métricas de Open Interest
e Put/Call Ratio por ativo e consolida a base histórica em data/b3_opcoes_posicoes_resumo.csv.
Adicionalmente, salva o snapshot granular completo da data mais recente em data/b3_opcoes_posicoes_aberto.csv.gz.

Uso:
    python scripts/carga_inicial_b3_opcoes.py
    python scripts/carga_inicial_b3_opcoes.py --dias 15
"""

import argparse
import sys
import time
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.b3_opcoes_posicoes_aberto import (
    ARQUIVO_GRANULAR,
    ARQUIVO_RESUMO,
    CABECALHO_GRANULAR,
    CABECALHO_RESUMO,
    capturar_dia,
    gerar_resumo_por_ativo,
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

log = ColorLogger("carga_b3_opcoes")
CHAVES_DEDUP_RESUMO = ["data_referencia", "codigo_ativo_objeto"]


def executar_carga_inicial(max_dias_uteis: int = 15) -> None:
    t0 = time.time()
    banner(
        "Carga Inicial — B3 Opções em Aberto",
        f"Captura histórica de posições em aberto e Put/Call ratio (~{max_dias_uteis} pregões)",
    )

    section("Calculando calendário de pregões", "clock")
    hoje = date.today()
    dias_uteis: list[date] = []
    d = hoje
    while len(dias_uteis) < max_dias_uteis:
        d = _CAL.offset(d, -1)
        dias_uteis.append(d)

    dias_uteis.reverse()  # Mais antigo para mais recente
    print_info(f"Período selecionado: {dias_uteis[0]} até {dias_uteis[-1]} ({len(dias_uteis)} dias úteis)")

    section("Coletando posições em aberto via B3", "search")
    resumos_coletados: list[pd.DataFrame] = []
    mais_recente_granular: tuple[list[dict], str] | None = None
    dias_com_dados = 0
    dias_sem_dados = 0

    for idx, d_alvo in enumerate(dias_uteis, 1):
        str_d = d_alvo.strftime("%Y-%m-%d")
        print_start(f"[{idx}/{len(dias_uteis)}] Pregão {str_d}...")
        try:
            regs, str_ref = capturar_dia(d_alvo)
            if regs:
                df_dia = pd.DataFrame(regs)
                df_resumo_dia = gerar_resumo_por_ativo(df_dia, str_ref)
                if not df_resumo_dia.empty:
                    resumos_coletados.append(df_resumo_dia)
                    dias_com_dados += 1
                    mais_recente_granular = (regs, str_ref)
                    print_done(
                        f"Pregão {str_ref}: {len(regs):,} opções capturadas -> {len(df_resumo_dia)} ativos consolidados."
                    )
                else:
                    dias_sem_dados += 1
                    print_warn(f"Pregão {str_ref}: sem dados agregados gerados.")
            else:
                dias_sem_dados += 1
                print_warn(f"Pregão {str_d}: sem dados retornados pela B3.")
            time.sleep(0.4)
        except Exception as e:
            dias_sem_dados += 1
            print_warn(f"Pregão {str_d}: falha na captura ({e}).")

    if not resumos_coletados:
        print_warn("Nenhum registro de opções capturado.")
        return

    section("Consolidando Resumo Histórico de Opções", "chart")
    df_novos_resumos = pd.concat(resumos_coletados, ignore_index=True)

    if ARQUIVO_RESUMO.exists():
        try:
            df_antigo = pd.read_csv(ARQUIVO_RESUMO, dtype=str)
            print_info(f"Arquivo existente com {len(df_antigo)} linhas encontrado.")
            # Força tipos consistentes para deduplicação
            df_combinado = pd.concat([df_antigo, df_novos_resumos], ignore_index=True)
        except Exception as e:
            print_warn(f"Erro ao ler resumo existente ({e}), usando dados novos.")
            df_combinado = df_novos_resumos
    else:
        df_combinado = df_novos_resumos

    # Deduplicação
    cols_dedup = [c for c in CHAVES_DEDUP_RESUMO if c in df_combinado.columns]
    df_resumo_final = df_combinado.drop_duplicates(subset=cols_dedup, keep="last")

    if "data_referencia" in df_resumo_final.columns:
        df_resumo_final = df_resumo_final.sort_values(by=["data_referencia", "posicao_aberta_total"], ascending=[True, False])

    cols_ordem = [c for c in CABECALHO_RESUMO if c in df_resumo_final.columns]
    df_resumo_final = df_resumo_final[cols_ordem]

    ARQUIVO_RESUMO.parent.mkdir(parents=True, exist_ok=True)
    df_resumo_final.to_csv(ARQUIVO_RESUMO, index=False, encoding="utf-8")
    print_done(f"Resumo consolidado salvo em {ARQUIVO_RESUMO} com {len(df_resumo_final)} linhas.")

    # Salva o snapshot mais recente granular
    if mais_recente_granular:
        section("Salvando Snapshot Granular Mais Recente", "file")
        regs_rec, ref_rec = mais_recente_granular
        df_gran = pd.DataFrame(regs_rec)
        df_gran = df_gran.sort_values(by=["codigo_ativo_objeto", "data_vencimento", "preco_exercicio"])
        cols_gran = [c for c in CABECALHO_GRANULAR if c in df_gran.columns]
        df_gran[cols_gran].to_csv(ARQUIVO_GRANULAR, index=False, compression="gzip", encoding="utf-8")
        print_done(f"Snapshot granular salvo em {ARQUIVO_GRANULAR} ({ref_rec}: {len(df_gran):,} linhas).")

    elapsed = time.time() - t0
    print_summary(
        title="Carga de Opções B3 Concluída",
        total=len(dias_uteis),
        success=dias_com_dados,
        failed=dias_sem_dados,
        elapsed=elapsed,
        details=[
            ("chart", "Registros de resumo", str(len(df_resumo_final))),
            ("clock", "Pregões processados", str(dias_com_dados)),
            ("file", "Resumo gerado", ARQUIVO_RESUMO.name),
        ],
    )


def main():
    parser = argparse.ArgumentParser(description="Carga inicial B3 Opções em Aberto")
    parser.add_argument(
        "--dias",
        type=int,
        default=15,
        help="Quantidade de dias úteis retroativos para varredura (padrão: 15)",
    )
    args = parser.parse_args()
    executar_carga_inicial(max_dias_uteis=args.dias)


if __name__ == "__main__":
    main()
