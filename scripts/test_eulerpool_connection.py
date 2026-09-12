#!/usr/bin/env python
"""
scripts/test_eulerpool_connection.py
------------------------------------
Utilitário CLI para testar e validar a chave de API e conectividade com
a API REST da Eulerpool Financial Data (https://api.eulerpool.com).

Uso:
  python scripts/test_eulerpool_connection.py
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.eulerpool_client import EulerpoolClient
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
    banner("Eulerpool Financial Data — Teste de Conexão e Autenticação")

    client = EulerpoolClient()

    print(bold("1. Verificando Configuração de Ambiente:"))
    if client.api_key:
        print_info(
            f"EULERPOOL_API_KEY : {cyan(client.api_key[:6] + '...' if len(client.api_key) > 6 else client.api_key)}"
        )
    else:
        print_warn("EULERPOOL_API_KEY : (não configurado no .env)")

    print_info(f"Base API          : {dim(client.base_url)}")
    print()

    if not client.has_credentials:
        print_fail("API Key ausente!")
        print()
        print(yellow("Para configurar o acesso à Eulerpool Financial Data:"))
        print(f"  1. Obtenha sua chave gratuita em: {cyan('https://eulerpool.com/developers')}")
        print("  2. Adicione ao seu arquivo .env:")
        print("     EULERPOOL_API_KEY=sua_chave_aqui")
        print()
        return 1

    print(bold("2. Testando Comunicação e Autenticação com a Eulerpool API..."))
    result = client.test_connection()

    if result.get("ok"):
        print_done(f"Conexão e Autenticação bem-sucedidas! {b_green('✔')}")
        print(f"   API Key ativa : {dim(result.get('api_key_sample', ''))}")
        print(f"   Endpoint base : {dim(result.get('base_url', ''))}")
        print()
        print(b_green("Tudo pronto para plugar novos scrapers na API da Eulerpool!"))
        return 0
    else:
        print_fail(f"Falha na comunicação/autenticação: {result.get('message')}")
        print()
        print(
            dim(
                "Dica: Verifique se sua chave no .env está ativa no portal eulerpool.com/developers."
            )
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
