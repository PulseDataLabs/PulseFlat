import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

# Adiciona o diretório raiz ao sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.base import get_logger
from utils.parsers import hash_row

log = get_logger("converter_csv_debentures")


def format_date(val):
    if not val:
        return ""
    val_strip = val.strip()
    for fmt in ("%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(val_strip, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return val


def main():
    csv_file = (
        ROOT_DIR / "data" / "debentures_mercado_secundario_precos_negociacao.csv.gz"
    )
    if not csv_file.exists():
        log.error(f"Arquivo {csv_file} não encontrado.")
        return

    log.info(f"Lendo {csv_file}...")
    df = pd.read_csv(csv_file, dtype=str, keep_default_na=False)
    log.info(f"{len(df)} registros lidos.")

    log.info("Formatando data_referencia...")
    df["data_referencia"] = df["data_referencia"].apply(format_date)

    log.info("Recalculando registro_hash...")
    records = df.to_dict(orient="records")
    new_hashes = []

    for idx, item in enumerate(records):
        # Para calcular o hash original de enriquecer:
        # 1. Excluir data_captura
        # 2. Excluir registro_hash se já existir
        hash_input = {
            k: v for k, v in item.items() if k not in ("data_captura", "registro_hash")
        }
        new_hashes.append(hash_row(hash_input))

        if idx > 0 and idx % 100000 == 0:
            log.info(f"  {idx} hashes calculados...")

    df["registro_hash"] = new_hashes

    log.info(f"Salvando CSV corrigido em {csv_file}...")
    df.to_csv(csv_file, index=False)
    log.info("Conversão concluída com sucesso!")


if __name__ == "__main__":
    main()
