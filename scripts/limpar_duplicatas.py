"""
scripts/limpar_duplicatas.py
-----------------------------
Remove duplicatas dos CSVs históricos, mantendo apenas a captura mais
recente de cada combinação de chaves por dia.

Execute uma única vez para limpar o histórico acumulado:

    python scripts/limpar_duplicatas.py

A partir daí, salvar_csv() garante que novas execuções nunca dupliquem.
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

CONFIGS = [
    {
        "arquivo":    Path("data/anbima_indicadores.csv"),
        "chaves":     ["data_captura", "indicador"],
        "ordenar_por": ["data_captura", "hora_captura"],
    },
    {
        "arquivo":    Path("data/anbima_projecoes.csv"),
        "chaves":     ["data_captura", "indice", "mes_referencia", "tipo_projecao"],
        "ordenar_por": ["data_captura", "hora_captura"],
    },
    {
        "arquivo":    Path("data/b3_fiis_listados.csv"),
        "chaves":     ["data_captura", "codigo_fundo"],
        "ordenar_por": ["data_captura", "hora_captura"],
    },
    {
        "arquivo":    Path("data/b3_etfs_listados.csv"),
        "chaves":     ["data_captura", "categoria_etf", "codigo_fundo"],
        "ordenar_por": ["data_captura", "hora_captura"],
    },
    {
        "arquivo":    Path("data/b3_carteiras_teoricas.csv"),
        "chaves":     ["data_captura", "indice", "codigo_ativo"],
        "ordenar_por": ["data_captura", "hora_captura"],
    },
]


def limpar(arquivo: Path, chaves: list[str], ordenar_por: list[str]) -> None:
    if not arquivo.exists():
        print(f"[SKIP] {arquivo.name} — arquivo não encontrado.")
        return

    with arquivo.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cabecalho = list(reader.fieldnames or [])
        linhas = list(reader)

    total_antes = len(linhas)

    # Ordena para que a entrada MAIS RECENTE fique por último
    linhas.sort(key=lambda r: tuple(r.get(c, "") for c in ordenar_por))

    # Mantém apenas a última ocorrência de cada chave composta
    vistos: dict[tuple, dict] = {}
    for linha in linhas:
        chave = tuple(linha.get(c, "") for c in chaves)
        vistos[chave] = linha  # sobrescreve — fica o mais recente

    resultado = list(vistos.values())
    total_depois = len(resultado)
    removidas = total_antes - total_depois

    with arquivo.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cabecalho, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(resultado)

    status = f"{removidas} duplicata(s) removida(s)" if removidas else "sem duplicatas"
    print(f"[OK] {arquivo.name}: {total_antes} → {total_depois} linhas ({status}).")


if __name__ == "__main__":
    print("Limpando duplicatas nos CSVs históricos...\n")
    for cfg in CONFIGS:
        limpar(**cfg)
    print("\nConcluído.")
