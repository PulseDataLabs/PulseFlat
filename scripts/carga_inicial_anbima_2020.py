"""
scripts/carga_inicial_anbima_2020.py
-----------------------------------
Script de carga inicial retroativa dos 9 novos datasets oficiais
da API ANBIMA Developers (ANBIMA Data), desde 01/01/2020 até 11/09/2026.

Recursos:
- Processamento paralelo inteligente com ThreadPoolExecutor (max_workers=4)
- Retry com backoff exponencial para respeitar os limites de requisição da Sensedia
- Verificação incremental (busca apenas as datas que ainda não estão no arquivo)
- Deduplicação estrita e recálculo de hashes padrão PulseFlat
- Atualização em lote de last_updates.json e last_updates.js
"""

import argparse
import datetime
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from scrapers.utils.anbima_data_client import AnbimaDataClient
from utils.base import agora_brt, get_logger
from utils.parsers import hash_row

log = get_logger("carga_inicial_anbima_2020")


def clean_s(val):
    if val is None:
        return ""
    s = str(val).strip()
    return "" if s in ("-", "--", "nan", "None") else s


def clean_n(val, dec=6):
    if val is None:
        return ""
    try:
        f = float(val)
        return f"{f:.{dec}f}".rstrip("0").rstrip(".")
    except (ValueError, TypeError):
        return clean_s(val)


def gerar_dias_uteis(dt_inicio: datetime.date, dt_fim: datetime.date) -> list[str]:
    curr = dt_inicio
    dias = []
    while curr <= dt_fim:
        if curr.weekday() < 5:
            dias.append(curr.strftime("%Y-%m-%d"))
        curr += datetime.timedelta(days=1)
    return dias


def atualizar_last_updates(file_name: str, min_date: str, max_date: str):
    target_json = ROOT_DIR / "data" / "last_updates.json"
    target_js = ROOT_DIR / "data" / "last_updates.js"

    if target_json.exists():
        try:
            with target_json.open("r", encoding="utf-8") as f:
                data = json.load(f)
            data[file_name] = {"min": min_date, "max": max_date}
            with target_json.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log.warning(f"Erro ao atualizar {target_json.name}: {e}")

    if target_js.exists():
        try:
            with target_json.open("r", encoding="utf-8") as f:
                data = json.load(f)
            with target_js.open("w", encoding="utf-8") as f:
                f.write(
                    f"window.PULSEFLAT_LAST_UPDATES = {json.dumps(data, indent=2, ensure_ascii=False)};\n"
                )
        except Exception as e:
            log.warning(f"Erro ao atualizar {target_js.name}: {e}")


# ==============================================================================
# CONFIGURAÇÕES E PARSERS DOS 9 DATASETS
# ==============================================================================

DATASETS_CONFIG = {
    "vna": {
        "file": "anbima_titulos_publicos_vna.csv.gz",
        "endpoint": "/feed/precos-indices/v1/titulos-publicos/vna",
        "chaves_dedup": ["data_referencia", "tipo_titulo"],
        "ordem": ["tipo_titulo"],
        "parse_fn": "parse_vna",
    },
    "ida": {
        "file": "anbima_indice_ida.csv.gz",
        "endpoint": "/feed/precos-indices/v1/indices/resultados-ida-fechado",
        "chaves_dedup": ["data_referencia", "indice"],
        "ordem": ["indice"],
        "parse_fn": "parse_ida",
    },
    "ima": {
        "file": "anbima_indices_ima_resultados.csv.gz",
        "endpoint": "/feed/precos-indices/v1/indices/resultados-ima",
        "chaves_dedup": ["data_referencia", "indice"],
        "ordem": ["indice"],
        "parse_fn": "parse_ima",
    },
    "fidc": {
        "file": "anbima_fidc_mercado_secundario.csv.gz",
        "endpoint": "/feed/precos-indices/v1/fidc/mercado-secundario",
        "chaves_dedup": ["data_referencia", "codigo_b3"],
        "ordem": ["codigo_b3"],
        "parse_fn": "parse_fidc",
    },
    "curvas_credito": {
        "file": "anbima_curvas_credito.csv.gz",
        "endpoint": "/feed/precos-indices/v1/debentures/curvas-credito",
        "chaves_dedup": ["data_referencia", "vertice_anos"],
        "ordem": ["vertice_anos"],
        "parse_fn": "parse_curvas_credito",
    },
    "ettj": {
        "file": "anbima_curvas_juros_ettj.csv.gz",
        "endpoint": "/feed/precos-indices/v1/titulos-publicos/curvas-juros",
        "chaves_dedup": ["data_referencia", "vertice_du"],
        "ordem": ["vertice_du"],
        "parse_fn": "parse_ettj",
    },
    "tpf": {
        "file": "anbima_titulos_publicos_mercado_secundario.csv.gz",
        "endpoint": "/feed/precos-indices/v1/titulos-publicos/mercado-secundario-TPF",
        "chaves_dedup": ["data_referencia", "codigo_selic", "data_vencimento"],
        "ordem": ["tipo_titulo", "data_vencimento"],
        "parse_fn": "parse_tpf",
    },
    "letras_financeiras": {
        "file": "anbima_letras_financeiras.csv.gz",
        "endpoint": "/feed/precos-indices/v1/letras-financeiras/matrizes-vertices-emissor",
        "chaves_dedup": ["data_referencia", "cnpj_emissor", "letra_financeira", "vertice_meses"],
        "ordem": ["emissor", "letra_financeira", "vertice_meses"],
        "parse_fn": "parse_lf",
    },
    "cri_cra": {
        "file": "anbima_cri_cra_mercado_secundario.csv.gz",
        "endpoint": "/feed/precos-indices/v1/cri-cra/mercado-secundario",
        "chaves_dedup": ["data_referencia", "codigo_ativo"],
        "ordem": ["codigo_ativo"],
        "parse_fn": "parse_cri_cra",
    },
}


def parse_vna(data_str, raw, dt_cap):
    if isinstance(raw, list) and raw:
        raw = raw[0]
    if not isinstance(raw, dict):
        return []
    rows = []
    for t in raw.get("titulos", []):
        tipo = clean_s(t.get("tipo_titulo"))
        if tipo:
            rows.append(
                {
                    "data_captura": dt_cap,
                    "data_referencia": data_str,
                    "tipo_titulo": tipo,
                    "codigo_selic": clean_s(t.get("codigo_selic")),
                    "vna": clean_n(t.get("vna"), dec=6),
                    "index": clean_n(t.get("index"), dec=4),
                    "tipo_correcao": clean_s(t.get("tipo_correcao")),
                    "data_validade": clean_s(t.get("data_validade")),
                }
            )
    return rows


def parse_ida(data_str, raw, dt_cap):
    items = (
        raw if isinstance(raw, list) else (raw.get("content", []) if isinstance(raw, dict) else [])
    )
    rows = []
    for item in items:
        ind = clean_s(item.get("indice"))
        if ind:
            rows.append(
                {
                    "data_captura": dt_cap,
                    "data_referencia": data_str,
                    "indice": ind,
                    "numero_indice": clean_n(item.get("numero_indice"), dec=6),
                    "variacao_diaria": clean_n(item.get("variacao_diaria"), dec=4),
                    "variacao_mensal": clean_n(item.get("variacao_mensal"), dec=4),
                    "variacao_anual": clean_n(item.get("variacao_anual"), dec=4),
                    "variacao_ult12m": clean_n(item.get("variacao_ult12m"), dec=4),
                    "variacao_ult24m": clean_n(item.get("variacao_ult24m"), dec=4),
                    "duration": clean_n(item.get("duration"), dec=2),
                    "peso": clean_n(item.get("peso"), dec=4),
                    "valor_mercado": clean_n(item.get("valor_mercado"), dec=2),
                }
            )
    return rows


def parse_ima(data_str, raw, dt_cap):
    items = (
        raw if isinstance(raw, list) else (raw.get("content", []) if isinstance(raw, dict) else [])
    )
    rows = []
    for item in items:
        ind = clean_s(item.get("indice"))
        if ind:
            rows.append(
                {
                    "data_captura": dt_cap,
                    "data_referencia": data_str,
                    "indice": ind,
                    "numero_indice": clean_n(item.get("numero_indice"), dec=6),
                    "variacao_diaria": clean_n(item.get("variacao_diaria"), dec=4),
                    "variacao_mensal": clean_n(item.get("variacao_mensal"), dec=4),
                    "variacao_anual": clean_n(item.get("variacao_anual"), dec=4),
                    "variacao_ult12m": clean_n(item.get("variacao_ult12m"), dec=4),
                    "variacao_ult24m": clean_n(item.get("variacao_ult24m"), dec=4),
                    "duration": clean_n(item.get("duration"), dec=2),
                    "pmr": clean_n(item.get("pmr"), dec=2),
                    "yield": clean_n(item.get("yield"), dec=4),
                    "redemption_yield": clean_n(item.get("redemption_yield"), dec=4),
                    "convexidade": clean_n(item.get("convexidade"), dec=4),
                    "peso_indice": clean_n(item.get("peso_indice"), dec=4),
                    "valor_mercado": clean_n(item.get("valor_mercado"), dec=2),
                }
            )
    return rows


def parse_fidc(data_str, raw, dt_cap):
    items = (
        raw if isinstance(raw, list) else (raw.get("content", []) if isinstance(raw, dict) else [])
    )
    rows = []
    for item in items:
        b3 = clean_s(item.get("codigo_b3"))
        if b3:
            rows.append(
                {
                    "data_captura": dt_cap,
                    "data_referencia": data_str,
                    "codigo_b3": b3,
                    "nome": clean_s(item.get("nome")),
                    "serie": clean_s(item.get("serie")),
                    "emissor": clean_s(item.get("emissor")),
                    "isin": clean_s(item.get("isin")),
                    "data_vencimento": clean_s(item.get("data_vencimento")),
                    "tipo_remuneracao": clean_s(item.get("tipo_remuneracao")),
                    "taxa_correcao": clean_n(item.get("taxa_correcao"), dec=4),
                    "taxa_indicativa": clean_n(item.get("taxa_indicativa"), dec=4),
                    "taxa_compra": clean_n(item.get("taxa_compra"), dec=4),
                    "taxa_venda": clean_n(item.get("taxa_venda"), dec=4),
                    "pu": clean_n(item.get("pu"), dec=6),
                    "percent_pu_par": clean_n(item.get("percent_pu_par"), dec=4),
                    "duration": clean_n(item.get("duration"), dec=2),
                    "desvio_padrao": clean_n(item.get("desvio_padrao"), dec=4),
                }
            )
    return rows


def parse_curvas_credito(data_str, raw, dt_cap):
    items = (
        raw if isinstance(raw, list) else (raw.get("content", []) if isinstance(raw, dict) else [])
    )
    rows = []
    for item in items:
        v_anos = item.get("vertice_anos")
        if v_anos is not None:
            rec = {
                "data_captura": dt_cap,
                "data_referencia": data_str,
                "vertice_anos": clean_n(v_anos, dec=2),
                "aaa": clean_n(item.get("aaa"), dec=4),
                "aa": clean_n(item.get("aa"), dec=4),
                "a": clean_n(item.get("a"), dec=4),
            }
            for k, v in item.items():
                if k not in ("data_referencia", "vertice_anos", "aaa", "aa", "a"):
                    rec[k] = clean_n(v, dec=4)
            rows.append(rec)
    return rows


def parse_ettj(data_str, raw, dt_cap):
    if isinstance(raw, list) and raw:
        raw = raw[0]
    if not isinstance(raw, dict):
        return []
    rows = []
    for p in raw.get("ettj", []):
        v_du = p.get("vertice_du")
        if v_du is not None:
            rows.append(
                {
                    "data_captura": dt_cap,
                    "data_referencia": data_str,
                    "vertice_du": str(int(v_du)),
                    "taxa_prefixadas": clean_n(p.get("taxa_prefixadas"), dec=4),
                    "taxa_ipca": clean_n(p.get("taxa_ipca"), dec=4),
                    "taxa_implicita": clean_n(p.get("taxa_implicita"), dec=4),
                }
            )
    return rows


def parse_tpf(data_str, raw, dt_cap):
    items = (
        raw if isinstance(raw, list) else (raw.get("content", []) if isinstance(raw, dict) else [])
    )
    rows = []
    for item in items:
        tipo = clean_s(item.get("tipo_titulo"))
        selic = clean_s(item.get("codigo_selic"))
        if tipo and selic:
            rows.append(
                {
                    "data_captura": dt_cap,
                    "data_referencia": data_str,
                    "tipo_titulo": tipo,
                    "codigo_selic": selic,
                    "codigo_isin": clean_s(item.get("codigo_isin")),
                    "data_vencimento": clean_s(item.get("data_vencimento")),
                    "data_base": clean_s(item.get("data_base")),
                    "expressao": clean_s(item.get("expressao")),
                    "taxa_indicativa": clean_n(item.get("taxa_indicativa"), dec=4),
                    "taxa_compra": clean_n(item.get("taxa_compra"), dec=4),
                    "taxa_venda": clean_n(item.get("taxa_venda"), dec=4),
                    "pu": clean_n(item.get("pu"), dec=6),
                    "desvio_padrao": clean_n(item.get("desvio_padrao"), dec=6),
                    "intervalo_min_d0": clean_n(item.get("intervalo_min_d0"), dec=4),
                    "intervalo_max_d0": clean_n(item.get("intervalo_max_d0"), dec=4),
                    "intervalo_min_d1": clean_n(item.get("intervalo_min_d1"), dec=4),
                    "intervalo_max_d1": clean_n(item.get("intervalo_max_d1"), dec=4),
                }
            )
    return rows


def parse_lf(data_str, raw, dt_cap):
    items = (
        raw if isinstance(raw, list) else (raw.get("content", []) if isinstance(raw, dict) else [])
    )
    rows = []
    for item in items:
        emissor = clean_s(item.get("emissor"))
        cnpj = clean_s(item.get("cnpj_emissor"))
        lf_tipo = clean_s(item.get("letra_financeira"))
        idx = clean_s(item.get("indexador"))
        flx = clean_s(item.get("fluxo"))
        for v in item.get("vertices", []):
            vm = clean_s(v.get("vertice"))
            if vm:
                rows.append(
                    {
                        "data_captura": dt_cap,
                        "data_referencia": data_str,
                        "emissor": emissor,
                        "cnpj_emissor": cnpj,
                        "letra_financeira": lf_tipo,
                        "indexador": idx,
                        "fluxo": flx,
                        "vertice_meses": vm,
                        "taxa_indicativa": clean_n(v.get("taxa_indicativa"), dec=4),
                        "taxa_compra": clean_n(v.get("taxa_compra"), dec=4),
                        "taxa_venda": clean_n(v.get("taxa_venda"), dec=4),
                    }
                )
    return rows


def parse_cri_cra(data_str, raw, dt_cap):
    items = (
        raw if isinstance(raw, list) else (raw.get("content", []) if isinstance(raw, dict) else [])
    )
    rows = []
    for item in items:
        ticker = clean_s(item.get("codigo_ativo"))
        if ticker:
            rows.append(
                {
                    "data_captura": dt_cap,
                    "data_referencia": data_str,
                    "codigo_ativo": ticker,
                    "emissor": clean_s(item.get("emissor")),
                    "originador": clean_s(item.get("originador")),
                    "originador_credito": clean_s(item.get("originador_credito")),
                    "tipo_contrato": clean_s(item.get("tipo_contrato")),
                    "serie": clean_s(item.get("serie")),
                    "emissao": clean_s(item.get("emissao")),
                    "data_vencimento": clean_s(item.get("data_vencimento")),
                    "tipo_remuneracao": clean_s(item.get("tipo_remuneracao")),
                    "taxa_correcao": clean_n(item.get("taxa_correcao"), dec=4),
                    "taxa_indicativa": clean_n(item.get("taxa_indicativa"), dec=4),
                    "taxa_compra": clean_n(item.get("taxa_compra"), dec=4),
                    "taxa_venda": clean_n(item.get("taxa_venda"), dec=4),
                    "pu": clean_n(item.get("pu"), dec=6),
                    "duration": clean_n(item.get("duration"), dec=2),
                    "z_spread": clean_n(item.get("z_spread"), dec=4),
                    "percent_reune": clean_s(item.get("percent_reune")),
                }
            )
    return rows


PARSERS = {
    "parse_vna": parse_vna,
    "parse_ida": parse_ida,
    "parse_ima": parse_ima,
    "parse_fidc": parse_fidc,
    "parse_curvas_credito": parse_curvas_credito,
    "parse_ettj": parse_ettj,
    "parse_tpf": parse_tpf,
    "parse_lf": parse_lf,
    "parse_cri_cra": parse_cri_cra,
}


def processar_dataset(
    key: str, client: AnbimaDataClient, dias_alvo: list[str], max_workers: int = 4
):
    cfg = DATASETS_CONFIG[key]
    file_path = ROOT_DIR / "data" / cfg["file"]
    endpoint = cfg["endpoint"]
    chaves_dedup = cfg["chaves_dedup"]
    ordem = cfg["ordem"]
    parser_func = PARSERS[cfg["parse_fn"]]

    log.info("\n=======================================================")
    log.info(f"Iniciando carga inicial para: {key} ({cfg['file']})")
    log.info(f"Endpoint: {endpoint}")

    df_existente = pd.DataFrame()
    datas_existentes = set()
    if file_path.exists():
        try:
            df_existente = pd.read_csv(file_path, dtype=str, keep_default_na=False)
            datas_existentes = set(df_existente["data_referencia"].dropna().unique())
            log.info(
                f"Arquivo existente possui {len(df_existente)} linhas e {len(datas_existentes)} datas."
            )
        except Exception as e:
            log.warning(f"Erro ao ler arquivo existente: {e}")

    datas_a_buscar = [d for d in dias_alvo if d not in datas_existentes]
    log.info(f"Total de datas a buscar: {len(datas_a_buscar)} (de {len(dias_alvo)} dias úteis)")

    if not datas_a_buscar:
        log.info(f"Nenhuma data pendente para {key}. Concluído.")
        return

    data_captura_padrao, _ = agora_brt()

    def fetch_single_date(dt_str):
        for tentativa in range(3):
            try:
                res = client.get(endpoint, params={"data": dt_str})
                parsed_rows = parser_func(dt_str, res, data_captura_padrao)
                return dt_str, parsed_rows, None
            except Exception as e:
                err_msg = str(e)
                if "HTTP 404" in err_msg:
                    # Sem dados / feriado / sem negócios
                    return dt_str, [], None
                if "HTTP 429" in err_msg:
                    time.sleep(2.0 * (tentativa + 1))
                    continue
                if tentativa == 2:
                    return dt_str, [], err_msg
                time.sleep(1.0)
        return dt_str, [], "Timeout/Excesso de tentativas"

    novas_linhas = []
    sucessos = 0
    erros = 0
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_single_date, dt): dt for dt in datas_a_buscar}
        total = len(futures)
        concluidos = 0

        for fut in as_completed(futures):
            concluidos += 1
            dt_str, rows, err = fut.result()
            if rows:
                novas_linhas.extend(rows)
                sucessos += 1
            elif err:
                erros += 1

            if concluidos % 100 == 0 or concluidos == total:
                elapsed = time.time() - t0
                taxa = concluidos / elapsed if elapsed > 0 else 0
                log.info(
                    f"  [{concluidos}/{total}] {concluidos * 100 / total:.1f}% concluído | "
                    f"{len(novas_linhas):,} registros coletados | {taxa:.1f} req/s"
                )

    log.info(f"Coleta concluída em {time.time() - t0:.2f}s. Novos registros: {len(novas_linhas):,}")

    if not novas_linhas and df_existente.empty:
        log.warning("Nenhum dado encontrado para salvar.")
        return

    df_novos = pd.DataFrame(novas_linhas)
    if not df_existente.empty:
        df_final = pd.concat([df_existente, df_novos], ignore_index=True)
    else:
        df_final = df_novos

    # Deduplicação
    log.info("Deduplicando e ordenando...")
    df_final.drop_duplicates(subset=chaves_dedup, keep="last", inplace=True)

    # Ordenação
    sort_cols = ["data_referencia"] + [
        c for c in ordem if c in df_final.columns and c != "data_referencia"
    ]
    df_final.sort_values(by=sort_cols, inplace=True)
    df_final.reset_index(drop=True, inplace=True)

    # Recalcula hashes
    log.info("Recalculando hashes de integridade...")
    records_dict = df_final.to_dict(orient="records")
    new_hashes = [
        hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
        for r in records_dict
    ]
    df_final["registro_hash"] = new_hashes

    # Gravação comprimida
    log.info(f"Gravando {file_path.name}...")
    df_final.to_csv(file_path, index=False, compression="gzip", encoding="utf-8")

    min_d = df_final["data_referencia"].min()
    max_d = df_final["data_referencia"].max()
    num_datas = df_final["data_referencia"].nunique()
    log.info(f"✔ Sucesso! Total: {len(df_final):,} linhas | {num_datas} datas ({min_d} a {max_d})")

    atualizar_last_updates(cfg["file"], str(min_d), str(max_d))


def main():
    parser = argparse.ArgumentParser(
        description="Carga inicial retroativa ANBIMA Data (desde 01/01/2020)"
    )
    parser.add_argument(
        "--target",
        type=str,
        default="all",
        help=f"Dataset alvo a processar: {list(DATASETS_CONFIG.keys())} ou 'all'",
    )
    parser.add_argument(
        "--workers", type=int, default=4, help="Número de threads simultâneas (default: 4)"
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default="2020-01-02",
        help="Data de início no formato YYYY-MM-DD (default: 2020-01-02)",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default="2026-09-11",
        help="Data de fim no formato YYYY-MM-DD (default: 2026-09-11)",
    )

    args = parser.parse_args()

    client = AnbimaDataClient()
    if not client.has_credentials:
        log.error("Credenciais ANBIMA não configuradas no .env")
        sys.exit(1)

    dt_ini = datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()
    dt_fim = datetime.datetime.strptime(args.end_date, "%Y-%m-%d").date()

    dias_uteis = gerar_dias_uteis(dt_ini, dt_fim)
    log.info(
        f"Calendário gerado: {len(dias_uteis)} dias úteis entre {args.start_date} e {args.end_date}"
    )

    targets = list(DATASETS_CONFIG.keys()) if args.target == "all" else [args.target]

    t_inicio_geral = time.time()
    for t in targets:
        if t not in DATASETS_CONFIG:
            log.error(f"Target inválido: {t}. Opções: {list(DATASETS_CONFIG.keys())}")
            continue
        processar_dataset(t, client, dias_uteis, max_workers=args.workers)

    log.info("\n=======================================================")
    log.info(
        f"Carga inicial concluída com sucesso para todos os alvos em {time.time() - t_inicio_geral:.2f}s!"
    )


if __name__ == "__main__":
    main()
