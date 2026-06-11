"""
scripts/padronizar_datasets.py
-------------------------------
Aplica padronização em todos os CSVs de data/:
  - Corrige nomes de coluna afetados por acentos removidos (NFKD)
  - Padroniza formatos de data para ISO YYYY-MM-DD
  - Move data_captura para posição 0
  - Renomeia colunas Unnamed em bacen_conglomerados.csv
"""

import csv, re, os, shutil
from pathlib import Path
from collections import OrderedDict

DATA = Path("data")

# ── Mapa de renomeação de colunas corrompidas ──────────────────────────
RENAMES: dict[str, dict[str, str]] = {
    "anbima_indice_imab.csv": {
        "data_de_refer_ncia": "data_de_referencia",
        "duration_d_u": "duration_du",
        "n_mero_ndice": "numero_indice",
        "ndice": "indice",
        "varia_o_12_meses": "variacao_12_meses",
        "varia_o_24_meses": "variacao_24_meses",
        "varia_o_di_ria": "variacao_diaria",
        "varia_o_no_ano": "variacao_no_ano",
        "varia_o_no_m_s": "variacao_no_mes",
    },
    "debentures_mercado_secundario_precos_negociacao.csv": {
        "c_digo_do_ativo": "codigo_do_ativo",
        "n_mero_de_neg_cios": "numero_de_negocios",
        "pu_m_nimo": "pu_minimo",
        "pu_m_dio": "pu_medio",
        "pu_m_ximo": "pu_maximo",
    },
}

# ── Arquivos que precisam ter data_captura movida para pos 0 ──────────
REORDER_DATA_CAPTURA = [
    "anbima_debentures.csv",        # pos 16 → 0
    "debentures_mercado_secundario_precos_negociacao.csv",  # pos 10 → 0
    "debentures_emissoes_caracteristicas.csv",  # pos 84 → 0
]

# ── Arquivos com datas não-ISO ─────────────────────────────────────────
DATE_FIXES: dict[str, dict[str, str]] = {
    "anbima_matriz_probabilidade_resgate.csv": {
        "data": "YYYY/MM/DD",  # formato atual
    },
    "debentures_mercado_secundario_precos_negociacao.csv": {
        "data": "D/M/YYYY",    # formato atual
    },
}


def ler_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames[:]
        rows = list(reader)
    return header, rows


def escrever_csv(path: Path, header: list[str], rows: list[dict]):
    tmp = path.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    shutil.move(str(tmp), str(path))


def renomear_colunas(header: list[str], renames: dict[str, str]) -> list[str]:
    return [renames.get(col, col) for col in header]


def renomear_nas_linhas(rows: list[dict], renames: dict[str, str]) -> list[dict]:
    out = []
    for row in rows:
        new_row: dict[str, str] = {}
        for k, v in row.items():
            new_row[renames.get(k, k)] = v
        out.append(new_row)
    return out


def mover_data_captura(header: list[str], rows: list[dict]) -> tuple[list[str], list[dict]]:
    if "data_captura" not in header:
        return header, rows
    if header[0] == "data_captura":
        return header, rows  # já está na pos 0
    new_header = ["data_captura"] + [c for c in header if c != "data_captura"]
    new_rows = []
    for row in rows:
        new_row: dict[str, str] = {}
        new_row["data_captura"] = row["data_captura"]
        for k, v in row.items():
            if k != "data_captura":
                new_row[k] = v
        new_rows.append(new_row)
    return new_header, new_rows


def parse_date_ymd_slash(val: str) -> str:
    """Converte YYYY/MM/DD → YYYY-MM-DD"""
    val = val.strip()
    if not val or "-" in val:
        return val
    m = re.match(r"^(\d{4})/(\d{1,2})/(\d{1,2})$", val)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return val


def parse_date_dmy(val: str) -> str:
    """Converte D/M/YYYY ou DD/MM/YYYY → YYYY-MM-DD"""
    val = val.strip()
    if not val or "-" in val:
        return val
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", val)
    if m:
        return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    return val


def fixar_datas(header: list[str], rows: list[dict], fixes: dict[str, str]) -> list[dict]:
    for col, fmt in fixes.items():
        if col not in header:
            continue
        parser = {"YYYY/MM/DD": parse_date_ymd_slash, "D/M/YYYY": parse_date_dmy}.get(fmt)
        if not parser:
            continue
        for row in rows:
            row[col] = parser(row[col])
    return rows


def fix_bacen_conglomerados(header: list[str], rows: list[dict]) -> tuple[list[str], list[dict]]:
    renames = {
        "BANCO CENTRAL DO BRASIL - BACEN": "departamento",
        "Unnamed: 1": "secao_1",
        "Unnamed: 2": "secao_2",
        "Unnamed: 3": "secao_3",
        "Unnamed: 4": "tipo_documento",
        "Unnamed: 5": "data_documento",
        "Unnamed: 6": "detalhe",
    }
    header = renomear_colunas(header, renames)
    rows = renomear_nas_linhas(rows, renames)
    return header, rows


def processar():
    # ── 1. Renomear colunas corrompidas ──────────────────────────────────
    for fname, renames in RENAMES.items():
        path = DATA / fname
        if not path.exists():
            print(f"  [SKIP] {fname} — não encontrado")
            continue
        header, rows = ler_csv(path)
        header = renomear_colunas(header, renames)
        rows = renomear_nas_linhas(rows, renames)
        escrever_csv(path, header, rows)
        print(f"  [OK] {fname} — colunas renomeadas")

    # ── 2. Consertar bacen_conglomerados.csv ──────────────────────────────
    path = DATA / "bacen_conglomerados.csv"
    if path.exists():
        header, rows = ler_csv(path)
        header, rows = fix_bacen_conglomerados(header, rows)
        escrever_csv(path, header, rows)
        print(f"  [OK] bacen_conglomerados.csv — Unnamed renomeadas")

    # ── 3. Padronizar datas ───────────────────────────────────────────────
    for fname, fixes in DATE_FIXES.items():
        path = DATA / fname
        if not path.exists():
            print(f"  [SKIP] {fname} — não encontrado")
            continue
        header, rows = ler_csv(path)
        rows = fixar_datas(header, rows, fixes)
        escrever_csv(path, header, rows)
        print(f"  [OK] {fname} — datas padronizadas")

    # ── 4. Mover data_captura para pos 0 ─────────────────────────────────
    for fname in REORDER_DATA_CAPTURA:
        path = DATA / fname
        if not path.exists():
            print(f"  [SKIP] {fname} — não encontrado")
            continue
        header, rows = ler_csv(path)
        header, rows = mover_data_captura(header, rows)
        escrever_csv(path, header, rows)
        print(f"  [OK] {fname} — data_captura movida para pos 0")

    print("\n  Todos os CSVs padronizados com sucesso.")


if __name__ == "__main__":
    processar()
