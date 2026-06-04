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
from typing import Optional

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
    "anbima_ima":                           "anbima",
    "anbima_550":                           "anbima",
    "anbima_idka":                          "anbima",   # novo
    "anbima_ranking_global":               "anbima",   # novo
    "anbima_matriz_probabilidade_resgate": "anbima",   # novo

    # ── B3 ──────────────────────────────────────────────────────────────────
    "b3_fiis":                              "b3",
    "b3_etfs":                              "b3",
    "b3_carteiras":                         "b3",
    "b3_futuros_ajustes":                   "b3",
    "b3_indicadores_financeiros":           "b3",
    "b3_bdi_indicadores_economicos":        "b3",
    "b3_bdi_di_over":                       "b3",
    "b3_bdi_trades_acoes":                  "b3",
    "b3_carteira_ibov":                     "b3",
    "b3_bmf_taxas_juros":                   "b3",
    "b3_series_historicas":                 "b3",       # novo

    # ── BCB / BACEN ─────────────────────────────────────────────────────────
    "bcb_ptax":                             "bcb",
    "bcb_sgs":                              "bcb",
    "bacen_balancetes_bancos":              "bcb",      # novo
    "bacen_conglomerados":                  "bcb",      # novo
    "bacen_parcelas_capital_basileia":      "bcb",      # novo

    # ── IBGE ────────────────────────────────────────────────────────────────
    "ibge_sidra":                           "ibge",

    # ── CVM ─────────────────────────────────────────────────────────────────
    "cvm_fundos_cadastro":                  "cvm",
    "cvm_fundos_informe_diario":            "cvm",

    # ── RATINGS ─────────────────────────────────────────────────────────────
    # A ordem importa: entidades devem rodar antes de ratings
    "s_p_entidades_brasil":                "ratings",  # novo
    "s_p_ratings_brasil":                  "ratings",  # novo
    "s_p_acoes_ratings":                   "ratings",  # novo
    "moodys_local_ratings":                "ratings",  # novo

    # ── MISC ────────────────────────────────────────────────────────────────
    "yahoo_finance_series":                "misc",     # novo
    "investing_etf":                       "misc",     # novo
}


def run_scraper(module_name: str) -> bool:
    """Importa e executa um scraper pelo nome do módulo. Retorna True se ok."""
    try:
        logger.info(f"▶  Iniciando: {module_name}")
        mod = importlib.import_module(f"scrapers.{module_name}")
        # Convenção PulseFlat: cada módulo expõe uma classe com o mesmo nome
        # em snake_case → CamelCase, ou chama scraper.run() diretamente.
        class_name = "".join(word.capitalize() for word in module_name.split("_")) + "Scraper"
        if hasattr(mod, class_name):
            scraper = getattr(mod, class_name)()
            scraper.run()
        elif hasattr(mod, "main"):
            mod.main()
        else:
            logger.error(f"   Módulo {module_name} não tem classe {class_name} nem função main().")
            return False
        logger.info(f"✔  Concluído: {module_name}")
        return True
    except Exception:
        logger.error(f"✖  Erro em {module_name}:\n{traceback.format_exc()}")
        return False


def main(group: Optional[str] = None, scraper: Optional[str] = None) -> None:
    if scraper:
        # Executa apenas um scraper específico
        if scraper not in SCRAPERS:
            logger.error(f"Scraper '{scraper}' não encontrado no registro.")
            sys.exit(1)
        success = run_scraper(scraper)
        sys.exit(0 if success else 1)

    # Filtra por grupo, se informado
    targets = {
        name: grp for name, grp in SCRAPERS.items()
        if group is None or grp == group
    }

    if not targets:
        logger.error(
            f"Grupo '{group}' não encontrado. "
            f"Grupos disponíveis: {sorted(set(SCRAPERS.values()))}"
        )
        sys.exit(1)

    results: dict[str, bool] = {}
    for name in targets:
        results[name] = run_scraper(name)

    # Resumo
    ok = [n for n, r in results.items() if r]
    fail = [n for n, r in results.items() if not r]

    logger.info("=" * 60)
    logger.info(f"Concluído – ✔ {len(ok)} ok  ✖ {len(fail)} erro(s)")
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
    args = parser.parse_args()
    main(group=args.group, scraper=args.scraper)
