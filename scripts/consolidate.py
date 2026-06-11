#!/usr/bin/env python
# coding: utf-8
"""
scripts/consolidate.py
-----------------------
Gera tabela consolidada com o último valor de cada indicador financeiro
time-series (séries temporais). Exclui contagens e dados transacionais.

Saídas:
  data/consolidated.json  — dados consolidados (formato JSON)
  data/consolidated.csv   — dados consolidados (formato CSV)
  data/consolidated.js    — fallback offline para a página web
"""

import csv
import json
import sys
import time
import argparse
import re
from pathlib import Path
from typing import Optional
from collections import OrderedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils.ux import (
    banner, section, print_start, print_done, print_fail, print_warn, print_info,
    print_summary, add_common_args, apply_common_args, ColorLogger, ICON,
)

log = ColorLogger("consolidate")

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


# ── Helpers ────────────────────────────────────────────────────────────

def _read_csv(path: str) -> list[dict]:
    if not Path(path).exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sorted_by(rows: list[dict], col: str, reverse: bool = True) -> list[dict]:
    return sorted(rows, key=lambda r: r.get(col, ""), reverse=reverse)


def _parse_br_float(val: str) -> Optional[float]:
    if not val or not val.strip():
        return None
    try:
        return float(val.strip().replace(",", "."))
    except ValueError:
        return None


def _fmt_val(val: str) -> str:
    f = _parse_br_float(val)
    if f is None:
        return val
    abs_f = abs(f)
    if abs_f >= 1000:
        decimals = 0
    elif abs_f >= 1:
        decimals = 2
    elif abs_f >= 0.01:
        decimals = 4
    else:
        decimals = 6
    return f"{f:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _fmt_pct(val: str, decimals: int = 2) -> str:
    f = _parse_br_float(val)
    if f is None:
        return val
    return f"{f:,.{decimals}f}%".replace(",", "X").replace(".", ",").replace("X", ".")


def _safe(val: str) -> str:
    return (val or "").strip()


# ── Nomes amigáveis de datasets ────────────────────────────────────────

DATASET_LABEL = {
    "bcb_sgs.csv": "BCB SGS",
    "anbima_indicadores.csv": "ANBIMA Indicadores",
    "b3_bdi_di_over.csv": "B3 DI Over",
    "b3_bmf_taxas_juros.csv": "B3 BMF Taxas",
    "b3_indicadores_financeiros.csv": "B3 Indicadores Financeiros",
    "b3_taxa_cambio_referencia.csv": "B3 Taxa Câmbio",
    "bcb_ptax.csv": "BCB PTAX",
    "yahoo_finance_series.csv": "Yahoo Finance",
    "anbima_indice_imab.csv": "ANBIMA IMA-B",
    "anbima_titulos_publicos.csv": "ANBIMA Títulos Públicos",
}


# ── Definições dos indicadores ─────────────────────────────────────────

INDICATOR_DEFS = [
    # ── B3 DI Over ─────────────────────────────────────────────────
    {
        "dataset": "b3_bdi_di_over.csv",
        "source": "B3",
        "label": "DI Over (SELIC equivalente)",
        "value_col": "average",
        "date_col": "rpt_dt",
        "fmt": "pct",
    },
    {
        "dataset": "b3_bdi_di_over.csv",
        "source": "B3",
        "label": "DI Over — Volume financeiro",
        "value_col": "financial_volume",
        "date_col": "rpt_dt",
        "fmt": "number",
    },
    # ── B3 BMF Taxas de Juros ──────────────────────────────────────
    {
        "dataset": "b3_bmf_taxas_juros.csv",
        "source": "B3",
        "indicator_col": "curva",
        "value_col": "taxa",
        "date_col": "data_referencia",
        "fmt": "pct",
        "note_col": "prazo_dias",
        "category": "Taxas de Juros",
    },
    # ── B3 Indicadores Financeiros ─────────────────────────────────
    {
        "dataset": "b3_indicadores_financeiros.csv",
        "source": "B3",
        "indicator_col": "description",
        "value_col_main": "value",
        "value_col_fallback": "rate",
        "date_col": "last_update",
        "category": "Indicadores B3",
    },
    # ── B3 Taxa de Câmbio ──────────────────────────────────────────
    {
        "dataset": "b3_taxa_cambio_referencia.csv",
        "source": "B3",
        "indicator_col": "description",
        "value_col_main": "value",
        "value_col_fallback": "rate",
        "date_col": "lastupdate",
        "category": "Taxas de Câmbio",
    },
    # ── BCB PTAX ───────────────────────────────────────────────────
    {
        "dataset": "bcb_ptax.csv",
        "source": "BCB",
        "label": "PTAX USD — Compra",
        "value_col": "cotacao_compra",
        "date_col": "data_hora_cotacao",
        "category": "Taxas de Câmbio",
    },
    {
        "dataset": "bcb_ptax.csv",
        "source": "BCB",
        "label": "PTAX USD — Venda",
        "value_col": "cotacao_venda",
        "date_col": "data_hora_cotacao",
        "category": "Taxas de Câmbio",
    },
    # ── BCB SGS ────────────────────────────────────────────────────
    *[
        {
            "dataset": "bcb_sgs.csv",
            "source": "BCB",
            "label": nome,
            "value_col": "valor",
            "date_col": "data",
            "filter_col": "codigo_serie",
            "filter_val": codigo,
            "fmt": "pct",
            "category": "Séries SGS",
        }
        for codigo, nome in [
            ("11",   "SELIC (% a.d.)"),
            ("1",    "IGP-M"),
            ("189",  "IGP-M (índice)"),
            ("190",  "IGP-M 12m"),
            ("433",  "IPCA 12m"),
        ]
    ],
    # ── ANBIMA Indicadores ─────────────────────────────────────────
    {
        "dataset": "anbima_indicadores.csv",
        "source": "ANBIMA",
        "indicator_col": "indicador",
        "value_col": "valor",
        "date_col": "data_referencia",
        "category_col": "categoria",
        "unit_col": "unidade",
    },
    # ── ANBIMA Títulos Públicos ───────────────────────────────────
    {
        "dataset": "anbima_titulos_publicos.csv",
        "source": "ANBIMA",
        "indicator_col": "codigo_selic",
        "value_cols": [
            ("tx_indicativa", "Taxa indicativa", "pct"),
            ("pu", "PU", "number"),
        ],
        "date_col": "data_referencia",
        "note_col": "titulo",
        "category": "Títulos Públicos",
    },
    # ── ANBIMA IMA-B ───────────────────────────────────────────────
    {
        "dataset": "anbima_indice_imab.csv",
        "source": "ANBIMA",
        "indicator_col": "indice",
        "value_cols": [
            ("numero_indice", "Número-índice", "number"),
            ("variacao_diaria", "Variação diária", "pct"),
            ("duration_du", "Duration (d.u.)", "number"),
        ],
        "date_col": "data_de_referencia",
        "category": "IMA-B",
    },
    # ── Yahoo Finance ──────────────────────────────────────────────
    *[
        {
            "dataset": "yahoo_finance_series.csv",
            "source": "Yahoo Finance",
            "label": ticker,
            "value_col": "vr_fechamento",
            "date_col": "dt_ref",
            "filter_col": "ticker",
            "filter_val": ticker,
            "category": "Mercados Globais",
        }
        for ticker in ["^BVSP", "BRL=X", "GLD", "^TNX"]
    ],
]


# ── Extratores ────────────────────────────────────────────────────────

def _build_base(idef: dict) -> dict:
    return {
        "dataset": idef["dataset"],
        "dataset_label": DATASET_LABEL.get(idef["dataset"], idef["dataset"].replace(".csv", "")),
        "fonte": idef["source"],
        "categoria": idef.get("category", ""),
        "tipo": "indicador",
    }


def _fmt(idef: dict, raw_val: str) -> str:
    fmt = idef.get("fmt", "")
    if fmt == "pct":
        return _fmt_pct(raw_val)
    if fmt == "number":
        return _fmt_val(raw_val)
    f = _parse_br_float(raw_val)
    if f is not None:
        return _fmt_val(raw_val)
    return raw_val


def _ref_date(idef: dict, row: dict) -> str:
    date_col = idef["date_col"]
    d = _safe(row.get(date_col, ""))[:10]
    if d:
        return d
    return _safe(row.get("data_captura", ""))[:10]


def _extract_single_value(
    rows: list[dict], idef: dict
) -> Optional[dict]:
    value_col = idef["value_col"]
    rows_sorted = _sorted_by(rows, idef["date_col"])
    if not rows_sorted:
        return None
    latest = rows_sorted[0]
    raw_val = _safe(latest.get(value_col, ""))
    if not raw_val:
        return None
    out = _build_base(idef)
    out["indicador"] = idef.get("label", "")
    out["valor"] = _fmt(idef, raw_val)
    out["unidade"] = idef.get("unit", "")
    out["data_referencia"] = _ref_date(idef, latest)
    out["captura_em"] = _safe(latest.get("data_captura", ""))[:10]
    out["metrica"] = value_col
    return out


def _extract_filtered_value(
    rows: list[dict], idef: dict
) -> Optional[dict]:
    filtered = [
        r for r in rows
        if _safe(r.get(idef["filter_col"], "")) == idef["filter_val"]
    ]
    if not filtered:
        return None
    return _extract_single_value(filtered, idef)


def _extract_grouped_value(
    rows: list[dict], idef: dict
) -> list[dict]:
    indicator_col = idef["indicator_col"]
    value_col = idef["value_col"]
    category_col = idef.get("category_col", "")
    unit_col = idef.get("unit_col", "")

    groups: dict[str, list[dict]] = {}
    for r in rows:
        key = _safe(r.get(indicator_col, ""))
        if key:
            groups.setdefault(key, []).append(r)

    results = []
    for indicator_name, grp in sorted(groups.items()):
        grp_sorted = _sorted_by(grp, idef["date_col"])
        if not grp_sorted:
            continue
        latest = grp_sorted[0]
        raw_val = _safe(latest.get(value_col, ""))
        if not raw_val:
            continue
        out = _build_base(idef)
        out["indicador"] = indicator_name
        out["valor"] = _fmt(idef, raw_val)
        out["unidade"] = _safe(latest.get(unit_col, "")) if unit_col else ""
        out["categoria"] = (_safe(latest.get(category_col, "")) or idef.get("category", "")) if category_col else idef.get("category", "")
        out["data_referencia"] = _ref_date(idef, latest)
        out["captura_em"] = _safe(latest.get("data_captura", ""))[:10]
        out["metrica"] = value_col
        results.append(out)
    return results


def _extract_multi_value(
    rows: list[dict], idef: dict
) -> list[dict]:
    indicator_col = idef.get("indicator_col", "")
    value_cols = idef["value_cols"]
    note_col = idef.get("note_col", "")

    if indicator_col:
        groups: dict[str, list[dict]] = {}
        for r in rows:
            key = _safe(r.get(indicator_col, ""))
            if key:
                groups.setdefault(key, []).append(r)
    else:
        groups = {"": rows}

    results = []
    for indicator_name, grp in groups.items():
        grp_sorted = _sorted_by(grp, idef["date_col"])
        if not grp_sorted:
            continue
        latest = grp_sorted[0]
        note = _safe(latest.get(note_col, "")) if note_col else ""
        label_base = indicator_name or idef.get("label", "")
        if note and indicator_name:
            label_base = f"{indicator_name} ({note})"

        for col_name, col_label, col_fmt in value_cols:
            raw_val = _safe(latest.get(col_name, ""))
            if not raw_val:
                continue
            out = _build_base(idef)
            out["indicador"] = label_base
            out["valor"] = _fmt_pct(raw_val) if col_fmt == "pct" else _fmt_val(raw_val)
            out["unidade"] = col_label
            out["data_referencia"] = _ref_date(idef, latest)
            out["captura_em"] = _safe(latest.get("data_captura", ""))[:10]
            out["metrica"] = col_name
            results.append(out)
    return results


def _extract_dual_value(
    rows: list[dict], idef: dict
) -> list[dict]:
    indicator_col = idef.get("indicator_col", "")
    main_col = idef["value_col_main"]
    fallback_col = idef["value_col_fallback"]

    groups: dict[str, list[dict]] = {}
    for r in rows:
        key = _safe(r.get(indicator_col, ""))
        if key:
            groups.setdefault(key, []).append(r)

    results = []
    for indicator_name, grp in groups.items():
        grp_sorted = _sorted_by(grp, idef["date_col"])
        if not grp_sorted:
            continue
        latest = grp_sorted[0]
        raw_val = _safe(latest.get(main_col, ""))
        used_col = main_col
        if not raw_val:
            raw_val = _safe(latest.get(fallback_col, ""))
            used_col = fallback_col
        if not raw_val:
            continue
        out = _build_base(idef)
        out["indicador"] = indicator_name
        out["valor"] = _fmt(idef, raw_val)
        out["unidade"] = ""
        out["data_referencia"] = _ref_date(idef, latest)
        out["captura_em"] = _safe(latest.get("data_captura", ""))[:10]
        out["metrica"] = used_col
        results.append(out)
    return results


# ── Gerador principal ─────────────────────────────────────────────────

def generate(dry_run: bool = False) -> None:
    t0 = time.time()
    banner("Consolidado", "Extrai último valor de cada indicador financeiro → consolidated.json/csv")
    section("Processando indicadores", "chart")

    all_results: list[dict] = []
    total = len(INDICATOR_DEFS)

    for idx, idef in enumerate(INDICATOR_DEFS, 1):
        label = idef.get("label", idef.get("indicator_col", idef["dataset"]))
        print_start(f"[{idx}/{total}] {label} ({idef['dataset']})", icon="search")

        csv_path = DATA_DIR / idef["dataset"]
        if not csv_path.exists():
            print_warn(f"{idef['dataset']}: arquivo não encontrado")
            continue

        rows = _read_csv(str(csv_path))
        if not rows:
            print_warn(f"{idef['dataset']}: sem dados")
            continue

        if "value_cols" in idef:
            results = _extract_multi_value(rows, idef)

        elif "filter_col" in idef:
            result = _extract_filtered_value(rows, idef)
            results = [result] if result else []

        elif "indicator_col" in idef and "value_col_main" in idef:
            results = _extract_dual_value(rows, idef)

        elif "indicator_col" in idef:
            results = _extract_grouped_value(rows, idef)

        else:
            result = _extract_single_value(rows, idef)
            results = [result] if result else []

        all_results.extend(results)
        if results:
            print_done(f"{label} → {len(results)} indicador(es)")
        else:
            print_warn(f"{label}: sem dados")

    if not all_results:
        print_warn("Nenhum dado consolidado extraído.")
        return

    all_results.sort(key=lambda r: (r["fonte"], r["dataset"], r["indicador"]))

    if not dry_run:
        section("Escrevendo saída", "package")

        json_path = DATA_DIR / "consolidated.json"
        csv_path = DATA_DIR / "consolidated.csv"
        js_path = DATA_DIR / "consolidated.js"

        json_path.parent.mkdir(parents=True, exist_ok=True)

        json_path.write_text(
            json.dumps(all_results, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print_done(f"consolidated.json — {len(all_results)} registros")

        js_path.write_text(
            f"window.PULSEFLAT_CONSOLIDATED = {json.dumps(all_results, indent=2, ensure_ascii=False)};\n",
            encoding="utf-8",
        )
        print_done(f"consolidated.js — {len(all_results)} registros")

        fieldnames = [
            "dataset", "dataset_label", "fonte", "categoria", "tipo",
            "indicador", "valor", "unidade", "data_referencia", "captura_em", "metrica",
        ]
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        print_done(f"consolidated.csv — {len(all_results)} registros")

    else:
        print_info(f"Dry-run: {len(all_results)} registros seriam gerados.")

    elapsed = time.time() - t0
    print_summary(
        "Consolidado gerado",
        total=total,
        success=len(all_results),
        failed=0,
        elapsed=elapsed,
        details=[
            ("chart", "Indicadores", str(len(all_results))),
            ("info", "Fontes", str(len({r["fonte"] for r in all_results}))),
        ],
    )


# ── Pivoteamento (multivalor → colunas) ───────────────────────────────

def generate_pivoted() -> None:
    """Lê consolidated.json e gera consolidated_pivoted.json/js.
    Cada grupo (dataset_label, fonte, data_referencia, indicador) vira uma
    única linha. Se o grupo tiver 2+ registros com unidades diferentes,
    cada unidade vira uma coluna; caso contrário usa 'Valor'.
    """
    src = DATA_DIR / "consolidated.json"
    if not src.exists():
        return

    raw = json.loads(src.read_text(encoding="utf-8"))
    if not raw:
        return

    # First pass: group raw records
    from collections import defaultdict
    buckets: dict[tuple, list[dict]] = defaultdict(list)
    for r in raw:
        key = (r.get("dataset_label", ""), r.get("fonte", ""),
               r.get("data_referencia", ""), r.get("indicador", ""))
        buckets[key].append(r)

    pivoted: list[OrderedDict] = []
    all_metrics: set[str] = set()

    for key, recs in buckets.items():
        row = OrderedDict()
        for k in ("data_referencia", "indicador", "fonte", "dataset_label", "categoria"):
            row[k] = recs[0].get(k, "")

        # Determine metric columns for this group
        units = list(OrderedDict.fromkeys(r.get("unidade", "") or "" for r in recs))
        non_empty = [u for u in units if u]

        if len(non_empty) >= 2:
            # Multi-metric group: use unit labels as columns
            for r in recs:
                metric = r.get("unidade", "") or ""
                row[metric] = r.get("valor", "")
                all_metrics.add(metric)
        else:
            # Single-metric group: use "Valor"
            row["Valor"] = recs[0].get("valor", "")
            all_metrics.add("Valor")

        pivoted.append(row)

    pivoted.sort(key=lambda x: (x.get("data_referencia", ""), x.get("indicador", "")))

    section("Escrevendo pivô", "package")

    json_path = DATA_DIR / "consolidated_pivoted.json"
    js_path = DATA_DIR / "consolidated_pivoted.js"

    json_path.write_text(
        json.dumps(pivoted, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print_done(f"consolidated_pivoted.json — {len(pivoted)} registros")

    js_path.write_text(
        f"window.PULSEFLAT_PIVOTED = {json.dumps(pivoted, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    print_done(f"consolidated_pivoted.js — {len(pivoted)} registros")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="📊 Gera dados consolidados (consolidated.json/csv/js) a partir dos CSVs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
exemplos:
  python scripts/consolidate.py
  python scripts/consolidate.py --dry-run
  python scripts/consolidate.py --quiet
        """,
    )
    add_common_args(parser)
    args = parser.parse_args()
    if args.dry_run:
        log.info("Modo dry-run: arquivos não serão salvos.")
    apply_common_args(args)
    generate(dry_run=args.dry_run)
    if not args.dry_run:
        generate_pivoted()
