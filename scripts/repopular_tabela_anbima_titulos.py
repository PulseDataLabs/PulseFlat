import sys
import pandas as pd
from pathlib import Path

# Adiciona o diretório raiz ao sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.base import get_logger
from utils.db import get_connection, upload_dataframe

log = get_logger("repopular_tabela_anbima_titulos")

def main():
    csv_file = ROOT_DIR / "data" / "anbima_titulos_publicos.csv"
    if not csv_file.exists():
        log.error(f"Arquivo {csv_file} não encontrado.")
        return

    table_name = "ANBIMA_TITULOS_PUBLICOS"
    
    log.info("Lendo dados do CSV histórico de títulos públicos...")
    df = pd.read_csv(csv_file, dtype=str, keep_default_na=False)
    log.info(f"{len(df)} registros carregados.")

    log.info("Conectando ao Oracle...")
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

    log.info("Iniciando upload de todo o DataFrame histórico para o Oracle...")
    chaves_dedup = ["data_captura", "titulo", "data_vencimento"]
    success = upload_dataframe(df, table_name, chaves_dedup=chaves_dedup)
    
    if success:
        log.info("Repopulação da tabela concluída com sucesso!")
    else:
        log.error("Falha ao sincronizar dados com o banco Oracle.")

if __name__ == "__main__":
    main()
