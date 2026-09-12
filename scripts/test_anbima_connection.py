#!/usr/bin/env python
"""
scripts/test_anbima_connection.py
---------------------------------
Utilitário CLI para testar e validar as credenciais e conectividade com
o portal ANBIMA Data / Developers (OAuth 2.0).

Uso:
  python scripts/test_anbima_connection.py
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_client import AnbimaDataClient
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
    banner("ANBIMA Data — Teste de Conexão e Autenticação")

    client = AnbimaDataClient()

    print(bold("1. Verificando Configuração de Ambiente:"))
    if client.client_id:
        print_info(
            f"ANBIMA_CLIENT_ID : {cyan(client.client_id[:6] + '...' if len(client.client_id) > 6 else client.client_id)}"
        )
    else:
        print_warn("ANBIMA_CLIENT_ID : (não configurado no .env)")

    if client.client_secret:
        print_info(f"ANBIMA_CLIENT_SECRET : {dim('********')}")
    else:
        print_warn("ANBIMA_CLIENT_SECRET : (não configurado no .env)")

    print_info(f"OAuth URL : {dim(client.oauth_url)}")
    print_info(f"Base API  : {dim(client.base_url)}")
    print()

    if not client.has_credentials:
        print_fail("Credenciais ausentes!")
        print()
        print(yellow("Para configurar o acesso à ANBIMA Developers:"))
        print(
            f"  1. Obtenha seu Client ID e Client Secret em: {cyan('https://developers.anbima.com.br/pt/')}"
        )
        print("  2. Adicione ao seu arquivo .env:")
        print("     ANBIMA_CLIENT_ID=seu_client_id_aqui")
        print("     ANBIMA_CLIENT_SECRET=seu_client_secret_aqui")
        print()
        return 1

    print(bold("2. Testando Troca de Token OAuth 2.0 (Client Credentials)..."))
    result = client.test_connection()

    if result.get("ok"):
        print_done(f"Autenticação bem-sucedida! {b_green('✔')}")
        print(f"   Token obtido   : {dim(result.get('token_sample', ''))}")
        print(
            f"   Tempo expiração: {cyan(str(result.get('expires_in_seconds', '')) + ' segundos')}"
        )
        print()
        print(b_green("Tudo pronto para plugar novos scrapers na ANBIMA Data!"))
        return 0
    else:
        print_fail(f"Falha na autenticação: {result.get('message')}")
        print()
        print(dim("Dica: Verifique se suas credenciais no .env estão ativas no portal ANBIMA."))
        return 1


if __name__ == "__main__":
    sys.exit(main())
