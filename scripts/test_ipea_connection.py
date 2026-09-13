#!/usr/bin/env python
"""
scripts/test_ipea_connection.py
-------------------------------
Utilitário CLI para testar conectividade, latência e integridade com a API OData v4 do IPEADATA.

Uso:
  python scripts/test_ipea_connection.py
  python scripts/test_ipea_connection.py --serie IGP12_IGPDI12
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.ipea_client import IpeaClient
from scripts.utils.ux import (
    b_green,
    banner,
    bold,
    cyan,
    dim,
    print_done,
    print_fail,
    print_info,
    yellow,
)


def main():
    parser = argparse.ArgumentParser(description="Testa a conectividade com a API do IPEADATA.")
    parser.add_argument(
        "--serie",
        default="BM12_TJOVER12",
        help="Código da série para teste (padrão: BM12_TJOVER12 - Selic Over Mensal).",
    )
    args = parser.parse_args()

    banner("IPEADATA — Diagnóstico de Conexão (API OData v4)")

    client = IpeaClient()

    print(bold("1. Configurações de Acesso:"))
    print_info(f"Base API     : {cyan(client.base_url)}")
    print_info(f"Fallback URL : {dim(client.FALLBACK_BASE_URL)}")
    print_info(f"Autenticação : {b_green('Pública / Open Access (sem chave exigida)')}")
    print()

    print(bold(f"2. Testando Comunicação OData (Série: {cyan(args.serie)})..."))
    result = client.test_connection(test_serie=args.serie)

    if result.get("ok"):
        print_done(f"Conexão com a API do IPEADATA bem-sucedida! {b_green('✔')}")
        print(f"   Série testada        : {cyan(result.get('serie_testada', ''))}")
        print(f"   Nome                 : {bold(result.get('serie_nome', ''))}")
        print(f"   Periodicidade        : {result.get('periodicidade', '')}")
        print(f"   Unidade              : {result.get('unidade', '')}")
        print(f"   Fonte Primária       : {dim(result.get('fonte', ''))}")
        print(f"   Latência de Resposta : {yellow(str(result.get('latency_ms', '')) + ' ms')}")
        print(f"   Amostras Retornadas  : {b_green(str(result.get('amostras_retornadas', '')) + ' observações')}")
        print()
        print(b_green("Tudo pronto para execução dos scrapers do IPEADATA no PulseFlat!"))
        return 0
    else:
        print_fail(f"Falha na comunicação com o IPEADATA: {result.get('error')}")
        print()
        print(yellow("Dicas de resolução:"))
        print("  1. Verifique sua conexão à internet e a resolução DNS para ipeadata.gov.br.")
        print("  2. O servidor do IPEA pode estar momentaneamente indisponível.")
        print("  3. Teste acessar diretamente no navegador: http://www.ipeadata.gov.br/api/odata4/")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
