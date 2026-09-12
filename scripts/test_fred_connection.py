#!/usr/bin/env python
"""
scripts/test_fred_connection.py
-------------------------------
Utilitário CLI para testar conectividade e autenticação com a API do FRED (St. Louis Fed).

Uso:
  python scripts/test_fred_connection.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.fred_client import FredClient
from scripts.utils.ux import (
    b_green,
    banner,
    bold,
    cyan,
    dim,
    print_done,
    print_fail,
    print_info,
    print_warn,
    yellow,
)


def main():
    banner("FRED — Teste de Conexão e Autenticação (Federal Reserve Economic Data)")

    client = FredClient()

    print(bold("1. Verificando Configuração de Ambiente:"))
    if client.api_key:
        print_info(
            f"FRED_API_KEY : {cyan(client.api_key[:6] + '...' if len(client.api_key) > 6 else client.api_key)}"
        )
    else:
        print_warn("FRED_API_KEY : (não configurado no .env)")

    print_info(f"Base API     : {dim(client.base_url)}")
    print()

    if not client.has_credentials:
        print_fail("API Key ausente!")
        print()
        print(yellow("Para configurar o acesso ao FRED:"))
        print(
            f"  1. Crie sua conta e gere uma chave gratuita em: {cyan('https://fred.stlouisfed.org/docs/api/api_key.html')}"
        )
        print("  2. Adicione ao seu arquivo .env:")
        print("     FRED_API_KEY=sua_chave_aqui")
        print()
        return 1

    print(bold("2. Testando Comunicação com a API do FRED (Série DGS10 - US 10Y)..."))
    result = client.test_connection()

    if result.get("ok"):
        print_done(f"Conexão e Autenticação com o FRED bem-sucedidas! {b_green('✔')}")
        print(f"   API Key ativa : {dim(result.get('api_key_sample', ''))}")
        print(f"   Latência      : {cyan(str(result.get('latency_seconds', '')) + ' segundos')}")
        print()
        print(b_green("Tudo pronto para plugar novos scrapers no FRED!"))
        return 0
    else:
        print_fail(f"Falha na comunicação/autenticação: {result.get('message')}")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
