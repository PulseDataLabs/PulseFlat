"""
scrapers/bacen_negociacao_tpf.py
---------------------------------
Captura dados de negociacao de Titulos Publicos Federais (TPF)
Extra-grupo do Banco Central (BCB/DEMAB).

Fontes:
  - https://www4.bcb.gov.br/pom/demab/negociacoes/download/NegEYYYYMM.ZIP
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import get_logger, nova_session, salvar_csv
from utils.parsers import date_ref, replace_date_vars, rows_from_zip, enriquecer, read_existing_header

log = get_logger("bacen_negociacao_tpf")

URL_TPLT = "https://www4.bcb.gov.br/pom/demab/negociacoes/download/NegEYYYYMM.ZIP"
ARQUIVOS = [
    {
        "id": "bacen_negociacao_tpf_extragrupo_mes_corrente",
        "arquivo": Path("data/bacen_negociacao_tpf_extragrupo_mes_corrente.csv"),
    },
    {
        "id": "bacen_negociacao_tpf_extragrupo_mes_anterior",
        "arquivo": Path("data/bacen_negociacao_tpf_extragrupo_mes_anterior.csv"),
    },
]


def capturar() -> list[dict]:
    session = nova_session()
    registros = []

    for cfg in ARQUIVOS:
        dataset_id = cfg["id"]
        arquivo = cfg["arquivo"]

        if "anterior" in dataset_id:
            dt = date_ref("mes_anterior")
        else:
            dt = date_ref(None)

        url = replace_date_vars(URL_TPLT, dt)
        log.info(f"[{dataset_id}] Baixando {url}")

        try:
            resp = session.get(url, timeout=120)
            resp.raise_for_status()
            rows = rows_from_zip(resp.content)
            if not rows:
                raise RuntimeError("Sem linhas apos processamento")

            enriched, header_novo = enriquecer(dataset_id, rows)
            header_existente = read_existing_header(arquivo)
            header = []
            for col in header_existente + header_novo:
                if col and col not in header:
                    header.append(col)

            salvar_csv(arquivo, enriched, header, chaves_dedup=["data_captura", "conjunto", "registro_hash"])
            log.info(f"[{dataset_id}] {len(enriched)} linha(s) salvas")
            registros.extend(enriched)
        except Exception as e:
            log.error(f"[{dataset_id}] Falha: {e}")

    return registros


def main():
    log.info("=== BCB — Negociacao TPF Extra-grupo ===")
    capturar()


if __name__ == "__main__":
    main()
