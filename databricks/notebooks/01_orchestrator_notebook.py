# Databricks notebook source
# MAGIC %md
# MAGIC # ⚡ PulseFlat - Orquestrador Interativo (Databricks)
# MAGIC
# MAGIC Este notebook permite executar e depurar os pipelines de coleta do **PulseFlat** diretamente no Databricks.
# MAGIC Você pode filtrar por grupo de dados, selecionar scrapers individuais, e configurar execução concorrente.

# COMMAND ----------
# MAGIC %md
# MAGIC ### 1. Instalação e Verificação de Dependências

# COMMAND ----------
# MAGIC %pip install -r ../../requirements.txt --quiet

# COMMAND ----------
# MAGIC %md
# MAGIC ### 2. Configuração de Parâmetros (Widgets)

# COMMAND ----------
# Objeto dbutils injetado no runtime Databricks
try:
    _ = dbutils  # noqa: F821
except NameError:
    from pyspark.dbutils import DBUtils
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()
    dbutils = DBUtils(spark)

# Criação de widgets interativos no topo do notebook
dbutils.widgets.dropdown(
    "group",
    "all",
    ["all", "anbima", "bcb", "b3", "cvm", "fred", "ibge", "global", "ratings", "misc"],
    "Grupo de Dados",
)
dbutils.widgets.text("scraper", "", "Scraper Específico (opcional)")
dbutils.widgets.dropdown("mode", "parallel", ["parallel", "sequential"], "Modo de Execução")
dbutils.widgets.text("max_workers", "8", "Workers Concorrentes")
dbutils.widgets.dropdown("check_holes", "false", ["true", "false"], "Verificar Buracos Históricos")

# COMMAND ----------
# MAGIC %md
# MAGIC ### 3. Setup de Ambiente e Segredos

# COMMAND ----------
import os
import sys
from pathlib import Path

# Localiza a raiz do repositório no Workspace
NOTEBOOK_DIR = Path(os.getcwd())
REPO_ROOT = NOTEBOOK_DIR.parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.chdir(str(REPO_ROOT))

# Carrega segredos se disponíveis no Scope 'pulseflat'
SECRET_SCOPE = "pulseflat"
KEYS = [
    "ORACLE_DB_DSN",
    "ORACLE_DB_USER",
    "ORACLE_DB_PASSWORD",
    "ORACLE_DB_WALLET_PASSWORD",
    "ORACLE_DB_WALLET_BASE64",
    "ANBIMA_CLIENT_ID",
    "ANBIMA_CLIENT_SECRET",
    "EULERPOOL_API_KEY",
    "FRED_API_KEY",
]

for key in KEYS:
    if not os.getenv(key):
        try:
            val = dbutils.secrets.get(scope=SECRET_SCOPE, key=key)
            if val:
                os.environ[key] = val
        except Exception:
            pass

# Setup de Wallet Oracle se aplicável
wallet_b64 = os.getenv("ORACLE_DB_WALLET_BASE64")
if wallet_b64 and not os.getenv("ORACLE_DB_WALLET_DIR"):
    import base64
    import zipfile
    from io import BytesIO

    wallet_dir = Path("/tmp/oracle_wallet")
    wallet_dir.mkdir(parents=True, exist_ok=True)
    zip_data = base64.b64decode(wallet_b64)
    with zipfile.ZipFile(BytesIO(zip_data)) as z:
        z.extractall(wallet_dir)
    os.environ["ORACLE_DB_WALLET_DIR"] = str(wallet_dir)

# COMMAND ----------
# MAGIC %md
# MAGIC ### 4. Execução do Pipeline PulseFlat

# COMMAND ----------
group = dbutils.widgets.get("group")
scraper = dbutils.widgets.get("scraper")
mode = dbutils.widgets.get("mode")
max_workers = dbutils.widgets.get("max_workers")
check_holes = dbutils.widgets.get("check_holes") == "true"

args = []
if group and group != "all":
    args.extend(["--group", group])

if scraper.strip():
    args.extend(["--scraper", scraper.strip()])

if mode == "parallel":
    args.extend(["--parallel", "--max-workers", str(max_workers)])
else:
    args.append("--sequential")

if check_holes:
    args.append("--check-holes")

# Simula sys.argv para o orquestrador run_all
sys.argv = ["run_all.py"] + args

import run_all

print(f"Disparando PulseFlat com argumentos: {args}")
run_all.main()
