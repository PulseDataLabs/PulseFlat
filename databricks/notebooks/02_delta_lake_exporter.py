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

catalog = dbutils.widgets.get("catalog")
database = dbutils.widgets.get("database")
write_mode = dbutils.widgets.get("write_mode")

# Criação do banco/schema caso não exista
spark.sql(f"CREATE DATABASE IF NOT EXISTS {catalog}.{database}")  # noqa: F821
print(f"Alvo configurado: {catalog}.{database}")

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

# Encontra todos os arquivos parquet e csv dentro de data/
parquet_files = list(DATA_DIR.rglob("*.parquet"))

total_converted = 0

# Processa Parquets
for pfile in parquet_files:
    table_name = pfile.stem.lower().replace("-", "_").replace(" ", "_")
    target_table = f"{catalog}.{database}.{table_name}"

    try:
        df = spark.read.parquet(str(pfile))  # noqa: F821
        # Adiciona metadados de ingestão
        df = df.withColumn("_ingested_at", F.current_timestamp())

        df.write.format("delta").mode(write_mode).option("mergeSchema", "true").saveAsTable(
            target_table
        )
        print(f"✓ Tabela Delta atualizada: {target_table} ({df.count()} registros)")
        total_converted += 1
    except Exception as e:
        print(f"✗ Erro ao carregar {pfile.name} para {target_table}: {e}")

print(f"\nConcluído! {total_converted} tabelas Delta sincronizadas.")
