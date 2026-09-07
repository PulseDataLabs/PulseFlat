import gzip

#!/usr/bin/env python
# coding: utf-8
"""
scripts/verificar_buracos.py
----------------------------
Verifica se as séries temporais nos CSVs não possuem "buracos"
(dias úteis faltantes) entre a menor e a maior data de referência.

Usa a bizdays.Calendar já definida em utils/parsers.py para determinar
a sequência esperada de dias úteis.

Uso:
    python scripts/verificar_buracos.py
    python scripts/verificar_buracos.py --verbose
    python scripts/verificar_buracos.py --csv anbima_ima_completo.csv
    python scripts/verificar_buracos.py --threshold 5
    python scripts/verificar_buracos.py --fail-on-holes
    python scripts/verificar_buracos.py --dry-run
"""

import argparse
import csv
import sys
import time
from datetime import date
from pathlib import Path

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
from utils.parsers import _CAL

log = ColorLogger("verificar_buracos")

CONFIG: dict[str, dict] = {
    "anbima_ima_completo.csv": {
        "date_col": "data_referencia",
        "group_by": ["indice"],
    },
    "anbima_idka.csv": {
        "date_col": "data_captura",
        "group_by": ["no_indexador", "no_indice"],
    },
    "anbima_titulos_publicos.csv": {
        "date_col": "data_referencia",
        "group_by": ["titulo", "codigo_selic"],
    },
    "anbima_550.csv": {
        "date_col": "data_captura",
        "group_by": ["titulo"],
    },
    "anbima_debentures.csv": {
        "date_col": "data_referencia",
        "group_by": ["codigo"],
    },
    "anbima_indice_imab.csv": {
        "date_col": "data_referencia",
        "group_by": ["indice"],
    },
    "b3_bdi_di_over.csv": {
        "date_col": "data_referencia",
        "group_by": [],
    },
    "b3_bmf_taxas_juros.csv": {
        "date_col": "data_captura",
        "group_by": ["curva", "prazo_dias"],
    },
    "yahoo_acoes_brasileiras.csv": {
        "date_col": "data_referencia",
        "group_by": ["codigo_ativo"],
        "market": "B3",
    },
    "yahoo_acoes_internacionais.csv": {
        "date_col": "data_referencia",
        "group_by": ["codigo_ativo"],
        "market": "US",
    },
    "yahoo_cambio_moedas.csv": {
        "date_col": "data_referencia",
        "group_by": ["codigo_ativo"],
    },
    "yahoo_criptoativos.csv": {
        "date_col": "data_referencia",
        "group_by": ["codigo_ativo"],
    },
    "yahoo_commodities.csv": {
        "date_col": "data_referencia",
        "group_by": ["codigo_ativo"],
        "market": "US",
    },
    "yahoo_indices_globais.csv": {
        "date_col": "data_referencia",
        "group_by": ["codigo_ativo"],
        "market": "US",
    },
    "yahoo_renda_fixa.csv": {
        "date_col": "data_referencia",
        "group_by": ["codigo_ativo"],
        "market": "US",
    },
    "yahoo_etfs.csv": {
        "date_col": "data_referencia",
        "group_by": ["codigo_ativo"],
    },
    "yahoo_fiis_fiagros.csv": {
        "date_col": "data_referencia",
        "group_by": ["codigo_ativo"],
        "market": "B3",
    },
    "ipea_mercados_diarios.csv": {
        "date_col": "data_referencia",
        "group_by": ["codigo_ativo"],
        "market": "US",
    },
}


def _entity_label(key: tuple[str, ...]) -> str:
    if len(key) == 1 and key[0] == "*":
        return ""
    parts = []
    from_globals = CONFIG.get(getattr(_entity_label, "_csv_name", ""), {})
    group_by = from_globals.get("group_by", [])
    for col, val in zip(group_by, key):
        if val:
            parts.append(f"{col}={val}")
    return " · ".join(parts)


def _parse_date(val: str) -> str | None:
    val = val.strip()
    if not val:
        return None
    if "T" in val:
        val = val.split("T")[0]
    if len(val) == 10 and val[4] == "-" and val[7] == "-":
        return val
    if len(val) == 8 and val.isdigit():
        return f"{val[:4]}-{val[4:6]}-{val[6:]}"
    return None


def load_entity_dates(
    csv_path: Path,
    date_col: str,
    group_by_cols: list[str],
) -> dict[tuple[str, ...], set[str]]:
    entity_dates: dict[tuple[str, ...], set[str]] = {}
    is_gz = str(csv_path).endswith(".gz")
    open_func = gzip.open if is_gz else open
    open_mode = "rt" if is_gz else "r"
    open_kwargs = (
        {"encoding": "utf-8", "newline": ""}
        if is_gz
        else {"newline": "", "encoding": "utf-8"}
    )
    with open_func(csv_path, open_mode, **open_kwargs) as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return entity_dates
        col_lower = {c.lower().strip(): c for c in reader.fieldnames}
        actual_date_col = col_lower.get(date_col.lower().strip())
        if not actual_date_col:
            return entity_dates
        actual_group_cols = []
        for col in group_by_cols:
            actual = col_lower.get(col.lower().strip())
            actual_group_cols.append(actual if actual else col)

        for row in reader:
            raw = row.get(actual_date_col, "")
            date_val = _parse_date(raw)
            if not date_val:
                continue
            if actual_group_cols and all(actual_group_cols):
                key = tuple(row.get(c, "").strip() for c in actual_group_cols)
            else:
                key = ("*",)
            if key not in entity_dates:
                entity_dates[key] = set()
            entity_dates[key].add(date_val)

    return entity_dates


B3_EXCHANGE_HOLIDAYS = {
    # Vésperas de Natal e Ano Novo (Pregão B3 fechado)
    "2024-12-24", "2024-12-31",
    "2025-12-24", "2025-12-31",
    "2026-12-24", "2026-12-31",
}

US_MARKET_HOLIDAYS = {
    # 2024
    "2024-01-01", "2024-01-15", "2024-02-19", "2024-03-29", "2024-05-27",
    "2024-06-19", "2024-07-04", "2024-09-02", "2024-11-28", "2024-12-25",
    # 2025 (inclui luto nacional Jimmy Carter 09/01/2025)
    "2025-01-01", "2025-01-09", "2025-01-20", "2025-02-17", "2025-04-18", "2025-05-26",
    "2025-06-19", "2025-07-04", "2025-09-01", "2025-11-27", "2025-12-25",
    # 2026
    "2026-01-01", "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25",
    "2026-06-19", "2026-07-03", "2026-09-07", "2026-11-26", "2026-12-25",
}

UK_MARKET_HOLIDAYS = {
    # 2024
    "2024-01-01", "2024-03-29", "2024-04-01", "2024-05-06", "2024-05-27", "2024-08-26", "2024-12-25", "2024-12-26",
    # 2025
    "2025-01-01", "2025-04-18", "2025-04-21", "2025-05-05", "2025-05-26", "2025-08-25", "2025-12-25", "2025-12-26",
    # 2026
    "2026-01-01", "2026-04-03", "2026-04-06", "2026-05-04", "2026-05-25", "2026-08-31", "2026-12-25", "2026-12-28",
}


def get_extra_holidays(key: tuple[str, ...], config: dict, csv_name: str) -> set[str]:
    hols = set()
    market = config.get("market")
    if market == "US":
        hols.update(US_MARKET_HOLIDAYS)
    elif market == "B3":
        hols.update(B3_EXCHANGE_HOLIDAYS)
    elif market == "UK":
        hols.update(UK_MARKET_HOLIDAYS)

    ticker = key[0] if key and key[0] != "*" else ""
    if ticker.endswith(".SA") or "acoes_brasileiras" in csv_name or "fiis_fiagros" in csv_name:
        hols.update(B3_EXCHANGE_HOLIDAYS)
    elif ticker.endswith(".L"):
        hols.update(UK_MARKET_HOLIDAYS)
    elif ticker and not ticker.endswith(".SA") and not ticker.endswith(".L") and config.get("group_by") == ["codigo_ativo"]:
        hols.update(US_MARKET_HOLIDAYS)
        if "BRENT" in ticker:
            hols.update(UK_MARKET_HOLIDAYS)

    return hols

def check_gaps(
    entity_dates: dict[tuple[str, ...], set[str]],
    threshold: int = 3,
    extra_holidays: set[str] | None = None,
) -> dict[tuple[str, ...], list[str]]:
    gaps: dict[tuple[str, ...], list[str]] = {}

    # Limites suportados pelo Calendar em utils/parsers.py
    start_cal = date(2024, 1, 1)
    end_cal = date(2028, 12, 31)

    for key, dates in entity_dates.items():
        if len(dates) < threshold:
            continue
        sorted_dates = sorted(dates)
        min_date = date.fromisoformat(sorted_dates[0])
        max_date = date.fromisoformat(sorted_dates[-1])

        # Ajusta datas para os limites suportados
        effective_min = max(min_date, start_cal)
        effective_max = min(max_date, end_cal)

        if effective_min > effective_max:
            continue

        expected = _CAL.seq(effective_min, effective_max)
        expected_strs = {d.strftime("%Y-%m-%d") for d in expected}

        # Filtra as datas reais para comparar apenas as que estão no período do calendário
        actual_filtered = {
            d for d in dates if start_cal <= date.fromisoformat(d) <= end_cal
        }

        missing_set = expected_strs - actual_filtered
        if extra_holidays:
            missing_set -= extra_holidays
        missing = sorted(missing_set)
        if missing:
            gaps[key] = missing

    return gaps


def run_csv(
    csv_path: Path,
    config: dict,
    threshold: int,
    verbose: bool,
) -> tuple[int, int, dict]:
    date_col = config["date_col"]
    group_by_cols = config.get("group_by", [])
    entity_dates = load_entity_dates(csv_path, date_col, group_by_cols)
    if not entity_dates:
        return 0, 0, {}

    total_entities = len(entity_dates)
    gaps: dict[tuple[str, ...], list[str]] = {}
    csv_name = csv_path.name
    for key, dates in entity_dates.items():
        extra_hols = get_extra_holidays(key, config, csv_name)
        res = check_gaps({key: dates}, threshold=threshold, extra_holidays=extra_hols)
        if res:
            gaps.update(res)
    gaps_count = len(gaps)

    sum(len(missing) for missing in gaps.values())

    affected_entity_names = []
    if verbose:
        for key, missing in sorted(gaps.items()):
            label = _entity_label(key)
            if label:
                line = f"  {label}: {', '.join(missing)} ({len(missing)} buraco{'s' if len(missing) > 1 else ''})"
            else:
                line = f"  Datas faltantes: {', '.join(missing)} ({len(missing)} buraco{'s' if len(missing) > 1 else ''})"
            affected_entity_names.append(line)

    return gaps_count, total_entities, gaps


def main(
    csv_filter: list[str] | None = None,
    threshold: int = 3,
    fail_on_holes: bool = False,
    resolve: bool = False,
    dry_run: bool = False,
    quiet: bool = False,
    verbose: bool = False,
) -> None:
    t0 = time.time()
    if not quiet:
        banner(
            "Verificar Buracos em Séries Temporais",
            "Valida continuidade de dias úteis nos CSVs",
        )

    if dry_run:
        if not quiet:
            print_info("Modo dry-run: nenhuma verificação será executada de fato.")
        return

    root_dir = Path(__file__).resolve().parents[1]
    data_dir = root_dir / "data"

    if csv_filter:
        targets = {k: v for k, v in CONFIG.items() if k in csv_filter}
    else:
        targets = dict(CONFIG)

    if not targets:
        if not quiet:
            print_warn("Nenhum CSV habilitado para verificação.")
        return

    if not quiet:
        section("Processando arquivos", "search")

    total = len(targets)
    total_ok = 0
    total_holes = 0
    total_skipped = 0
    total_gaps_found = 0
    total_entities_checked = 0
    details = []
    gaps_by_csv: dict[str, list[str]] = {}

    for idx, (csv_name, config) in enumerate(sorted(targets.items()), 1):
        if not quiet:
            print_start(f"[{idx}/{total}] {csv_name}", icon="file")

        csv_path = data_dir / csv_name
        if not csv_path.exists():
            if (data_dir / (csv_name + ".gz")).exists():
                csv_path = data_dir / (csv_name + ".gz")
            else:
                if not quiet:
                    print_warn(f"{csv_name}: arquivo não encontrado.")
                total_skipped += 1
                details.append(("skip", csv_name, "arquivo não encontrado"))
                continue

        if dry_run:
            if not quiet:
                print_done(f"{csv_name}: dry-run (pularia verificação)")
            total_ok += 1
            continue

        _entity_label._csv_name = csv_name

        gaps_count, entity_count, gaps = run_csv(
            csv_path,
            config,
            threshold=threshold,
            verbose=verbose,
        )

        total_entities_checked += entity_count
        if entity_count == 0:
            if not quiet:
                print_warn(f"{csv_name}: sem dados para verificar.")
            total_skipped += 1
            details.append(("skip", csv_name, "sem dados"))
            continue

        if gaps_count == 0:
            if not quiet:
                print_done(
                    f"OK — {entity_count} entidade{'s' if entity_count > 1 else ''}, 0 buracos"
                )
            total_ok += 1
            details.append(("success", csv_name, "0 buracos"))
        else:
            total_gaps = sum(len(m) for m in gaps.values())
            total_holes += 1
            total_gaps_found += total_gaps
            all_missing = sorted(list({d for dates in gaps.values() for d in dates}))
            gaps_by_csv[csv_name] = all_missing
            if not quiet:
                print_fail(
                    f"BURACOS: {gaps_count} entidade{'s' if gaps_count > 1 else ''} "
                    f"com {total_gaps} data{'s' if total_gaps > 1 else ''} faltante{'s' if total_gaps > 1 else ''}"
                )
                if verbose:
                    for line in gaps.get("_lines", []) if "_lines" in gaps else []:
                        pass
                for key, missing in sorted(gaps.items()):
                    label = _entity_label(key)
                    gap_count = len(missing)
                    gap_dates = ", ".join(missing[:5])
                    if len(missing) > 5:
                        gap_dates += f" ... (+{len(missing) - 5})"
                    if label:
                        detail_line = f"    {label}: {gap_dates}"
                    else:
                        detail_line = f"    Datas: {gap_dates}"
                    if verbose:
                        if not quiet:
                            print_info(detail_line, icon="warn")
                    details.append(
                        (
                            "fail",
                            f"{csv_name} ({label})" if label else csv_name,
                            f"{gap_count} buraco(s): {gap_dates}",
                        )
                    )
            else:
                details.append(("fail", csv_name, f"{total_gaps} data(s) faltante(s)"))

    if not quiet:
        elapsed = time.time() - t0
        print_summary(
            "Verificação concluída",
            total=total,
            success=total_ok,
            failed=0,
            skipped=total_skipped,
            elapsed=elapsed,
            details=[
                ("success", "CSVs OK", str(total_ok)),
                ("fail", "CSVs com buracos", str(total_holes)),
                ("skip", "CSVs ignorados", str(total_skipped)),
                ("search", "Entidades verificadas", str(total_entities_checked)),
                ("gear", "Total de datas faltantes", str(total_gaps_found)),
            ],
        )

    if resolve and gaps_by_csv:
        if not quiet:
            section("Resolvendo buracos detectados via Backfill", "gear")
            print_info(f"Iniciando backfill automático em {len(gaps_by_csv)} arquivo(s)...", icon="refresh")
        from scripts.backfill_buracos import main as run_backfill
        run_backfill(
            csv_filter=list(gaps_by_csv.keys()),
            threshold=threshold,
            dry_run=dry_run,
            quiet=quiet,
            verbose=verbose,
        )
        if not quiet:
            section("Reavaliando séries pós-backfill", "search")
        return main(
            csv_filter=csv_filter,
            threshold=threshold,
            fail_on_holes=fail_on_holes,
            resolve=False,
            dry_run=dry_run,
            quiet=quiet,
            verbose=verbose,
        )

    if fail_on_holes and total_holes > 0:
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verifica buracos (dias úteis faltantes) em séries temporais CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
exemplos:
  python scripts/verificar_buracos.py
  python scripts/verificar_buracos.py --verbose
  python scripts/verificar_buracos.py --csv anbima_ima_completo.csv
  python scripts/verificar_buracos.py --threshold 5
  python scripts/verificar_buracos.py --fail-on-holes
  python scripts/verificar_buracos.py --dry-run
        """,
    )
    add_common_args(parser)
    parser.add_argument(
        "--csv",
        nargs="+",
        metavar="CSV",
        help="Verificar apenas CSVs específicos (ex: anbima_ima_completo.csv)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        metavar="N",
        help="Ignorar entidades com menos de N datas (padrão: 3)",
    )
    parser.add_argument(
        "--fail-on-holes",
        action="store_true",
        help="Sair com exit code 1 se houver buracos",
    )
    parser.add_argument(
        "--resolve",
        action="store_true",
        help="Executar backfill automático para resolver os buracos encontrados",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Listar CSVs habilitados para verificação e sair",
    )

    args = parser.parse_args()
    apply_common_args(args)

    if args.dry_run:
        log.info("Modo dry-run: nenhuma verificação será executada de fato.")

    if args.list:
        root_dir = Path(__file__).resolve().parents[1]
        data_dir = root_dir / "data"
        print("CSVs habilitados para verificação de buracos:")
        for csv_name, config in sorted(CONFIG.items()):
            exists = "✓" if (data_dir / csv_name).exists() else "✗"
            date_col = config["date_col"]
            group_by = ", ".join(config.get("group_by", [])) or "(sem agrupamento)"
            print(f"  {exists}  {csv_name:<45} data={date_col:<20} grupo={group_by}")
        sys.exit(0)

    main(
        csv_filter=args.csv,
        threshold=args.threshold,
        fail_on_holes=args.fail_on_holes,
        resolve=args.resolve,
        dry_run=args.dry_run,
        quiet=args.quiet,
        verbose=args.verbose,
    )
