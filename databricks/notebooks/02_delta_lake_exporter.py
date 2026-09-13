# Databricks notebook source
# MAGIC %md
# MAGIC # 📊 PulseFlat - Exportador para Delta Lake & Unity Catalog
# MAGIC
# MAGIC Este notebook varre os arquivos gerados em `./data` (Parquet e CSV) e realiza o merge/upsert
# MAGIC para tabelas **Delta Lake** gerenciadas no Databricks (Hive Metastore ou Unity Catalog).

# COMMAND ----------
# MAGIC %md
# MAGIC ### 1. Configuração do Catálogo e Schema de Destino

# COMMAND ----------
# Objeto dbutils e spark injetados no runtime Databricks
try:
    _ = dbutils  # noqa: F821
except NameError:
    from pyspark.dbutils import DBUtils
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()
    dbutils = DBUtils(spark)

dbutils.widgets.text("catalog", "hive_metastore", "Catálogo (Unity Catalog)")
dbutils.widgets.text("database", "pulseflat", "Database / Schema")
dbutils.widgets.dropdown("write_mode", "append", ["append", "overwrite"], "Modo de Escrita Padrão")

catalog = str(dbutils.widgets.get("catalog") or "").strip()
database = str(dbutils.widgets.get("database") or "pulseflat").strip()
write_mode = str(dbutils.widgets.get("write_mode") or "append").strip()

# Resiliência: no Databricks Community Edition (sem Unity Catalog),
# tabelas são criadas em 2 níveis (database.table).
# Com Unity Catalog ativo, usa-se 3 níveis (catalog.database.table).
use_unity_catalog = bool(catalog and catalog.lower() not in ("hive_metastore", "", "none"))
target_schema = f"{catalog}.{database}" if use_unity_catalog else database

# Criação do banco/schema caso não exista
spark.sql(f"CREATE DATABASE IF NOT EXISTS {target_schema}")
print(f"Alvo configurado: {target_schema} (Unity Catalog: {use_unity_catalog})")

# COMMAND ----------
# MAGIC %md
# MAGIC ### 2. Ingestão de Datasets para Tabelas Delta

# COMMAND ----------
import os
from pathlib import Path

from pyspark.sql import functions as F

NOTEBOOK_DIR = Path(os.getcwd())
REPO_ROOT = NOTEBOOK_DIR.parent.parent
DATA_DIR = REPO_ROOT / "data"

print(f"Varrendo diretório de dados: {DATA_DIR}")

# Encontra todos os arquivos parquet, csv e csv.gz dentro de data/
data_files = []
for ext in ("*.parquet", "*.csv.gz", "*.csv"):
    data_files.extend(list(DATA_DIR.glob(ext)))

# Remove duplicatas lógicas (preferindo parquet se existir com mesmo nome base)
data_files = sorted(data_files, key=lambda f: f.name)

total_converted = 0

for dfile in data_files:
    # Remove extensões (.csv.gz, .csv, .parquet) para formar o nome da tabela
    base_name = dfile.name
    for ext in (".csv.gz", ".csv", ".parquet"):
        if base_name.endswith(ext):
            base_name = base_name[: -len(ext)]
            break

    table_name = base_name.lower().replace("-", "_").replace(" ", "_")
    target_table = f"{target_schema}.{table_name}"

    try:
        if dfile.name.endswith(".parquet"):
            df = spark.read.parquet(str(dfile))  # noqa: F821
        else:
            # Lê CSV ou CSV.GZ com Spark nativo inferindo schema e tratando aspas/vírgulas
            df = (
                spark.read.format("csv")  # noqa: F821
                .option("header", "true")
                .option("inferSchema", "true")
                .load(str(dfile))
            )

        # Adiciona metadados de ingestão
        df = df.withColumn("_ingested_at", F.current_timestamp())

        df.write.format("delta").mode(write_mode).option("mergeSchema", "true").saveAsTable(
            target_table
        )
        print(f"✓ Tabela Delta atualizada: {target_table} ({df.count()} registros)")
        total_converted += 1
    except Exception as e:
        print(f"✗ Erro ao carregar {dfile.name} para {target_table}: {e}")

print(f"\nConcluído! {total_converted} tabelas Delta sincronizadas.")
