import sys
from pathlib import Path

import pandas as pd

# Adiciona o diretório raiz ao sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.base import get_logger
from utils.db import get_connection, upload_dataframe

log = get_logger("repopular_tabelas_yahoo")


def repopulate_table(table_name, csv_filename):
    csv_file = ROOT_DIR / "data" / csv_filename
    if not csv_file.exists():
        log.error(f"Arquivo {csv_file} não encontrado.")
        return

    log.info(f"Lendo dados de {csv_filename}...")
    df = pd.read_csv(csv_file, dtype=str, keep_default_na=False)
    log.info(f"{len(df)} registros carregados.")

    log.info(f"Conectando ao Oracle para {table_name}...")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        log.info(f"Truncando a tabela {table_name}...")
        cursor.execute(f"TRUNCATE TABLE {table_name}")
        conn.commit()
        log.info("Tabela truncada com sucesso!")

        cursor.close()
        conn.close()
    except Exception as e:
        log.error(f"Erro ao truncar a tabela {table_name} no Oracle: {e}")
        return

    log.info(f"Iniciando upload de todo o DataFrame histórico para {table_name}...")
    chaves_dedup = ["data_referencia", "codigo_ativo"]
    success = upload_dataframe(df, table_name, chaves_dedup=chaves_dedup)

    if success:
        log.info(f"Repopulação da tabela {table_name} concluída com sucesso!\n")
    else:
        log.error(f"Falha ao sincronizar dados com o banco Oracle para {table_name}.\n")


def main():
    repopulate_table("YAHOO_ACOES_BRASILEIRAS", "yahoo_acoes_brasileiras.csv")
    repopulate_table("YAHOO_FIIS_FIAGROS", "yahoo_fiis_fiagros.csv")
    repopulate_table("YAHOO_ETFS", "yahoo_etfs.csv")
    repopulate_table("YAHOO_CRIPTOATIVOS", "yahoo_criptoativos.csv")


if __name__ == "__main__":
    main()
