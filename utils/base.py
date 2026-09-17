"""
utils/base.py
-------------
Funções e classes utilitárias compartilhadas por todos os scrapers.
"""

import csv
import gzip
import json
import logging
import sys
import time
from base64 import b64encode
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Union
from zoneinfo import ZoneInfo

import pandas as pd
import requests
import urllib3
import urllib3.response
from urllib3.exceptions import InvalidChunkLength

from scripts.utils.ux import ColorLogger

# Desabilita avisos de SSL inseguro globais
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Monkeypatch do urllib3 para tratar conexão fechada prematuramente pelo proxy local (InvalidChunkLength) como EOF normal
def _patched_update_chunk_length(self):
    if self.chunk_left is not None:
        return
    if not self._fp or not hasattr(self._fp, "fp") or not self._fp.fp:
        self.chunk_left = 0
        return
    try:
        line = self._fp.fp.readline()
        line = line.split(b";", 1)[0]
    except Exception:
        self.chunk_left = 0
        return
    try:
        self.chunk_left = int(line, 16)
    except ValueError:
        if not line or line.strip() == b"":
            self.chunk_left = 0
        else:
            self.close()
            raise InvalidChunkLength(self, line)


urllib3.response.HTTPResponse._update_chunk_length = _patched_update_chunk_length

# Patch global do requests para impor limite e padrão de timeout (evita travamentos longos) e desabilitar verificação de SSL
_orig_request = requests.Session.request


def _patched_request(self, method, url, *args, **kwargs):
    # Desabilita SSL verify para evitar problemas com proxy auto-assinado no sandbox
    kwargs["verify"] = False

    timeout = kwargs.get("timeout")
    if timeout is None:
        kwargs["timeout"] = (10, 30)
    elif isinstance(timeout, (int, float)):
        conn = min(timeout, 10)
        read = min(timeout, 30)
        kwargs["timeout"] = (conn, read)
    elif isinstance(timeout, tuple):
        conn, read = timeout
        conn_val = min(conn, 10) if conn is not None else 10
        read_val = min(read, 30) if read is not None else 30
        kwargs["timeout"] = (conn_val, read_val)

    # Resiliência global: 2 tentativas (original + 1 retry rápido de 1s) para falhas transitórias
    # Ignora ConnectTimeout para evitar esticar tempo quando IPs/servidores estão bloqueados
    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        try:
            resp = _orig_request(self, method, url, *args, **kwargs)
            if resp.status_code in (502, 503, 504) and attempt < max_attempts:
                time.sleep(1.0)
                continue
            return resp
        except requests.exceptions.ConnectTimeout as e:
            raise e
        except requests.RequestException as e:
            if attempt == max_attempts:
                raise e
            time.sleep(1.0)


requests.Session.request = _patched_request

DRIFTS = []

FUSO = ZoneInfo("America/Sao_Paulo")

HEADERS_HTTP = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.b3.com.br/",
    "Origin": "https://www.b3.com.br",
}


def get_logger(name: str) -> logging.Logger:
    """Retorna um logger. Usa ColorLogger de scripts.utils.ux se disponível."""
    try:
        return ColorLogger(name)
    except Exception:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
        return logging.getLogger(name)


def agora_brt() -> tuple[str, str]:
    """Retorna (data_captura YYYY-MM-DD, hora_captura HH:MM:SS) em BRT."""
    now = datetime.now(FUSO)
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")


def limpar(valor) -> str:
    if valor is None or pd.isna(valor):
        return ""
    return str(valor).strip()


def b64_encode_params(params: dict) -> str:
    """Codifica dict como JSON em Base64 — padrão da API interna da B3."""
    payload = json.dumps(params, separators=(",", ":"))
    return b64encode(payload.encode("utf-8")).decode("utf-8")


def nova_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS_HTTP)
    return s


def read_existing_header(arquivo: Path) -> list[str]:
    """Lê o cabeçalho existente de um arquivo CSV."""
    if not arquivo.exists() or arquivo.stat().st_size == 0:
        return []
    try:
        if arquivo.suffix == ".gz":
            with gzip.open(arquivo, "rt", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                header = next(reader, [])
                return [col.strip() for col in header if col.strip()]
        else:
            with arquivo.open("r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                header = next(reader, [])
                return [col.strip() for col in header if col.strip()]
    except Exception:
        return []


def get_type_badge(col_name: str, series: pd.Series | None = None) -> str:
    """
    Infere a tipagem do campo para governança e exibição no catálogo (date, float, int, str).
    Combina inspeção em tempo de execução dos dados/dtypes do pandas com padrões léxicos de mercado financeiro.
    """
    col_name = col_name.lower()
    if (
        col_name.startswith("dt_")
        or col_name.endswith("_dt")
        or col_name.endswith("_data")
        or "data" in col_name
        or "date" in col_name
    ):
        return "date"

    if series is not None and not series.empty:
        if pd.api.types.is_float_dtype(series):
            return "float"
        if pd.api.types.is_integer_dtype(series):
            return "int"
        if pd.api.types.is_datetime64_any_dtype(series):
            return "date"
        non_null = series.dropna()
        sample = non_null.head(30).astype(str).str.strip()
        sample = sample[~sample.isin(["", "nan", "None", "--", "N/D", "ND", "-", "null"])]
        if not sample.empty:
            if sample.str.match(r"^\d{4}-\d{2}-\d{2}").all():
                return "date"
            try:
                num = pd.to_numeric(sample, errors="raise")
                if (num % 1 == 0).all() and not sample.str.contains(r"\.").any():
                    # Preserva códigos e identificadores com zeros à esquerda como texto
                    if (sample.str.startswith("0") & (sample.str.len() > 1)).any():
                        return "str"
                    return "int"
                return "float"
            except Exception:
                pass

    if (
        col_name.startswith("vr_")
        or col_name.startswith("vl_")
        or col_name.startswith("tx_")
        or col_name.startswith("pct_")
        or col_name.startswith("interv_")
        or col_name.startswith("intervalo_")
        or col_name.startswith("pu_")
        or col_name.endswith("_val")
        or col_name.endswith("_perc")
        or col_name.endswith("_taxa")
        or col_name.endswith("_pu")
        or "preco" in col_name
        or "taxa" in col_name
        or "valor" in col_name
        or "saldo" in col_name
        or "patrimonio" in col_name
        or "cota" in col_name
        or "desvio" in col_name
        or "duration" in col_name
        or "ratio" in col_name
        or "spread" in col_name
        or "yield" in col_name
        or "variacao" in col_name
        or "peso" in col_name
        or "pmr" in col_name
        or "convexidade" in col_name
        or col_name in ("pu", "duration", "pct_reune", "desvio_padrao", "numero_indice")
        or col_name
        in (
            "ret_dia_perc",
            "ret_mes_perc",
            "ret_ano_perc",
            "ret_12_meses_perc",
            "vol_aa_perc",
            "taxa_juros_aa_perc_compra_d1",
            "taxa_juros_aa_perc_venda_d0",
        )
    ):
        if col_name not in ("publico_alvo",):
            return "float"
    if (
        col_name.startswith("qt_")
        or col_name.startswith("nr_")
        or "quantidade" in col_name
        or ("numero" in col_name and col_name != "numero_indice")
        or col_name
        in (
            "id_registro_fundo",
            "id_registro_classe",
            "prazo",
            "prazo_dias",
            "Ordem",
            "page_number",
        )
    ):
        return "int"
    return "str"


def _salvar_csv_logger():
    return ColorLogger("utils.salvar_csv")


def _normalize_date_str(val: str) -> str | None:
    if not val:
        return None
    val = str(val).split()[0].replace("T", " ").split()[0].strip()
    if len(val) >= 10 and val[4] == "-" and val[7] == "-":
        return val[:10]
    if len(val) >= 10 and val[2] == "/" and val[5] == "/":
        parts = val[:10].split("/")
        return f"{parts[2]}-{parts[1]}-{parts[0]}"
    if len(val) == 6 and val.isdigit():
        return f"{val[:4]}-{val[4:6]}-01"
    if len(val) == 8 and val.isdigit():
        return f"{val[:4]}-{val[4:6]}-{val[6:8]}"
    return None

def salvar_csv(
    arquivo: Path,
    registros: Union[list, "pd.DataFrame"],
    cabecalho: list[str],
    chaves_dedup: list[str] | None = None,
    acumular: bool = True,
) -> None:
    log = _salvar_csv_logger()

    is_empty = registros.empty if isinstance(registros, pd.DataFrame) else not registros
    if is_empty:
        log.warning("Nenhum registro para salvar — abortando.")
        sys.exit(1)

    # --- Preparação de df_novos ---
    arquivo.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(registros, pd.DataFrame):
        df_novos = registros.copy()
    else:
        df_novos = pd.DataFrame(registros, columns=cabecalho)

    # --- Reconciliação Inteligente de Schema e Unificação de Colunas ---
    from utils.schema_intelligence import (
        are_columns_equivalent,
        find_internal_duplicate_aliases,
        reconcile_columns,
        unify_dataframe_columns,
    )

    schemas_path = arquivo.parent / "schemas.json"
    schemas = []
    ref_cols: list[str] = []
    if schemas_path.exists():
        try:
            with schemas_path.open("r", encoding="utf-8") as sf:
                schemas = json.load(sf)
            import re
            for s in schemas:
                files_declared = [f.strip() for f in re.split(r"·| e ", s.get("files", ""))]
                if arquivo.name in files_declared:
                    ref_cols = [f["name"] for f in s.get("fields", [])]
                    break
        except Exception as e:
            log.warning(f"Erro ao ler schemas.json para {arquivo.name}: {e}")

    header_existente = read_existing_header(arquivo) if arquivo.exists() else []
    if not ref_cols and header_existente:
        ref_cols = header_existente

    # 1. Unificação interna em df_novos se houver colunas duplicadas
    internal_map = find_internal_duplicate_aliases(df_novos.columns)
    if internal_map:
        for var, can in internal_map.items():
            log.info(
                f"SCHEMA AUTO-HEAL em {arquivo.name}: Coluna '{var}' unificada para '{can}' nos novos registros."
            )
        df_novos = unify_dataframe_columns(df_novos, internal_map)
        cabecalho = [c for c in cabecalho if c not in internal_map]

    # 2. Reconciliação inteligente com schema/arquivo existente
    if ref_cols:
        reconcile_map = reconcile_columns(df_novos.columns, ref_cols)
        if reconcile_map:
            for var, can in reconcile_map.items():
                log.info(
                    f"SCHEMA AUTO-HEAL em {arquivo.name}: Coluna '{var}' unificada para o padrão canônico '{can}'."
                )
            df_novos = unify_dataframe_columns(df_novos, reconcile_map)
            cabecalho = [reconcile_map.get(c, c) for c in cabecalho]
            cabecalho = list(dict.fromkeys(cabecalho))

    # --- Detecção e Auto-Resolução de Schema Drift ---
    try:
        if schemas:
            filtered_cols = [
                c
                for c in cabecalho
                if c
                not in ("conjunto", "arquivo_origem", "registro_hash", "dt_captura")
            ]

            import re

            for s in schemas:
                files_declared = [
                    f.strip() for f in re.split(r"·| e ", s.get("files", ""))
                ]
                if arquivo.name in files_declared:
                    existing_cols = [f["name"] for f in s.get("fields", [])]
                    raw_added = [c for c in filtered_cols if c not in existing_cols]
                    raw_removed = []
                    if len(files_declared) == 1:
                        raw_removed = [c for c in existing_cols if c not in filtered_cols]

                    # Auto-resolução de drifts: se colunas equivalentes existem, não gera drift
                    added = [
                        a for a in raw_added
                        if not any(are_columns_equivalent(a, e) for e in existing_cols)
                    ]
                    removed = [
                        r for r in raw_removed
                        if not any(are_columns_equivalent(r, f) for f in filtered_cols)
                    ]

                    if added or removed:
                        drift_info = {
                            "file": arquivo.name,
                            "added": added,
                            "removed": removed,
                            "timestamp": datetime.now().isoformat(),
                        }
                        DRIFTS.append(drift_info)
                        log.warning(
                            f"SCHEMA DRIFT detectado em {arquivo.name}: Adicionadas: {added} | Removidas: {removed}"
                        )
                    break
    except Exception as e:
        log.warning(f"Erro ao detectar schema drift para {arquivo.name}: {e}")

    substituidas = 0

    if acumular and arquivo.exists():
        df_antigo = pd.DataFrame()
        try:
            df_antigo = pd.read_csv(arquivo, dtype=str, keep_default_na=False)
            antigo_internal_map = find_internal_duplicate_aliases(df_antigo.columns)
            if antigo_internal_map:
                for var, can in antigo_internal_map.items():
                    log.info(
                        f"SCHEMA AUTO-HEAL em {arquivo.name}: Unificando coluna legada '{var}' para '{can}' nos dados históricos."
                    )
                df_antigo = unify_dataframe_columns(df_antigo, antigo_internal_map)

            if ref_cols:
                antigo_reconcile = reconcile_columns(df_antigo.columns, ref_cols)
                if antigo_reconcile:
                    df_antigo = unify_dataframe_columns(df_antigo, antigo_reconcile)

            header_existente = list(df_antigo.columns)
        except Exception as e:
            log.warning(
                f"Erro ao ler arquivo existente para acumular: {e}"
            )
            header_existente = read_existing_header(arquivo)

        merged = []
        for col in header_existente + cabecalho:
            if col and col not in merged:
                merged.append(col)
        cabecalho = merged

        try:
            for c in cabecalho:
                if c not in df_novos.columns:
                    df_novos[c] = ""
                if c not in df_antigo.columns:
                    df_antigo[c] = ""

            if df_antigo.empty:
                substituidas = 0
                df_antigo_filtrado = df_antigo
            elif chaves_dedup:
                keys_new = df_novos[chaves_dedup].astype(str).agg("-".join, axis=1)
                keys_old = df_antigo[chaves_dedup].astype(str).agg("-".join, axis=1)
                mask_keep = ~keys_old.isin(keys_new)
                substituidas = int(len(df_antigo) - mask_keep.sum())
                df_antigo_filtrado = df_antigo[mask_keep]
            else:
                datas_novas = df_novos["data_captura"].unique()
                mask_keep = ~df_antigo["data_captura"].isin(datas_novas)
                substituidas = int(len(df_antigo) - mask_keep.sum())
                df_antigo_filtrado = df_antigo[mask_keep]

            if df_antigo_filtrado.empty:
                df_final = df_novos[cabecalho]
            elif df_novos.empty:
                df_final = df_antigo_filtrado[cabecalho]
            else:
                df_final = pd.concat(
                    [df_antigo_filtrado, df_novos[cabecalho]], ignore_index=True
                )
        except Exception as e:
            log.warning(
                f"Erro ao mesclar registros com arquivo existente, reescrevendo: {e}"
            )
            df_final = df_novos[cabecalho]
    else:
        df_final = df_novos[cabecalho]

    df_final.to_csv(arquivo, index=False, columns=cabecalho, encoding="utf-8")

    # --- Persistência no Banco de Dados Oracle ---
    try:
        from utils.db import upload_dataframe

        table_name = arquivo.name.split(".")[0].upper()

        # Identificar se há colunas de período
        candidates = [
            "AnoMes",
            "ANOMES",
            "data_base",
            "DATA_BASE",
            "data_referencia",
            "DATA_REFERENCIA",
            "data_captura",
            "DATA_CAPTURA",
            "data",
            "DATA",
            "dt_captura",
            "DT_CAPTURA",
        ]
        has_period_col = any(c in df_novos.columns for c in candidates)

        if has_period_col:
            log.info(
                f"Iniciando carga incremental para '{table_name}' usando novos registros..."
            )
            upload_dataframe(
                df_novos[[c for c in cabecalho if c in df_novos.columns]],
                table_name,
                chaves_dedup=chaves_dedup,
            )
        else:
            log.info(
                f"Iniciando carga total para '{table_name}' usando registros acumulados..."
            )
            upload_dataframe(df_final, table_name, chaves_dedup=chaves_dedup)
    except Exception as db_err:
        log.warning(
            f"Não foi possível persistir os dados no banco Oracle para {arquivo.name}: {db_err}"
        )

    try:
        last_updates_path = arquivo.parent / "last_updates.json"
        last_updates = {}
        if last_updates_path.exists():
            try:
                with last_updates_path.open("r", encoding="utf-8") as lf:
                    last_updates = json.load(lf)
            except Exception:
                pass

        if not df_final.empty:
            date_col = None
            for candidate in [
                "data_referencia",
                "refdate",
                "data_base",
                "data_pregao",
                "dt_pregao",
                "data_mov",
                "data_operacao",
                "data",
                "rpt_dt",
                "data_atualizacao",
                "data_geracao",
                "data_captura",
                "data_coleta",
                "dt_captura",
            ]:
                if candidate in cabecalho:
                    date_col = candidate
                    break

            if date_col and date_col in df_final.columns:
                raw_datas = df_final[date_col].dropna().unique()
                datas = []
                for rd in raw_datas:
                    nd = _normalize_date_str(str(rd))
                    if nd:
                        datas.append(nd)
                if datas:
                    last_updates[arquivo.name] = {"min": min(datas), "max": max(datas)}
                    with last_updates_path.open("w", encoding="utf-8") as lf:
                        json.dump(last_updates, lf, indent=2, ensure_ascii=False)

                    last_updates_js_path = arquivo.parent / "last_updates.js"
                    with last_updates_js_path.open("w", encoding="utf-8") as lf:
                        json_str = json.dumps(last_updates, indent=2, ensure_ascii=False)
                        lf.write("window.PULSEFLAT_LAST_UPDATES = " + json_str + ";\n")
    except Exception as e:
        log.warning(f"Não foi possível atualizar last_updates.json/js: {e}")

    try:
        previews_path = arquivo.parent / "previews.json"
        previews = {}
        if previews_path.exists():
            try:
                with previews_path.open("r", encoding="utf-8") as pf:
                    previews = json.load(pf)
            except Exception:
                pass

        if not df_final.empty:
            tail_df = df_final.tail(30).copy()
            sort_col = None
            for candidate in [
                "data_referencia",
                "refdate",
                "data_base",
                "data_pregao",
                "dt_pregao",
                "data_mov",
                "data_operacao",
                "data",
                "rpt_dt",
                "data_atualizacao",
                "data_geracao",
                "data_captura",
                "data_coleta",
                "dt_captura",
            ]:
                if candidate in tail_df.columns:
                    sort_col = candidate
                    break

            if sort_col:
                tail_df = tail_df.sort_values(by=sort_col, ascending=False)
            else:
                tail_df = tail_df.iloc[::-1]

            display_tail = tail_df.head(15)
            clean_rows = display_tail[cabecalho].fillna("").astype(str).values.tolist()

            previews[arquivo.name] = {
                "headers": cabecalho,
                "rows": clean_rows,
            }

            with previews_path.open("w", encoding="utf-8") as pf:
                json.dump(previews, pf, indent=2, ensure_ascii=False)

            previews_js_path = arquivo.parent / "previews.js"
            with previews_js_path.open("w", encoding="utf-8") as pf:
                json_str = json.dumps(previews, indent=2, ensure_ascii=False)
                pf.write("window.PULSEFLAT_PREVIEWS = " + json_str + ";\n")
    except Exception as e:
        log.warning(f"Não foi possível atualizar previews.json/js: {e}")

    try:
        import re

        schemas_path = arquivo.parent / "schemas.json"
        schemas = []
        if schemas_path.exists():
            try:
                with schemas_path.open("r", encoding="utf-8") as sf:
                    schemas = json.load(sf)
            except Exception:
                pass

        filtered_cols = [
            c
            for c in cabecalho
            if c not in ("conjunto", "arquivo_origem", "registro_hash", "dt_captura")
        ]
        first_reg = df_final.iloc[0].to_dict() if not df_final.empty else {}
        fields = []
        for c in filtered_cols:
            t_badge = get_type_badge(c, df_final[c] if c in df_final.columns else None)
            ex_val = str(first_reg.get(c, ""))
            if ex_val == "nan" or ex_val == "None":
                ex_val = ""
            fields.append({"name": c, "type": t_badge, "example": ex_val})

        found = False
        for s in schemas:
            files_declared = [f.strip() for f in re.split(r"·| e ", s.get("files", ""))]
            if arquivo.name in files_declared:
                if len(files_declared) > 1:
                    new_names = {f["name"] for f in fields}
                    merged_fields = fields.copy()
                    for existing_field in s.get("fields", []):
                        if existing_field["name"] not in new_names:
                            merged_fields.append(existing_field)
                    s["fields"] = merged_fields
                else:
                    s["fields"] = fields
                found = True
                break

        if not found:

            def get_source_from_filename(filename: str) -> str:
                filename = filename.lower()
                if filename.startswith("anbima_"):
                    return "anbima"
                elif filename.startswith("b3_"):
                    return "b3"
                elif filename.startswith("bcb_") or filename.startswith("bacen_"):
                    return "bcb"
                elif filename.startswith("cvm_") or filename.startswith("registro_"):
                    return "cvm"
                elif filename.startswith("ibge_"):
                    return "ibge"
                elif filename.startswith("debentures_"):
                    return "debentures"
                elif filename.startswith("yahoo_") or filename.startswith("onu_"):
                    return "misc"
                return "other"

            guessed_title = arquivo.name.replace(".csv", "").replace("_", " ").title()
            schemas.append(
                {
                    "title": guessed_title,
                    "files": arquivo.name,
                    "source": get_source_from_filename(arquivo.name),
                    "fields": fields,
                }
            )

        with schemas_path.open("w", encoding="utf-8") as sf:
            json.dump(schemas, sf, indent=2, ensure_ascii=False)
    except Exception as e:
        log.warning(f"Não foi possível atualizar schemas.json: {e}")

    log.info(
        f"CSV atualizado → {arquivo} | "
        f"{len(df_novos)} novos registros salvos"
        + (f" | {substituidas} linha(s) antigas substituídas" if substituidas else "")
    )


try:
    import fcntl
except ImportError:
    fcntl = None


@contextmanager
def acquire_lock(lock_name: str, blocking: bool = True):
    """
    Adquire um lock de arquivo exclusivo para evitar execuções concorrentes.
    Usa fcntl (Linux/Unix) para liberação automática se o processo cair.
    """

    lock_file = Path(__file__).resolve().parents[1] / "data" / f"{lock_name}.lock"
    lock_file.parent.mkdir(parents=True, exist_ok=True)

    if fcntl:
        f = open(lock_file, "w")
        try:
            if blocking:
                fcntl.flock(f, fcntl.LOCK_EX)
            else:
                try:
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    f.close()
                    raise RuntimeError(f"O processo '{lock_name}' já está em execução.")
            yield
        finally:
            try:
                fcntl.flock(f, fcntl.LOCK_UN)
            except Exception:
                pass
            f.close()
    else:
        # Fallback para ambientes sem fcntl (ex: Windows)
        if not blocking and lock_file.exists():
            if time.time() - lock_file.stat().st_mtime < 3600:
                raise RuntimeError(f"O processo '{lock_name}' já está em execução.")

        lock_file.touch()
        try:
            yield
        finally:
            try:
                lock_file.unlink(missing_ok=True)
            except Exception:
                pass
