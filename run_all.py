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

# ---------------------------------------------------------------------------
# Registro de scrapers
# Formato: { "nome_do_modulo": "grupo" }
# ---------------------------------------------------------------------------
SCRAPERS: dict[str, str] = {
    # ── ANBIMA ──────────────────────────────────────────────────────────────
    "anbima_indicadores":                   "anbima",
    "anbima_projecoes":                     "anbima",
    "anbima_titulos_publicos":              "anbima",
    "anbima_debentures":                    "anbima",
    "anbima_ima_completo":                  "anbima",
    "anbima_550":                           "anbima",
    "anbima_idka":                          "anbima",   # novo
    "anbima_ranking_global":               "anbima",   # novo
    "anbima_matriz_probabilidade_resgate": "anbima",   # novo
    "anbima_indice_imab":                   "anbima",   # novo
    "debentures_emissoes_caracteristicas": "anbima",   # novo
    "debentures_mercado_secundario_precos_negociacao": "anbima", # novo

    # ── B3 ──────────────────────────────────────────────────────────────────
    "b3_fiis":                              "b3",
    "b3_etfs":                              "b3",
    "b3_carteiras":                         "b3",
    "b3_futuros_ajustes":                   "b3",
    "b3_indicadores_financeiros":           "b3",
    "b3_bdi_di_over":                       "b3",
    "b3_bdi_trades_acoes":                  "b3",
    "b3_bmf_taxas_juros":                   "b3",
    "b3_series_historicas":                 "b3",       # novo
    "b3_carteira_teorica_ibov":             "b3",       # novo
    "b3_carteira_teorica_smll":             "b3",       # novo
    "b3_carteira_teorica_bdrx":             "b3",       # novo
    "b3_carteira_teorica_isee":             "b3",       # novo
    "b3_carteira_teorica_ibxl":             "b3",       # novo
    "b3_carteira_teorica_ifnc":             "b3",       # novo
    "b3_carteira_teorica_agfs_iagro":       "b3",       # novo
    "b3_carteira_teorica_ibsd":             "b3",       # novo
    "b3_titulos_negociaveis":               "b3",       # novo

    # ── BCB / BACEN ─────────────────────────────────────────────────────────
    "bcb_ptax":                             "bcb",
    "bcb_sgs":                              "bcb",
    "bacen_balancetes_bancos":              "bcb",      # novo
    "bacen_conglomerados":                  "bcb",      # novo
    "bacen_parcelas_capital_basileia":      "bcb",      # novo
    "bacen_negociacao_tpf":                 "bcb",      # novo

    # ── IBGE ────────────────────────────────────────────────────────────────
    "ibge_sidra":                           "ibge",

    # ── CVM ─────────────────────────────────────────────────────────────────
    "cvm_fundos_informe_diario":            "cvm",
    "cvm_fundos_classe":                    "cvm",      # novo

    # ── RATINGS ─────────────────────────────────────────────────────────────
    # A ordem importa: entidades devem rodar antes de ratings
    "s_p_entidades_brasil":                "ratings",  # novo
    "s_p_ratings_brasil":                  "ratings",  # novo
    "s_p_acoes_ratings":                   "ratings",  # novo
    "moodys_local_ratings":                "ratings",  # novo

    # ── MISC ────────────────────────────────────────────────────────────────
    "yahoo_finance_series":                "misc",     # novo
    "investing_etf":                       "misc",     # novo
    "onu_pacto_global":                    "misc",     # novo
}


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
    
    # Inicializa ou carrega o status existente
    status_data = {
        "timestamp": datetime.now().isoformat(),
        "elapsed_seconds": total_elapsed,
        "status": "success",
        "summary": {
            "total": len(SCRAPERS),
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
    total_scrapers = len(SCRAPERS)
    success_count = 0
    failed_count = 0
    
    # Preenche scrapers que ainda não rodaram se não estiverem no JSON
    for name in SCRAPERS:
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

    status_data["summary"]["total"] = total_scrapers
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
    
    if scraper:
        if scraper not in SCRAPERS:
            logger.error(f"Scraper '{scraper}' não encontrado no registro.")
            sys.exit(1)
        targets = {scraper: SCRAPERS[scraper]}
    else:
        targets = {
            name: grp for name, grp in SCRAPERS.items()
            if group is None or grp == group
        }
        
    if not targets:
        logger.error(
            f"Nenhum scraper selecionado. Grupo '{group}' ou Scraper '{scraper}' inválido."
        )
        sys.exit(1)

    # Separação por Fases de Dependência
    phase2_names = ["s_p_ratings_brasil"]
    phase1_targets = [name for name in targets if name not in phase2_names]
    phase2_targets = [name for name in targets if name in phase2_names]

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
    parser.add_argument(
        "--group",
        choices=sorted(set(SCRAPERS.values())),
        help="Executa apenas os scrapers de um grupo",
    )
    parser.add_argument(
        "--scraper",
        choices=sorted(SCRAPERS.keys()),
        help="Executa apenas um scraper específico",
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
    args = parser.parse_args()
    main(
        group=args.group,
        scraper=args.scraper,
        parallel=args.parallel,
        max_workers=args.max_workers
    )
