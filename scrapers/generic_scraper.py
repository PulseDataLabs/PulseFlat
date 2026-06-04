"""
scrapers/generic_scraper.py
----------------------------
Scraper genérico e robusto baseado em classes que consome as definições de resources.yaml.
"""

import base64
import sys
import time
from pathlib import Path
import yaml
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.utils.base import BaseScraper
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


def _limpar_int(valor) -> str:
    if valor is None:
        return ""
    texto = str(valor).strip()
    clean = texto.replace(".", "").replace(" ", "")
    if "," in clean:
        clean = clean.split(",")[0]
    return clean


def _limpar_float(valor) -> str:
    if valor is None:
        return ""
    texto = str(valor).strip()
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    return texto.replace("%", "").strip()


def clean_csv_text(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ""
    
    idx = 0
    for i, line in enumerate(lines[:10]):
        num_delimiters = sum(line.count(d) for d in (";", ",", "\t", "|"))
        if num_delimiters >= 4:
            idx = i
            break
    else:
        idx = 0
    
    if idx > 0:
        log.info(f"Descartadas {idx} linhas de título descritivo do CSV.")
        return "\n".join(lines[idx:])
    return "\n".join(lines)


class GenericScraper(BaseScraper):
    resource_name = ""

    def __init__(self, resource_name=None):
        if resource_name:
            self.resource_name = resource_name

        yaml_path = Path(__file__).resolve().parents[1] / "resources.yaml"
        if not yaml_path.exists():
            raise RuntimeError(f"Arquivo resources.yaml não encontrado em {yaml_path}")

        with yaml_path.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        resources = config.get("resources", [])
        self.res_config = next((r for r in resources if r.get("name") == self.resource_name), None)
        if not self.res_config:
            raise ValueError(f"Recurso '{self.resource_name}' não encontrado no resources.yaml")

        file_name = self.res_config.get("file_name")
        base_name = Path(file_name).name
        if base_name.endswith(".base64"):
            base_name = base_name[:-7]
        if not base_name.endswith(".csv"):
            ext = Path(base_name).suffix
            if ext:
                base_name = base_name.replace(ext, ".csv")
            else:
                base_name += ".csv"

        self.name = base_name.replace(".csv", "")
        self.accumulate = self.res_config.get("acumular", True)

        is_portfolio = self.resource_name.startswith("B3 - Carteira Teórica")
        if is_portfolio:
            self.chaves_dedup = ["data_captura", "indice", "codigo_ativo"]
        else:
            self.chaves_dedup = ["data_captura", "conjunto", "registro_hash"]

        super().__init__()

    def fetch(self) -> pd.DataFrame:
        url_template = self.res_config.get("url")
        file_name = self.res_config.get("file_name")
        type_response = self.res_config.get("type_response")

        dt = date_ref(None)
        url = replace_date_vars(url_template, dt)

        self.logger.info(f"URL de download: {url}")

        session = nova_session()
        resp = None
        for tentativa in range(1, 4):
            try:
                resp = session.get(url, timeout=120)
                resp.raise_for_status()
                break
            except Exception as e:
                self.logger.warning(f"Tentativa {tentativa}/3 falhou: {e}")
                if tentativa == 3:
                    raise e
                time.sleep(5)

        if not resp or not resp.content:
            raise RuntimeError("Resposta vazia recebida do servidor.")

        content = resp.content
        if content.strip() == b"null":
            self.logger.warning(f"O servidor retornou 'null' para a URL {url}. Encerrando sem registros.")
            return pd.DataFrame()

        is_portfolio = self.resource_name.startswith("B3 - Carteira Teórica")
        rows = []

        if is_portfolio:
            content_str = content.decode("utf-8", errors="ignore").strip()
            if content_str.startswith('"') and content_str.endswith('"'):
                content_str = content_str[1:-1]
            try:
                decoded_bytes = base64.b64decode(content_str)
            except Exception as e:
                self.logger.error(f"Falha ao decodificar conteúdo base64: {e}")
                sys.exit(1)
            decoded_text = decode_bytes(decoded_bytes)
            
            base_name = Path(file_name).name
            key = base_name.replace("b3_carteira_teorica_", "").split(".")[0]
            MAP_INDICES = {
                "ibov": ("IBOV", "Ibovespa"),
                "smll": ("SMLL", "Small Cap"),
                "bdrx": ("BDRX", "BDRX"),
                "isee": ("ISEE", "ISEE"),
                "ibxl": ("IBXL", "IBrX 50"),
                "ifnc": ("IFNC", "Índice Financeiro"),
                "agfs_iagro": ("AGFS", "AGFS"),
                "ibsd": ("IBSD", "IBSD"),
            }
            index_code, index_name = MAP_INDICES.get(key, (key.upper(), key.upper()))
            data_captura, _ = agora_brt()

            lines = [ln.strip() for ln in decoded_text.splitlines() if ln.strip()]
            for ln in lines:
                parts = [p.strip() for p in ln.split(";")]
                if len(parts) < 5:
                    continue
                if parts[0].lower() in ("código", "cdigo", "codigo") or "carteira" in parts[0].lower() or "dia" in parts[0].lower():
                    continue
                if "total" in parts[0].lower() or "redutor" in parts[0].lower():
                    continue

                rows.append({
                    "data_captura":       data_captura,
                    "indice":             index_code,
                    "indice_nome":        index_name,
                    "codigo_ativo":       parts[0],
                    "nome_ativo":         parts[1],
                    "tipo_ativo":         parts[2],
                    "quantidade_teorica": _limpar_int(parts[3]),
                    "participacao_pct":   _limpar_float(parts[4]),
                    "reducao_capital":    _limpar_float(parts[5]) if len(parts) > 5 else "",
                    "segmento":           parts[6] if len(parts) > 6 else "",
                })
        else:
            if type_response == "json":
                rows = json_rows(resp.json())
            elif type_response == "csv":
                decoded_text = decode_bytes(content)
                decoded_text = clean_csv_text(decoded_text)
                rows = csv_rows(decoded_text)
            elif type_response == "base64":
                content_str = content.decode("utf-8", errors="ignore").strip()
                if content_str.startswith('"') and content_str.endswith('"'):
                    content_str = content_str[1:-1]
                try:
                    decoded_bytes = base64.b64decode(content_str)
                except Exception as e:
                    self.logger.error(f"Falha ao decodificar conteúdo base64: {e}")
                    sys.exit(1)
                decoded_text = decode_bytes(decoded_bytes)
                decoded_text = clean_csv_text(decoded_text)
                rows = csv_rows(decoded_text)
            elif type_response == "txt":
                rows = [{"linha": ln} for ln in decode_bytes(content).splitlines() if ln.strip()]
            elif type_response == "xls":
                rows = xls_rows(content)
            elif type_response == "zip":
                rows = rows_from_zip(content)
            else:
                self.logger.error(f"Tipo de resposta não suportado: {type_response}")
                sys.exit(1)

        if not rows:
            self.logger.warning("Nenhum registro encontrado após o parsing.")
            return pd.DataFrame()

        if is_portfolio:
            return pd.DataFrame(rows)

        dataset_id = self.resource_name.lower().replace(" ", "_").replace("-", "_")
        enriched, _ = enriquecer(dataset_id, rows)
        return pd.DataFrame(enriched)


def run_resource(resource_name: str, output_file_override: Path = None):
    scraper = GenericScraper(resource_name)
    if output_file_override:
        scraper.output_file = output_file_override
    scraper.run()
