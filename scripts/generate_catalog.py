"""
scripts/generate_catalog.py
----------------------------
Script que lê as definições dos scrapers (classes ou arquivos funcionais)
e gera o arquivo data/datasets.json de forma automatizada e sincronizada.
"""

import importlib
import json
import logging
import sys
from pathlib import Path

# Configura caminhos para permitir importações corretas do projeto
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from run_all import SCRAPERS
from scrapers.utils.base import BaseScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("generate_catalog")


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
    if "ratings" in src or "s&p" in src or "moody" in src:
        return "icon-ratings"
    return "icon-misc"


def generate():
    datasets_json_path = ROOT_DIR / "data" / "datasets.json"

    # 1. Carrega o datasets.json existente como fallback
    old_datasets = {}
    if datasets_json_path.exists():
        try:
            with datasets_json_path.open("r", encoding="utf-8") as f:
                data_list = json.load(f)
                for item in data_list:
                    if "file" in item:
                        old_datasets[item["file"]] = item
            logger.info(f"Carregado catálogo atual de fallbacks com {len(old_datasets)} datasets.")
        except Exception as e:
            logger.warning(f"Não foi possível ler datasets.json atual para fallback: {e}")

    new_catalog = []
    processed_files = set()

    # 2. Itera sobre cada scraper registrado em run_all.py
    for module_name, group in SCRAPERS.items():
        logger.info(f"Processando metadados do módulo: {module_name} (Grupo: {group})")

        # Dados extraídos do scraper
        title = ""
        description = ""
        icon = ""
        icon_class = ""
        badge = ""
        badge_class = ""
        tags = []
        source = ""
        filename = f"{module_name}.csv"  # Padrão fallback

        try:
            # Importa o módulo do scraper
            mod = importlib.import_module(f"scrapers.{module_name}")

            # Identifica se é baseado em classe
            class_name = "".join(word.capitalize() for word in module_name.split("_")) + "Scraper"
            if hasattr(mod, class_name):
                cls = getattr(mod, class_name)
                # Instancia para obter atributos dinâmicos do BaseScraper
                inst = cls()
                
                title = getattr(inst, "title", "")
                description = getattr(inst, "description", "")
                icon = getattr(inst, "icon", "")
                icon_class = getattr(inst, "icon_class", "")
                badge = getattr(inst, "badge", "")
                badge_class = getattr(inst, "badge_class", "")
                tags = getattr(inst, "tags", [])
                source = getattr(inst, "source", "")

                # Se a classe redefiniu a saída de arquivo
                if hasattr(inst, "output_file") and inst.output_file:
                    filename = inst.output_file.name
                else:
                    filename = f"{inst.name}.csv"
            
            # Se for funcional, verifica se possui METADATA global
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
                if "file" in meta:
                    filename = meta["file"]

        except Exception as e:
            logger.warning(f"Erro ao importar {module_name} para metadados, usando fallback do datasets.json: {e}")

        # 3. Aplica lógica de Fallback com o datasets.json anterior
        # Procuramos correspondência pelo arquivo CSV gerado
        fallback = old_datasets.get(filename, {})
        if not fallback:
            # Tenta encontrar correspondência pelo próprio nome do módulo
            fallback = old_datasets.get(f"{module_name}.csv", {})

        title = title or fallback.get("title") or module_name.replace("_", " ").title()
        description = description or fallback.get("description") or "Sem descrição fornecida."
        icon = icon or fallback.get("icon") or "📊"
        badge = badge or fallback.get("badge") or "Diário"
        badge_class = badge_class or fallback.get("badgeClass") or "badge-daily"
        tags = tags or fallback.get("tags") or [group]
        source = source or fallback.get("source") or group.upper()
        icon_class = icon_class or fallback.get("iconClass") or get_source_class(source)

        # URL bruta do arquivo no repositório do github
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
            "url": url
        }

        new_catalog.append(dataset_entry)
        processed_files.add(filename)

    # 4. Adiciona quaisquer itens do datasets.json antigo que não foram mapeados em run_all.py (ex: datasets secundários do mesmo scraper)
    for file, old_item in old_datasets.items():
        if file not in processed_files:
            logger.info(f"Mantendo dataset secundário do datasets.json original: {file}")
            new_catalog.append(old_item)

    # Ordena o catálogo por fonte (source) e por título (title)
    new_catalog.sort(key=lambda x: (x["source"].lower(), x["title"].lower()))

    # Salva o arquivo final
    try:
        datasets_json_path.parent.mkdir(parents=True, exist_ok=True)
        with datasets_json_path.open("w", encoding="utf-8") as f:
            json.dump(new_catalog, f, indent=2, ensure_ascii=False)
        logger.info(f"Sucesso! Catálogo gerado e salvo em {datasets_json_path} com {len(new_catalog)} datasets.")
    except Exception as e:
        logger.error(f"Erro ao salvar datasets.json: {e}")
        sys.exit(1)


if __name__ == "__main__":
    generate()
