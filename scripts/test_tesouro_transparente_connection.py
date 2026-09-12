#!/usr/bin/env python
"""
scripts/test_tesouro_transparente_connection.py
-----------------------------------------------
Utilitário CLI para testar conectividade e resposta da API CKAN do Tesouro Nacional.

Uso:
  python scripts/test_tesouro_transparente_connection.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.tesouro_transparente_client import TesouroTransparenteClient
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
    banner("Tesouro Transparente — Teste de Conexão CKAN (Tesouro Nacional)")

    client = TesouroTransparenteClient()

    print(bold("1. Configuração do Endpoint CKAN:"))
    print_info(f"Base API : {cyan(client.base_url)}")
    print()

    print(bold("2. Testando Comunicação com a API CKAN (Package List)..."))
    result = client.test_connection()

    if result.get("ok"):
        print_done(f"Conexão com o Tesouro Transparente bem-sucedida! {b_green('✔')}")
        print(f"   Status HTTP : {b_green(str(result.get('status_code', 200)))}")
        print(f"   Latência    : {cyan(str(result.get('latency_seconds', '')) + ' segundos')}")
        print(
            f"   Pacotes     : {dim(str(result.get('sample_packages_count', '')) + ' pacotes verificados no catálogo')}"
        )
        print()
        print(b_green("Tudo pronto para plugar novos scrapers no Tesouro Transparente!"))
        return 0
    else:
        print_fail(f"Falha na comunicação com o Tesouro Transparente: {result.get('message')}")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
