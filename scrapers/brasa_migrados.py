"""
scrapers/brasa_migrados.py
--------------------------
Migração de conjuntos do projeto brasa para o padrão PulseFlat.

Regras:
- Apenas coletas via requests (sem Selenium)
- Exclui conjuntos já existentes no PulseFlat
- Saída em CSV com data/hora de captura
"""

import base64
import csv
import hashlib
import io
import json
import os
import re
import sys
import time
import unicodedata
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

import xlrd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import FUSO, b64_encode_params, get_logger, agora_brt, limpar, nova_session, salvar_csv

log = get_logger("brasa_migrados")

FIXOS = ["data_captura", "hora_captura", "conjunto", "arquivo_origem", "registro_hash"]

DATASETS = [
    {
        "id": "anbima_indice_imab",
        "tipo": "xls",
        "url": "https://s3-data-prd-use1-precos.s3.us-east-1.amazonaws.com/arquivos/indices-historico/IMAGERAL-HISTORICO.xls",
        "arquivo": Path("data/anbima_indice_imab.csv"),
    },
    {
        "id": "b3_bvbg028",
        "tipo": "zip_generico",
        "url": "https://www.b3.com.br/pesquisapregao/download?filelist=IN%y%m%d.zip",
        "type_date": "dia_anterior",
        "arquivo": Path("data/b3_bvbg028.csv"),
    },
    {
        "id": "b3_bvbg086",
        "tipo": "zip_generico",
        "url": "https://www.b3.com.br/pesquisapregao/download?filelist=PR%y%m%d.zip",
        "type_date": "dia_anterior",
        "arquivo": Path("data/b3_bvbg086.csv"),
    },
    {
        "id": "b3_bvbg087",
        "tipo": "zip_generico",
        "url": "https://www.b3.com.br/pesquisapregao/download?filelist=IR%y%m%d.zip",
        "type_date": "dia_anterior",
        "arquivo": Path("data/b3_bvbg087.csv"),
    },
    {
        "id": "b3_cotahist_diario",
        "tipo": "zip_fwf_cotahist",
        "url": "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_D%d%m%Y.ZIP",
        "type_date": "dia_anterior",
        "arquivo": Path("data/b3_cotahist_diario.csv"),
    },
    {
        "id": "b3_cotahist_anual",
        "tipo": "zip_fwf_cotahist",
        "url_format": "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{year}.ZIP",
        "year": "current",
        "arquivo": Path("data/b3_cotahist_anual.csv"),
    },
    {
        "id": "b3_indicadores_economicos_fwf",
        "tipo": "zip_fwf_indicadores",
        "url": "https://www.b3.com.br/pesquisapregao/download?filelist=ID%y%m%d.ex_",
        "type_date": "dia_anterior",
        "arquivo": Path("data/b3_indicadores_economicos_fwf.csv"),
    },
    {
        "id": "b3_negocios_balcao",
        "tipo": "b3_otc_base64_csv",
        "url": "https://bvmf.bmfbovespa.com.br/NegociosRealizados/Registro/DownloadArquivoDiretorio?data=%d-%m-%Y",
        "type_date": "dia_anterior",
        "arquivo": Path("data/b3_negocios_balcao.csv"),
    },
    {
        "id": "bcb_sgs_series",
        "tipo": "bcb_sgs",
        "arquivo": Path("data/bcb_sgs_series.csv"),
    },
    {
        "id": "bcb_moedas_ptax",
        "tipo": "bcb_ptax",
        "arquivo": Path("data/bcb_moedas_ptax.csv"),
    },
    {
        "id": "cvm_cadastro_companhias_abertas",
        "tipo": "csv",
        "url": "https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv",
        "arquivo": Path("data/cvm_cadastro_companhias_abertas.csv"),
    },
    {
        "id": "b3_indices_precos_historicos",
        "tipo": "b3_index_history",
        "arquivo": Path("data/b3_indices_precos_historicos.csv"),
    },
    {
        "id": "b3_companhias_detalhes",
        "tipo": "b3_company_details",
        "arquivo": Path("data/b3_companhias_detalhes.csv"),
    },
    {
        "id": "b3_companhias_info",
        "tipo": "b3_company_info",
        "arquivo": Path("data/b3_companhias_info.csv"),
    },
    {
        "id": "b3_dividendos_dinheiro",
        "tipo": "b3_cash_dividends",
        "arquivo": Path("data/b3_dividendos_dinheiro.csv"),
    },
]

COTAHIST_WIDTHS = [2, 8, 2, 12, 3, 12, 10, 3, 4, 13, 13, 13, 13, 13, 13, 13, 5, 18, 18, 13, 1, 8, 7, 13, 12, 3]
COTAHIST_FIELDS = [
    "regtype", "refdate", "bdi_code", "symbol", "instrument_market", "corporation_name", "specification_code",
    "days_to_settlement", "trading_currency", "open", "high", "low", "average", "close", "best_bid", "best_ask",
    "trade_quantity", "traded_contracts", "volume", "strike_price", "strike_price_adjustment_indicator",
    "maturity_date", "allocation_lot_size", "strike_price_in_points", "isin", "distribution_id",
]

INDICADORES_WIDTHS = [6, 3, 2, 8, 2, 25, 25, 2, 36]
INDICADORES_FIELDS = [
    "id_transacao", "compl_transacao", "tipo_registro", "data_geracao_arquivo", "grupo_indicador",
    "cod_indicador", "valor_indicador", "num_casas_decimais", "reserva",
]

SGS_CODES_DEFAULT = [1, 11, 12, 433, 4380, 189]
PTAX_CURRENCIES_DEFAULT = ["USD", "EUR"]
INDEX_CODES_DEFAULT = ["IBOV", "IBRA", "IFIX", "IDIV", "SMLL"]


def _date_ref(type_date: str | None) -> datetime:
    now = datetime.now(FUSO)
    if type_date == "dia_anterior":
        return now - timedelta(days=1)
    if type_date == "mes_anterior":
        return (now.replace(day=1) - timedelta(days=1)).replace(day=1)
    return now


def _replace_date_vars(url: str, type_date: str | None) -> str:
    dt = _date_ref(type_date)
    return dt.strftime(url)


def _decode_bytes(content: bytes) -> str:
    for enc in ("utf-8-sig", "latin1", "cp1252"):
        try:
            return content.decode(enc)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")


def _normalize_key(k: str) -> str:
    key = limpar(k).lower().replace(" ", "_")
    key = re.sub(r"[^a-z0-9_]+", "_", key)
    key = re.sub(r"_+", "_", key).strip("_")
    return key or "campo"


def _normalize_keys(row: dict) -> dict:
    out = {}
    for k, v in row.items():
        out[_normalize_key(str(k))] = limpar(v)
    return out


def _hash_row(row: dict) -> str:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _csv_rows(text: str, delimiter: str | None = None) -> list[dict]:
    text = text.replace("\x00", "").strip()
    if not text:
        return []

    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return []

    if delimiter is None:
        sample = "\n".join(lines[:40])
        try:
            delimiter = csv.Sniffer().sniff(sample, delimiters=";,\t|").delimiter
        except Exception:
            delimiter = ";" if ";" in lines[0] else ","

    try:
        reader = csv.DictReader(io.StringIO("\n".join(lines)), delimiter=delimiter)
        rows = [_normalize_keys(r) for r in reader if any((v or "").strip() for v in r.values())]
        if rows:
            return rows
    except Exception:
        pass

    return [{"linha": ln} for ln in lines]


def _fwf_rows(text: str, fields: list[str], widths: list[int], only_regtype_01: bool = False) -> list[dict]:
    lines = [ln for ln in text.splitlines() if ln.strip()]
    rows = []
    for ln in lines:
        if len(ln) < sum(widths):
            continue
        pos = 0
        row = {}
        for name, width in zip(fields, widths):
            row[name] = ln[pos:pos + width].strip()
            pos += width
        if only_regtype_01 and row.get("regtype") != "01":
            continue
        if "valor_indicador" in row and row.get("num_casas_decimais", "").isdigit():
            casas = int(row["num_casas_decimais"])
            valor = row["valor_indicador"].replace(".", "").replace(",", "")
            if valor.lstrip("-").isdigit() and casas >= 0:
                if casas:
                    sinal = "-" if valor.startswith("-") else ""
                    dig = valor.lstrip("-")
                    dig = dig.rjust(casas + 1, "0")
                    row["valor_indicador"] = f"{sinal}{dig[:-casas]}.{dig[-casas:]}"
                else:
                    row["valor_indicador"] = valor
        rows.append(_normalize_keys(row))
    return rows


def _json_rows(payload) -> list[dict]:
    if isinstance(payload, dict):
        if isinstance(payload.get("results"), list):
            items = payload["results"]
        elif isinstance(payload.get("data"), list):
            items = payload["data"]
        else:
            items = [payload]
    elif isinstance(payload, list):
        items = payload
    else:
        items = [{"valor": str(payload)}]

    rows = []
    for it in items:
        if isinstance(it, dict):
            flat = {}
            for k, v in it.items():
                if isinstance(v, (dict, list)):
                    flat[k] = json.dumps(v, ensure_ascii=False)
                else:
                    flat[k] = limpar(v)
            rows.append(_normalize_keys(flat))
        else:
            rows.append({"valor": limpar(it)})
    return rows


def _strip_ns(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def _xml_rows(content: bytes) -> list[dict]:
    root = ET.fromstring(content)
    rows = []
    for elem in root.iter():
        children = list(elem)
        if not children:
            continue
        if any(list(ch) for ch in children):
            continue
        row = {"xml_tag": _strip_ns(elem.tag)}
        for ch in children:
            row[_normalize_key(_strip_ns(ch.tag))] = limpar(ch.text)
        if len(row) > 1:
            rows.append(row)
    if rows:
        return rows
    return [{"xml_root": _strip_ns(root.tag), "xml_tamanho_bytes": str(len(content))}]


def _xls_rows(content: bytes) -> list[dict]:
    def _norm_sheet_name(name: str) -> str:
        txt = unicodedata.normalize("NFKD", name)
        txt = "".join(c for c in txt if not unicodedata.combining(c))
        return txt.lower()

    book = xlrd.open_workbook(file_contents=content)
    target = None
    for name in book.sheet_names():
        if _norm_sheet_name(name) == "historico":
            target = name
            break
    sheet = book.sheet_by_name(target) if target else book.sheet_by_index(0)
    headers = [_normalize_key(str(sheet.cell_value(0, c))) for c in range(sheet.ncols)]
    rows = []
    for r in range(1, sheet.nrows):
        item = {}
        has_value = False
        for c, key in enumerate(headers):
            value = sheet.cell_value(r, c)
            if isinstance(value, float):
                if value.is_integer():
                    value = str(int(value))
                else:
                    value = str(value)
            else:
                value = limpar(value)
            item[key] = value
            if value:
                has_value = True
        if has_value:
            rows.append(item)
    return rows


def _read_existing_header(arquivo: Path) -> list[str]:
    if not arquivo.exists():
        return []
    with arquivo.open(newline="", encoding="utf-8") as f:
        first = f.readline().strip()
    return [c.strip() for c in first.split(",") if c.strip()] if first else []


def _enriquecer_rows(dataset_id: str, rows: list[dict]) -> tuple[list[dict], list[str]]:
    data_captura, hora_captura = agora_brt()
    enriched = []
    campos = set()
    for row in rows:
        item = {k: limpar(v) for k, v in row.items()}
        item["data_captura"] = data_captura
        item["hora_captura"] = hora_captura
        item["conjunto"] = dataset_id
        item.setdefault("arquivo_origem", "")
        item["registro_hash"] = _hash_row({k: v for k, v in item.items() if k not in ("data_captura", "hora_captura")})
        campos.update(item.keys())
        enriched.append(item)

    ordenados = [c for c in sorted(campos) if c not in FIXOS]
    header = ["data_captura", "hora_captura", "conjunto", "arquivo_origem"] + ordenados + ["registro_hash"]
    return enriched, header


def _rows_from_response(content: bytes, tipo: str) -> list[dict]:
    if tipo == "csv":
        return _csv_rows(_decode_bytes(content))
    if tipo == "json":
        return _json_rows(json.loads(_decode_bytes(content)))
    if tipo == "xls":
        return _xls_rows(content)
    if tipo == "zip_generico":
        rows = []
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            for info in zf.infolist():
                if info.is_dir() or info.file_size == 0:
                    continue
                raw = zf.read(info.filename)
                lower = info.filename.lower()
                if lower.endswith(".xml"):
                    parsed = _xml_rows(raw)
                elif lower.endswith((".csv", ".txt", ".tsv")):
                    parsed = _csv_rows(_decode_bytes(raw))
                else:
                    parsed = [{"arquivo_binario": info.filename, "tamanho_bytes": str(info.file_size)}]
                for r in parsed:
                    r["arquivo_origem"] = info.filename
                    rows.append(r)
        return rows
    if tipo == "zip_fwf_cotahist":
        rows = []
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            for info in zf.infolist():
                if info.is_dir() or info.file_size == 0:
                    continue
                text = _decode_bytes(zf.read(info.filename))
                parsed = _fwf_rows(text, COTAHIST_FIELDS, COTAHIST_WIDTHS, only_regtype_01=True)
                for r in parsed:
                    r["arquivo_origem"] = info.filename
                    rows.append(r)
        return rows
    if tipo == "zip_fwf_indicadores":
        rows = []
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            for info in zf.infolist():
                if info.is_dir() or info.file_size == 0:
                    continue
                text = _decode_bytes(zf.read(info.filename))
                parsed = _fwf_rows(text, INDICADORES_FIELDS, INDICADORES_WIDTHS)
                for r in parsed:
                    r["arquivo_origem"] = info.filename
                    rows.append(r)
        return rows
    if tipo == "b3_otc_base64_csv":
        txt = _decode_bytes(content).strip()
        decoded = txt
        if not txt.startswith("Data;") and not txt.startswith("Instrumento"):
            try:
                decoded_bytes = base64.b64decode(txt, validate=False)
                decoded = _decode_bytes(decoded_bytes)
            except Exception:
                decoded = txt
        rows = _csv_rows(decoded, delimiter=";")
        return [r for r in rows if str(r.get("data", "")).lower() != "data"]
    return []


def _download_simple(session, cfg: dict) -> tuple[list[dict], str]:
    if cfg.get("url_format"):
        year = datetime.now(FUSO).year if cfg.get("year") == "current" else int(cfg.get("year"))
        url = cfg["url_format"].format(year=year)
    else:
        url = _replace_date_vars(cfg["url"], cfg.get("type_date"))
    resp = session.get(url, timeout=180)
    resp.raise_for_status()
    rows = _rows_from_response(resp.content, cfg["tipo"])
    return rows, url


def _parse_env_int_list(name: str, default: list[int]) -> list[int]:
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return default
    out = []
    for p in raw.split(","):
        p = p.strip()
        if p.isdigit():
            out.append(int(p))
    return out or default


def _parse_env_str_list(name: str, default: list[str]) -> list[str]:
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return default
    out = [p.strip().upper() for p in raw.split(",") if p.strip()]
    return out or default


def _parse_env_int(name: str, default: int) -> int:
    raw = (os.getenv(name) or "").strip()
    return int(raw) if raw.isdigit() else default


def _download_bcb_sgs(session, cfg: dict) -> tuple[list[dict], str]:
    codes = _parse_env_int_list("BRASA_BCB_SGS_CODES", SGS_CODES_DEFAULT)
    end = datetime.now(FUSO).date()
    lookback_days = _parse_env_int("BRASA_BCB_SGS_DAYS", 45)
    start = end - timedelta(days=lookback_days)
    rows = []
    for code in codes:
        url = (
            f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?formato=json"
            f"&dataInicial={start.strftime('%d/%m/%Y')}&dataFinal={end.strftime('%d/%m/%Y')}"
        )
        try:
            resp = session.get(url, timeout=90)
            resp.raise_for_status()
            for row in _json_rows(resp.json()):
                row["codigo_serie"] = str(code)
                rows.append(row)
        except Exception as e:
            log.warning(f"[bcb_sgs_series] código {code} falhou: {e}")
    return rows, "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"


def _download_bcb_ptax(session, cfg: dict) -> tuple[list[dict], str]:
    moedas = _parse_env_str_list("BRASA_BCB_PTAX_MOEDAS", PTAX_CURRENCIES_DEFAULT)
    end = datetime.now(FUSO).date()
    lookback_days = _parse_env_int("BRASA_BCB_PTAX_DAYS", 7)
    start = end - timedelta(days=lookback_days)
    rows = []
    for moeda in moedas:
        url = (
            "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
            "CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
            f"@moeda='{moeda}'&@dataInicial='{start.strftime('%m-%d-%Y')}'&@dataFinalCotacao='{end.strftime('%m-%d-%Y')}'"
            "&$format=json"
        )
        try:
            resp = session.get(url, timeout=90)
            resp.raise_for_status()
            payload = resp.json()
            for row in _json_rows(payload.get("value", [])):
                row["moeda"] = moeda
                rows.append(row)
        except Exception as e:
            log.warning(f"[bcb_moedas_ptax] moeda {moeda} falhou: {e}")
    return rows, "https://olinda.bcb.gov.br/olinda/servico/PTAX"


def _b3_get_company_seeds(session) -> list[dict]:
    base = "https://sistemaswebb3-listados.b3.com.br/shareCapitalProxy/ShareCapitalCall/GetList/"
    seeds = []
    page = 1
    while True:
        payload = {"name": "", "pageNumber": page, "pageSize": 200, "language": "pt-br"}
        url = base + b64_encode_params(payload)
        resp = session.get(url, timeout=120)
        resp.raise_for_status()
        data = resp.json() or {}
        items = data.get("results") or data.get("result") or data.get("data") or []
        for it in items:
            code_cvm = limpar(it.get("codeCVM") or it.get("codeCvm") or it.get("codCvm"))
            trading_name = limpar(it.get("companyName") or it.get("tradingName") or it.get("name"))
            issuing = limpar(it.get("issuingCompany") or it.get("code") or it.get("acronym"))
            if not issuing and trading_name:
                issuing = re.sub(r"\W+", "", trading_name.upper())
            seeds.append({
                "codeCVM": code_cvm,
                "tradingName": trading_name,
                "issuingCompany": issuing,
            })
        total_pages = (data.get("page") or {}).get("totalPages") or 1
        if page >= int(total_pages):
            break
        page += 1
        time.sleep(0.2)
    uniq = []
    seen = set()
    for s in seeds:
        key = (s["codeCVM"], s["tradingName"], s["issuingCompany"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(s)
    return uniq


def _download_b3_company_details(session, cfg: dict) -> tuple[list[dict], str]:
    seeds = _b3_get_company_seeds(session)
    base = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetDetail/"
    rows = []
    for s in seeds:
        if not s["codeCVM"]:
            continue
        url = base + b64_encode_params({"codeCVM": s["codeCVM"], "language": "pt-br"})
        try:
            resp = session.get(url, timeout=60)
            resp.raise_for_status()
            payload = resp.json() or {}
            row = _normalize_keys(payload)
            if row:
                row["codecvm_consulta"] = s["codeCVM"]
                rows.append(row)
        except Exception as e:
            log.warning(f"[b3_companhias_detalhes] codeCVM {s['codeCVM']} falhou: {e}")
        time.sleep(0.2)
    return rows, base


def _download_b3_company_info(session, cfg: dict) -> tuple[list[dict], str]:
    seeds = _b3_get_company_seeds(session)
    base = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedSupplementCompany/"
    rows = []
    for s in seeds:
        if not s["issuingCompany"]:
            continue
        url = base + b64_encode_params({"issuingCompany": s["issuingCompany"], "language": "pt-br"})
        try:
            resp = session.get(url, timeout=60)
            resp.raise_for_status()
            payload = resp.json() or {}
            base_row = payload.get("info") if isinstance(payload.get("info"), dict) else payload
            if isinstance(base_row, dict):
                row = _normalize_keys(base_row)
                row["issuingcompany_consulta"] = s["issuingCompany"]
                rows.append(row)
            for sub_key in ("cashDividends", "stockDividends", "subscriptions"):
                for item in payload.get(sub_key, []) or []:
                    sub_row = _normalize_keys(item)
                    sub_row["tipo_bloco"] = _normalize_key(sub_key)
                    sub_row["issuingcompany_consulta"] = s["issuingCompany"]
                    rows.append(sub_row)
        except Exception as e:
            log.warning(f"[b3_companhias_info] issuingCompany {s['issuingCompany']} falhou: {e}")
        time.sleep(0.2)
    return rows, base


def _download_b3_cash_dividends(session, cfg: dict) -> tuple[list[dict], str]:
    seeds = _b3_get_company_seeds(session)
    base = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedCashDividends/"
    rows = []
    for s in seeds:
        trading_name = s["tradingName"]
        if not trading_name:
            continue
        page = 1
        while True:
            payload = {"tradingName": trading_name, "language": "pt-br", "pageNumber": page, "pageSize": 200}
            url = base + b64_encode_params(payload)
            try:
                resp = session.get(url, timeout=60)
                resp.raise_for_status()
                data = resp.json() or {}
                result = data.get("results") or []
                for item in result:
                    row = _normalize_keys(item)
                    row["trading_name_consulta"] = trading_name
                    rows.append(row)
                total_pages = (data.get("page") or {}).get("totalPages") or 1
                if page >= int(total_pages or 1):
                    break
                page += 1
                time.sleep(0.2)
            except Exception as e:
                log.warning(f"[b3_dividendos_dinheiro] tradingName {trading_name} falhou: {e}")
                break
        time.sleep(0.1)
    return rows, base


def _download_b3_index_history(session, cfg: dict) -> tuple[list[dict], str]:
    indices = _parse_env_str_list("BRASA_B3_INDICES", INDEX_CODES_DEFAULT)
    ano_atual = datetime.now(FUSO).year
    anos = [ano_atual - 1, ano_atual]
    base = "https://sistemaswebb3-listados.b3.com.br/indexStatisticsProxy/IndexCall/GetPortfolioDay/"
    rows = []
    for idx in indices:
        for ano in anos:
            url = base + b64_encode_params({"language": "pt-br", "year": ano, "index": idx})
            try:
                resp = session.get(url, timeout=60)
                resp.raise_for_status()
                data = resp.json() or {}
                result = data.get("results") or []
                for item in result:
                    row = _normalize_keys(item)
                    row["indice"] = idx
                    row["ano"] = str(ano)
                    rows.append(row)
            except Exception as e:
                log.warning(f"[b3_indices_precos_historicos] {idx}/{ano} falhou: {e}")
            time.sleep(0.2)
    return rows, base


def _baixar_dataset(session, cfg: dict) -> tuple[list[dict], str]:
    tipo = cfg["tipo"]
    if tipo in {"csv", "xls", "zip_generico", "zip_fwf_cotahist", "zip_fwf_indicadores", "b3_otc_base64_csv"}:
        return _download_simple(session, cfg)
    if tipo == "bcb_sgs":
        return _download_bcb_sgs(session, cfg)
    if tipo == "bcb_ptax":
        return _download_bcb_ptax(session, cfg)
    if tipo == "b3_index_history":
        return _download_b3_index_history(session, cfg)
    if tipo == "b3_company_details":
        return _download_b3_company_details(session, cfg)
    if tipo == "b3_company_info":
        return _download_b3_company_info(session, cfg)
    if tipo == "b3_cash_dividends":
        return _download_b3_cash_dividends(session, cfg)
    raise RuntimeError(f"Tipo não suportado: {tipo}")


def capturar() -> tuple[int, int]:
    session = nova_session()
    total_ok, total_err = 0, 0

    for cfg in DATASETS:
        dataset_id = cfg["id"]
        arquivo = cfg["arquivo"]
        log.info(f"[{dataset_id}] Capturando...")

        try:
            rows, _ = _baixar_dataset(session, cfg)
            if not rows:
                raise RuntimeError("Sem linhas após processamento")

            enriched, header_novo = _enriquecer_rows(dataset_id, rows)
            header_existente = _read_existing_header(arquivo)
            header = []
            for col in header_existente + header_novo:
                if col and col not in header:
                    header.append(col)

            salvar_csv(
                arquivo,
                enriched,
                header,
                chaves_dedup=["data_captura", "conjunto", "registro_hash"],
            )
            log.info(f"[{dataset_id}] {len(enriched)} linha(s) salvas em {arquivo}")
            total_ok += 1
            time.sleep(0.4)
        except Exception as e:
            log.error(f"[{dataset_id}] Falha: {e}")
            total_err += 1

    return total_ok, total_err


def main():
    log.info("=== Migração brasa (requests) ===")
    ok, err = capturar()
    log.info(f"Conjuntos processados: {ok} OK | {err} erro(s)")
    if err:
        sys.exit(1)


if __name__ == "__main__":
    main()
