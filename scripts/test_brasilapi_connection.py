#!/usr/bin/env python
"""
scripts/test_brasilapi_connection.py
------------------------------------
Utilitário CLI para testar conectividade e latência com a BrasilAPI
(https://brasilapi.com.br/api).

Uso:
  python scripts/test_brasilapi_connection.py
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.brasilapi_client import BrasilApiClient
from scripts.utils.ux import (
    b_green,
    banner,
    bold,
    cyan,
    dim,
    print_done,
    print_fail,
    print_info,
)


def main():
    banner("BrasilAPI — Teste de Conexão e Latência")

    client = BrasilApiClient()

    print(bold("1. Configuração do Endpoint:"))
    print_info(f"Base API : {cyan(client.base_url)}")
    print()

    print(bold("2. Testando Comunicação com a BrasilAPI (/taxas/v1)..."))
    result = client.test_connection()

    if result.get("ok"):
        print_done(f"Conexão com a BrasilAPI bem-sucedida! {b_green('✔')}")
        print(f"   Status HTTP : {b_green(str(result.get('status_code', 200)))}")
        print(f"   Latência    : {cyan(str(result.get('latency_seconds', '')) + ' segundos')}")
        print(
            f"   Registros   : {dim(str(result.get('sample_count', '')) + ' itens retornados no teste')}"
        )
        print()
        print(b_green("Tudo pronto para plugar novos scrapers na BrasilAPI!"))
        return 0
    else:
        print_fail(f"Falha na comunicação: {result.get('message')}")
        print(f"   Latência registrada: {dim(str(result.get('latency_seconds', '')) + 's')}")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
