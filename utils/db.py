import os
import re
import logging
from datetime import datetime
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Garantir que as variáveis de ambiente locais sejam carregadas
load_dotenv()

log = logging.getLogger("utils.db")

# Tentar importar oracledb e sqlalchemy silenciosamente
try:
    import oracledb
    from sqlalchemy import create_engine
    # Habilitar o Thin Mode explicitamente (padrão no oracledb, mas garante que não tentará Thick)
    oracledb.init_oracle_client = None 
except ImportError:
    log.warning("oracledb ou sqlalchemy não estão instalados. Cargas no banco serão ignoradas.")
    oracledb = None
    create_engine = None

# Cache para reutilização do SQLAlchemy engine (Pooling de conexões ativo)
_engine = None

def get_engine():
    """
    Cria e retorna o SQLAlchemy Engine configurado para o Oracle Database.
    """
    global _engine
    if _engine is not None:
        return _engine

    if oracledb is None or create_engine is None:
        raise ImportError("Os pacotes 'oracledb' e 'sqlalchemy' devem estar instalados.")

    user = os.getenv("ORACLE_DB_USER")
    password = os.getenv("ORACLE_DB_PASSWORD")
    dsn = os.getenv("ORACLE_DB_DSN")
    wallet_dir = os.getenv("ORACLE_DB_WALLET_DIR")
    wallet_password = os.getenv("ORACLE_DB_WALLET_PASSWORD")

    if not user or not password or not dsn:
        raise ValueError(
            "Credenciais do banco ausentes. Defina ORACLE_DB_USER, "
            "ORACLE_DB_PASSWORD e ORACLE_DB_DSN no ambiente ou no arquivo .env."
        )

    # Codificar caracteres especiais do usuário e senha para evitar erros no parser da URL
    import urllib.parse
    safe_user = urllib.parse.quote_plus(user)
    safe_password = urllib.parse.quote_plus(password)
    
    # URL de conexão para o dialeto oracle+oracledb
    url = f"oracle+oracledb://{safe_user}:{safe_password}@{dsn}"

    connect_args = {}
    if wallet_dir and os.path.exists(wallet_dir) and os.path.isdir(wallet_dir) and os.listdir(wallet_dir):
        wallet_dir_path = os.path.abspath(wallet_dir)
        log.info(f"Configurando Engine com Wallet mTLS localizada em: {wallet_dir_path}")
        connect_args["config_dir"] = wallet_dir_path
        connect_args["wallet_location"] = wallet_dir_path
        if wallet_password:
            connect_args["wallet_password"] = wallet_password
    else:
        log.info("Configurando Engine para One-Way TLS direto (sem Wallet)...")

    # Criação do engine com pool_pre_ping para resiliência de conexões instáveis
    _engine = create_engine(
        url,
        connect_args=connect_args,
        pool_pre_ping=True
    )
    return _engine

def get_connection():
    """
    Cria e retorna uma conexão bruta (DBAPI/oracledb) obtida a partir do SQLAlchemy Engine.
    Mantém compatibilidade com inserções em lote executemany de alta performance.
    """
    engine = get_engine()
    return engine.raw_connection()

def sanitize_column_name(col_name: str) -> str:
    """
    Limpa e formata o nome da coluna para que seja um identificador Oracle SQL válido.
    - Converte para maiúsculas
    - Substitui caracteres especiais, espaços, acentos e barras por sublinhados (_)
    - Limita o tamanho ao limite de 128 caracteres
    """
    # Remover acentos e caracteres especiais comuns
    name = str(col_name).strip().upper()
    name = re.sub(r'[ÁÀÂÃÄ]', 'A', name)
    name = re.sub(r'[ÉÈÊË]', 'E', name)
    name = re.sub(r'[ÍÌÎÏ]', 'I', name)
    name = re.sub(r'[ÓÒÔÕÖ]', 'O', name)
    name = re.sub(r'[ÚÙÛÜ]', 'U', name)
    name = re.sub(r'[Ç]', 'C', name)
    
    # Substituir qualquer coisa que não seja alfanumérica ou sublinhado por _
    name = re.sub(r'[^A-Z0-9_]', '_', name)
    # Colapsar múltiplos sublinhados
    name = re.sub(r'_+', '_', name)
    # Se o nome começar com número, adicionar prefixo C_ (de Conta)
    if name and name[0].isdigit():
        name = f"C_{name}"
        
    # Lista de palavras reservadas do Oracle (caso a coluna coincida, adiciona sufixo)
    reserved_keywords = {"DATE", "NUMBER", "VARCHAR", "TABLE", "USER", "GROUP", "LEVEL", "ORDER", "COMMENT", "INDEX", "VIEW", "GRANT", "SELECT"}
    if name in reserved_keywords:
        name = f"{name}_VAL"
        
    return name[:128]

def infer_oracle_type(series: pd.Series) -> str:
    """
    Infere o tipo SQL do Oracle apropriado para uma série do Pandas.
    """
    col_name_lower = str(series.name).lower()
    
    # Verificar se parece com data
    if "data" in col_name_lower or "date" in col_name_lower or col_name_lower.startswith("dt_"):
        # Se os valores válidos forem períodos de 6 dígitos (como 202406) ou 4 (como 2024), não deve ser DATE
        non_nulls = series.dropna().astype(str).str.strip()
        if not non_nulls.empty:
            if non_nulls.str.match(r'^\d{6}$').all() or non_nulls.str.match(r'^\d{4}$').all():
                return "VARCHAR2(4000)"
        return "DATE"
        
    # Verificar tipo de dados Pandas
    if pd.api.types.is_bool_dtype(series):
        return "NUMBER(1)" # Oracle não possui boolean nativo até 23c, usamos NUMBER(1)
    elif pd.api.types.is_integer_dtype(series):
        return "NUMBER(19)"
    elif pd.api.types.is_numeric_dtype(series):
        return "NUMBER"
    else:
        return "VARCHAR2(4000)"

def create_table_from_df(cursor, table_name: str, df: pd.DataFrame, clean_cols: dict[str, str]) -> bool:
    """
    Cria a tabela no Oracle caso ela não exista, inferindo os tipos do DataFrame.
    Retorna True se a tabela já existia, False caso tenha sido criada agora.
    """
    # Checar se a tabela existe
    cursor.execute(
        "SELECT COUNT(*) FROM user_tables WHERE table_name = :1", 
        [table_name.upper()]
    )
    exists = cursor.fetchone()[0] > 0
    
    if exists:
        log.info(f"Tabela '{table_name}' já existe no banco.")
        return True

    # Construir SQL de criação
    columns_sql = []
    for col_orig, col_clean in clean_cols.items():
        sql_type = infer_oracle_type(df[col_orig])
        columns_sql.append(f"{col_clean} {sql_type}")
        
    create_sql = f"CREATE TABLE {table_name.upper()} (\n  " + ",\n  ".join(columns_sql) + "\n)"
    log.info(f"Criando tabela '{table_name}' com SQL:\n{create_sql}")
    cursor.execute(create_sql)
    return False

def standardize_val(val):
    """
    Padroniza um valor para comparação de chaves sem depender de tipo exato.
    """
    if val is None or pd.isna(val):
        return None
    
    # Se for uma data, datetime ou Timestamp
    if isinstance(val, (datetime, pd.Timestamp)):
        return val.strftime("%Y-%m-%d")
    if hasattr(val, "strftime"):
        return val.strftime("%Y-%m-%d")
        
    # Se for string representando data, padronizar
    if isinstance(val, str):
        val_strip = val.strip()
        if len(val_strip) == 10 and val_strip[4] == '-' and val_strip[7] == '-':
            return val_strip
        if len(val_strip) == 10 and val_strip[2] == '/' and val_strip[5] == '/':
            try:
                return datetime.strptime(val_strip, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                pass
        return val_strip
        
    # Se for numérico
    if isinstance(val, (int, float, np.integer, np.floating)):
        return float(val)
        
    try:
        import decimal
        if isinstance(val, decimal.Decimal):
            return float(val)
    except ImportError:
        pass
        
    return str(val).strip()

def standardize_tuple(tup):
    """
    Padroniza uma tupla de valores de chaves.
    """
    return tuple(standardize_val(v) for v in tup)

def upload_dataframe(df: pd.DataFrame, table_name: str, batch_size: int = 5000, chaves_dedup: list[str] | None = None) -> bool:
    """
    Carrega um DataFrame para o banco de dados Oracle de forma otimizada.
    Realiza uma carga incremental inteligente inserindo apenas os novos registros.
    """
    if os.getenv("SKIP_ORACLE_DB"):
        log.info("Carga no banco Oracle desativada via SKIP_ORACLE_DB.")
        return False

    if oracledb is None or create_engine is None:
        log.warning("oracledb ou sqlalchemy não estão disponíveis. Pulando carga no banco.")
        return False

    if df is None or df.empty:
        log.warning(f"DataFrame vazio enviado para '{table_name}'. Carga abortada.")
        return False

    # Verificação de credenciais antes de prosseguir
    user = os.getenv("ORACLE_DB_USER")
    password = os.getenv("ORACLE_DB_PASSWORD")
    dsn = os.getenv("ORACLE_DB_DSN")
    if not user or not password or not dsn:
        log.info("Credenciais do banco Oracle não configuradas no ambiente. Pulando persistência.")
        return False

    table_name = table_name.upper()
    
    # Mapear e higienizar nomes de colunas
    clean_cols = {col: sanitize_column_name(col) for col in df.columns}
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Garantir que a tabela existe
        exists = create_table_from_df(cursor, table_name, df, clean_cols)
        
        # 2. Identificar as chaves para identificação de duplicatas
        keys_to_check = []
        if chaves_dedup:
            keys_to_check = [k for k in chaves_dedup if k in df.columns]
            
        # Identificar coluna de período para filtrar a busca se necessário
        period_col = None
        candidates = [
            "AnoMes", "ANOMES", 
            "data_base", "DATA_BASE", 
            "data_referencia", "DATA_REFERENCIA", 
            "data_captura", "DATA_CAPTURA", 
            "data", "DATA",
            "dt_captura", "DT_CAPTURA"
        ]
        for col_cand in candidates:
            found = [c for c in df.columns if clean_cols[c] == col_cand.upper()]
            if found:
                period_col = found[0]
                break

        if not keys_to_check:
            if period_col:
                keys_to_check = [period_col]
            else:
                keys_to_check = list(df.columns)
                
        # 3. Buscar chaves existentes se a tabela já existia
        existing_set = set()
        if exists and keys_to_check:
            cols_to_select = [clean_cols[k] for k in keys_to_check]
            cols_str = ", ".join(cols_to_select)
            
            if period_col and period_col in keys_to_check:
                clean_period_col = clean_cols[period_col]
                unique_periods = df[period_col].dropna().unique()
                if len(unique_periods) > 0:
                    # Obter tipo da coluna de período no banco
                    db_col_type = "VARCHAR"
                    try:
                        cursor.execute(
                            "SELECT data_type FROM user_tab_columns WHERE table_name = :1 AND column_name = :2",
                            [table_name, clean_period_col]
                        )
                        res = cursor.fetchone()
                        if res:
                            db_col_type = res[0]
                    except Exception:
                        pass
                        
                    formatted_periods = []
                    for p in unique_periods:
                        if "DATE" in db_col_type:
                            if isinstance(p, str):
                                try:
                                    formatted_periods.append(datetime.strptime(p.strip(), "%Y-%m-%d").date())
                                except ValueError:
                                    formatted_periods.append(p)
                            else:
                                formatted_periods.append(p)
                        else:
                            formatted_periods.append(str(p))
                            
                    # Buscar chaves em lotes de 1000 períodos
                    for chunk_idx in range(0, len(formatted_periods), 1000):
                        chunk_periods = formatted_periods[chunk_idx : chunk_idx + 1000]
                        placeholders = ", ".join([f":{j+1}" for j in range(len(chunk_periods))])
                        select_sql = f"SELECT {cols_str} FROM {table_name} WHERE {clean_period_col} IN ({placeholders})"
                        log.info(f"Buscando chaves existentes no banco para deduplicação (restringido por período): {select_sql}")
                        cursor.execute(select_sql, chunk_periods)
                        for row in cursor.fetchall():
                            existing_set.add(standardize_tuple(row))
            else:
                # Sem coluna de período ou período não faz parte das chaves, busca tudo da tabela
                select_sql = f"SELECT {cols_str} FROM {table_name}"
                log.info(f"Buscando chaves existentes no banco para deduplicação (tabela completa): {select_sql}")
                cursor.execute(select_sql)
                for row in cursor.fetchall():
                    existing_set.add(standardize_tuple(row))

        # 4. Filtrar o DataFrame localmente para manter apenas novas linhas
        if existing_set:
            new_rows_mask = []
            for row in df.itertuples(index=False):
                key_vals = [getattr(row, k) for k in keys_to_check]
                std_key = standardize_tuple(key_vals)
                new_rows_mask.append(std_key not in existing_set)
                
            df_filtered = df[new_rows_mask]
            log.info(f"Filtrados {len(df) - len(df_filtered)} registros duplicados. Restam {len(df_filtered)} registros novos para inserção.")
            df = df_filtered
        else:
            log.info(f"Nenhum registro existente ou tabela nova. Inserindo todos os {len(df)} registros.")

        # Se não há mais linhas a inserir, retornar sucesso
        if df.empty:
            log.info(f"Todos os registros já existem no banco Oracle para {table_name}. Carga concluída sem inserções.")
            return True

        # 5. Montar a query de inserção em lotes
        cols_str = ", ".join(clean_cols.values())
        binds_str = ", ".join([f":{i+1}" for i in range(len(clean_cols))])
        insert_sql = f"INSERT INTO {table_name} ({cols_str}) VALUES ({binds_str})"
        
        # Identificar quais colunas são do tipo DATE no banco de dados para tratar no insert
        date_cols = set()
        try:
            cursor.execute(
                "SELECT column_name FROM user_tab_columns WHERE table_name = :1 AND data_type = 'DATE'",
                [table_name]
            )
            date_cols = {row[0].upper() for row in cursor.fetchall()}
        except Exception:
            # Fallback para inferência baseada no DataFrame original
            date_cols = {clean_cols[col] for col in df.columns if infer_oracle_type(df[col]) == "DATE"}
        
        # 6. Executar a inserção em blocos com limpeza sob demanda para economizar RAM
        total_rows = len(df)
        inserted = 0
        log.info(f"Iniciando inserção de {total_rows} linhas em lotes de {batch_size}...")
        
        for i in range(0, total_rows, batch_size):
            chunk = df.iloc[i : i + batch_size]
            
            # Limpar os dados do chunk local
            batch = []
            for row in chunk.itertuples(index=False):
                clean_row = []
                for idx, val in enumerate(row):
                    col_orig = df.columns[idx]
                    col_clean = clean_cols[col_orig]
                    
                    if val is None or (isinstance(val, float) and (np.isnan(val) or np.isinf(val))) or pd.isna(val):
                        clean_row.append(None)
                    elif col_clean in date_cols:
                        if isinstance(val, (pd.Timestamp, datetime)):
                            clean_row.append(val.date() if hasattr(val, 'date') else val)
                        elif hasattr(val, 'to_pydatetime'):
                            clean_row.append(val.to_pydatetime().date())
                        elif isinstance(val, str) and len(val.strip()) == 10 and val.strip()[4] == '-' and val.strip()[7] == '-':
                            try:
                                clean_row.append(datetime.strptime(val.strip(), "%Y-%m-%d").date())
                            except ValueError:
                                clean_row.append(val)
                        else:
                            clean_row.append(val)
                    else:
                        clean_row.append(val)
                batch.append(tuple(clean_row))
                
            cursor.executemany(insert_sql, batch)
            conn.commit()
            inserted += len(batch)
            log.info(f"Progresso: {inserted}/{total_rows} linhas inseridas em {table_name}")
            
        log.info(f"Sucesso! Carga concluída para a tabela {table_name} ({inserted} linhas inseridas).")
        return True
        
    except Exception as e:
        log.error(f"Erro ao carregar dados na tabela {table_name}: {e}")
        # Fazer rollback em caso de falha
        try:
            conn.rollback()
        except Exception:
            pass
        return False
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass
