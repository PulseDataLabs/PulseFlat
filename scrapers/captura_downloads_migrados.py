"""
scrapers/captura_downloads_migrados.py
-------------------------------------
Migra conjuntos do projeto captura_downloads para o padrão PulseFlat.

Regras:
- Apenas fontes compatíveis com requests (sem Selenium)
- Exclui conjuntos já cobertos pelos scrapers atuais do PulseFlat
- Saída sempre em CSV com data/hora de captura
"""

import csv
import hashlib
import io
import json
import sys
import time
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import FUSO, get_logger, agora_brt, limpar, nova_session, salvar_csv

log = get_logger("captura_downloads_migrados")


DATASETS = [
    {
        "id": "anbima_mercado_secundario_debentures",
        "url": "https://www.anbima.com.br/informacoes/merc-sec-debentures/arqs/dbYYMMDD.txt",
        "tipo": "texto_tabular",
        "type_date": "dia_anterior",
        "arquivo": Path("data/anbima_mercado_secundario_debentures.csv"),
    },
    {
        "id": "anbima_mercado_secundario_titulos_publicos",
        "url": "https://www.anbima.com.br/informacoes/merc-sec/arqs/msYYMMDD.txt",
        "tipo": "texto_tabular",
        "type_date": "dia_anterior",
        "arquivo": Path("data/anbima_mercado_secundario_titulos_publicos.csv"),
    },
    {
        "id": "anbima_ima_completo",
        "url": "https://www.anbima.com.br/informacoes/ima/arqs/ima_completo.txt",
        "tipo": "texto_tabular",
        "arquivo": Path("data/anbima_ima_completo.csv"),
    },
    {
        "id": "bacen_negociacao_tpf_extragrupo_mes_corrente",
        "url": "https://www4.bcb.gov.br/pom/demab/negociacoes/download/NegEYYYYMM.ZIP",
        "tipo": "zip_tabular",
        "type_date": "mes_atual",
        "arquivo": Path("data/bacen_negociacao_tpf_extragrupo_mes_corrente.csv"),
    },
    {
        "id": "bacen_negociacao_tpf_extragrupo_mes_anterior",
        "url": "https://www4.bcb.gov.br/pom/demab/negociacoes/download/NegEYYYYMM.ZIP",
        "tipo": "zip_tabular",
        "type_date": "mes_anterior",
        "arquivo": Path("data/bacen_negociacao_tpf_extragrupo_mes_anterior.csv"),
    },
    {
        "id": "b3_instrumentos_listados",
        "url_token": "https://arquivos.b3.com.br/api/download/requestname?fileName=InstrumentsConsolidatedFile&date=YYYY-MM-DD&recaptchaToken=",
        "url": "https://arquivos.b3.com.br/api/download/?token=B3_TOKEN",
        "tipo": "csv_tabular",
        "type_date": "dia_anterior",
        "arquivo": Path("data/b3_instrumentos_listados.csv"),
    },
    {
        "id": "b3_indicadores_financeiros",
        "url": "https://sistemaswebb3-derivativos.b3.com.br/financialIndicatorsProxy/FinancialIndicators/GetFinancialIndicators/eyJsYW5ndWFnZSI6InB0LWJyIn0=",
        "tipo": "json",
        "arquivo": Path("data/b3_indicadores_financeiros.csv"),
    },
    {
        "id": "b3_taxa_cambio_referencia",
        "url": "https://sistemaswebb3-derivativos.b3.com.br/financialIndicatorsProxy/ReferenceExchangeRate/GetReferenceExchangeRate/eyJsYW5ndWFnZSI6InB0LWJyIn0=",
        "tipo": "json",
        "arquivo": Path("data/b3_taxa_cambio_referencia.csv"),
    },
    {
        "id": "b3_capital_social_empresas",
        "url": "https://sistemaswebb3-listados.b3.com.br/shareCapitalProxy/ShareCapitalCall/GetList/eyJuYW1lIjoiIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjEyMH0=",
        "tipo": "json",
        "arquivo": Path("data/b3_capital_social_empresas.csv"),
    },
    {
        "id": "debentures_emissoes_caracteristicas",
        "url": "https://www.debentures.com.br/exploreosnd/consultaadados/emissoesdedebentures/caracteristicas_e.asp?tip_deb=publicas&op_exc=Nada",
        "tipo": "csv_tabular",
        "arquivo": Path("data/debentures_emissoes_caracteristicas.csv"),
    },
    {
        "id": "debentures_mercado_secundario_precos_negociacao",
        "url": "https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_e.asp?op_exc=Nada&emissor=&isin=&ativo=&dt_ini=20250101&dt_fim=YYYYMMDD",
        "tipo": "csv_tabular",
        "arquivo": Path("data/debentures_mercado_secundario_precos_negociacao.csv"),
    },
    {
        "id": "debentures_mercado_pu_historico",
        "url": "https://www.debentures.com.br/exploreosnd/consultaadados/emissoesdedebentures/puhistorico_e.asp?op_exc=Nada&ativo=&dt_ini=01/01/2025&dt_fim=DD/MM/YYYY&Submit.x=16&Submit.y=14",
        "tipo": "csv_tabular",
        "arquivo": Path("data/debentures_mercado_pu_historico.csv"),
    },
    {
        "id": "cvm_cad_fi",
        "url": "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv",
        "tipo": "csv_tabular",
        "arquivo": Path("data/cvm_cad_fi.csv"),
    },
    {
        "id": "cvm_extrato_fi",
        "url": "https://dados.cvm.gov.br/dados/FI/DOC/EXTRATO/DADOS/extrato_fi.csv",
        "tipo": "csv_tabular",
        "arquivo": Path("data/cvm_extrato_fi.csv"),
    },
    {
        "id": "cvm_registro_fundo_classe",
        "url": "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/registro_fundo_classe.zip",
        "tipo": "zip_tabular",
        "arquivo": Path("data/cvm_registro_fundo_classe.csv"),
    },
    {
        "id": "b3_classificacao_setorial",
        "url": "https://bvmf.bmfbovespa.com.br/InstDados/InformacoesEmpresas/ClassifSetorial.zip",
        "tipo": "zip_tabular",
        "arquivo": Path("data/b3_classificacao_setorial.csv"),
    },
    {
        "id": "b3_titulos_negociaveis",
        "url": "https://bvmf.bmfbovespa.com.br/suplemento/ExecutaAcaoDownload.asp?arquivo=Titulos_Negociaveis.zip&server=L",
        "tipo": "zip_tabular",
        "arquivo": Path("data/b3_titulos_negociaveis.csv"),
    },
]

FIXOS = ["data_captura", "hora_captura", "conjunto", "arquivo_origem", "registro_hash"]


def _date_ref(type_date: str | None) -> datetime:
    now = datetime.now(FUSO)
    if type_date == "dia_anterior":
        return now - timedelta(days=1)
    if type_date == "mes_anterior":
        return (now.replace(day=1) - timedelta(days=1)).replace(day=1)
    return now


def _replace_date_vars(url: str, type_date: str | None) -> str:
    dt = _date_ref(type_date)
    mapping = {
        "DD/MM/YYYY": dt.strftime("%d/%m/%Y"),
        "YYYY-MM-DD": dt.strftime("%Y-%m-%d"),
        "YYYYMMDD": dt.strftime("%Y%m%d"),
        "YYMMDD": dt.strftime("%y%m%d"),
        "YYYYMM": dt.strftime("%Y%m"),
    }
    for key, value in mapping.items():
        url = url.replace(key, value)
    return url


def _decode_bytes(content: bytes) -> str:
    for enc in ("utf-8-sig", "latin1", "cp1252"):
        try:
            return content.decode(enc)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")


def _normalize_keys(row: dict) -> dict:
    out = {}
    for k, v in row.items():
        key = limpar(k).lower().replace(" ", "_") or "campo"
        out[key] = limpar(v)
    return out


def _csv_rows(text: str) -> list[dict]:
    text = text.replace("\x00", "").strip()
    if not text:
        return []

    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return []

    sample = "\n".join(lines[:40])
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=";,\t|")
        delim = dialect.delimiter
    except Exception:
        delim = ";" if ";" in lines[0] else ","

    try:
        reader = csv.DictReader(io.StringIO("\n".join(lines)), delimiter=delim)
        rows = [_normalize_keys(r) for r in reader if any((v or "").strip() for v in r.values())]
        if rows:
            return rows
    except Exception:
        pass

    # fallback: arquivo não tabular; guarda linha a linha
    return [{"linha": ln} for ln in lines]


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


def _hash_row(row: dict) -> str:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _coletar_token_b3(session, cfg: dict) -> str:
    url_token = _replace_date_vars(cfg["url_token"], cfg.get("type_date"))
    resp = session.get(url_token, timeout=60)
    resp.raise_for_status()
    return (resp.json() or {}).get("token", "")


def _rows_from_response(content: bytes, tipo: str) -> list[dict]:
    if tipo in ("csv_tabular", "texto_tabular"):
        return _csv_rows(_decode_bytes(content))
    if tipo == "json":
        return _json_rows(json.loads(_decode_bytes(content)))
    if tipo == "zip_tabular":
        rows = []
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            for info in zf.infolist():
                if info.is_dir() or info.file_size == 0:
                    continue
                name = info.filename
                raw = zf.read(name)
                if name.lower().endswith((".csv", ".txt", ".tsv")):
                    for row in _csv_rows(_decode_bytes(raw)):
                        row["arquivo_origem"] = name
                        rows.append(row)
                else:
                    rows.append({"arquivo_origem": name, "tamanho_bytes": str(info.file_size)})
        return rows
    return []


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


def _baixar_dataset(session, cfg: dict) -> tuple[list[dict], str]:
    url = _replace_date_vars(cfg["url"], cfg.get("type_date"))

    if cfg.get("url_token"):
        token = _coletar_token_b3(session, cfg)
        if not token:
            raise RuntimeError("Token B3 não retornado")
        url = url.replace("B3_TOKEN", token)

    resp = session.get(url, timeout=120)
    resp.raise_for_status()
    return _rows_from_response(resp.content, cfg["tipo"]), url


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
    log.info("=== Migração captura_downloads (requests) ===")
    ok, err = capturar()
    log.info(f"Conjuntos processados: {ok} OK | {err} erro(s)")
    if err:
        sys.exit(1)


if __name__ == "__main__":
    main()
