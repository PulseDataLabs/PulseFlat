#!/usr/bin/env python
# coding: utf-8
"""
scripts/carga_inicial_b3_opcoes.py
----------------------------------
Carga histórica completa e incremental do dataset B3 Opções — Resumo de Posições em Aberto e Put/Call Ratio.
Varre pregões úteis na B3 (com suporte a multithreading), computa as métricas de Open Interest
e Put/Call Ratio por ativo e consolida a base histórica em data/b3_opcoes_posicoes_resumo.csv.

Pula automaticamente pregões já capturados no arquivo existente.

Uso:
    python scripts/carga_inicial_b3_opcoes.py --dias 60
    python scripts/carga_inicial_b3_opcoes.py --data-inicio 2024-01-01
    python scripts/carga_inicial_b3_opcoes.py --desde-2020
"""

import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta
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


def obter_datas_existentes() -> set[str]:
    """Retorna o conjunto de datas já presentes no arquivo de resumo."""
    if not ARQUIVO_RESUMO.exists():
        return set()
    try:
        df = pd.read_csv(ARQUIVO_RESUMO, usecols=["data_referencia"], dtype=str)
        return set(df["data_referencia"].dropna().unique())
    except Exception as e:
        log.warning(f"Erro ao ler datas existentes ({e})")
        return set()


def processar_um_dia(d_alvo: date) -> tuple[str, pd.DataFrame | None, list[dict] | None]:
    """Captura e processa um único dia útil."""
    str_d = d_alvo.strftime("%Y-%m-%d")
    try:
        regs, str_ref = capturar_dia(d_alvo)
        if regs:
            df_dia = pd.DataFrame(regs)
            df_resumo = gerar_resumo_por_ativo(df_dia, str_ref)
            return str_ref, df_resumo, regs
        return str_d, None, None
    except Exception:
        return str_d, None, None


def salvar_resumos_acumulados(novos_resumos: list[pd.DataFrame]) -> int:
    """Mescla novos resumos no arquivo final e deduplica."""
    if not novos_resumos:
        return 0

    df_novos = pd.concat(novos_resumos, ignore_index=True)

    if ARQUIVO_RESUMO.exists():
        try:
            df_antigo = pd.read_csv(ARQUIVO_RESUMO, dtype=str)
            df_combinado = pd.concat([df_antigo, df_novos], ignore_index=True)
        except Exception:
            df_combinado = df_novos
    else:
        df_combinado = df_novos

    cols_dedup = [c for c in CHAVES_DEDUP_RESUMO if c in df_combinado.columns]
    df_final = df_combinado.drop_duplicates(subset=cols_dedup, keep="last")

    if "data_referencia" in df_final.columns:
        df_final = df_final.sort_values(
            by=["data_referencia", "posicao_aberta_total"],
            ascending=[True, False],
        )

    cols_ordem = [c for c in CABECALHO_RESUMO if c in df_final.columns]
    df_final = df_final[cols_ordem]

    ARQUIVO_RESUMO.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(ARQUIVO_RESUMO, index=False, encoding="utf-8")
    return len(df_final)


def executar_carga(
    data_inicio: date,
    data_fim: date,
    max_workers: int = 6,
    forcar: bool = False,
) -> None:
    t0 = time.time()
    banner(
        "Carga Histórica — B3 Opções em Aberto",
        f"Período: {data_inicio} até {data_fim} (concorrência: {max_workers} threads)",
    )

    section("Calculando calendário de pregões", "clock")
    datas_existentes = set() if forcar else obter_datas_existentes()
    if datas_existentes:
        print_info(f"Encontradas {len(datas_existentes)} datas já carregadas no resumo.")

    def is_dia_util(dt: date) -> bool:
        if dt.weekday() >= 5:
            return False
        try:
            return bool(_CAL.isbizday(dt))
        except Exception:
            return True

    dias_uteis: list[date] = []
    d = data_inicio
    while d <= data_fim:
        # Se for dia útil
        if is_dia_util(d):
            str_d = d.strftime("%Y-%m-%d")
            if str_d not in datas_existentes:
                dias_uteis.append(d)
        d += timedelta(days=1)

    # Ordena do mais recente para o mais antigo ou vice-versa
    dias_uteis = sorted(dias_uteis)
    total_dias = len(dias_uteis)
    print_info(f"Total de novos pregões a capturar: {total_dias}")

    if not dias_uteis:
        print_done("Todas as datas do período selecionado já estão carregadas!")
        return

    section("Coletando opções em paralelo via B3", "search")
    resumos_buffer: list[pd.DataFrame] = []
    ultimo_snapshot_granular: tuple[list[dict], str] | None = None
    dias_com_dados = 0
    dias_sem_dados = 0
    concluidos = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futuros = {executor.submit(processar_um_dia, d): d for d in dias_uteis}

        for fut in as_completed(futuros):
            concluidos += 1
            str_ref, df_resumo, regs = fut.result()

            if df_resumo is not None and not df_resumo.empty:
                dias_com_dados += 1
                resumos_buffer.append(df_resumo)
                if not ultimo_snapshot_granular or str_ref > ultimo_snapshot_granular[1]:
                    ultimo_snapshot_granular = (regs, str_ref)
                print_done(
                    f"[{concluidos}/{total_dias}] {str_ref}: {len(df_resumo)} ativos com opções em aberto."
                )
            else:
                dias_sem_dados += 1
                print_warn(f"[{concluidos}/{total_dias}] {str_ref}: sem dados retornados.")

            # Gravação em lotes a cada 25 dias para garantir persistência
            if len(resumos_buffer) >= 25:
                salvar_resumos_acumulados(resumos_buffer)
                resumos_buffer = []

    # Salva o restante do buffer
    if resumos_buffer:
        total_linhas = salvar_resumos_acumulados(resumos_buffer)
    else:
        total_linhas = len(pd.read_csv(ARQUIVO_RESUMO)) if ARQUIVO_RESUMO.exists() else 0

    # Atualiza snapshot granular se for mais recente
    if ultimo_snapshot_granular and not ARQUIVO_GRANULAR.exists():
        section("Atualizando Snapshot Granular", "file")
        regs, str_ref = ultimo_snapshot_granular
        df_gran = pd.DataFrame(regs).sort_values(
            by=["codigo_ativo_objeto", "data_vencimento", "preco_exercicio"]
        )
        cols_gran = [c for c in CABECALHO_GRANULAR if c in df_gran.columns]
        df_gran[cols_gran].to_csv(
            ARQUIVO_GRANULAR, index=False, compression="gzip", encoding="utf-8"
        )
        print_done(f"Snapshot granular salvo em {ARQUIVO_GRANULAR} ({str_ref}: {len(df_gran):,} linhas).")

    elapsed = time.time() - t0
    print_summary(
        title="Carga de Opções B3 Concluída",
        total=total_dias,
        success=dias_com_dados,
        failed=dias_sem_dados,
        elapsed=elapsed,
        details=[
            ("chart", "Total linhas no resumo", str(total_linhas)),
            ("clock", "Pregões capturados com sucesso", str(dias_com_dados)),
            ("file", "Arquivo consolidado", ARQUIVO_RESUMO.name),
        ],
    )


def main():
    parser = argparse.ArgumentParser(description="Carga histórica B3 Opções em Aberto")
    parser.add_argument(
        "--dias",
        type=int,
        default=None,
        help="Quantidade de dias úteis retroativos",
    )
    parser.add_argument(
        "--data-inicio",
        type=str,
        default=None,
        help="Data de início (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--data-fim",
        type=str,
        default=None,
        help="Data de fim (YYYY-MM-DD, padrão: hoje)",
    )
    parser.add_argument(
        "--desde-2020",
        action="store_true",
        help="Carrega todo o histórico disponível desde julho/2020",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=6,
        help="Número de threads simultâneas (padrão: 6)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Sobrescreve/re-processa datas existentes",
    )

    args = parser.parse_args()

    hoje = date.today()
    data_fim = (
        datetime.strptime(args.data_fim, "%Y-%m-%d").date() if args.data_fim else hoje
    )

    if args.desde_2020:
        data_inicio = date(2020, 7, 15)
    elif args.data_inicio:
        data_inicio = datetime.strptime(args.data_inicio, "%Y-%m-%d").date()
    elif args.dias:
        d = data_fim
        for _ in range(args.dias):
            d = _CAL.offset(d, -1)
        data_inicio = d
    else:
        # Padrão: 2024 até hoje (~1.5 ano de histórico)
        data_inicio = date(2024, 1, 2)

    executar_carga(
        data_inicio=data_inicio,
        data_fim=data_fim,
        max_workers=args.workers,
        forcar=args.force,
    )


if __name__ == "__main__":
    main()
