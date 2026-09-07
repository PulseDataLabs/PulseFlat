"""
scrapers/anbima_ima_completo.py
-------------------------------
Índices de mercado ANBIMA (IMA, IDA, IDKA) — dados mark-to-market diários.

Fonte: https://www.anbima.com.br/informacoes/ima/arqs/ima_completo.txt
Campos: DATA_REFERENCIA, INDICE, NUMERO_INDICE, VARIACAO_DIARIA,
        VARIACAO_MENSAL, VARIACAO_ANUAL, VARIACAO_ULTIMOS_12_MESES,
        VARIACAO_ULTIMOS_24_MESES, DURATION_DU, PESO_GERAL,
        CARTEIRA_A_MERCADO_RS_MIL, NUMERO_OPERACOES,
        QUANT_NEGOCIADA_1000_TITULOS, VALOR_NEGOCIADO_RS_MIL,
        PMR, CONVEXIDADE, YIELD, REDEMPTION_YIELD
"""

import sys
import time
from datetime import datetime
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd

from scrapers.utils.base import BaseScraper
from utils import agora_brt, get_logger, limpar, nova_session
from utils.parsers import _CAL

log = get_logger("anbima_ima_completo")

ARQUIVO = Path("data/anbima_ima_completo.csv")
URL = "https://www.anbima.com.br/informacoes/ima/arqs/ima_completo.txt"

CABECALHO = [
    "data_captura",
    "data_referencia",
    "indice",
    "numero_indice",
    "variacao_diaria",
    "variacao_mensal",
    "variacao_anual",
    "variacao_ultimos_12_meses",
    "variacao_ultimos_24_meses",
    "duration_du",
    "peso_geral",
    "carteira_a_mercado_rs_mil",
    "numero_operacoes",
    "quant_negociada_1000_titulos",
    "valor_negociado_rs_mil",
    "pmr",
    "convexidade",
    "yield_",
    "redemption_yield",
]

COLUNAS_ARQUIVO = [
    "data_referencia",
    "indice",
    "numero_indice",
    "variacao_diaria",
    "variacao_mensal",
    "variacao_anual",
    "variacao_ultimos_12_meses",
    "variacao_ultimos_24_meses",
    "duration_du",
    "peso_geral",
    "carteira_a_mercado_rs_mil",
    "numero_operacoes",
    "quant_negociada_1000_titulos",
    "valor_negociado_rs_mil",
    "pmr",
    "convexidade",
    "yield_",
    "redemption_yield",
]


def obter_d1_util() -> str:
    """Retorna a data do dia útil anterior (D-1) no formato DD/MM/YYYY."""
    data_hoje_str, _ = agora_brt()
    hoje = datetime.strptime(data_hoje_str, "%Y-%m-%d").date()
    ref = _CAL.offset(hoje, -1)
    return ref.strftime("%d/%m/%Y")


def _formatar_data_iso(data_str: str) -> str:
    parts = data_str.split("/")
    if len(parts) == 3:
        return f"{parts[2]}-{parts[1]}-{parts[0]}"
    return data_str


def capturar() -> list[dict]:
    log.info(f"Buscando IMA ANBIMA: {URL}")
    session = nova_session()

    for tentativa in range(1, 4):
        try:
            resp = session.get(URL, timeout=30)
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                raise RuntimeError("Falha ao baixar IMA ANBIMA.") from e
            time.sleep(5)

    for enc in ("latin-1", "utf-8", "cp1252"):
        try:
            texto = resp.content.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        texto = resp.content.decode("utf-8", errors="replace")

    linhas = texto.splitlines()
    # Remove comentários (##) e pega até linha em branco
    dados_linhas = []
    for linha in linhas:
        if linha.startswith("##"):
            continue
        if not linha.strip():
            break
        dados_linhas.append(linha)

    # As 3 primeiras linhas são cabeçalho do arquivo
    dados_linhas = dados_linhas[3:]

    # Validar que a data de referência no arquivo corresponde ao D-1 útil esperado
    d1_util_str = obter_d1_util()
    log.info(f"D-1 útil esperado: {d1_util_str}")

    primeira_linha_valida = next((l for l in dados_linhas if "@" in l), None)
    if primeira_linha_valida:
        p = primeira_linha_valida.split("@")
        if len(p) > 1:
            file_date = p[1].strip()
            if file_date != d1_util_str:
                raise ValueError(
                    f"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str})."
                )

    data_captura, _ = agora_brt()
    registros = []

    for linha in dados_linhas:
        if "@" not in linha:
            continue
        partes = linha.split("@")
        if len(partes) < len(COLUNAS_ARQUIVO) + 1:
            partes += [""] * (len(COLUNAS_ARQUIVO) + 1 - len(partes))

        registro = {"data_captura": data_captura}
        # Zipa pulando o primeiro elemento (partes[0]), que é o tipo de registro
        for col, val in zip(COLUNAS_ARQUIVO, partes[1:]):
            val_clean = limpar(val.replace(",", ".")).replace("--", "")
            if col == "data_referencia":
                val_clean = _formatar_data_iso(val_clean)
            registro[col] = val_clean
        registros.append(registro)

    if not registros:
        log.error("Nenhum dado IMA extraído.")
        sys.exit(1)

    log.info(f"{len(registros)} índices IMA capturados.")
    return registros


class AnbimaImaCompletoScraper(BaseScraper):
    name = "anbima_ima_completo"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    chaves_dedup = ["data_referencia", "indice"]

    # Catálogo de Metadados
    title = "ANBIMA — Família IMA / IDA Completo"
    description = "Série histórica e diária da família completa de Índices de Mercado ANBIMA (IMA-Geral, IMA-B, IMA-B 5, IMA-B 5+, IMA-C, IRF-M e IRF-M 1/1+), incluindo número índice, variação diária, rentabilidade mensal/anual, duration e yield médio."
    icon = "📊"
    icon_class = "icon-anbima"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = ["ima-geral", "irf-m", "ida", "idka", "duration"]
    source = "ANBIMA"

    def fetch(self) -> pd.DataFrame:
        log.info("=== ANBIMA IMA Completo ===")
        # Se datas específicas foram solicitadas (ex: via backfill ou target_date)
        target_dates = getattr(self, "missing_dates", None)
        if not target_dates and self.target_date:
            target_dates = [self.target_date]

        if target_dates:
            log.info(f"Modo histórico/backfill ativo para {len(target_dates)} data(s).")
            registros = capturar_historico(target_dates)
            if registros:
                df = pd.DataFrame(registros)
                colunas = [c for c in CABECALHO if c in df.columns]
                return df[colunas]

        # Modo diário padrão via ima_completo.txt
        try:
            dados = capturar()
            df = pd.DataFrame(dados)
            if not df.empty:
                colunas = [c for c in CABECALHO if c in df.columns]
                return df[colunas]
        except Exception as e:
            log.warning(f"Falha no endpoint txt diário ({e}). Tentando fallback S3 histórico ANBIMA...")
            try:
                ref_d1 = _formatar_data_iso(obter_d1_util())
                registros = capturar_historico([ref_d1])
                if registros:
                    df = pd.DataFrame(registros)
                    colunas = [c for c in CABECALHO if c in df.columns]
                    return df[colunas]
            except Exception as e_s3:
                log.error(f"Fallback S3 também falhou: {e_s3}")
            raise

        return pd.DataFrame()


HISTORICAL_S3_BASE = "https://s3-data-prd-use1-precos.s3.us-east-1.amazonaws.com/arquivos/indices-historico/"
HISTORICAL_S3_FILES = {
    "IRFM1-HISTORICO.xls": "IRF-M 1",
    "IRFM1MAIS-HISTORICO.xls": "IRF-M 1+",
    "IRFM-HISTORICO.xls": "IRF-M",
    "IMAB5-HISTORICO.xls": "IMA-B 5",
    "IMAB5MAIS-HISTORICO.xls": "IMA-B 5+",
    "IMAB-HISTORICO.xls": "IMA-B",
    "IMAS-HISTORICO.xls": "IMA-S",
    "IMAGERALEXC-HISTORICO.xls": "IMA-GERAL-EX-C",
    "IMAGERAL-HISTORICO.xls": "IMA-GERAL",
}


def capturar_historico(datas: set[str] | list[str] | None = None) -> list[dict]:
    """Baixa séries históricas dos 9 índices ANBIMA a partir do repositório oficial S3."""
    import io
    import openpyxl

    alvo_datas = {d if isinstance(d, str) else d.strftime("%Y-%m-%d") for d in datas} if datas else None
    log.info(f"Buscando histórico ANBIMA S3 (datas: {sorted(alvo_datas) if alvo_datas else 'todas'})...")
    session = nova_session()
    registros = []

    for fname, idx_name in HISTORICAL_S3_FILES.items():
        url = f"{HISTORICAL_S3_BASE}{fname}"
        resp = None
        for tentativa in range(1, 4):
            try:
                resp = session.get(url, timeout=30)
                resp.raise_for_status()
                break
            except requests.RequestException as e:
                log.warning(f"Tentativa {tentativa}/3 para {fname}: {e}")
                if tentativa == 3:
                    log.error(f"Falha ao baixar {fname} do S3")
                time.sleep(2)

        if not resp or resp.status_code != 200:
            continue

        try:
            wb = openpyxl.load_workbook(io.BytesIO(resp.content), data_only=True)
            ws = wb.active
            for row in list(ws.iter_rows(values_only=True))[1:]:
                dt_val = row[1]
                if not dt_val:
                    continue
                dt_str = dt_val.strftime("%Y-%m-%d") if hasattr(dt_val, "strftime") else str(dt_val)[:10]
                if alvo_datas and dt_str not in alvo_datas:
                    continue

                registros.append({
                    "data_captura": dt_str,
                    "data_referencia": dt_str,
                    "indice": idx_name,
                    "numero_indice": float(row[2]) if row[2] is not None else None,
                    "variacao_diaria": float(row[3]) if row[3] is not None else None,
                    "variacao_mensal": float(row[4]) if row[4] is not None else None,
                    "variacao_anual": float(row[5]) if row[5] is not None else None,
                    "variacao_ultimos_12_meses": float(row[6]) if row[6] is not None else None,
                    "variacao_ultimos_24_meses": float(row[7]) if row[7] is not None else None,
                    "duration_du": row[8],
                    "peso_geral": 100.0 if idx_name == "IMA-GERAL" else None,
                    "carteira_a_mercado_rs_mil": None,
                    "numero_operacoes": None,
                    "quant_negociada_1000_titulos": None,
                    "valor_negociado_rs_mil": None,
                    "pmr": float(row[9]) if row[9] is not None else None,
                    "convexidade": None,
                    "yield_": None,
                    "redemption_yield": None,
                })
        except Exception as e:
            log.error(f"Erro ao processar planilha {fname}: {e}")

    log.info(f"{len(registros)} registros extraídos do S3 histórico ANBIMA.")
    return registros


if __name__ == "__main__":
    AnbimaImaCompletoScraper().run()
