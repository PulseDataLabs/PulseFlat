#!/usr/bin/env python
# coding: utf-8
"""
PulseFlat – Orquestrador de scrapers

Uso:
  python run_all.py                        # executa todos os scrapers habilitados
  python run_all.py --group anbima         # apenas o grupo anbima
  python run_all.py --group b3             # apenas o grupo b3
  python run_all.py --group bcb            # apenas o grupo bcb
  python run_all.py --group cvm            # apenas o grupo cvm
  python run_all.py --group ibge           # apenas o grupo ibge
  python run_all.py --group ratings        # apenas o grupo ratings
  python run_all.py --group misc           # apenas o grupo misc
  python run_all.py --scraper anbima_idka  # apenas um scraper específico
  python run_all.py --sequential           # execução sequencial (debug)
  python run_all.py --parallel --max-workers 8
  python run_all.py --generate-catalog     # só regenera datasets.json
"""

import argparse
import importlib
import json
import logging
import sys
import traceback
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── Logger minimalista ────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("run_all")

# Silencia loggers de libs ruidosas no nível raiz
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)


# ── UX compartilhada (cores, ícones, helpers visuais) ────────────────
from scripts.utils.ux import (
    USE_COLOR, IS_TTY,
    bold, dim, green, yellow, red, cyan, blue, magenta, white,
    b_green, b_yellow, b_red, b_cyan, b_white,
    _line, _progress_bar,
    GROUP_ICON, GROUP_COLOR,
)


# ── Helpers visuais ───────────────────────────────────────────────────────────

def _banner() -> None:
    """Imprime o cabeçalho do pipeline."""
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    print()
    print(_line("═"))
    print(
        bold(white("  ⚡ PulseFlat")) +
        dim("  Pipeline Serverless de Dados Financeiros Brasileiros")
    )
    print(dim(f"  {now}"))
    print(_line("═"))
    print()


def _section(title: str, icon: str = "▶") -> None:
    print()
    print(_line())
    print(f"  {icon}  {bold(title)}")
    print(_line())


def _scraper_start(name: str, group: str, idx: int, total: int) -> None:
    icon  = GROUP_ICON.get(group, "⬜")
    color = GROUP_COLOR.get(group, dim)
    pct   = f"{idx}/{total}"
    print(
        f"  {dim(pct.rjust(7))}  {icon}  "
        + color(f"{name:<40}")
        + dim("iniciando…")
    )


def _scraper_done(name: str, group: str, elapsed: float, idx: int, total: int) -> None:
    icon  = GROUP_ICON.get(group, "⬜")
    color = GROUP_COLOR.get(group, dim)
    pct   = f"{idx}/{total}"
    t     = f"{elapsed:6.1f}s"
    print(
        f"  {dim(pct.rjust(7))}  {icon}  "
        + color(f"{name:<40}")
        + b_green("  ✔  ") + dim(t)
    )


def _scraper_fail(name: str, group: str, elapsed: float, idx: int, total: int) -> None:
    icon  = GROUP_ICON.get(group, "⬜")
    pct   = f"{idx}/{total}"
    t     = f"{elapsed:6.1f}s"
    print(
        f"  {dim(pct.rjust(7))}  {icon}  "
        + b_red(f"{name:<40}")
        + b_red("  ✖  ") + dim(t)
    )


def _summary_table(
    results: dict[str, tuple[bool, float, Optional[str]]],
    registry: dict[str, dict],
    total_elapsed: float,
) -> None:
    """Imprime a tabela final de resultados."""
    ok   = [(n, r) for n, r in results.items() if r[0]]
    fail = [(n, r) for n, r in results.items() if not r[0]]

    print()
    print(_line("═"))
    print(f"  {bold('RESUMO FINAL')}")
    print(_line("─"))

    # Linha de totais
    total = len(results)
    print(
        f"  {bold('Total')}: {white(str(total))} scrapers  │  "
        + b_green(f"✔ {len(ok)} ok") + "  │  "
        + (b_red(f"✖ {len(fail)} erro(s)") if fail else dim("0 erros"))
        + "  │  "
        + cyan(f"⏱  {total_elapsed:.1f}s")
    )

    if ok:
        print()
        print(dim("  ── Sucesso " + "─" * 57))
        for name, (_, elapsed, _) in sorted(ok, key=lambda x: -x[1][1]):
            group = registry.get(name, {}).get("group", "misc")
            icon  = GROUP_ICON.get(group, "⬜")
            color = GROUP_COLOR.get(group, dim)
            print(
                f"    {icon}  {color(name):<50}"
                + b_green("✔") + dim(f"  {elapsed:5.1f}s")
            )

    if fail:
        print()
        print(dim("  ── Erros " + "─" * 59))
        for name, (_, elapsed, err) in fail:
            group = registry.get(name, {}).get("group", "misc")
            icon  = GROUP_ICON.get(group, "⬜")
            print(
                f"    {icon}  {b_red(name):<50}"
                + b_red("✖") + dim(f"  {elapsed:5.1f}s")
            )
            if err:
                # Mostra apenas a última linha do traceback
                last_line = [l for l in err.strip().splitlines() if l.strip()]
                hint = last_line[-1].strip() if last_line else ""
                if hint:
                    print(f"         {dim('↳')} {red(hint)}")

    print(_line("═"))
    print()


# ── Descoberta dinâmica ───────────────────────────────────────────────────────

def discover_scrapers() -> dict[str, dict]:
    """
    Varre scrapers/ e retorna metadados de cada scraper descoberto.
    { module_name: { group, enabled, phase, title, class_name } }
    """
    scrapers: dict[str, dict] = {}
    scrapers_dir = Path(__file__).resolve().parent / "scrapers"

    for file_path in sorted(scrapers_dir.glob("*.py")):
        module_name = file_path.stem
        if module_name in ("__init__", "generic_scraper"):
            continue
        try:
            mod        = importlib.import_module(f"scrapers.{module_name}")
            class_name = "".join(w.capitalize() for w in module_name.split("_")) + "Scraper"
            if hasattr(mod, class_name):
                cls = getattr(mod, class_name)
                scrapers[module_name] = {
                    "group":      getattr(cls, "group",   "misc"),
                    "enabled":    getattr(cls, "enabled", True),
                    "phase":      getattr(cls, "phase",   1),
                    "class_name": class_name,
                    "title":      getattr(cls, "title", module_name.replace("_", " ").title()),
                }
        except Exception as e:
            logger.warning(yellow(f"  ⚠  Não foi possível carregar metadados de {module_name}: {e}"))

    return scrapers


# ── Execução individual ───────────────────────────────────────────────────────

def run_scraper(module_name: str) -> tuple[bool, float, Optional[str]]:
    """Executa um scraper. Retorna (success, elapsed_s, error_msg_or_None)."""
    t0 = time.time()
    try:
        mod        = importlib.import_module(f"scrapers.{module_name}")
        class_name = "".join(w.capitalize() for w in module_name.split("_")) + "Scraper"
        if hasattr(mod, class_name):
            getattr(mod, class_name)().run()
        elif hasattr(mod, "main"):
            mod.main()
        else:
            msg = f"Módulo {module_name} não possui classe {class_name} nem função main()."
            return False, time.time() - t0, msg
        return True, time.time() - t0, None
    except Exception:
        return False, time.time() - t0, traceback.format_exc()


# ── Execução de subconjuntos (paralelo / sequencial) ──────────────────────────

def run_subset(
    names: list[str],
    registry: dict[str, dict],
    parallel: bool,
    max_workers: int,
    phase_label: str,
) -> dict[str, tuple[bool, float, Optional[str]]]:
    results: dict[str, tuple[bool, float, Optional[str]]] = {}
    if not names:
        return results

    total = len(names)
    _section(f"Fase {phase_label} — {total} scraper{'s' if total > 1 else ''}", "⚙")

    if parallel:
        print(f"  {dim('Modo')} {cyan('paralelo')}  {dim(f'max_workers={max_workers}')}\n")
        done_count = 0
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            future_map = {ex.submit(run_scraper, n): n for n in names}
            for future in as_completed(future_map):
                name = future_map[future]
                group = registry.get(name, {}).get("group", "misc")
                done_count += 1
                try:
                    success, elapsed, err = future.result()
                except Exception:
                    success, elapsed, err = False, 0.0, traceback.format_exc()

                if success:
                    _scraper_done(name, group, elapsed, done_count, total)
                else:
                    _scraper_fail(name, group, elapsed, done_count, total)

                results[name] = (success, elapsed, err)
                # Barra de progresso inline
                print(f"  {_progress_bar(done_count, total)}", end="\r" if done_count < total else "\n")
    else:
        print(f"  {dim('Modo')} {yellow('sequencial')}\n")
        for idx, name in enumerate(names, 1):
            group = registry.get(name, {}).get("group", "misc")
            _scraper_start(name, group, idx, total)
            success, elapsed, err = run_scraper(name)
            # Sobe uma linha e reescreve com resultado
            print("\033[1A\033[2K", end="") if USE_COLOR else None
            if success:
                _scraper_done(name, group, elapsed, idx, total)
            else:
                _scraper_fail(name, group, elapsed, idx, total)
            results[name] = (success, elapsed, err)
            print(f"  {_progress_bar(idx, total)}", end="\r" if idx < total else "\n")

    return results


# ── Salvamento de status ──────────────────────────────────────────────────────

def save_pipeline_status(
    results: dict[str, tuple[bool, float, Optional[str]]],
    total_elapsed: float,
) -> None:
    from utils.base import DRIFTS

    root_dir        = Path(__file__).resolve().parent
    status_path     = root_dir / "data" / "pipeline_status.json"
    status_js_path  = root_dir / "data" / "pipeline_status.js"
    scrapers_registry = discover_scrapers()
    active_scrapers   = {k: v for k, v in scrapers_registry.items() if v["enabled"]}

    status_data: dict = {
        "timestamp":       datetime.now().isoformat(),
        "elapsed_seconds": total_elapsed,
        "status":          "success",
        "summary":         {"total": 0, "success": 0, "failed": 0, "drifts": 0},
        "scrapers":        {},
        "drifts":          {},
    }

    # Carrega status anterior (para preservar scrapers não executados nesta rodada)
    if status_path.exists():
        try:
            with status_path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded.get("scrapers"), dict):
                status_data["scrapers"] = loaded["scrapers"]
            if isinstance(loaded.get("drifts"), dict):
                status_data["drifts"] = loaded["drifts"]
        except Exception as e:
            logger.warning(yellow(f"  ⚠  Não foi possível carregar status anterior: {e}"))

    # Atualiza com resultados desta execução
    now_iso = datetime.now().isoformat()
    for name, (success, elapsed, err) in results.items():
        status_data["scrapers"][name] = {
            "status":          "success" if success else "error",
            "elapsed_seconds": elapsed,
            "error":           err,
            "timestamp":       now_iso,
        }

    # Drifts: limpa os de scrapers que rodaram agora e adiciona os novos
    processed_files = {f"{n}.csv" for n in results}
    for filename in list(status_data["drifts"].keys()):
        if filename in processed_files:
            del status_data["drifts"][filename]
    for d in DRIFTS:
        status_data["drifts"][d["file"]] = {
            "added":     d["added"],
            "removed":   d["removed"],
            "timestamp": d["timestamp"],
        }

    # Preenche scrapers nunca executados
    for name in active_scrapers:
        if name not in status_data["scrapers"]:
            status_data["scrapers"][name] = {
                "status": "unknown", "elapsed_seconds": 0.0,
                "error": None, "timestamp": None,
            }

    # Recalcula resumo
    ok_cnt = sum(1 for s in status_data["scrapers"].values() if s["status"] == "success")
    fail_cnt = sum(1 for s in status_data["scrapers"].values() if s["status"] == "error")
    status_data["summary"] = {
        "total":   len(active_scrapers),
        "success": ok_cnt,
        "failed":  fail_cnt,
        "drifts":  len(status_data["drifts"]),
    }
    status_data["status"] = (
        "error"   if fail_cnt > 0 else
        "warning" if status_data["drifts"] else
        "success"
    )

    try:
        status_path.parent.mkdir(parents=True, exist_ok=True)
        with status_path.open("w", encoding="utf-8") as f:
            json.dump(status_data, f, indent=2, ensure_ascii=False)
        with status_js_path.open("w", encoding="utf-8") as f:
            f.write(
                f"window.PULSEFLAT_PIPELINE_STATUS = "
                f"{json.dumps(status_data, indent=2, ensure_ascii=False)};\n"
            )
        print(f"  {dim('📄 pipeline_status.json atualizado')}")
    except Exception as e:
        logger.error(red(f"  ✖  Erro ao salvar status do pipeline: {e}"))


# ── Listagem de scrapers disponíveis ──────────────────────────────────────────

def list_scrapers(registry: dict[str, dict]) -> None:
    _section("Scrapers disponíveis", "📋")
    by_group: dict[str, list] = {}
    for name, info in sorted(registry.items()):
        by_group.setdefault(info["group"], []).append((name, info))

    for group, items in sorted(by_group.items()):
        icon  = GROUP_ICON.get(group, "⬜")
        color = GROUP_COLOR.get(group, dim)
        print(f"\n  {icon}  {bold(color(group.upper()))}")
        for name, info in items:
            enabled_marker = green("●") if info["enabled"] else dim("○")
            phase_tag      = dim(f"[ph{info['phase']}]")
            print(
                f"    {enabled_marker}  {color(name):<42} "
                + phase_tag + "  " + dim(info.get("title", ""))
            )
    print()


# ── Orquestrador principal ────────────────────────────────────────────────────

def main(
    group:       Optional[str] = None,
    scraper:     Optional[str] = None,
    parallel:    bool = True,
    max_workers: int  = 4,
    list_only:   bool = False,
) -> None:
    _banner()
    t0       = time.time()
    registry = discover_scrapers()

    if list_only:
        list_scrapers(registry)
        return

    # Filtra alvos
    if scraper:
        if scraper not in registry:
            print(b_red(f"  ✖  Scraper '{scraper}' não encontrado."))
            sys.exit(1)
        targets = {scraper: registry[scraper]}
    else:
        targets = {
            n: info for n, info in registry.items()
            if info["enabled"] and (group is None or info["group"] == group)
        }

    if not targets:
        msg = f"grupo='{group}'" if group else "critério informado"
        print(b_red(f"  ✖  Nenhum scraper encontrado para {msg}."))
        sys.exit(1)

    # Mostra plano de execução
    phase1 = [n for n, i in targets.items() if i["phase"] == 1]
    phase2 = [n for n, i in targets.items() if i["phase"] == 2]
    mode_label = cyan("paralelo") if parallel else yellow("sequencial")
    print(
        f"  {bold('Plano')}: "
        + dim(f"{len(targets)} scrapers  │  ")
        + dim(f"fase 1: {len(phase1)}  │  fase 2: {len(phase2)}  │  ")
        + f"modo: {mode_label}  │  "
        + dim(f"workers: {max_workers}")
    )

    # Agrupa por grupo para dar uma visão rápida
    group_counts: dict[str, int] = {}
    for info in targets.values():
        group_counts[info["group"]] = group_counts.get(info["group"], 0) + 1
    group_summary = "  ".join(
        f"{GROUP_ICON.get(g,'⬜')} {GROUP_COLOR.get(g, dim)(g)}:{n}"
        for g, n in sorted(group_counts.items())
    )
    print(f"  {group_summary}")

    results: dict[str, tuple[bool, float, Optional[str]]] = {}

    if phase1:
        results.update(run_subset(phase1, registry, parallel, max_workers, "1"))
    if phase2:
        results.update(run_subset(phase2, registry, parallel, max_workers, "2"))

    total_elapsed = time.time() - t0

    # Persiste status
    _section("Pós-processamento", "💾")
    save_pipeline_status(results, total_elapsed)

    # Regenera catálogo se rodou tudo
    if not group and not scraper:
        try:
            from scripts.generate_catalog import generate
            generate()
            print(f"  {dim('📦 datasets.json regenerado')}")
        except Exception as e:
            print(yellow(f"  ⚠  Não foi possível regenerar o catálogo: {e}"))

    # Tabela resumo final
    _summary_table(results, registry, total_elapsed)

    # Exit code
    if any(not r[0] for r in results.values()):
        sys.exit(1)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    registry = discover_scrapers()
    available_groups   = sorted({i["group"] for i in registry.values() if i["enabled"]})
    available_scrapers = sorted(registry.keys())

    parser = argparse.ArgumentParser(
        description="⚡ PulseFlat – Orquestrador de scrapers de dados financeiros brasileiros",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
exemplos:
  python run_all.py
  python run_all.py --group b3
  python run_all.py --scraper bcb_ptax
  python run_all.py --sequential
  python run_all.py --parallel --max-workers 8
  python run_all.py --list
  python run_all.py --generate-catalog
        """,
    )

    parser.add_argument("--group",    choices=available_groups,   metavar="GRUPO",   help="Filtra por grupo de scrapers")
    parser.add_argument("--scraper",  choices=available_scrapers, metavar="SCRAPER", help="Executa um scraper específico")
    parser.add_argument("--parallel",    action="store_true",  default=True,  help="Execução paralela (padrão)")
    parser.add_argument("--sequential",  action="store_false", dest="parallel", help="Execução sequencial")
    parser.add_argument("--max-workers", type=int, default=4,  metavar="N",   help="Threads para modo paralelo (padrão: 4)")
    parser.add_argument("--list",        action="store_true",                 help="Lista todos os scrapers disponíveis e sai")
    parser.add_argument("--generate-catalog", action="store_true",            help="Regenera datasets.json e sai")

    args = parser.parse_args()

    if args.generate_catalog:
        _banner()
        _section("Gerando catálogo de datasets", "📦")
        from scripts.generate_catalog import generate
        generate()
        print(b_green("\n  ✔  datasets.json atualizado com sucesso.\n"))
        sys.exit(0)

    main(
        group=args.group,
        scraper=args.scraper,
        parallel=args.parallel,
        max_workers=args.max_workers,
        list_only=args.list,
    )
