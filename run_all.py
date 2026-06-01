"""
run_all.py
----------
Orquestrador: executa scrapers em sequência e imprime resumo.

Uso:
    python run_all.py                     # todos
    python run_all.py anbima              # grupo ANBIMA
    python run_all.py b3                  # grupo B3
    python run_all.py anbima_indicadores  # scraper específico
"""

import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import get_logger

log = get_logger("run_all")

SCRAPERS = [
    {"id": "anbima_indicadores", "modulo": "scrapers.anbima_indicadores",
     "descricao": "ANBIMA — Indicadores (SELIC, DI, IGP-M, IPCA, Câmbio, TR, FDS)", "grupo": "anbima"},
    {"id": "anbima_projecoes",   "modulo": "scrapers.anbima_projecoes",
     "descricao": "ANBIMA — Projeções IPCA e IGP-M",                                 "grupo": "anbima"},
    {"id": "b3_fiis",            "modulo": "scrapers.b3_fiis",
     "descricao": "B3 — FIIs Listados",                                              "grupo": "b3"},
    {"id": "b3_etfs",            "modulo": "scrapers.b3_etfs",
     "descricao": "B3 — ETFs Listados (RV + RF)",                                   "grupo": "b3"},
    {"id": "b3_carteiras",       "modulo": "scrapers.b3_carteiras",
     "descricao": "B3 — Carteiras Teóricas (22 índices)",                           "grupo": "b3"},
    {"id": "b3_boletim_diario",  "modulo": "scrapers.b3_boletim_diario",
     "descricao": "B3 — Boletim Diário (arquivos para download)",                   "grupo": "b3"},
    {"id": "captura_downloads_migrados", "modulo": "scrapers.captura_downloads_migrados",
     "descricao": "Migração captura_downloads — conjuntos requests em CSV",          "grupo": "migrados"},
]


def executar(scraper: dict) -> tuple[bool, float]:
    inicio = time.time()
    try:
        mod = importlib.import_module(scraper["modulo"])
        mod.main()
        return True, time.time() - inicio
    except SystemExit as e:
        return (e.code in (0, None)), time.time() - inicio
    except Exception as e:
        log.error(f"[{scraper['id']}] Erro inesperado: {e}", exc_info=True)
        return False, time.time() - inicio


def main():
    filtro = sys.argv[1].lower() if len(sys.argv) > 1 else None

    selecionados = [
        s for s in SCRAPERS
        if filtro is None or filtro == s["id"] or filtro == s["grupo"]
    ]

    if not selecionados:
        validos = [s["id"] for s in SCRAPERS] + list({s["grupo"] for s in SCRAPERS})
        log.error(f"Filtro '{filtro}' inválido. Opções: {', '.join(sorted(validos))}")
        sys.exit(1)

    log.info("=" * 60)
    log.info(f"Iniciando {len(selecionados)} scraper(s)")
    log.info("=" * 60)

    resultados = []
    for s in selecionados:
        log.info(f"\n▶  {s['descricao']}")
        ok, dur = executar(s)
        resultados.append((s["id"], ok, dur))
        log.info(f"   {'✓ OK' if ok else '✗ ERRO'}  ({dur:.1f}s)")
        time.sleep(1)

    log.info("\n" + "=" * 60)
    log.info("RESUMO")
    log.info("=" * 60)
    for id_, ok, dur in resultados:
        log.info(f"  {'✓' if ok else '✗'}  {id_:<26} {dur:>6.1f}s")
    n_ok  = sum(1 for _, ok, _ in resultados if ok)
    n_err = len(resultados) - n_ok
    log.info(f"\n  Total: {n_ok} OK  |  {n_err} erro(s)")
    log.info("=" * 60)

    if n_err:
        sys.exit(1)


if __name__ == "__main__":
    main()
