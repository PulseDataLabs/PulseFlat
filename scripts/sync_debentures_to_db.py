import sys
import pandas as pd
from pathlib import Path

# Adiciona o diretório raiz ao sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.base import get_logger
from utils.db import upload_dataframe

log = get_logger("sync_debentures_to_db")

def main():
    csv_file = ROOT_DIR / "data" / "debentures_mercado_secundario_precos_negociacao.csv.gz"
    if not csv_file.exists():
        log.error(f"Arquivo {csv_file} não encontrado.")
        return

    log.info(f"Lendo dados de {csv_file}...")
    df = pd.read_csv(csv_file, dtype=str, keep_default_na=False)
    log.info(f"{len(df)} registros carregados do CSV.")

    table_name = "DEBENTURES_MERCADO_SECUNDARIO_PRECOS_NEGOCIACAO"
    chaves_dedup = ["data_referencia", "codigo_ativo", "isin"]

    log.info(f"Iniciando sincronização para a tabela {table_name} no Oracle...")
    success = upload_dataframe(df, table_name, chaves_dedup=chaves_dedup)
    
    if success:
        log.info("Sincronização concluída com sucesso!")
    else:
        log.error("Falha ao sincronizar dados com o banco Oracle.")

if __name__ == "__main__":
    main()
