import sys
from pathlib import Path

import pandas as pd

# Adiciona o diretório raiz ao sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.base import get_logger
from utils.db import get_connection, upload_dataframe

log = get_logger("repopular_tabela_bacen_negociacao")


def main():
    csv_file = ROOT_DIR / "data" / "bacen_negociacao_tpf_extragrupo.csv.gz"
    if not csv_file.exists():
        log.error(f"Arquivo {csv_file} não encontrado.")
        return

    table_name = "BACEN_NEGOCIACAO_TPF_EXTRAGRUPO"

    log.info("Lendo dados do CSV histórico corrigido...")
    df = pd.read_csv(csv_file, dtype=str, keep_default_na=False)
    log.info(f"{len(df)} registros carregados.")

    log.info("Conectando ao banco de dados Oracle...")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Truncar a tabela existente
        log.info(f"Truncando a tabela {table_name}...")
        cursor.execute(f"TRUNCATE TABLE {table_name}")
        conn.commit()
        log.info("Tabela truncada com sucesso!")

        cursor.close()
        conn.close()
    except Exception as e:
        log.error(f"Erro ao truncar a tabela no Oracle: {e}")
        return

    # 2. Fazer o upload completo do DataFrame atualizado
    log.info("Iniciando upload de todo o DataFrame histórico para o Oracle...")
    chaves_dedup = ["data_captura", "conjunto", "registro_hash"]
    success = upload_dataframe(df, table_name, chaves_dedup=chaves_dedup)

    if success:
        log.info("Repopulação da tabela concluída com sucesso!")
    else:
        log.error("Falha ao sincronizar dados com o banco Oracle.")


if __name__ == "__main__":
    main()
