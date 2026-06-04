"""
utils/base.py
-------------
Funções e classes utilitárias compartilhadas por todos os scrapers.
"""

import csv
import json
import logging
import sys
from base64 import b64encode
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

import time

# Patch global do requests para impor limite e padrão de timeout (evita travamentos longos)
_orig_request = requests.Session.request

def _patched_request(self, method, url, *args, **kwargs):
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

FUSO = ZoneInfo("America/Sao_Paulo")

HEADERS_HTTP = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept":  "application/json, text/plain, */*",
    "Referer": "https://www.b3.com.br/",
    "Origin":  "https://www.b3.com.br",
}


def get_logger(name: str) -> logging.Logger:
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
    if valor is None:
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
        with arquivo.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, [])
            return [col.strip() for col in header if col.strip()]
    except Exception:
        return []


def salvar_csv(
    arquivo: Path,
    registros: list[dict],
    cabecalho: list[str],
    chaves_dedup: list[str] | None = None,
    acumular: bool = True,
) -> None:
    """
    Salva registros no CSV acumulativo com deduplicação automática.

    Estratégia:
    - Se `acumular` for False, sobrescreve o arquivo existente apenas com os novos registros.
    - Se `chaves_dedup` for fornecido, remove do CSV existente qualquer linha
      cujo conjunto de chaves coincida com algum novo registro (ex: mesma
      data_captura + mesmo indicador). Assim, re-execuções no mesmo dia
      substituem a captura anterior em vez de duplicar.
    - Se `chaves_dedup` for None, remove todas as linhas com a mesma
      `data_captura` dos novos dados (dedup simples por dia).
    - O histórico de dias anteriores é sempre preservado integralmente.
    """
    log = get_logger("utils.salvar_csv")

    if not registros:
        log.warning("Nenhum registro para salvar — abortando.")
        sys.exit(1)

    arquivo.parent.mkdir(parents=True, exist_ok=True)

    # Se acumular e o arquivo existir, mescla o cabeçalho existente para preservar colunas antigas e a ordem
    if acumular and arquivo.exists():
        header_existente = read_existing_header(arquivo)
        merged = []
        for col in header_existente + cabecalho:
            if col and col not in merged:
                merged.append(col)
        cabecalho = merged

    # Determina datas presentes nos novos dados (para dedup simples)
    datas_novas = {r.get("data_captura") for r in registros}

    # Determina chaves compostas dos novos dados (para dedup preciso)
    chaves_novas: set[tuple] | None = None
    if chaves_dedup:
        chaves_novas = {
            tuple(r.get(c, "") for c in chaves_dedup)
            for r in registros
        }

    linhas_anteriores: list[dict] = []
    substituidas = 0

    if acumular and arquivo.exists():
        with arquivo.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for linha in reader:
                if chaves_novas is not None:
                    chave = tuple(linha.get(c, "") for c in chaves_dedup)
                    if chave in chaves_novas:
                        substituidas += 1
                        continue
                else:
                    if linha.get("data_captura") in datas_novas:
                        substituidas += 1
                        continue
                linhas_anteriores.append(linha)

    todas = linhas_anteriores + registros

    with arquivo.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cabecalho, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(todas)

    # Atualiza data/last_updates.json com a data mais recente
    try:
        last_updates_path = arquivo.parent / "last_updates.json"
        last_updates = {}
        if last_updates_path.exists():
            try:
                with last_updates_path.open("r", encoding="utf-8") as lf:
                    last_updates = json.load(lf)
            except Exception:
                pass
        
        if registros:
            # Identifica a coluna de data no cabeçalho
            date_col = None
            for candidate in ["data_captura", "data_referencia", "data", "rpt_dt"]:
                if candidate in cabecalho:
                    date_col = candidate
                    break
            
            if date_col:
                datas = [r.get(date_col) for r in todas if r.get(date_col)]
                if datas:
                    last_updates[arquivo.name] = {
                        "min": min(datas),
                        "max": max(datas)
                    }
                    with last_updates_path.open("w", encoding="utf-8") as lf:
                        json.dump(last_updates, lf, indent=2, ensure_ascii=False)
                    
                    # Salva também como last_updates.js para carregamento local offline (file://)
                    last_updates_js_path = arquivo.parent / "last_updates.js"
                    with last_updates_js_path.open("w", encoding="utf-8") as lf:
                        lf.write(f"window.PULSEFLAT_LAST_UPDATES = {json.dumps(last_updates, indent=2, ensure_ascii=False)};\n")
    except Exception as e:
        log.warning(f"Não foi possível atualizar last_updates.json/js: {e}")

    log.info(
        f"CSV atualizado → {arquivo} | "
        f"{len(registros)} novos registros salvos"
        + (f" | {substituidas} linha(s) antigas substituídas" if substituidas else "")
    )
