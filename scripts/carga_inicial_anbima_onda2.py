"""
scripts/carga_inicial_anbima_onda2.py
------------------------------------
Carga inicial retroativa dos 6 novos datasets de inteligência da API ANBIMA Data
desde 01/01/2020 até 11/09/2026:
1. IDKA Resultados (diário)
2. Projeções de Inflação IPCA/IGP-M (diário)
3. Parâmetros Svensson ETTJ (diário)
4. Estimativa Selic Oficial (diário)
5. Carteira Teórica IMA (mensal)
6. Carteira Teórica IDA (mensal)

Recursos:
- Processamento paralelo com ThreadPoolExecutor (max_workers=4)
- Tratamento automático de rate limits (HTTP 429) com retry exponencial
- Verificação incremental para idempotência
- Recálculo de hashes e atualização de last_updates.json / last_updates.js
"""

import argparse
import datetime
import gzip
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

log = get_logger("carga_inicial_anbima_onda2")


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


def gerar_primeiros_dias_uteis_mes(dt_inicio: datetime.date, dt_fim: datetime.date) -> list[str]:
    curr = dt_inicio
    meses_vistos = set()
    dias_mensais = []
    while curr <= dt_fim:
        ym = curr.strftime("%Y-%m")
        if ym not in meses_vistos and curr.weekday() < 5:
            # Pegar por volta do dia 2 ou 3 do mês quando as carteiras teóricas entram em vigor
            if curr.day >= 2 or curr.weekday() < 5:
                dias_mensais.append(curr.strftime("%Y-%m-%d"))
                meses_vistos.add(ym)
        curr += datetime.timedelta(days=1)
    return dias_mensais


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


def parse_idka(dados: list, data_str: str, data_cap: str) -> list[dict]:
    res = []
    for item in dados:
        nome = clean_s(item.get("nome") or item.get("indice"))
        if not nome:
            continue
        res.append(
            {
                "data_captura": data_cap,
                "data_referencia": data_str,
                "nome": nome,
                "numero_indice": clean_n(item.get("numero_indice"), dec=6),
                "tx_compra": clean_n(item.get("tx_compra"), dec=4),
                "tx_venda": clean_n(item.get("tx_venda"), dec=4),
                "variacao_diaria": clean_n(item.get("variacao_diaria"), dec=4),
                "variacao_mensal": clean_n(item.get("variacao_mensal"), dec=4),
                "variacao_anual": clean_n(item.get("variacao_anual"), dec=4),
                "variacao_ult12m": clean_n(item.get("variacao_ult12m"), dec=4),
                "volatilidade": clean_n(item.get("volatilidade"), dec=4),
            }
        )
    return res


def parse_projecoes(dados: list, data_str: str, data_cap: str) -> list[dict]:
    res = []
    for item in dados:
        indice = clean_s(item.get("indice"))
        mes_ref = clean_s(item.get("mes_referencia"))
        if not indice or not mes_ref:
            continue
        res.append(
            {
                "data_captura": data_cap,
                "data_coleta": clean_s(item.get("data_coleta")) or data_str,
                "data_validade": clean_s(item.get("data_validade")),
                "indice": indice,
                "tipo_projecao": clean_s(item.get("tipo_projecao")),
                "mes_referencia": mes_ref,
                "variacao_projetada": clean_n(item.get("variacao_projetada"), dec=4),
            }
        )
    return res


def parse_svensson(dados: any, data_str: str, data_cap: str) -> list[dict]:
    res = []
    if isinstance(dados, list) and dados:
        dados = dados[0]
    if not isinstance(dados, dict):
        return res

    parametros = dados.get("parametros", [])
    erros = {item.get("grupo_indexador"): item.get("valor_erro") for item in dados.get("erros", [])}

    for p in parametros:
        idx = clean_s(p.get("grupo_indexador"))
        if not idx:
            continue
        res.append(
            {
                "data_captura": data_cap,
                "data_referencia": data_str,
                "grupo_indexador": idx,
                "b1": clean_n(p.get("b1"), dec=8),
                "b2": clean_n(p.get("b2"), dec=8),
                "b3": clean_n(p.get("b3"), dec=8),
                "b4": clean_n(p.get("b4"), dec=8),
                "l1": clean_n(p.get("l1"), dec=8),
                "l2": clean_n(p.get("l2"), dec=8),
                "valor_erro": clean_n(erros.get(idx), dec=8),
            }
        )
    return res


def parse_selic(dados: list, data_str: str, data_cap: str) -> list[dict]:
    res = []
    for item in dados:
        dt_item = clean_s(item.get("data_referencia")) or data_str
        res.append(
            {
                "data_captura": data_cap,
                "data_referencia": dt_item,
                "estimativa_taxa_selic": clean_n(item.get("estimativa_taxa_selic"), dec=4),
            }
        )
    return res


def parse_carteira_ima(dados: list, data_str: str, data_cap: str) -> list[dict]:
    res = []
    for grupo in dados:
        indice = clean_s(grupo.get("indice"))
        dt_inicio = clean_s(grupo.get("data_inicio"))
        dt_fim = clean_s(grupo.get("data_fim"))
        referencias = grupo.get("referencias", [])

        for ref in referencias:
            isin = clean_s(ref.get("codigo_isin"))
            tipo_tit = clean_s(ref.get("tipo_titulo"))
            if not isin and not tipo_tit:
                continue
            res.append(
                {
                    "data_captura": data_cap,
                    "data_referencia": data_str,
                    "indice": indice,
                    "data_inicio": dt_inicio,
                    "data_fim": dt_fim,
                    "tipo_titulo": tipo_tit,
                    "codigo_selic_titulo": clean_s(ref.get("codigo_selic_titulo")),
                    "codigo_isin": isin,
                    "data_vencimento": clean_s(ref.get("data_vencimento")),
                    "pu": clean_n(ref.get("pu"), dec=6),
                    "quantidade_indice": clean_n(ref.get("quantidade_indice"), dec=4),
                    "peso": clean_n(ref.get("peso"), dec=4),
                    "duration": clean_n(ref.get("duration"), dec=2),
                }
            )
    return res


def parse_carteira_ida(dados: list, data_str: str, data_cap: str) -> list[dict]:
    res = []
    for grupo in dados:
        indice = clean_s(grupo.get("indice"))
        dt_inicio = clean_s(grupo.get("data_inicio"))
        dt_fim = clean_s(grupo.get("data_fim"))
        referencias = grupo.get("referencias", [])

        for ref in referencias:
            cod_tit = clean_s(ref.get("codigo_titulo"))
            if not cod_tit:
                continue
            res.append(
                {
                    "data_captura": data_cap,
                    "data_referencia": data_str,
                    "indice": indice,
                    "data_inicio": dt_inicio,
                    "data_fim": dt_fim,
                    "codigo_titulo": cod_tit,
                    "emissor": clean_s(ref.get("emissor")),
                    "codigo_isin_titulo": clean_s(ref.get("codigo_isin_titulo")),
                    "data_vencimento": clean_s(ref.get("data_vencimento")),
                    "indexador": clean_s(ref.get("indexador")),
                    "pu": clean_n(ref.get("pu"), dec=6),
                    "quantidade_indice": clean_n(ref.get("quantidade_indice"), dec=4),
                    "peso": clean_n(ref.get("peso"), dec=4),
                    "duration": clean_n(ref.get("duration"), dec=2),
                }
            )
    return res


CONFIGS = {
    "idka": {
        "file": "anbima_indices_idka_resultados.csv.gz",
        "endpoint": "/feed/precos-indices/v1/indices/resultados-idka",
        "chaves_dedup": ["data_referencia", "nome"],
        "ordem": ["data_referencia", "nome"],
        "parse_fn": parse_idka,
        "tipo_datas": "diario",
        "data_col": "data_referencia",
    },
    "projecoes": {
        "file": "anbima_projecoes_inflacao.csv.gz",
        "endpoint": "/feed/precos-indices/v1/debentures/projecoes",
        "chaves_dedup": ["data_coleta", "indice", "mes_referencia"],
        "ordem": ["data_coleta", "indice", "mes_referencia"],
        "parse_fn": parse_projecoes,
        "tipo_datas": "diario",
        "data_col": "data_coleta",
    },
    "svensson": {
        "file": "anbima_curvas_juros_parametros_svensson.csv.gz",
        "endpoint": "/feed/precos-indices/v1/titulos-publicos/curvas-juros",
        "chaves_dedup": ["data_referencia", "grupo_indexador"],
        "ordem": ["data_referencia", "grupo_indexador"],
        "parse_fn": parse_svensson,
        "tipo_datas": "diario",
        "data_col": "data_referencia",
    },
    "selic": {
        "file": "anbima_titulos_publicos_estimativa_selic.csv.gz",
        "endpoint": "/feed/precos-indices/v1/titulos-publicos/estimativa-selic",
        "chaves_dedup": ["data_referencia"],
        "ordem": ["data_referencia"],
        "parse_fn": parse_selic,
        "tipo_datas": "diario",
        "data_col": "data_referencia",
    },
    "carteira_ima": {
        "file": "anbima_indices_carteira_teorica_ima.csv.gz",
        "endpoint": "/feed/precos-indices/v1/indices/carteira-teorica-ima",
        "chaves_dedup": ["data_inicio", "indice", "codigo_isin"],
        "ordem": ["data_inicio", "indice", "tipo_titulo"],
        "parse_fn": parse_carteira_ima,
        "tipo_datas": "mensal",
        "data_col": "data_inicio",
    },
    "carteira_ida": {
        "file": "anbima_indices_carteira_teorica_ida.csv.gz",
        "endpoint": "/feed/precos-indices/v1/indices/carteira-teorica-ida",
        "chaves_dedup": ["data_inicio", "indice", "codigo_titulo"],
        "ordem": ["data_inicio", "indice", "codigo_titulo"],
        "parse_fn": parse_carteira_ida,
        "tipo_datas": "mensal",
        "data_col": "data_inicio",
    },
}


def processar_alvo(
    key: str,
    client: AnbimaDataClient,
    dias_diarios: list[str],
    dias_mensais: list[str],
    max_workers: int = 4,
):
    cfg = CONFIGS[key]
    file_path = ROOT_DIR / "data" / cfg["file"]
    log.info("\n=======================================================")
    log.info(f"Iniciando carga inicial para: {key} ({cfg['file']})")
    log.info(f"Endpoint: {cfg['endpoint']}")

    dias_base = dias_mensais if cfg["tipo_datas"] == "mensal" else dias_diarios

    existentes_df = pd.DataFrame()
    datas_existentes = set()
    dt_col = cfg["data_col"]

    if file_path.exists():
        try:
            with gzip.open(file_path, "rt", encoding="utf-8") as f:
                existentes_df = pd.read_csv(f, dtype=str)
                if dt_col in existentes_df.columns:
                    datas_existentes = set(existentes_df[dt_col].dropna().unique())
            log.info(
                f"Arquivo existente possui {len(existentes_df)} linhas e {len(datas_existentes)} datas."
            )
        except Exception as e:
            log.warning(f"Não foi possível ler {cfg['file']}: {e}")

    datas_a_buscar = [d for d in dias_base if d not in datas_existentes]
    log.info(f"Total de datas a buscar: {len(datas_a_buscar)} (de {len(dias_base)} datas)")

    if not datas_a_buscar:
        log.info(f"Arquivo {cfg['file']} já está 100% atualizado! Pulando.")
        return

    novos_registros = []
    concluidos = 0
    total = len(datas_a_buscar)
    t0 = time.time()
    data_cap_padrao, _ = agora_brt()

    def worker(dt_str):
        for tentativa in range(5):
            try:
                raw = client.get(cfg["endpoint"], params={"data": dt_str})
                if isinstance(raw, dict) and "content" in raw:
                    raw = raw["content"]
                if raw:
                    return cfg["parse_fn"](raw, dt_str, data_cap_padrao)
                return []
            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg:
                    time.sleep(2.0 * (tentativa + 1))
                elif "404" in err_msg:
                    return []
                elif "500" in err_msg or "502" in err_msg or "503" in err_msg:
                    time.sleep(1.5)
                else:
                    return []
        return []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_date = {executor.submit(worker, d): d for d in datas_a_buscar}

        for fut in as_completed(future_to_date):
            concluidos += 1
            try:
                res = fut.result()
                if res:
                    novos_registros.extend(res)
            except Exception as e:
                log.debug(f"Erro no worker: {e}")

            if concluidos % 100 == 0 or concluidos == total:
                elapsed = time.time() - t0
                taxa = concluidos / elapsed if elapsed > 0 else 0
                pct = (concluidos / total) * 100
                print(
                    f"  [{concluidos}/{total}] {pct:.1f}% concluído | {len(novos_registros):,d} registros coletados | {taxa:.1f} req/s",
                    flush=True,
                )

    log.info(
        f"Coleta concluída em {time.time() - t0:.2f}s. Novos registros: {len(novos_registros):,d}"
    )

    novos_df = pd.DataFrame(novos_registros, dtype=str) if novos_registros else pd.DataFrame()
    if existentes_df.empty and novos_df.empty:
        log.warning("Nenhum dado existente e nenhum novo dado coletado.")
        return

    log.info("Deduplicando e ordenando...")
    df_comb = (
        pd.concat([existentes_df, novos_df], ignore_index=True)
        if not existentes_df.empty
        else novos_df
    )
    df_comb.drop_duplicates(subset=cfg["chaves_dedup"], keep="last", inplace=True)

    ordem_cols = [c for c in cfg["ordem"] if c in df_comb.columns]
    if ordem_cols:
        df_comb.sort_values(by=ordem_cols, inplace=True)
    df_comb.reset_index(drop=True, inplace=True)

    log.info("Recalculando hashes de integridade...")
    recs = df_comb.to_dict(orient="records")
    df_comb["registro_hash"] = [
        hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
        for r in recs
    ]

    log.info(f"Gravando {cfg['file']}...")
    with gzip.open(file_path, "wt", encoding="utf-8") as f:
        df_comb.to_csv(f, index=False)

    min_date = df_comb[dt_col].min() if dt_col in df_comb.columns else ""
    max_date = df_comb[dt_col].max() if dt_col in df_comb.columns else ""
    n_datas = len(df_comb[dt_col].unique()) if dt_col in df_comb.columns else 0

    atualizar_last_updates(cfg["file"], min_date, max_date)
    log.info(
        f"✔ Sucesso! Total: {len(df_comb):,d} linhas | {n_datas} datas ({min_date} a {max_date})"
    )


def main():
    parser = argparse.ArgumentParser(description="Carga Inicial ANBIMA 2ª Onda (2020 a 2026)")
    parser.add_argument(
        "--target",
        choices=["all", "idka", "projecoes", "svensson", "selic", "carteira_ima", "carteira_ida"],
        default="all",
        help="Alvo a executar (padrão: all)",
    )
    parser.add_argument(
        "--workers", type=int, default=4, help="Número de threads concorrentes (padrão: 4)"
    )
    args = parser.parse_args()

    client = AnbimaDataClient()

    dt_inicio = datetime.date(2020, 1, 1)
    dt_fim = datetime.date(2026, 9, 11)

    dias_diarios = gerar_dias_uteis(dt_inicio, dt_fim)
    dias_mensais = gerar_primeiros_dias_uteis_mes(dt_inicio, dt_fim)

    t_inicio_geral = time.time()
    targets = (
        ["carteira_ima", "carteira_ida", "selic", "svensson", "projecoes", "idka"]
        if args.target == "all"
        else [args.target]
    )

    for t in targets:
        processar_alvo(t, client, dias_diarios, dias_mensais, max_workers=args.workers)

    log.info("\n=======================================================")
    log.info(
        f"Carga inicial concluída com sucesso para todos os alvos em {time.time() - t_inicio_geral:.2f}s!"
    )


if __name__ == "__main__":
    main()
