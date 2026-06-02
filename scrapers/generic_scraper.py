"""
scrapers/generic_scraper.py
----------------------------
Scraper genérico e robusto que consome as definições de resources.yaml.
"""

import base64
import sys
import time
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.base import get_logger, nova_session, salvar_csv, agora_brt
from utils.parsers import (
    decode_bytes,
    csv_rows,
    json_rows,
    xls_rows,
    rows_from_zip,
    enriquecer,
    read_existing_header,
    date_ref,
    replace_date_vars,
)

log = get_logger("generic_scraper")


def clean_csv_text(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ""
    # Se a primeira linha não possuir delimitador (; ou ,), é provável que seja um cabeçalho descritivo (título),
    # então nós a descartamos para que o DictReader leia a linha seguinte como o cabeçalho real.
    first_line = lines[0]
    if ";" not in first_line and "," not in first_line:
        log.info(f"Descartando linha de título do CSV: '{first_line}'")
        return "\n".join(lines[1:])
    return "\n".join(lines)


def run_resource(resource_name: str, output_file_override: Path = None):
    # Carrega definições do resources.yaml
    yaml_path = Path(__file__).resolve().parents[1] / "resources.yaml"
    if not yaml_path.exists():
        log.error(f"Arquivo resources.yaml não encontrado em {yaml_path}")
        sys.exit(1)

    with yaml_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    resources = config.get("resources", [])
    res = next((r for r in resources if r.get("name") == resource_name), None)
    if not res:
        log.error(f"Recurso '{resource_name}' não encontrado no resources.yaml")
        sys.exit(1)

    url_template = res.get("url")
    file_name = res.get("file_name")
    type_response = res.get("type_response")

    # Determina o arquivo de saída
    if output_file_override:
        arquivo_saida = output_file_override
    else:
        # Se não houver override, salva na pasta data/ com o nome baseado no file_name
        base_name = Path(file_name).name
        # Remove a extensão .base64 se existir
        if base_name.endswith(".base64"):
            base_name = base_name[:-7]
        # Altera a extensão final para .csv
        if not base_name.endswith(".csv"):
            ext = Path(base_name).suffix
            if ext:
                base_name = base_name.replace(ext, ".csv")
            else:
                base_name += ".csv"
        arquivo_saida = Path(__file__).resolve().parents[1] / "data" / base_name

    # Substitui as variáveis de data na URL
    dt = date_ref(None)
    url = replace_date_vars(url_template, dt)

    log.info(f"Iniciando captura do recurso: {resource_name}")
    log.info(f"URL de download: {url}")
    log.info(f"Arquivo de destino: {arquivo_saida}")

    session = nova_session()

    # Download com retries
    resp = None
    for tentativa in range(1, 4):
        try:
            resp = session.get(url, timeout=120)
            resp.raise_for_status()
            break
        except Exception as e:
            log.warning(f"Tentativa {tentativa}/3 falhou: {e}")
            if tentativa == 3:
                log.error("Todas as tentativas de download falharam.")
                raise e
            time.sleep(5)

    if not resp or not resp.content:
        log.error("Resposta vazia recebida do servidor.")
        sys.exit(1)

    content = resp.content
    # Evita processar strings como 'null' vindas de endpoints da B3
    if content.strip() == b"null":
        log.warning(f"O servidor retornou 'null' para a URL {url}. Encerrando sem registros.")
        return

    # Parse conforme o tipo de resposta
    rows = []
    if type_response == "json":
        rows = json_rows(resp.json())
    elif type_response == "csv":
        rows = csv_rows(decode_bytes(content))
    elif type_response == "base64":
        content_str = content.decode("utf-8", errors="ignore").strip()
        # Remove aspas se a resposta JSON encapsular o base64
        if content_str.startswith('"') and content_str.endswith('"'):
            content_str = content_str[1:-1]
        try:
            decoded_bytes = base64.b64decode(content_str)
        except Exception as e:
            log.error(f"Falha ao decodificar conteúdo base64: {e}")
            sys.exit(1)
        decoded_text = decode_bytes(decoded_bytes)
        decoded_text = clean_csv_text(decoded_text)
        rows = csv_rows(decoded_text)
    elif type_response == "txt":
        # Se for TXT genérico, converte para linhas
        rows = [{"linha": ln} for ln in decode_bytes(content).splitlines() if ln.strip()]
    elif type_response == "xls":
        rows = xls_rows(content)
    elif type_response == "zip":
        rows = rows_from_zip(content)
    else:
        log.error(f"Tipo de resposta não suportado: {type_response}")
        sys.exit(1)

    if not rows:
        log.warning("Nenhum registro encontrado após o parsing.")
        return

    # Enriquecimento dos dados
    dataset_id = resource_name.lower().replace(" ", "_").replace("-", "_")
    enriched, header_novo = enriquecer(dataset_id, rows)
    header_existente = read_existing_header(arquivo_saida)

    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)

    # Salva no arquivo CSV acumulativo
    salvar_csv(
        arquivo_saida,
        enriched,
        header,
        chaves_dedup=["data_captura", "conjunto", "registro_hash"],
    )
    log.info(f"Sucesso: {len(enriched)} registros salvos em {arquivo_saida}")
