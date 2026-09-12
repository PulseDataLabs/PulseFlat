#!/usr/bin/env python
"""
scripts/test_bcb_olinda_connection.py
-------------------------------------
Utilitário CLI para testar conectividade e resposta da API OData do Banco Central (Olinda).

Uso:
  python scripts/test_bcb_olinda_connection.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.bcb_olinda_client import BcbOlindaClient
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
    banner("BCB Olinda — Teste de Conexão OData (Banco Central)")

    client = BcbOlindaClient()

    print(bold("1. Configuração do Endpoint OData:"))
    print_info(f"Base API : {cyan(client.base_url)}")
    print()

    print(bold("2. Testando Comunicação com a API OData do BCB (Boletim Focus)..."))
    result = client.test_connection()

    if result.get("ok"):
        print_done(f"Conexão com o BCB Olinda bem-sucedida! {b_green('✔')}")
        print(f"   Status HTTP : {b_green(str(result.get('status_code', 200)))}")
        print(f"   Latência    : {cyan(str(result.get('latency_seconds', '')) + ' segundos')}")
        print(
            f"   Amostra     : {dim(str(result.get('sample_count', '')) + ' registro(s) OData recebido(s)')}"
        )
        print()
        print(b_green("Tudo pronto para plugar novos scrapers no BCB Olinda!"))
        return 0
    else:
        print_fail(f"Falha na comunicação com o BCB Olinda: {result.get('message')}")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
