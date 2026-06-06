#!/usr/bin/env python
# coding: utf-8
"""
scripts/generate_market_latest.py
----------------------------------
Lê os CSVs mais recentes em data/ e extrai os últimos valores dos principais
indicadores financeiros, gerando data/market_latest.json e market_latest.js.

Uso:
    python scripts/generate_market_latest.py
    python scripts/generate_market_latest.py --dry-run
    python scripts/generate_market_latest.py --quiet
"""

import csv
import json
import sys
import time
import argparse
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils.ux import (
    banner, section, print_start, print_done, print_fail, print_warn, print_info,
    print_summary, add_common_args, apply_common_args, ColorLogger, ICON,
)

log = ColorLogger("generate_market_latest")

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


# ── Helpers de formatação BR ──────────────────────────────────────────────

def _parse_br_float(val: str) -> Optional[float]:
    if not val or not val.strip():
        return None
    try:
        return float(val.strip().replace(",", "."))
    except ValueError:
        return None


def _format_pct(val: float, decimals: int = 2) -> str:
    return f"{val:,.{decimals}f}%".replace(",", "X").replace(".", ",").replace("X", ".")


def _format_number(val: float, decimals: int = 2) -> str:
    return f"{val:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _calc_change(old: float, new: float) -> Optional[float]:
    if old == 0:
        return None
    return ((new / old) - 1) * 100


def _format_change(change: Optional[float]) -> Optional[str]:
    if change is None:
        return None
    signal = "+" if change >= 0 else ""
    return f"{signal}{change:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")


def _infer_type(change: Optional[float]) -> str:
    if change is None:
        return "neutral"
    if change > 0.01:
        return "up"
    if change < -0.01:
        return "down"
    return "neutral"


# ── Leitores de CSV ───────────────────────────────────────────────────────

def _read_csv(path: str) -> list[dict]:
    if not Path(path).exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sorted_by(rows: list[dict], col: str, reverse: bool = True) -> list[dict]:
    return sorted(rows, key=lambda r: r.get(col, ""), reverse=reverse)


def _last_filtered(path: str, filter_col: str, filter_val: object, sort_col: str, n: int = 1) -> list[dict]:
    rows = _read_csv(path)
    if filter_col:
        rows = [r for r in rows if r.get(filter_col) == filter_val]
    rows = _sorted_by(rows, sort_col)
    seen: set[str] = set()
    deduped: list[dict] = []
    for r in rows:
        key = r.get(sort_col, "")[:10]
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return deduped[:n]


# ── Definição dos indicadores ─────────────────────────────────────────────

INDICATOR_DEFS = [
    {
        "label": "CDI",
        "csv": "b3_bdi_di_over.csv",
        "value_col": "average",
        "sort_col": "rpt_dt",
        "ref_col": "rpt_dt",
        "format": "pct",
        "decimals": 2,
        "track_change": False,
    },
    {
        "label": "SELIC",
        "csv": "anbima_indicadores.csv",
        "filter_col": "indicador",
        "filter_val": "Taxa SELIC (BC)",
        "value_col": "valor",
        "sort_col": "data_referencia",
        "ref_col": "data_referencia",
        "format": "pct",
        "decimals": 2,
        "track_change": False,
    },
    {
        "label": "IPCA 12m",
        "csv": "bcb_sgs.csv",
        "filter_col": "codigo_serie",
        "filter_val": "433",
        "value_col": "valor",
        "sort_col": "data",
        "ref_col": "data",
        "format": "pct",
        "decimals": 2,
        "track_change": False,
    },
    {
        "label": "IGP-M 12m",
        "csv": "bcb_sgs.csv",
        "filter_col": "codigo_serie",
        "filter_val": "190",
        "value_col": "valor",
        "sort_col": "data",
        "ref_col": "data",
        "format": "pct",
        "decimals": 2,
        "track_change": False,
    },
    {
        "label": "PTAX USD Venda",
        "csv": "bcb_ptax.csv",
        "value_col": "cotacao_venda",
        "sort_col": "data_hora_cotacao",
        "ref_col": "data_hora_cotacao",
        "format": "number",
        "decimals": 4,
        "track_change": True,
    },
    {
        "label": "PTAX USD Compra",
        "csv": "bcb_ptax.csv",
        "value_col": "cotacao_compra",
        "sort_col": "data_hora_cotacao",
        "ref_col": "data_hora_cotacao",
        "format": "number",
        "decimals": 4,
        "track_change": True,
    },
    {
        "label": "IBOVESPA",
        "csv": "yahoo_finance_series.csv",
        "filter_col": "ticker",
        "filter_val": "^BVSP",
        "value_col": "vr_fechamento",
        "sort_col": "dt_ref",
        "ref_col": "dt_ref",
        "format": "number",
        "decimals": 0,
        "track_change": True,
    },
    {
        "label": "IMA-GERAL",
        "csv": "anbima_ima_completo.csv",
        "filter_col": "indice",
        "filter_val": "IMA-GERAL",
        "value_col": "numero_indice",
        "sort_col": "data_referencia",
        "ref_col": "data_referencia",
        "format": "number",
        "decimals": 2,
        "track_change": False,
    },
]


def generate(dry_run: bool = False) -> None:
    t0 = time.time()
    banner("Market Latest", "Extrai últimos indicadores → market_latest.json")
    section("Lendo CSVs", "chart")

    results = []
    total = len(INDICATOR_DEFS)

    for idx, idef in enumerate(INDICATOR_DEFS, 1):
        label = idef["label"]
        csv_path = DATA_DIR / idef["csv"]
        print_start(f"[{idx}/{total}] {label} ({idef['csv']})", icon="search")

        n_rows = 2 if idef["track_change"] else 1
        rows = _last_filtered(
            str(csv_path),
            idef.get("filter_col"),
            idef.get("filter_val"),
            idef["sort_col"],
            n=n_rows,
        )

        if not rows:
            print_warn(f"{label}: sem dados em {idef['csv']}")
            continue

        latest = rows[0]
        raw_val = latest.get(idef["value_col"], "")
        val_float = _parse_br_float(raw_val)

        if val_float is None:
            print_warn(f"{label}: valor inválido '{raw_val}'")
            continue

        if idef["format"] == "pct":
            value = _format_pct(val_float, idef["decimals"])
        else:
            value = _format_number(val_float, idef["decimals"])

        ref_raw = latest.get(idef["ref_col"], "")
        ref_date = ref_raw[:10] if ref_raw else ""

        change_pct = None
        if idef["track_change"] and len(rows) > 1:
            old_val = _parse_br_float(rows[1].get(idef["value_col"], ""))
            if old_val is not None and old_val != 0:
                change_pct = _calc_change(old_val, val_float)

        entry = {
            "label": label,
            "value": value,
            "reference_date": ref_date,
            "type": _infer_type(change_pct),
        }

        if change_pct is not None:
            entry["change"] = _format_change(change_pct)

        results.append(entry)
        print_done(f"{label} → {value} ({ref_date})")

    if not dry_run and results:
        section("Escrevendo saída", "package")
        json_path = DATA_DIR / "market_latest.json"
        js_path = DATA_DIR / "market_latest.js"

        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps(results, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        js_path.write_text(
            f"window.PULSEFLAT_MARKET_LATEST = {json.dumps(results, indent=2, ensure_ascii=False)};\n",
            encoding="utf-8",
        )
        print_done(f"market_latest.json — {len(results)} indicadores")
        print_done(f"market_latest.js — {len(results)} indicadores")
    elif dry_run:
        print_info(f"Dry-run: {len(results)} indicadores seriam gerados.")
    else:
        print_warn("Nenhum indicador extraído — arquivo não gerado.")

    elapsed = time.time() - t0
    print_summary(
        "Market Latest gerado",
        total=total,
        success=len(results),
        failed=total - len(results),
        elapsed=elapsed,
        details=[
            ("chart", "Indicadores extraídos", str(len(results))),
        ],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="📈 Gera market_latest.json com os últimos valores dos indicadores",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
exemplos:
  python scripts/generate_market_latest.py
  python scripts/generate_market_latest.py --dry-run
  python scripts/generate_market_latest.py --quiet
        """,
    )
    add_common_args(parser)
    args = parser.parse_args()

    if args.dry_run:
        log.info("Modo dry-run: market_latest.json não será salvo.")

    apply_common_args(args)
    generate(dry_run=args.dry_run)
