"""
scripts/engordar_debentures_api.py
---------------------------------
Utilitário para migrar e engordar o arquivo
`data/debentures_mercado_secundario_precos_negociacao_api.csv.gz`
com todo o histórico retroativo (desde 2020) existente em
`data/debentures_mercado_secundario_precos_negociacao.csv.gz`.

Preserva dados completos da API oficial (taxas indicativas, REUNE, etc.)
para as datas já coletadas via API e complementa todo o histórico anterior
com mapeamento de colunas, cálculo exato de volume financeiro e re-hashing
padrão PulseFlat.
"""

import json
import sys
import time
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.base import get_logger
from utils.parsers import hash_row

log = get_logger("engordar_debentures_api")

COLUNAS_API = [
    "data_captura",
    "data_referencia",
    "emissor",
    "codigo_ativo",
    "isin",
    "quantidade",
    "numero_de_negocios",
    "pu_minimo",
    "pu_medio",
    "pu_maximo",
    "pu_da_curva",
    "pu_indicativo",
    "taxa_indicativa",
    "taxa_compra",
    "taxa_venda",
    "percentual_taxa",
    "volume_total_rs",
    "percent_reune",
    "data_vencimento",
    "registro_hash",
]


def format_pu(val) -> str:
    if val is None or pd.isna(val):
        return ""
    s = str(val).strip()
    if s in ("", "-", "nan", "None"):
        return ""
    try:
        f = float(s)
        return f"{f:.6f}".rstrip("0").rstrip(".")
    except ValueError:
        return s


def format_int_str(val) -> str:
    if val is None or pd.isna(val):
        return "0"
    s = str(val).strip()
    if s in ("", "-", "nan", "None"):
        return "0"
    try:
        f = float(s)
        return str(int(round(f)))
    except ValueError:
        return s


def calcular_volume(qtd_str: str, pu_med_str: str) -> str:
    try:
        qtd = float(qtd_str)
        pu = float(pu_med_str)
        if qtd > 0 and pu > 0:
            return f"{(qtd * pu):.2f}"
    except (ValueError, TypeError):
        pass
    return "0.00"


def atualizar_last_updates(min_date: str, max_date: str):
    """Atualiza last_updates.json e last_updates.js."""
    target_file_json = ROOT_DIR / "data" / "last_updates.json"
    target_file_js = ROOT_DIR / "data" / "last_updates.js"
    dataset_key = "debentures_mercado_secundario_precos_negociacao_api.csv.gz"

    if target_file_json.exists():
        try:
            with target_file_json.open("r", encoding="utf-8") as f:
                data = json.load(f)
            data[dataset_key] = {"min": min_date, "max": max_date}
            with target_file_json.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            log.info(f"last_updates.json atualizado: {min_date} a {max_date}")
        except Exception as e:
            log.warning(f"Erro ao atualizar last_updates.json: {e}")

    if target_file_js.exists():
        try:
            with target_file_json.open("r", encoding="utf-8") as f:
                data = json.load(f)
            with target_file_js.open("w", encoding="utf-8") as f:
                f.write(
                    f"window.PULSEFLAT_LAST_UPDATES = {json.dumps(data, indent=2, ensure_ascii=False)};\n"
                )
            log.info("last_updates.js atualizado.")
        except Exception as e:
            log.warning(f"Erro ao atualizar last_updates.js: {e}")


def run():
    f_snd = ROOT_DIR / "data" / "debentures_mercado_secundario_precos_negociacao.csv.gz"
    f_api = ROOT_DIR / "data" / "debentures_mercado_secundario_precos_negociacao_api.csv.gz"
    backups_dir = ROOT_DIR / "data" / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)

    if not f_snd.exists():
        log.error(f"Arquivo legado de origem não encontrado: {f_snd}")
        return

    log.info(f"1. Carregando arquivo legado SND: {f_snd.name}...")
    t0 = time.time()
    df_snd = pd.read_csv(f_snd, dtype=str, keep_default_na=False)
    log.info(f"   Carregados {len(df_snd)} registros em {time.time() - t0:.2f}s.")

    # Deduplica o SND por (data_referencia, codigo_ativo) mantendo a captura mais recente
    df_snd.drop_duplicates(subset=["data_referencia", "codigo_ativo"], keep="last", inplace=True)
    log.info(f"   Registros únicos no SND após dedup: {len(df_snd)}")

    # Carrega arquivo atual da API (se existir)
    df_api_existente = pd.DataFrame()
    if f_api.exists():
        log.info(f"2. Carregando arquivo atual da API: {f_api.name}...")
        df_api_existente = pd.read_csv(f_api, dtype=str, keep_default_na=False)
        log.info(f"   API existente possui {len(df_api_existente)} registros.")

    # Mapeamento e transformação dos dados do SND
    log.info("3. Mapeando e transformando registros do SND legado para o formato da API...")
    t1 = time.time()

    novos_registros = []
    for row in df_snd.to_dict(orient="records"):
        dt_ref = str(row.get("data_referencia", "")).strip()
        ticker = str(row.get("codigo_ativo", "")).strip()
        if not dt_ref or not ticker:
            continue

        qtd_str = format_int_str(row.get("quantidade"))
        neg_str = format_int_str(row.get("numero_de_negocios"))
        pu_min = format_pu(row.get("pu_minimo"))
        pu_med = format_pu(row.get("pu_medio"))
        pu_max = format_pu(row.get("pu_maximo"))
        pu_curva = format_pu(row.get("pu_da_curva"))

        vol_total = calcular_volume(qtd_str, pu_med)

        dt_cap = str(row.get("data_captura", "")).strip()
        if not dt_cap or dt_cap in ("nan", "None"):
            dt_cap = dt_ref

        rec = {
            "data_captura": dt_cap,
            "data_referencia": dt_ref,
            "emissor": str(row.get("emissor", "")).strip(),
            "codigo_ativo": ticker,
            "isin": str(row.get("isin", "")).strip(),
            "quantidade": qtd_str,
            "numero_de_negocios": neg_str,
            "pu_minimo": pu_min,
            "pu_medio": pu_med,
            "pu_maximo": pu_max,
            "pu_da_curva": pu_curva,
            "pu_indicativo": "",
            "taxa_indicativa": "",
            "taxa_compra": "",
            "taxa_venda": "",
            "percentual_taxa": "",
            "volume_total_rs": vol_total,
            "percent_reune": "",
            "data_vencimento": "",
        }
        novos_registros.append(rec)

    df_snd_transformado = pd.DataFrame(novos_registros)
    log.info(
        f"   Transformação concluída em {time.time() - t1:.2f}s ({len(df_snd_transformado)} registros)."
    )

    # Unificação: se o registro já existe no arquivo da API (com taxas/dados oficiais da API), ele tem preferência.
    log.info("4. Unificando dados (priorizando dados nativos da API sobrepostos)...")
    if not df_api_existente.empty:
        for c in COLUNAS_API:
            if c not in df_api_existente.columns:
                df_api_existente[c] = ""

        # Mantém apenas registros da API que realmente possuem dados da API (pu_indicativo preenchido ou data recente)
        api_legitimos = df_api_existente[df_api_existente["pu_indicativo"] != ""]
        if api_legitimos.empty:
            api_legitimos = df_api_existente[df_api_existente["data_referencia"] >= "2026-09-10"]

        chaves_api = set(
            api_legitimos["data_referencia"].astype(str)
            + "_"
            + api_legitimos["codigo_ativo"].astype(str)
        )

        mask_novo = ~(
            df_snd_transformado["data_referencia"].astype(str)
            + "_"
            + df_snd_transformado["codigo_ativo"].astype(str)
        ).isin(chaves_api)

        df_snd_complementar = df_snd_transformado[mask_novo]
        log.info(
            f"   Registros do SND a incorporar (sem duplicar com API legítima): {len(df_snd_complementar)}"
        )
        cols_sem_hash = [c for c in COLUNAS_API if c != "registro_hash"]
        df_final = pd.concat(
            [df_snd_complementar[cols_sem_hash], api_legitimos[cols_sem_hash]], ignore_index=True
        )
    else:
        df_final = df_snd_transformado

    # Deduplicação final por segurança
    df_final.drop_duplicates(subset=["data_referencia", "codigo_ativo"], keep="last", inplace=True)

    # Cálculo dos hashes para integridade
    log.info("5. Calculando hashes PulseFlat (hash_row) para auditoria...")
    t2 = time.time()
    records_dict = df_final.to_dict(orient="records")
    new_hashes = [
        hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
        for r in records_dict
    ]
    df_final["registro_hash"] = new_hashes
    log.info(f"   Hashes calculados em {time.time() - t2:.2f}s.")

    # Ordenação cronológica e por ticker
    log.info("6. Ordenando dados por data_referencia e codigo_ativo...")
    df_final.sort_values(by=["data_referencia", "codigo_ativo"], inplace=True)
    df_final.reset_index(drop=True, inplace=True)

    # Gravação comprimida
    log.info(f"7. Gravando arquivo final comprimido: {f_api}...")
    t3 = time.time()
    df_final.to_csv(f_api, index=False, columns=COLUNAS_API, compression="gzip", encoding="utf-8")
    log.info(f"   Gravação concluída em {time.time() - t3:.2f}s.")

    min_date = df_final["data_referencia"].min()
    max_date = df_final["data_referencia"].max()
    num_datas = df_final["data_referencia"].nunique()
    total_linhas = len(df_final)

    log.info("=== RESUMO DA ENGORDA ===")
    log.info(f"Arquivo destino: {f_api.name}")
    log.info(f"Total de registros: {total_linhas:,}")
    log.info(f"Total de datas únicas: {num_datas:,}")
    log.info(f"Período: {min_date} até {max_date}")

    # Atualiza metadados
    atualizar_last_updates(min_date, max_date)
    log.info("Processo de engorda concluído com sucesso!")


if __name__ == "__main__":
    run()
