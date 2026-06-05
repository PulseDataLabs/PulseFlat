#!/usr/bin/env python
# coding: utf-8
"""
scripts/populate_last_updates.py
---------------------------------
Varre o diretório data/, abre cada arquivo CSV, encontra a data_captura
mais recente, e salva o mapeamento em data/last_updates.json.

Uso:
    python scripts/populate_last_updates.py
    python scripts/populate_last_updates.py --dry-run
    python scripts/populate_last_updates.py --quiet
"""

import csv
import json
import sys
import time
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils.ux import (
    banner, section, print_start, print_done, print_fail, print_warn, print_info,
    print_summary, add_common_args, apply_common_args, ColorLogger,
)

log = ColorLogger("populate_last_updates")


def main(dry_run: bool = False) -> None:
    t0 = time.time()
    banner("Atualizar Últimas Datas", "Varre CSVs → last_updates.json")
    section("Processando arquivos", "file")

    root_dir = Path(__file__).resolve().parents[1]
    data_dir = root_dir / "data"
    output_path = data_dir / "last_updates.json"

    if not data_dir.exists():
        log.error(f"Diretório {data_dir} não encontrado.")
        sys.exit(1)

    last_updates = {}

    if output_path.exists():
        try:
            with output_path.open("r", encoding="utf-8") as f:
                last_updates = json.load(f)
            print_info("Carregado last_updates.json existente.")
        except Exception as e:
            print_warn(f"Erro ao ler last_updates.json: {e}. Criando novo.")

    last_updates = {k: v for k, v in last_updates.items() if (data_dir / k).exists()}

    csv_files = sorted(data_dir.glob("*.csv"))
    total_files = len(csv_files)
    total_ok = 0
    total_fail = 0
    total_warn = 0
    total_atualizados = 0

    for idx, csv_file in enumerate(csv_files, 1):
        nome = csv_file.name
        print_start(f"[{idx}/{total_files}] {nome}", icon="file")

        try:
            with csv_file.open("r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    print_warn(f"{nome}: sem colunas.")
                    total_warn += 1
                    continue

                date_col = None
                for candidate in ["data_captura", "data_referencia", "data", "rpt_dt"]:
                    for col in reader.fieldnames:
                        if col.lower() == candidate:
                            date_col = col
                            break
                    if date_col:
                        break

                if not date_col:
                    print_warn(f"{nome}: nenhuma coluna de data encontrada.")
                    total_warn += 1
                    continue

                datas = []
                for row in reader:
                    val = row.get(date_col)
                    if val and val.strip():
                        datas.append(val.strip())

                if datas:
                    min_date = min(datas)
                    max_date = max(datas)
                    last_updates[nome] = {"min": min_date, "max": max_date}
                    print_done(f"{nome}: {min_date} a {max_date}")
                    total_ok += 1
                    total_atualizados += 1
                else:
                    print_warn(f"{nome}: nenhum registro com data.")
                    total_warn += 1

        except Exception as e:
            print_fail(f"{nome}: {e}")
            total_fail += 1

    if not dry_run:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("w", encoding="utf-8") as f:
                json.dump(last_updates, f, indent=2, ensure_ascii=False)
            print_done("last_updates.json salvo.")

            js_path = data_dir / "last_updates.js"
            with js_path.open("w", encoding="utf-8") as f:
                f.write(
                    f"window.PULSEFLAT_LAST_UPDATES = "
                    f"{json.dumps(last_updates, indent=2, ensure_ascii=False)};\n"
                )
            print_done("last_updates.js salvo.")
        except Exception as e:
            print_fail(f"Erro ao salvar arquivos de metadados: {e}")
            sys.exit(1)

    elapsed = time.time() - t0
    print_summary(
        "Atualização concluída",
        total=total_files,
        success=total_ok,
        failed=total_fail,
        skipped=total_warn,
        elapsed=elapsed,
        details=[
            ("file", "CSVs processados", str(total_ok)),
            ("package", "Arquivos atualizados", str(total_atualizados)),
        ],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="📄 Atualiza last_updates.json com datas dos CSVs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
exemplos:
  python scripts/populate_last_updates.py
  python scripts/populate_last_updates.py --dry-run
  python scripts/populate_last_updates.py --quiet
  python scripts/populate_last_updates.py --verbose
        """,
    )
    add_common_args(parser)
    args = parser.parse_args()

    if args.dry_run:
        log.info("Modo dry-run: nenhum arquivo será salvo.")

    apply_common_args(args)
    main(dry_run=args.dry_run)
