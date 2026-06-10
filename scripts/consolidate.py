#!/usr/bin/env python
# coding: utf-8
"""
scripts/consolidate.py
-----------------------
Lê todos os CSVs em data/ e gera uma tabela consolidada com o último valor
disponível de cada indicador/série, normalizada em formato plano.

Saídas:
  data/consolidated.csv   — dados consolidados (formato CSV)
  data/consolidated.json  — dados consolidados (formato JSON)
  data/consolidated.js    — fallback offline para a página web

Uso:
    python scripts/consolidate.py
    python scripts/consolidate.py --dry-run
    python scripts/consolidate.py --quiet
"""

import csv
import json
import sys
import time
import argparse
import re
from pathlib import Path
from typing import Optional

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


def _fmt_val(val: str, decimals: int = 4) -> str:
    f = _parse_br_float(val)
    if f is None:
        return val
    return f"{f:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _fmt_pct(val: str, decimals: int = 2) -> str:
    f = _parse_br_float(val)
    if f is None:
        return val
    return f"{f:,.{decimals}f}%".replace(",", "X").replace(".", ",").replace("X", ".")


def _only_digits(s: str) -> str:
    return re.sub(r"\D", "", s)


def _safe(val: str) -> str:
    return (val or "").strip()


# ── Definições dos indicadores ─────────────────────────────────────────

INDICATOR_DEFS = [
    # ── BCB SGS (múltiplas séries) ────────────────────────────────
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
        }
        for codigo, nome in [
            ("11",   "SELIC (% a.d.)"),
            ("12",   "CDI (% a.d.)"),
            ("1",    "IGP-M"),
            ("189",  "IGP-M (índice)"),
            ("190",  "IGP-M 12m"),
            ("191",  "IGP-M acum. ano"),
            ("192",  "IGP-M acum. 3m"),
            ("433",  "IPCA 12m"),
            ("13522", "Dólar comercial (venda)"),
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
        "fmt": "auto",
    },
    # ── ANBIMA IMA Completo ───────────────────────────────────────
    {
        "dataset": "anbima_ima_completo.csv",
        "source": "ANBIMA",
        "indicator_col": "indice",
        "value_cols": [
            ("numero_indice", "Número-índice", "number"),
            ("variacao_diaria", "Variação diária", "pct"),
            ("variacao_mensal", "Variação mensal", "pct"),
            ("variacao_anual", "Variação anual", "pct"),
            ("variacao_ultimos_12_meses", "Variação 12m", "pct"),
            ("duration_du", "Duration (d.u.)", "number"),
            ("yield_", "Yield", "pct"),
        ],
        "date_col": "data_referencia",
    },
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
        "label": "DI Over — Operating Volume",
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
        "unit_col": "base",
        "fmt": "pct",
        "note_col": "prazo_dias",
    },
    # ── B3 Indicadores Financeiros ─────────────────────────────────
    {
        "dataset": "b3_indicadores_financeiros.csv",
        "source": "B3",
        "indicator_col": "description",
        "value_col_main": "value",
        "value_col_fallback": "rate",
        "date_col": "last_update",
        "category_col": "group_description",
        "fmt": "auto",
    },
    # ── B3 Taxa de Câmbio ──────────────────────────────────────────
    {
        "dataset": "b3_taxa_cambio_referencia.csv",
        "source": "B3",
        "indicator_col": "description",
        "value_col_main": "value",
        "value_col_fallback": "rate",
        "date_col": "lastupdate",
        "category_col": "groupdescription",
        "fmt": "number",
    },
    # ── BCB PTAX ───────────────────────────────────────────────────
    {
        "dataset": "bcb_ptax.csv",
        "source": "BCB",
        "label": "PTAX USD — Compra",
        "value_col": "cotacao_compra",
        "date_col": "data_hora_cotacao",
        "fmt": "number",
    },
    {
        "dataset": "bcb_ptax.csv",
        "source": "BCB",
        "label": "PTAX USD — Venda",
        "value_col": "cotacao_venda",
        "date_col": "data_hora_cotacao",
        "fmt": "number",
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
            "fmt": "number",
        }
        for ticker in ["^BVSP", "BRL=X", "GLD", "^TNX", "EWZ"]
    ],
    # ── ANBIMA Títulos Públicos (principais vencimentos) ──────────
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
    },
    # ── ANBIMA IDkA ────────────────────────────────────────────────
    {
        "dataset": "anbima_idka.csv",
        "source": "ANBIMA",
        "indicator_col": "no_indice",
        "value_cols": [
            ("nu_indice", "Número-índice", "number"),
            ("ret_dia_perc", "Retorno diário", "pct"),
            ("ret_mes_perc", "Retorno mensal", "pct"),
            ("taxa_juros_aa_perc_compra_d1", "Taxa compra (% a.a.)", "pct"),
        ],
        "date_col": "dt_referencia",
    },
    # ── ANBIMA IMA-B ───────────────────────────────────────────────
    {
        "dataset": "anbima_indice_imab.csv",
        "source": "ANBIMA",
        "indicator_col": "ndice",
        "value_cols": [
            ("n_mero_ndice", "Número-índice", "number"),
            ("varia_o_di_ria", "Variação diária", "pct"),
            ("duration_d_u", "Duration (d.u.)", "number"),
        ],
        "date_col": "data_de_refer_ncia",
    },
    # ── Debêntures - Emissões (contagem) ───────────────────────────
    {
        "dataset": "debentures_emissoes_caracteristicas.csv",
        "source": "Debêntures",
        "type": "count",
        "label": "Emissões de debêntures",
        "unit": "emissões",
    },
    # ── Debêntures - Mercado Secundário ────────────────────────────
    {
        "dataset": "debentures_mercado_secundario_precos_negociacao.csv",
        "source": "Debêntures",
        "indicator_col": "emissor",
        "value_cols": [
            ("quantidade", "Quantidade negociada", "number"),
            ("n_mero_de_neg_cios", "Número de negócios", "number"),
        ],
        "date_col": "data_captura",
        "fmt": "number",
    },
    # ── B3 ETFs ───────────────────────────────────────────────────
    {
        "dataset": "b3_etfs.csv",
        "source": "B3",
        "type": "count",
        "label": "ETFs listados na B3",
        "unit": "ETFs",
        "category": "Produtos Listados",
    },
    # ── B3 FIIs ────────────────────────────────────────────────────
    {
        "dataset": "b3_fiis.csv",
        "source": "B3",
        "type": "count",
        "label": "FIIs listados na B3",
        "unit": "FIIs",
        "category": "Produtos Listados",
    },
    # ── CVM Companhias Abertas ─────────────────────────────────────
    {
        "dataset": "cvm_cadastro_companhias_abertas.csv",
        "source": "CVM",
        "type": "count",
        "label": "Companhias abertas registradas",
        "unit": "companhias",
        "category": "Cadastro",
    },
    # ── Investing ETFs ─────────────────────────────────────────────
    {
        "dataset": "investing_etf.csv",
        "source": "Investing.com",
        "indicator_col": "ticker",
        "value_cols": [
            ("vr_ultimo", "Último valor", "number"),
            ("vr_variacao_pct", "Variação", "pct"),
            ("qt_volume", "Volume", "number"),
        ],
        "date_col": "data_captura",
    },
    # ── Bacen Balancetes (ativos totais dos maiores bancos) ───────
    {
        "dataset": "bacen_balancetes_bancos.csv",
        "source": "BACEN",
        "type": "count",
        "label": "Instituições financeiras (balancetes)",
        "unit": "instituições",
        "category": "Sistema Financeiro",
    },
    # ── B3 Carteiras Teóricas (contagem por índice) ────────────────
    *[
        {
            "dataset": f"b3_carteira_teorica_{idx}.csv",
            "source": "B3",
            "type": "count",
            "label": f"Ativos na cesta {nome}",
            "unit": "ativos",
            "category": f"Carteiras Teóricas",
        }
        for idx, nome in [
            ("ibov", "IBOV"),
            ("ibxl", "IBrX 50"),
            ("ibsd", "IBSD"),
            ("smll", "SMLL"),
            ("ifnc", "IFNC"),
            ("isee", "ISEE"),
            ("bdrx", "BDRX"),
            ("agfs_iagro", "IAGRO"),
        ]
    ],
    # ── Bacen Conglomerados ────────────────────────────────────────
    {
        "dataset": "bacen_conglomerados.csv",
        "source": "BACEN",
        "type": "count",
        "label": "Conglomerados financeiros",
        "unit": "conglomerados",
        "category": "Sistema Financeiro",
    },
    # ── ONU Pacto Global ───────────────────────────────────────────
    {
        "dataset": "onu_pacto_global.csv",
        "source": "ONU",
        "type": "count",
        "label": "Empresas signatárias do Pacto Global",
        "unit": "empresas",
        "category": "ESG",
    },
    # ── B3 Classificação Setorial ─────────────────────────────────
    {
        "dataset": "b3_classificacao_setorial.csv",
        "source": "B3",
        "type": "count",
        "label": "Empresas classificadas por setor",
        "unit": "empresas",
        "category": "Classificação",
    },
]


# ── Extratores ────────────────────────────────────────────────────────

def _extract_single_value(
    rows: list[dict], idef: dict
) -> Optional[dict]:
    """Extrai o último valor de uma série temporal simples."""
    value_col = idef["value_col"]
    date_col = idef["date_col"]
    fmt = idef.get("fmt", "auto")

    rows_sorted = _sorted_by(rows, date_col)
    if not rows_sorted:
        return None

    latest = rows_sorted[0]
    raw_val = _safe(latest.get(value_col, ""))
    ref_date = (_safe(latest.get(date_col, "")) or "")[:10]
    capture = _safe(latest.get("data_captura", ""))[:10]

    if not raw_val:
        return None

    if fmt == "pct":
        formatted = _fmt_pct(raw_val)
    elif fmt == "number":
        formatted = _fmt_val(raw_val)
    else:
        f = _parse_br_float(raw_val)
        if f is not None:
            formatted = _fmt_val(raw_val)
        else:
            formatted = raw_val

    return {
        "dataset": idef["dataset"],
        "fonte": idef["source"],
        "categoria": idef.get("category", idef.get("category_col", "")),
        "indicador": idef.get("label", ""),
        "valor": formatted,
        "unidade": idef.get("unit", ""),
        "data_referencia": ref_date,
        "captura_em": capture,
        "metrica": value_col,
    }


def _extract_grouped_value(
    rows: list[dict], idef: dict
) -> list[dict]:
    """Agrupa por indicator_col e extrai último valor de cada grupo."""
    indicator_col = idef["indicator_col"]
    value_col = idef["value_col"]
    date_col = idef["date_col"]
    fmt = idef.get("fmt", "auto")

    groups: dict[str, list[dict]] = {}
    for r in rows:
        key = _safe(r.get(indicator_col, ""))
        if key:
            groups.setdefault(key, []).append(r)

    results = []
    for indicator_name, grp in sorted(groups.items()):
        grp_sorted = _sorted_by(grp, date_col)
        if not grp_sorted:
            continue
        latest = grp_sorted[0]
        raw_val = _safe(latest.get(value_col, ""))
        ref_date = (_safe(latest.get(date_col, "")) or "")[:10]
        capture = _safe(latest.get("data_captura", ""))[:10]
        category = _safe(latest.get(idef.get("category_col", ""), "")) if idef.get("category_col") else ""
        unit = _safe(latest.get(idef.get("unit_col", ""), "")) if idef.get("unit_col") else ""

        if not raw_val:
            continue

        if fmt == "pct":
            formatted = _fmt_pct(raw_val)
        elif fmt == "number":
            formatted = _fmt_val(raw_val)
        else:
            f = _parse_br_float(raw_val)
            if f is not None:
                formatted = _fmt_val(raw_val)
            else:
                formatted = raw_val

        results.append({
            "dataset": idef["dataset"],
            "fonte": idef["source"],
            "categoria": category or idef.get("category", ""),
            "indicador": indicator_name,
            "valor": formatted,
            "unidade": unit or idef.get("unit", ""),
            "data_referencia": ref_date,
            "captura_em": capture,
            "metrica": value_col,
        })
    return results


def _extract_filtered_value(
    rows: list[dict], idef: dict
) -> Optional[dict]:
    """Filtra por filter_col == filter_val e extrai último valor."""
    filter_col = idef["filter_col"]
    filter_val = idef["filter_val"]
    filtered = [r for r in rows if _safe(r.get(filter_col, "")) == filter_val]
    if not filtered:
        return None
    return _extract_single_value(filtered, idef)


def _extract_multi_value(
    rows: list[dict], idef: dict
) -> list[dict]:
    """Extrai múltiplas métricas (value_cols) por indicador."""
    indicator_col = idef.get("indicator_col", "")
    date_col = idef["date_col"]
    value_cols = idef["value_cols"]

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
        grp_sorted = _sorted_by(grp, date_col)
        if not grp_sorted:
            continue
        latest = grp_sorted[0]
        ref_date = (_safe(latest.get(date_col, "")) or "")[:10]
        capture = _safe(latest.get("data_captura", ""))[:10]
        note = _safe(latest.get(idef.get("note_col", ""), "")) if idef.get("note_col") else ""

        label_base = indicator_name or idef.get("label", idef["dataset"])
        if note and indicator_name:
            label_base = f"{indicator_name} ({note})"

        for col_name, col_label, col_fmt in value_cols:
            raw_val = _safe(latest.get(col_name, ""))
            if not raw_val:
                continue
            if col_fmt == "pct":
                formatted = _fmt_pct(raw_val)
            else:
                formatted = _fmt_val(raw_val)

            results.append({
                "dataset": idef["dataset"],
                "fonte": idef["source"],
                "categoria": idef.get("category", ""),
                "indicador": label_base,
                "valor": formatted,
                "unidade": col_label,
                "data_referencia": ref_date,
                "captura_em": capture,
                "metrica": col_name,
            })
    return results


def _extract_dual_value(
    rows: list[dict], idef: dict
) -> list[dict]:
    """Extrai valor de value_col_main com fallback para value_col_fallback."""
    indicator_col = idef.get("indicator_col", "")
    date_col = idef["date_col"]
    main_col = idef["value_col_main"]
    fallback_col = idef["value_col_fallback"]
    fmt = idef.get("fmt", "auto")
    category_col = idef.get("category_col", "")

    groups: dict[str, list[dict]] = {}
    for r in rows:
        key = _safe(r.get(indicator_col, ""))
        if key:
            groups.setdefault(key, []).append(r)

    results = []
    for indicator_name, grp in groups.items():
        grp_sorted = _sorted_by(grp, date_col)
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
        ref_date = (_safe(latest.get(date_col, "")) or "")[:10]
        capture = _safe(latest.get("data_captura", ""))[:10]
        category = _safe(latest.get(category_col, "")) if category_col else ""

        if fmt == "pct":
            formatted = _fmt_pct(raw_val)
        elif fmt == "number":
            formatted = _fmt_val(raw_val)
        else:
            f = _parse_br_float(raw_val)
            if f is not None:
                formatted = _fmt_val(raw_val)
            else:
                formatted = raw_val

        results.append({
            "dataset": idef["dataset"],
            "fonte": idef["source"],
            "categoria": category or idef.get("category", ""),
            "indicador": indicator_name,
            "valor": formatted,
            "unidade": "",
            "data_referencia": ref_date,
            "captura_em": capture,
            "metrica": used_col,
        })
    return results


def _extract_count(
    rows: list[dict], idef: dict
) -> Optional[dict]:
    """Conta o número de registros únicos."""
    rows = _sorted_by(rows, "data_captura")
    if not rows:
        return None
    latest = rows[0]
    capture = _safe(latest.get("data_captura", ""))[:10]

    return {
        "dataset": idef["dataset"],
        "fonte": idef["source"],
        "categoria": idef.get("category", ""),
        "indicador": idef.get("label", idef["dataset"]),
        "valor": str(len(rows)),
        "unidade": idef.get("unit", "registros"),
        "data_referencia": capture,
        "captura_em": capture,
        "metrica": "count",
    }


# ── Gerador principal ─────────────────────────────────────────────────

def generate(dry_run: bool = False) -> None:
    t0 = time.time()
    banner("Consolidado", "Extrai último valor de cada indicador → consolidated.json/csv")
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

        kind = idef.get("type", "time_series")

        if kind == "count":
            result = _extract_count(rows, idef)
            if result:
                all_results.append(result)
                print_done(f"{label} → {result['valor']} {result['unidade']}")
            else:
                print_warn(f"{label}: sem dados")

        elif "value_cols" in idef:
            results = _extract_multi_value(rows, idef)
            all_results.extend(results)
            print_done(f"{label} → {len(results)} métricas")

        elif "filter_col" in idef:
            result = _extract_filtered_value(rows, idef)
            if result:
                all_results.append(result)
                print_done(f"{label} → {result['valor']} ({result['data_referencia']})")
            else:
                print_warn(f"{label}: sem dados para filtro")

        elif "indicator_col" in idef and "value_col_main" in idef:
            results = _extract_dual_value(rows, idef)
            all_results.extend(results)
            print_done(f"{label} → {len(results)} indicadores")

        elif "indicator_col" in idef:
            results = _extract_grouped_value(rows, idef)
            all_results.extend(results)
            print_done(f"{label} → {len(results)} indicadores")

        else:
            result = _extract_single_value(rows, idef)
            if result:
                all_results.append(result)
                print_done(f"{label} → {result['valor']} ({result['data_referencia']})")
            else:
                print_warn(f"{label}: sem dados")

    if not all_results:
        print_warn("Nenhum dado consolidado extraído.")
        return

    # Ordena por fonte, depois dataset, depois indicador
    all_results.sort(key=lambda r: (r["fonte"], r["dataset"], r["indicador"]))

    if not dry_run:
        section("Escrevendo saída", "package")

        json_path = DATA_DIR / "consolidated.json"
        csv_path = DATA_DIR / "consolidated.csv"
        js_path = DATA_DIR / "consolidated.js"

        json_path.parent.mkdir(parents=True, exist_ok=True)

        # JSON
        json_path.write_text(
            json.dumps(all_results, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print_done(f"consolidated.json — {len(all_results)} registros")

        # JS fallback
        js_path.write_text(
            f"window.PULSEFLAT_CONSOLIDATED = {json.dumps(all_results, indent=2, ensure_ascii=False)};\n",
            encoding="utf-8",
        )
        print_done(f"consolidated.js — {len(all_results)} registros")

        # CSV
        fieldnames = [
            "dataset", "fonte", "categoria", "indicador",
            "valor", "unidade", "data_referencia", "captura_em", "metrica",
        ]
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        print_done(f"consolidated.csv — {len(all_results)} registros")

    else:
        print_info(f"Dry-run: {len(all_results)} registros seriam gerados.")

    elapsed = time.time() - t0

    # Estatísticas
    total_sources = len({r["fonte"] for r in all_results})
    total_datasets = len({r["dataset"] for r in all_results})

    print_summary(
        "Consolidado gerado",
        total=total,
        success=len(all_results),
        failed=max(0, total - len(all_results)),
        elapsed=elapsed,
        details=[
            ("chart", "Registros consolidados", str(len(all_results))),
            ("folder", "Datasets processados", str(total_datasets)),
            ("info", "Fontes", str(total_sources)),
        ],
    )


# ── CLI ───────────────────────────────────────────────────────────────

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
