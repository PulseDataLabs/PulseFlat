"""
PulseFlat - Databricks Entrypoint Job
=====================================
Script para execução via Databricks Workflows (Python script task).

Permite executar o pipeline completo do PulseFlat (ou grupos específicos)
diretamente em um cluster Databricks ou Serverless Compute.

Compatível com:
  1. Databricks Git Folders (Repos)
  2. Workspace Files
  3. sys.argv / argparse para passagem de parâmetros do Job
  4. Databricks Secrets com fallback transparente para os.environ
"""

import argparse
import os
import sys
from pathlib import Path

# ── 1. Garantir que a raiz do repositório está no sys.path ────────────────────
CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Muda o CWD para a raiz do repositório para garantir caminhos relativos consistentes
os.chdir(str(REPO_ROOT))


# ── 2. Carregar segredos do Databricks (se disponíveis) ──────────────────────
def load_databricks_secrets(scope_name: str = "pulseflat") -> None:
    """Tenta carregar segredos do Databricks Secret Scope para os.environ.
    Se o scope não existir ou estiver rodando fora do Databricks, ignora silenciosamente.
    """
    try:
        from pyspark.dbutils import DBUtils
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.getOrCreate()
        dbutils = DBUtils(spark)

        keys = [
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

        for key in keys:
            if not os.getenv(key):
                try:
                    val = dbutils.secrets.get(scope=scope_name, key=key)
                    if val:
                        os.environ[key] = val
                except Exception:
                    pass
    except Exception:
        pass


# ── 3. Extração de Wallet Oracle se fornecida em base64 ───────────────────────
def setup_oracle_wallet() -> None:
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
        print(f"✓ Oracle Wallet configurada em: {wallet_dir}")


# ── 4. Parse de Parâmetros e Execução ─────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="⚡ PulseFlat – Databricks Workflow Job Runner"
    )
    parser.add_argument("--group", help="Filtra por grupo de scrapers (ex: anbima, bcb, b3)")
    parser.add_argument("--scraper", help="Executa um scraper específico")
    parser.add_argument(
        "--parallel",
        action="store_true",
        default=True,
        help="Execução paralela (padrão: True)",
    )
    parser.add_argument(
        "--sequential",
        action="store_false",
        dest="parallel",
        help="Execução sequencial",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Quantidade de workers paralelos (padrão: 4)",
    )
    parser.add_argument(
        "--check-holes",
        action="store_true",
        help="Executa verificação de buracos pós-coleta",
    )
    parser.add_argument(
        "--fail-on-holes",
        action="store_true",
        help="Falha se encontrar datas faltantes",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Lista os scrapers disponíveis",
    )
    return parser.parse_args()


def main() -> None:
    load_databricks_secrets()
    setup_oracle_wallet()

    args = parse_args()

    import run_all
    from utils.base import acquire_lock

    if args.list:
        run_all.main(
            group=args.group,
            scraper=args.scraper,
            parallel=args.parallel,
            max_workers=args.max_workers,
            list_only=True,
            check_holes=args.check_holes,
            fail_on_holes=args.fail_on_holes,
        )
    else:
        with acquire_lock("pulseflat_databricks", blocking=True):
            run_all.main(
                group=args.group,
                scraper=args.scraper,
                parallel=args.parallel,
                max_workers=args.max_workers,
                list_only=False,
                check_holes=args.check_holes,
                fail_on_holes=args.fail_on_holes,
            )


if __name__ == "__main__":
    main()
