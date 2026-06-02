#!/usr/bin/env python3
"""
scripts/populate_last_updates.py
---------------------------------
Varre o diretório data/, abre cada arquivo CSV, encontra a data_captura mais recente,
e salva o mapeamento no arquivo data/last_updates.json.
"""

import csv
import json
import logging
import sys
from pathlib import Path

# Configura logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("populate_last_updates")


def main():
    root_dir = Path(__file__).resolve().parents[1]
    data_dir = root_dir / "data"
    output_path = data_dir / "last_updates.json"

    if not data_dir.exists():
        log.error(f"Diretório {data_dir} não encontrado.")
        sys.exit(1)

    last_updates = {}

    # Se já existir last_updates.json, começa com os dados dele
    if output_path.exists():
        try:
            with output_path.open("r", encoding="utf-8") as f:
                last_updates = json.load(f)
            log.info("Carregado last_updates.json existente.")
        except Exception as e:
            log.warning(f"Erro ao ler last_updates.json existente: {e}. Criando um novo.")

    # Varre todos os arquivos .csv
    for csv_file in data_dir.glob("*.csv"):
        log.info(f"Processando {csv_file.name}...")
        try:
            with csv_file.open("r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    continue

                # Identifica a coluna de data de captura (geralmente data_captura)
                date_col = None
                for col in reader.fieldnames:
                    if col.lower() == "data_captura":
                        date_col = col
                        break

                if not date_col:
                    log.warning(f"  Coluna data_captura não encontrada em {csv_file.name}. Pulando.")
                    continue

                # Extrai todas as datas e encontra a mais recente
                datas = []
                for row in reader:
                    val = row.get(date_col)
                    if val and val.strip():
                        datas.append(val.strip())

                if datas:
                    max_date = max(datas)
                    last_updates[csv_file.name] = max_date
                    log.info(f"  Data mais recente: {max_date}")
                else:
                    log.warning(f"  Nenhum registro com data em {csv_file.name}.")
        except Exception as e:
            log.error(f"Erro ao processar {csv_file.name}: {e}")

    # Salva no arquivo JSON
    try:
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(last_updates, f, indent=2, ensure_ascii=False)
        log.info(f"Sucesso! Mapeamento atualizado salvo em {output_path}")

        # Salva no arquivo JS para carregamento estático offline (file://)
        js_path = data_dir / "last_updates.js"
        with js_path.open("w", encoding="utf-8") as f:
            f.write(f"window.PULSEFLAT_LAST_UPDATES = {json.dumps(last_updates, indent=2, ensure_ascii=False)};\n")
        log.info(f"Sucesso! Mapeamento estático JS salvo em {js_path}")
    except Exception as e:
        log.error(f"Erro ao salvar arquivos de metadados: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
