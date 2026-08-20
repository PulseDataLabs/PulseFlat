#!/usr/bin/env python
"""
scripts/backfill_buracos.py
--------------------------
Identifica "buracos" (dias úteis faltantes) nas séries temporais
e executa os respectivos scrapers direcionados de forma retroativa
para preenchê-los.
"""

import argparse
import importlib
import sys
import time
from datetime import date
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils.ux import (
    ColorLogger,
    add_common_args,
    apply_common_args,
    banner,
    print_done,
    print_fail,
    print_info,
    print_start,
    print_summary,
    print_warn,
    section,
)
from scripts.verificar_buracos import CONFIG, check_gaps, load_entity_dates

log = ColorLogger("backfill_buracos")


def main(
    csv_filter: list[str] | None = None,
    threshold: int = 3,
    dry_run: bool = False,
    quiet: bool = False,
    verbose: bool = False,
) -> None:
    t0 = time.time()
    if not quiet:
        banner(
            "Backfill Automático de Buracos",
            "Preenche lacunas de datas nas séries temporais",
        )

    root_dir = Path(__file__).resolve().parents[1]
    data_dir = root_dir / "data"

    if csv_filter:
        targets = {k: v for k, v in CONFIG.items() if k in csv_filter}
    else:
        targets = dict(CONFIG)

    if not targets:
        if not quiet:
            print_warn("Nenhum CSV selecionado para backfill.")
        return

    if not quiet:
        section("Detectando buracos existentes", "search")

    gaps_by_csv = {}
    for csv_name, config in sorted(targets.items()):
        csv_path = data_dir / csv_name
        if not csv_path.exists():
            if (data_dir / (csv_name + ".gz")).exists():
                csv_path = data_dir / (csv_name + ".gz")
            else:
                continue

        date_col = config["date_col"]
        group_by_cols = config.get("group_by", [])
        entity_dates = load_entity_dates(csv_path, date_col, group_by_cols)
        if not entity_dates:
            continue

        gaps = check_gaps(entity_dates, threshold=threshold)
        if gaps:
            # Reúne todas as datas faltantes únicas deste CSV
            all_missing = sorted(list({d for dates in gaps.values() for d in dates}))
            gaps_by_csv[csv_name] = all_missing

    if not gaps_by_csv:
        if not quiet:
            print_done("Nenhum buraco detectado nas bases analisadas! Tudo 100% OK.")
        return

    if not quiet:
        print_info(f"Buracos detectados em {len(gaps_by_csv)} arquivo(s).")
        for csv_name, dates in sorted(gaps_by_csv.items()):
            print_info(
                f"  {csv_name}: {len(dates)} data(s) faltante(s) ({dates[0]} até {dates[-1]})"
            )

    if dry_run:
        if not quiet:
            print_info(
                "\nModo dry-run: nenhuma execução de scraper será iniciada.",
                icon="gear",
            )
        return

    if not quiet:
        section("Iniciando execução dos scrapers em modo retroativo", "gear")

    total_scrapers_run = 0

    for csv_name, missing_dates in sorted(gaps_by_csv.items()):
        scraper_name = csv_name.replace(".csv", "")
        if not quiet:
            print_start(
                f"Processando backfill para {csv_name} usando scraper '{scraper_name}'",
                icon="refresh",
            )

        try:
            # Importa o scraper dinamicamente
            mod = importlib.import_module(f"scrapers.{scraper_name}")
            class_name = (
                "".join(w.capitalize() for w in scraper_name.split("_")) + "Scraper"
            )
            if not hasattr(mod, class_name):
                if not quiet:
                    print_fail(
                        f"Scraper classe '{class_name}' não encontrada no módulo scrapers.{scraper_name}"
                    )
                continue

            scraper_class = getattr(mod, class_name)

            if scraper_name.startswith("yahoo_"):
                # Yahoo Finance suporta período/intervalo
                min_date_str = missing_dates[0]
                max_date_str = missing_dates[-1]
                min_d = date.fromisoformat(min_date_str)
                max_d = date.fromisoformat(max_date_str)

                if not quiet:
                    print_info(
                        f"Executando Yahoo Finance Scraper no intervalo {min_date_str} a {max_date_str}"
                    )

                # Executa o scraper
                scraper = scraper_class()
                scraper.start_date = min_d
                scraper.end_date = max_d
                scraper.run()
                total_scrapers_run += 1
            else:
                # Scrapers diários: roda uma execução para cada data individual
                for d_str in missing_dates:
                    target_d = date.fromisoformat(d_str)
                    if not quiet:
                        print_info(f"  -> Baixando dados para data: {d_str}")

                    scraper = scraper_class()
                    scraper.target_date = target_d
                    scraper.run()
                    total_scrapers_run += 1
                    # Pequena pausa entre requisições
                    time.sleep(1.0)

            if not quiet:
                print_done(f"Finalizado backfill para {csv_name}")

        except Exception as e:
            if not quiet:
                print_fail(f"Erro ao executar backfill para {csv_name}: {e}")

    # Validação pós-backfill
    if not quiet:
        section("Reavaliando bases pós-backfill", "search")

    total_remaining = 0
    for csv_name, config in sorted(targets.items()):
        csv_path = data_dir / csv_name
        if not csv_path.exists():
            if (data_dir / (csv_name + ".gz")).exists():
                csv_path = data_dir / (csv_name + ".gz")
            else:
                continue

        date_col = config["date_col"]
        group_by_cols = config.get("group_by", [])
        entity_dates = load_entity_dates(csv_path, date_col, group_by_cols)
        if not entity_dates:
            continue

        gaps = check_gaps(entity_dates, threshold=threshold)
        if gaps:
            all_missing = sorted(list({d for dates in gaps.values() for d in dates}))
            total_remaining += len(all_missing)
            if not quiet:
                print_warn(
                    f"{csv_name}: ainda possui {len(all_missing)} buraco(s) (prováveis feriados/indisponibilidade na origem)."
                )
        else:
            if not quiet:
                print_done(f"{csv_name}: 0 buracos!")

    elapsed = time.time() - t0
    if not quiet:
        print_summary(
            "Backfill concluído",
            total=len(gaps_by_csv),
            success=len(gaps_by_csv),
            failed=0,
            skipped=0,
            elapsed=elapsed,
            details=[
                ("gear", "Scrapers executados", str(total_scrapers_run)),
                ("search", "Buracos restantes", str(total_remaining)),
            ],
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Backfill automático de buracos em séries temporais CSV",
    )
    add_common_args(parser)
    parser.add_argument(
        "--csv",
        nargs="+",
        metavar="CSV",
        help="Executar backfill apenas em CSVs específicos",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        metavar="N",
        help="Ignorar entidades com menos de N datas (padrão: 3)",
    )

    args = parser.parse_args()
    apply_common_args(args)

    main(
        csv_filter=args.csv,
        threshold=args.threshold,
        dry_run=args.dry_run,
        quiet=args.quiet,
        verbose=args.verbose,
    )
