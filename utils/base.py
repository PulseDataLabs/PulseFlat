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


def salvar_csv(
    arquivo: Path,
    registros: list[dict],
    cabecalho: list[str],
    chaves_dedup: list[str] | None = None,
) -> None:
    """
    Salva registros no CSV acumulativo com deduplicação automática.

    Estratégia:
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

    if arquivo.exists():
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
            datas = [r.get("data_captura") for r in registros if r.get("data_captura")]
            if datas:
                last_updates[arquivo.name] = max(datas)
                with last_updates_path.open("w", encoding="utf-8") as lf:
                    json.dump(last_updates, lf, indent=2, ensure_ascii=False)
    except Exception as e:
        log.warning(f"Não foi possível atualizar last_updates.json: {e}")

    log.info(
        f"CSV atualizado → {arquivo} | "
        f"{len(registros)} novos registros salvos"
        + (f" | {substituidas} linha(s) antigas substituídas" if substituidas else "")
    )
