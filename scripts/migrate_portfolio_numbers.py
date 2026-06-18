#!/usr/bin/env python
# coding: utf-8
"""
scripts/migrate_portfolio_numbers.py
-------------------------------------
Limpa valores numéricos (quantidade_teorica, participacao_pct, reducao_capital)
nos CSVs de carteiras teóricas da B3, removendo formatação inconsistente.

Uso:
    python scripts/migrate_portfolio_numbers.py
    python scripts/migrate_portfolio_numbers.py --dry-run
    python scripts/migrate_portfolio_numbers.py --quiet
"""

import csv
import sys
import time
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils.ux import (
    banner, section, print_start, print_done, print_fail, print_info,
    print_summary, add_common_args, apply_common_args, ColorLogger,
)

log = ColorLogger("migrate_portfolio_numbers")


def _limpar_int(valor) -> str:
    if valor is None:
        return ""
    texto = str(valor).strip()
    clean = texto.replace(".", "").replace(" ", "")
    if "," in clean:
        clean = clean.split(",")[0]
    return clean


def _limpar_float(valor) -> str:
    if valor is None:
        return ""
    texto = str(valor).strip()
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    return texto.replace("%", "").strip()


def process_file(file_path: Path, dry_run: bool = False) -> tuple[int, int]:
    """Processa um CSV limpando valores numéricos.
    Retorna (linhas_processadas, linhas_modificadas).
    """
    if not file_path.exists():
        return 0, -1

    rows = []
    headers = []
    modificadas = 0

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            original = dict(row)
            if "quantidade_teorica" in row:
                row["quantidade_teorica"] = _limpar_int(row["quantidade_teorica"])
            if "participacao_pct" in row:
                row["participacao_pct"] = _limpar_float(row["participacao_pct"])
            if "reducao_capital" in row:
                row["reducao_capital"] = _limpar_float(row["reducao_capital"])
            if row != original:
                modificadas += 1
            rows.append(row)

    if not dry_run and headers:
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    return len(rows), modificadas


def main(dry_run: bool = False) -> None:
    t0 = time.time()
    banner("Migrar Números Portfolio",
           "Limpa quantidade/participação em CSVs de carteiras B3")
    section("Processando arquivos", "clean")

    data_dir = Path(__file__).resolve().parents[1] / "data"
    compiled_file = data_dir / "b3_carteiras_teoricas.csv"
    individual_files = sorted(data_dir.glob("b3_carteira_teorica_*.csv"))
    all_files = [compiled_file] + individual_files if compiled_file.exists() else individual_files

    if not all_files:
        log.warning("Nenhum arquivo de carteira teórica encontrado.")
        return

    total_ok = 0
    total_fail = 0
    total_skip = 0
    total_linhas = 0
    total_modificadas = 0
    total_arquivos = len(all_files)

    for idx, file_path in enumerate(all_files, 1):
        nome = file_path.name
        print_start(f"[{idx}/{total_arquivos}] {nome}", icon="file")

        linhas, modificadas = process_file(file_path, dry_run=dry_run)

        if modificadas == -1:
            print_info(f"{nome} — arquivo não encontrado.")
            total_skip += 1
        elif modificadas > 0:
            print_done(f"{nome}: {linhas} linhas, {modificadas} modificada(s)")
            total_ok += 1
        else:
            print_info(f"{nome}: {linhas} linhas, sem alterações")
            total_ok += 1

        total_linhas += max(linhas, 0)
        total_modificadas += max(modificadas, 0)

    elapsed = time.time() - t0
    print_summary(
        "Migração concluída",
        total=total_arquivos,
        success=total_ok,
        failed=total_fail,
        skipped=total_skip,
        elapsed=elapsed,
        details=[
            ("file", "Arquivos processados", str(total_ok)),
            ("clean", "Linhas modificadas", str(total_modificadas)),
        ],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="🧹 Limpa valores numéricos em CSVs de carteiras B3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
exemplos:
  python scripts/migrate_portfolio_numbers.py
  python scripts/migrate_portfolio_numbers.py --dry-run
  python scripts/migrate_portfolio_numbers.py --quiet
        """,
    )
    add_common_args(parser)
    args = parser.parse_args()

    if args.dry_run:
        log.info("Modo dry-run: nenhum arquivo será alterado.")

    apply_common_args(args)
    main(dry_run=args.dry_run)
