#!/usr/bin/env python
"""
scripts/export_to_parquet.py
-----------------------------
Exporta datasets CSV (.csv e .csv.gz) da pasta data/ para formato Apache Parquet (.parquet).

O formato Parquet oferece compressão colunar superior, tipagem estrita e leitura
até 10x mais rápida em ferramentas analíticas como Pandas, Polars, DuckDB e Spark.

Uso:
    python scripts/export_to_parquet.py                    # converte todos os datasets
    python scripts/export_to_parquet.py --dataset bcb_ptax # converte dataset específico
    python scripts/export_to_parquet.py --compression zstd # usa compressão zstd
    python scripts/export_to_parquet.py --dry-run
"""

import argparse
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils.ux import (
    ColorLogger,
    add_common_args,
    apply_common_args,
    banner,
    print_done,
    print_fail,
    print_info,
    print_skip,
    print_start,
    print_summary,
    section,
)

log = ColorLogger("export_to_parquet")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exporta datasets de CSV (.csv / .csv.gz) para Parquet.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default=None,
        help="Nome específico do dataset (ex: bcb_ptax, anbima_550).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/parquet",
        help="Diretório de destino para os arquivos .parquet (padrão: data/parquet).",
    )
    parser.add_argument(
        "--compression",
        type=str,
        default="snappy",
        choices=["snappy", "gzip", "brotli", "zstd", "none"],
        help="Algoritmo de compressão Parquet (padrão: snappy).",
    )
    add_common_args(parser)
    return parser.parse_args()


def exportar_dataset(
    caminho_csv: Path,
    output_dir: Path,
    compression: str,
    dry_run: bool = False,
) -> tuple[bool, int, int, float]:
    """Lê o CSV, converte para Parquet e retorna (sucesso, linhas, tamanho_bytes, tempo_segundos)."""
    t0 = time.time()
    nome_base = caminho_csv.name
    if nome_base.endswith(".csv.gz"):
        nome_stem = nome_base[:-7]
    elif nome_base.endswith(".csv"):
        nome_stem = nome_base[:-4]
    else:
        nome_stem = caminho_csv.stem

    arquivo_parquet = output_dir / f"{nome_stem}.parquet"

    if dry_run:
        return True, 0, 0, 0.0

    try:
        df = pd.read_csv(caminho_csv, dtype=str, keep_default_na=False)
    except Exception:
        return False, 0, 0, 0.0
    if df.empty:
        return False, 0, 0, 0.0

    # Tenta inferir datas para otimizar armazenamento sem perder fidelidade
    for col in df.columns:
        if "data" in col.lower() and not col.lower().startswith("hora"):
            try:
                parsed_dates = pd.to_datetime(df[col], errors="coerce", format="mixed")
                if parsed_dates.notna().sum() > len(df) * 0.8:
                    df[col] = parsed_dates
            except Exception:
                pass

    comp = None if compression == "none" else compression
    df.to_parquet(arquivo_parquet, index=False, compression=comp, engine="pyarrow")

    elapsed = time.time() - t0
    tamanho = arquivo_parquet.stat().st_size
    return True, len(df), tamanho, elapsed


def main() -> int:
    t_global = time.time()
    args = parse_args()
    apply_common_args(args)

    banner(
        "PulseFlat – Exportador de Datasets Parquet",
        "Conversão colunar de alta performance para DuckDB / Analytics",
    )

    data_dir = Path(__file__).resolve().parents[1] / "data"
    output_dir = Path(__file__).resolve().parents[1] / args.output_dir

    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    arquivos_csv = sorted(
        list(data_dir.glob("*.csv")) + list(data_dir.glob("*.csv.gz"))
    )

    if args.dataset:
        termo = args.dataset.replace(".csv.gz", "").replace(".csv", "")
        arquivos_csv = [f for f in arquivos_csv if termo in f.name]

    if not arquivos_csv:
        print_info("Nenhum arquivo CSV encontrado para exportação.")
        return 0

    section(f"Convertendo {len(arquivos_csv)} dataset(s) para Parquet ({args.compression})")

    sucessos = 0
    falhas = 0
    total_linhas = 0
    total_bytes = 0

    for idx, arq in enumerate(arquivos_csv, 1):
        nome_display = f"[{idx}/{len(arquivos_csv)}] {arq.name}"

        if args.dry_run:
            print_skip(f"{nome_display} -> [dry-run] simulado")
            sucessos += 1
            continue

        print_start(f"Exportando {arq.name}...")
        try:
            ok, linhas, tamanho, elapsed = exportar_dataset(
                arq, output_dir, args.compression, args.dry_run
            )
            if ok:
                sucessos += 1
                total_linhas += linhas
                total_bytes += tamanho
                msg = f"{arq.name}: {linhas:,} lin | {tamanho / 1024:.1f} KB".replace(",", ".")
                print_done(msg, elapsed=elapsed)
            else:
                falhas += 1
                print_fail(f"{arq.name}: CSV vazio ou sem dados")
        except Exception as e:
            falhas += 1
            print_fail(f"{arq.name}: {e}")

    elapsed_total = time.time() - t_global
    print_summary(
        title="Resumo da Exportação Parquet",
        total=len(arquivos_csv),
        success=sucessos,
        failed=falhas,
        skipped=0,
        elapsed=elapsed_total,
        details=[
            ("info", "Total de registros convertidos", f"{total_linhas:,}".replace(",", ".")),
            ("info", "Tamanho Parquet total", f"{total_bytes / (1024 * 1024):.2f} MB"),
            ("info", "Diretório de saída", str(output_dir)),
        ],
    )

    return 0 if falhas == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
