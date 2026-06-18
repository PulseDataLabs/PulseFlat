#!/usr/bin/env python
# coding: utf-8
"""
scripts/limpar_duplicatas.py
-----------------------------
Remove duplicatas dos CSVs históricos, mantendo apenas a captura mais
recente de cada combinação de chaves por dia.

Execute uma única vez para limpar o histórico acumulado:

    python scripts/limpar_duplicatas.py

A partir daí, salvar_csv() garante que novas execuções nunca dupliquem.
"""

import csv
import time
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils.ux import (
    banner, section, print_start, print_done, print_info, print_skip,
    print_summary, add_common_args, apply_common_args, ColorLogger,
)

log = ColorLogger("limpar_duplicatas")

CONFIGS = [
    {
        "arquivo":    Path("data/anbima_indicadores.csv"),
        "chaves":     ["data_captura", "indicador"],
        "ordenar_por": ["data_captura", "hora_captura"],
    },
    {
        "arquivo":    Path("data/anbima_projecoes.csv"),
        "chaves":     ["data_captura", "indice", "mes_referencia", "tipo_projecao"],
        "ordenar_por": ["data_captura", "hora_captura"],
    },
    {
        "arquivo":    Path("data/b3_fiis_listados.csv"),
        "chaves":     ["data_captura", "codigo_fundo"],
        "ordenar_por": ["data_captura", "hora_captura"],
    },
    {
        "arquivo":    Path("data/b3_etfs_listados.csv"),
        "chaves":     ["data_captura", "categoria_etf", "codigo_fundo"],
        "ordenar_por": ["data_captura", "hora_captura"],
    },
    {
        "arquivo":    Path("data/b3_carteiras_teoricas.csv"),
        "chaves":     ["data_captura", "indice", "codigo_ativo"],
        "ordenar_por": ["data_captura", "hora_captura"],
    },
]


def limpar(arquivo: Path, chaves: list[str], ordenar_por: list[str], dry_run: bool = False) -> tuple[int, int, int]:
    """Remove duplicatas de um CSV. Retorna (antes, depois, removidas)."""
    if not arquivo.exists():
        return 0, 0, -1  # -1 indica skip

    with arquivo.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cabecalho = list(reader.fieldnames or [])
        linhas = list(reader)

    total_antes = len(linhas)

    # Ordena para que a entrada MAIS RECENTE fique por último
    linhas.sort(key=lambda r: tuple(r.get(c, "") for c in ordenar_por))

    # Mantém apenas a última ocorrência de cada chave composta
    vistos: dict[tuple, dict] = {}
    for linha in linhas:
        chave = tuple(linha.get(c, "") for c in chaves)
        vistos[chave] = linha

    resultado = list(vistos.values())
    total_depois = len(resultado)
    removidas = total_antes - total_depois

    if not dry_run:
        with arquivo.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=cabecalho, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(resultado)

    return total_antes, total_depois, removidas


def main(dry_run: bool = False) -> None:
    t0 = time.time()
    banner("Limpar Duplicatas", "Remove duplicatas históricas por chave composta")
    section("Processando arquivos", "clean")

    root_dir = Path(__file__).resolve().parents[1]
    total_ok = 0
    total_fail = 0
    total_skip = 0
    total_removidas = 0
    total_antes = 0
    total_depois = 0
    total_configs = len(CONFIGS)

    for idx, cfg in enumerate(CONFIGS, 1):
        arquivo = root_dir / cfg["arquivo"]
        nome = arquivo.name

        print_start(f"[{idx}/{total_configs}] {nome}", icon="file")
        antes, depois, removidas = limpar(arquivo, cfg["chaves"], cfg["ordenar_por"], dry_run=dry_run)

        if removidas == -1:
            print_skip(f"{nome} — arquivo não encontrado")
            total_skip += 1
        else:
            total_antes += antes
            total_depois += depois
            total_removidas += removidas
            if removidas:
                print_done(f"{nome}: {antes} → {depois} ({removidas} duplicata(s))")
            else:
                print_info(f"{nome}: {antes} linhas, sem duplicatas")
            total_ok += 1

    elapsed = time.time() - t0
    print_summary(
        "Limpeza concluída",
        total=total_configs,
        success=total_ok,
        failed=total_fail,
        skipped=total_skip,
        elapsed=elapsed,
        details=[
            ("file", "Arquivos", str(total_ok)),
            ("clean", "Removidas", str(total_removidas)),
            ("skip", "Pulados", str(total_skip)),
        ],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="🧹 Remove duplicatas dos CSVs históricos do PulseFlat",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
exemplos:
  python scripts/limpar_duplicatas.py
  python scripts/limpar_duplicatas.py --dry-run
  python scripts/limpar_duplicatas.py --quiet
        """,
    )
    add_common_args(parser)
    args = parser.parse_args()

    if args.dry_run:
        log.info("Modo dry-run: nenhum arquivo será alterado.")

    apply_common_args(args)
    main(dry_run=args.dry_run)
