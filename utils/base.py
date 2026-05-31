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


def salvar_csv(arquivo: Path, registros: list[dict], cabecalho: list[str]) -> None:
    """
    Acrescenta registros ao CSV acumulativo (append).
    Cria o arquivo com cabeçalho se ainda não existir.
    """
    log = get_logger("utils.salvar_csv")

    if not registros:
        log.warning("Nenhum registro para salvar — abortando.")
        sys.exit(1)

    arquivo.parent.mkdir(parents=True, exist_ok=True)
    novo = not arquivo.exists()

    with open(arquivo, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cabecalho, extrasaction="ignore")
        if novo:
            writer.writeheader()
        writer.writerows(registros)

    log.info(f"CSV atualizado → {arquivo}  ({len(registros)} linhas adicionadas)")
