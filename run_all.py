#!/usr/bin/env python
# coding: utf-8
"""
PulseFlat – Orquestrador de scrapers
Uso:
    python run_all.py                        # executa todos os scrapers
    python run_all.py --group anbima         # apenas o grupo anbima
    python run_all.py --group b3             # apenas o grupo b3
    python run_all.py --group bcb            # apenas o grupo bcb
    python run_all.py --group cvm            # apenas o grupo cvm
    python run_all.py --group ibge           # apenas o grupo ibge
    python run_all.py --group ratings        # apenas o grupo ratings (S&P, Moody's)
    python run_all.py --group misc           # Yahoo Finance, Investing, B3 séries
    python run_all.py --scraper anbima_idka  # apenas um scraper específico
"""
import argparse
import importlib
import logging
import sys
import traceback
import time
from datetime import datetime
from pathlib import Path
import json
from typing import Optional
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("run_all")


def discover_scrapers() -> dict[str, dict]:
    """
    Varre o diretório scrapers/ e descobre dinamicamente os scrapers registrados.
    Retorna um dicionário: { "nome_do_modulo": { "group": ..., "enabled": ..., "phase": ..., "title": ... } }
    """
    scrapers = {}
    scrapers_dir = Path(__file__).resolve().parent / "scrapers"
    
    for file_path in scrapers_dir.glob("*.py"):
        module_name = file_path.stem
        if module_name in ("__init__", "generic_scraper"):
            continue
            
        try:
            mod = importlib.import_module(f"scrapers.{module_name}")
            class_name = "".join(word.capitalize() for word in module_name.split("_")) + "Scraper"
            
            if hasattr(mod, class_name):
                cls = getattr(mod, class_name)
                group = getattr(cls, "group", "misc")
                enabled = getattr(cls, "enabled", True)
                phase = getattr(cls, "phase", 1)
                
                scrapers[module_name] = {
                    "group": group,
                    "enabled": enabled,
                    "phase": phase,
                    "class_name": class_name,
                    "title": getattr(cls, "title", module_name.replace("_", " ").title())
                }
        except Exception as e:
            logger.warning(f"Erro ao carregar metadados do scraper {module_name}: {e}")
            
    return scrapers


def run_scraper(module_name: str) -> tuple[bool, float, Optional[str]]:
    """Importa e executa um scraper pelo nome do módulo. Retorna (success, elapsed_seconds, error_msg)."""
    start_time = time.time()
    try:
        logger.info(f"▶  Iniciando: {module_name}")
        mod = importlib.import_module(f"scrapers.{module_name}")
        class_name = "".join(word.capitalize() for word in module_name.split("_")) + "Scraper"
        if hasattr(mod, class_name):
            scraper = getattr(mod, class_name)()
            scraper.run()
        elif hasattr(mod, "main"):
            mod.main()
        else:
            msg = f"Módulo {module_name} não tem classe {class_name} nem função main()."
            logger.error(f"   {msg}")
            return False, time.time() - start_time, msg
        
        elapsed = time.time() - start_time
        logger.info(f"✔  Concluído: {module_name} ({elapsed:.2f}s)")
        return True, elapsed, None
    except Exception:
        tb = traceback.format_exc()
        elapsed = time.time() - start_time
        logger.error(f"✖  Erro em {module_name}:\n{tb}")
        return False, elapsed, tb


def run_scrapers_subset(subset: list[str], parallel: bool, max_workers: int) -> dict[str, tuple[bool, float, Optional[str]]]:
    results = {}
    if not subset:
        return results

    if parallel:
        logger.info(f"Executando {len(subset)} scrapers em paralelo (max_workers={max_workers})...")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_name = {executor.submit(run_scraper, name): name for name in subset}
            for future in concurrent.futures.as_completed(future_to_name):
                name = future_to_name[future]
                try:
                    success, elapsed, err = future.result()
                    results[name] = (success, elapsed, err)
                except Exception as e:
                    tb = traceback.format_exc()
                    logger.error(f"Erro catastrófico ao submeter {name}: {e}\n{tb}")
                    results[name] = (False, 0.0, tb)
    else:
        logger.info(f"Executando {len(subset)} scrapers sequencialmente...")
        for name in subset:
            success, elapsed, err = run_scraper(name)
            results[name] = (success, elapsed, err)
            
    return results


def save_pipeline_status(results: dict[str, tuple[bool, float, Optional[str]]], total_elapsed: float) -> None:
    from utils.base import DRIFTS
    from datetime import datetime
    import json
    from pathlib import Path
    
    root_dir = Path(__file__).resolve().parent
    status_path = root_dir / "data" / "pipeline_status.json"
    status_js_path = root_dir / "data" / "pipeline_status.js"
    
    scrapers_registry = discover_scrapers()
    active_scrapers = {k: v for k, v in scrapers_registry.items() if v["enabled"]}
    
    # Inicializa ou carrega o status existente
    status_data = {
        "timestamp": datetime.now().isoformat(),
        "elapsed_seconds": total_elapsed,
        "status": "success",
        "summary": {
            "total": len(active_scrapers),
            "success": 0,
            "failed": 0,
            "drifts": 0
        },
        "scrapers": {},
        "drifts": {}
    }
    
    if status_path.exists():
        try:
            with status_path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    if isinstance(loaded.get("scrapers"), dict):
                        status_data["scrapers"] = loaded["scrapers"]
                    if isinstance(loaded.get("drifts"), dict):
                        status_data["drifts"] = loaded["drifts"]
        except Exception as e:
            logger.warning(f"Não foi possível carregar pipeline_status.json existente: {e}")

    # Atualiza com os resultados desta execução
    for name, (success, elapsed, err) in results.items():
        status_data["scrapers"][name] = {
            "status": "success" if success else "error",
            "elapsed_seconds": elapsed,
            "error": err,
            "timestamp": datetime.now().isoformat()
        }

    # Atualiza com os drifts desta execução (limpando drifts antigos para scrapers que rodaram nesta execução)
    processed_files = {f"{name}.csv" for name in results.keys()}
    for filename in list(status_data["drifts"].keys()):
        if filename in processed_files:
            del status_data["drifts"][filename]

    for d in DRIFTS:
        filename = d["file"]
        status_data["drifts"][filename] = {
            "added": d["added"],
            "removed": d["removed"],
            "timestamp": d["timestamp"]
        }

    # Recalcula o resumo
    success_count = 0
    failed_count = 0
    
    # Preenche scrapers que ainda não rodaram se não estiverem no JSON
    for name in active_scrapers:
        if name not in status_data["scrapers"]:
            status_data["scrapers"][name] = {
                "status": "unknown",
                "elapsed_seconds": 0.0,
                "error": None,
                "timestamp": None
            }
        
        stat = status_data["scrapers"][name]["status"]
        if stat == "success":
            success_count += 1
        elif stat == "error":
            failed_count += 1

    status_data["summary"]["total"] = len(active_scrapers)
    status_data["summary"]["success"] = success_count
    status_data["summary"]["failed"] = failed_count
    status_data["summary"]["drifts"] = len(status_data["drifts"])
    
    # Determina o status geral do pipeline
    if failed_count > 0:
        status_data["status"] = "error"
    elif len(status_data["drifts"]) > 0:
        status_data["status"] = "warning"
    else:
        status_data["status"] = "success"
        
    # Salva JSON
    try:
        status_path.parent.mkdir(parents=True, exist_ok=True)
        with status_path.open("w", encoding="utf-8") as f:
            json.dump(status_data, f, indent=2, ensure_ascii=False)
            
        # Salva JS
        with status_js_path.open("w", encoding="utf-8") as f:
            f.write(f"window.PULSEFLAT_PIPELINE_STATUS = {json.dumps(status_data, indent=2, ensure_ascii=False)};\n")
            
        logger.info(f"Relatório de status do pipeline salvo com sucesso em data/pipeline_status.json e .js")
    except Exception as e:
        logger.error(f"Erro ao salvar relatório de status do pipeline: {e}")


def main(group: Optional[str] = None, scraper: Optional[str] = None, parallel: bool = True, max_workers: int = 4) -> None:
    start_time = time.time()
    
    scrapers_registry = discover_scrapers()
    
    if scraper:
        if scraper not in scrapers_registry:
            logger.error(f"Scraper '{scraper}' não encontrado no registro.")
            sys.exit(1)
        targets = {scraper: scrapers_registry[scraper]}
    else:
        # Executa apenas os habilitados se rodar tudo ou por grupo
        targets = {
            name: info for name, info in scrapers_registry.items()
            if info["enabled"] and (group is None or info["group"] == group)
        }
        
    if not targets:
        logger.error(
            f"Nenhum scraper selecionado. Grupo '{group}' ou Scraper '{scraper}' inválido ou desabilitado."
        )
        sys.exit(1)

    # Separação por Fases de Dependência dinamicamente
    phase1_targets = [name for name, info in targets.items() if info["phase"] == 1]
    phase2_targets = [name for name, info in targets.items() if info["phase"] == 2]

    results: dict[str, tuple[bool, float, Optional[str]]] = {}

    # Executa Fase 1
    if phase1_targets:
        logger.info(f"=== FASE 1: Executando {len(phase1_targets)} scrapers independentes ===")
        phase1_results = run_scrapers_subset(phase1_targets, parallel, max_workers)
        results.update(phase1_results)

    # Executa Fase 2
    if phase2_targets:
        logger.info(f"=== FASE 2: Executando {len(phase2_targets)} scrapers dependentes ===")
        if "s_p_entidades_brasil" in results and not results["s_p_entidades_brasil"][0]:
            logger.warning("Aviso: s_p_entidades_brasil falhou na Fase 1. A Fase 2 pode falhar ou usar dados antigos.")
            
        phase2_results = run_scrapers_subset(phase2_targets, parallel, max_workers)
        results.update(phase2_results)

    total_elapsed = time.time() - start_time

    # Salva status do pipeline
    save_pipeline_status(results, total_elapsed)

    # Se executou todo o pipeline, regenera o catálogo de datasets dinamicamente
    if not group and not scraper:
        try:
            logger.info("=== Atualizando o catálogo de datasets dinamicamente ===")
            from scripts.generate_catalog import generate
            generate()
        except Exception as e:
            logger.warning(f"Aviso: Não foi possível regenerar o catálogo de datasets: {e}")

    # Resumo final
    ok = [n for n, r in results.items() if r[0]]
    fail = [n for n, r in results.items() if not r[0]]

    logger.info("=" * 60)
    logger.info(f"Concluído em {total_elapsed:.2f}s – ✔ {len(ok)} ok  ✖ {len(fail)} erro(s)")
    if fail:
        logger.error("Scrapers com erro: " + ", ".join(fail))
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PulseFlat – orquestrador de scrapers")
    
    # Carrega metadados dinamicamente para definir opções da linha de comando
    scrapers_registry = discover_scrapers()
    available_groups = sorted({s["group"] for s in scrapers_registry.values() if s["enabled"]})
    available_scrapers = sorted(scrapers_registry.keys())

    parser.add_argument(
        "--group",
        choices=available_groups,
        help="Executa apenas os scrapers de um grupo",
    )
    parser.add_argument(
        "--scraper",
        choices=available_scrapers,
        help="Executa apenas um scraper específico (mesmo se desabilitado por padrão)",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        default=True,
        help="Executa scrapers em paralelo usando threads (padrão)",
    )
    parser.add_argument(
        "--sequential",
        action="store_false",
        dest="parallel",
        help="Executa scrapers sequencialmente",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Número máximo de threads para execução paralela (padrão: 4)",
    )
    parser.add_argument(
        "--generate-catalog",
        action="store_true",
        help="Gera e atualiza o arquivo data/datasets.json a partir dos scrapers",
    )
    args = parser.parse_args()

    if args.generate_catalog:
        from scripts.generate_catalog import generate
        generate()
        sys.exit(0)

    main(
        group=args.group,
        scraper=args.scraper,
        parallel=args.parallel,
        max_workers=args.max_workers
    )
