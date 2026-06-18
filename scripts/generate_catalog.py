#!/usr/bin/env python
# coding: utf-8
"""
scripts/generate_catalog.py
----------------------------
Script que lê as definições dos scrapers (classes ou arquivos funcionais)
e gera o arquivo data/datasets.json de forma automatizada e sincronizada.

Uso:
    python scripts/generate_catalog.py
    python scripts/generate_catalog.py --dry-run
    python scripts/generate_catalog.py --quiet
"""

import importlib
import json
import sys
import time
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run_all import discover_scrapers
from scrapers.utils.base import BaseScraper

from scripts.utils.ux import (
    banner, section, print_start, print_done, print_fail, print_warn, print_info,
    print_summary, add_common_args, apply_common_args, ColorLogger, ICON,
)

log = ColorLogger("generate_catalog")


def get_source_class(source_name: str) -> str:
    """Retorna a classe de CSS para o ícone com base no grupo de origem."""
    src = source_name.lower()
    if "anbima" in src:
        return "icon-anbima"
    if "b3" in src:
        return "icon-b3"
    if "bcb" in src or "bacen" in src:
        return "icon-bcb"
    if "cvm" in src:
        return "icon-cvm"
    if "ibge" in src:
        return "icon-ibge"
    return "icon-misc"


def generate(dry_run: bool = False) -> None:
    t0 = time.time()
    banner("Gerar Catálogo de Datasets", "Sincroniza scrapers → datasets.json")
    section("Processando scrapers", "chart")

    datasets_json_path = Path(__file__).resolve().parents[1] / "data" / "datasets.json"

    old_datasets = {}
    if datasets_json_path.exists():
        try:
            with datasets_json_path.open("r", encoding="utf-8") as f:
                data_list = json.load(f)
                for item in data_list:
                    if "file" in item:
                        old_datasets[item["file"]] = item
            print_info(f"Carregado catálogo atual com {len(old_datasets)} datasets (fallback).")
        except Exception as e:
            print_warn(f"Não foi possível ler datasets.json para fallback: {e}")

    new_catalog = []
    processed_files = set()
    scrapers_registry = discover_scrapers()
    total_scrapers = len(scrapers_registry)
    idx = 0

    for module_name, info in scrapers_registry.items():
        idx += 1
        group = info["group"]
        print_start(f"[{idx}/{total_scrapers}] {module_name} ({group})", icon="search")

        title = ""
        description = ""
        icon = ""
        icon_class = ""
        badge = ""
        badge_class = ""
        tags = []
        source = ""
        accumulate = None
        filename = f"{module_name}.csv"

        try:
            mod = importlib.import_module(f"scrapers.{module_name}")
            class_name = "".join(word.capitalize() for word in module_name.split("_")) + "Scraper"

            if hasattr(mod, class_name):
                cls = getattr(mod, class_name)
                inst = cls()
                title = getattr(inst, "title", "")
                description = getattr(inst, "description", "")
                icon = getattr(inst, "icon", "")
                icon_class = getattr(inst, "icon_class", "")
                badge = getattr(inst, "badge", "")
                badge_class = getattr(inst, "badge_class", "")
                tags = getattr(inst, "tags", [])
                source = getattr(inst, "source", "")
                accumulate = getattr(inst, "accumulate", True)
                if hasattr(inst, "output_file") and inst.output_file:
                    filename = inst.output_file.name
                else:
                    filename = f"{inst.name}.csv"

            elif hasattr(mod, "METADATA") and isinstance(mod.METADATA, dict):
                meta = mod.METADATA
                title = meta.get("title", "")
                description = meta.get("description", "")
                icon = meta.get("icon", "")
                icon_class = meta.get("icon_class", "")
                badge = meta.get("badge", "")
                badge_class = meta.get("badge_class", "")
                tags = meta.get("tags", [])
                source = meta.get("source", "")
                accumulate = meta.get("accumulate", True)
                if "file" in meta:
                    filename = meta["file"]

        except Exception as e:
            print_warn(f"Erro ao importar {module_name}: {e}. Usando fallback.")

        fallback = old_datasets.get(filename, {})
        if not fallback:
            fallback = old_datasets.get(f"{module_name}.csv", {})

        title = title or fallback.get("title") or module_name.replace("_", " ").title()
        description = description or fallback.get("description") or "Sem descrição fornecida."
        icon = icon or fallback.get("icon") or "📊"
        badge = badge or fallback.get("badge") or "Diário"
        badge_class = badge_class or fallback.get("badgeClass") or "badge-daily"
        tags = tags or fallback.get("tags") or [group]
        source = source or fallback.get("source") or group.upper()
        icon_class = icon_class or fallback.get("iconClass") or get_source_class(source)
        accumulate = accumulate if accumulate is not None else fallback.get("accumulate", True)

        url = fallback.get("url") or f"https://raw.githubusercontent.com/royopa/PulseFlat/main/data/{filename}"

        dataset_entry = {
            "title": title,
            "file": filename,
            "description": description,
            "icon": icon,
            "iconClass": icon_class,
            "badge": badge,
            "badgeClass": badge_class,
            "tags": tags,
            "source": source,
            "url": url,
            "accumulate": accumulate,
        }

        new_catalog.append(dataset_entry)
        processed_files.add(filename)
        print_done(f"{module_name} → {filename}")

    for file, old_item in old_datasets.items():
        if file not in processed_files:
            print_info(f"Mantendo dataset secundário: {file}")
            new_catalog.append(old_item)

    new_catalog.sort(key=lambda x: (x["source"].lower(), x["title"].lower()))

    if not dry_run:
        try:
            datasets_json_path.parent.mkdir(parents=True, exist_ok=True)
            with datasets_json_path.open("w", encoding="utf-8") as f:
                json.dump(new_catalog, f, indent=2, ensure_ascii=False)
            print_done(f"Catálogo salvo em {datasets_json_path} com {len(new_catalog)} datasets.")
        except Exception as e:
            print_fail(f"Erro ao salvar datasets.json: {e}")
            sys.exit(1)
    else:
        print_info(f"Dry-run: {len(new_catalog)} datasets seriam gerados.")

    elapsed = time.time() - t0
    print_summary(
        "Catálogo gerado",
        total=len(scrapers_registry),
        success=len(new_catalog),
        failed=0,
        elapsed=elapsed,
        details=[
            ("chart", "Datasets no catálogo", str(len(new_catalog))),
            ("package", "Fallbacks usados", str(len(old_datasets))),
        ],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="📊 Gera datasets.json a partir dos scrapers registrados",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
exemplos:
  python scripts/generate_catalog.py
  python scripts/generate_catalog.py --dry-run
  python scripts/generate_catalog.py --quiet
        """,
    )
    add_common_args(parser)
    args = parser.parse_args()

    if args.dry_run:
        log.info("Modo dry-run: datasets.json não será salvo.")

    apply_common_args(args)
    generate(dry_run=args.dry_run)
