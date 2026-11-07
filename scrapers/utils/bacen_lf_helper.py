"""
scrapers/utils/bacen_lf_helper.py
---------------------------------
Utilitário compartilhado para download e parsing das 12 planilhas XLSX de
Estatísticas sobre Letras Financeiras do Banco Central do Brasil (BACEN/BCB).

Fonte oficial:
  https://www.bcb.gov.br/estatisticas/estats_letras_financeiras
  https://www.bcb.gov.br/content/estatisticas/estatisticas_sfn/estatisticas_letras_financeiras/<arquivo>.xlsx
"""

import re
import unicodedata
from io import BytesIO
from typing import Any

import openpyxl
import pandas as pd
import requests

from scrapers.utils.bacen_lf_cnpjs import resolve_emissor_cnpj14
from utils.base import agora_brt, get_logger, limpar

log = get_logger("bacen_lf_helper")

BASE_URL = (
    "https://www.bcb.gov.br/content/estatisticas/"
    "estatisticas_sfn/estatisticas_letras_financeiras/"
)

HEADERS_BCB = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, "
        "application/octet-stream, */*"
    ),
}

MESES_MAP = {
    "jan": "01",
    "fev": "02",
    "mar": "03",
    "abr": "04",
    "mai": "05",
    "jun": "06",
    "jul": "07",
    "ago": "08",
    "set": "09",
    "out": "10",
    "nov": "11",
    "dez": "12",
}


def _strip_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_header_token(raw_header: Any) -> str:
    """
    Normaliza um cabeçalho de coluna do Excel do BCB removendo notas de rodapé
    ('1/', '2/', '*'), acentos e espaços extras.
    """
    if raw_header is None:
        return ""
    s = str(raw_header).strip()
    # Remove marcadores de nota de rodapé como '1/', '2/', '*'
    s = re.sub(r"\b\d+/", "", s)
    s = s.replace("*", "").strip()
    s_ascii = _strip_accents(s).lower()
    s_ascii = re.sub(r"\s+", " ", s_ascii).strip()
    return s_ascii


def map_segment_column(raw_header: Any) -> str | None:
    """
    Mapeia cabeçalhos das planilhas de segmento (LF e LFS Estoque/Prazo por Segmento)
    para nomes canônicos em formato wide.
    """
    tok = normalize_header_token(raw_header)
    if not tok:
        return None
    if tok in ("mes", "mês"):
        return "mes"
    if "comercia" in tok:
        return "bancos_comerciais"
    if "invest" in tok:
        return "bancos_investimento"
    if "multiplo" in tok:
        return "bancos_multiplos"
    if tok == "scfi" or "financiamento" in tok:
        return "scfi"
    if "desenv" in tok:
        return "bancos_desenvolvimento"
    if "hipotec" in tok:
        return "companhias_hipotecarias"
    if "cooperativa" in tok:
        return "cooperativas_credito"
    if tok in ("total", "totais", "total geral"):
        return "total"
    return None


def download_workbook_bytes(
    excel_filename: str, session: requests.Session | None = None
) -> bytes:
    """Baixa o arquivo XLSX do servidor de conteúdo do BCB."""
    sess = session or requests.Session()
    url = BASE_URL + excel_filename
    log.info(f"Baixando planilha BCB Letras Financeiras: {url}")
    resp = sess.get(url, headers=HEADERS_BCB, timeout=60)
    resp.raise_for_status()
    if not resp.content or len(resp.content) < 500:
        raise RuntimeError(f"Arquivo XLSX vazio ou inválido recebido de {url}")
    return resp.content


def _extract_annual_ref_date(ws, year_str: str) -> str:
    """
    Extrai a data de referência exata informada no subtítulo da aba (ex: 'em 31/12/2025' -> '2025-12-31').
    Se não encontrar, usa '{year_str}-12-31'.
    """
    for r_idx in range(1, min(12, ws.max_row + 1)):
        for c_idx in range(1, min(6, ws.max_column + 1)):
            val = ws.cell(r_idx, c_idx).value
            if val and isinstance(val, str):
                m = re.search(r"(\d{2})/(\d{2})/(\d{4})", val)
                if m:
                    dd, mm, yyyy = m.group(1), m.group(2), m.group(3)
                    return f"{yyyy}-{mm}-{dd}"
    return f"{year_str}-12-31"


def _find_header_row(ws, first_col_keywords: tuple[str, ...]) -> int | None:
    """Localiza o índice (1-based) da linha de cabeçalho na aba."""
    for r_idx in range(1, min(18, ws.max_row + 1)):
        val = ws.cell(r_idx, 1).value
        tok = normalize_header_token(val)
        if tok and any(tok == kw or tok.startswith(kw) for kw in first_col_keywords):
            return r_idx
    return None


def _is_footer_or_total_label(label_raw: Any) -> bool:
    """Identifica se o rótulo da primeira coluna é rodapé, legenda, nota ou linha de soma ('Total'/'Totais')."""
    if label_raw is None:
        return True
    s = str(label_raw).strip()
    if not s:
        return True
    s_low = _strip_accents(s).lower().strip()
    if (
        s_low in ("total", "totais", "total geral", "soma")
        or s_low.startswith("legenda")
        or s_low.startswith("fonte")
        or s_low.startswith("nota")
        or s_low.startswith("*")
        or re.match(r"^\d+/", s_low)
    ):
        return True
    return False


def _format_num(val: Any, scale: float = 1.0, is_int: bool = False, decimals: int | None = None) -> str:
    """Formata um valor numérico escalado para string padrão ISO (ponto decimal) ou vazio."""
    if val is None or val == "":
        return ""
    if isinstance(val, str):
        v_str = val.strip()
        if not v_str or v_str in ("-", "--", "N/D", "ND"):
            return ""
        try:
            num = float(v_str.replace(".", "").replace(",", ".")) if "," in v_str else float(v_str)
        except ValueError:
            return ""
    elif isinstance(val, (int, float)):
        if pd.isna(val):
            return ""
        num = float(val)
    else:
        return ""

    num = num * scale
    if is_int:
        return str(int(round(num)))
    if decimals is not None:
        rounded_dec = round(num, decimals)
        if rounded_dec == int(rounded_dec):
            return f"{int(rounded_dec)}.0"
        return str(rounded_dec)
    # Mantém precisão limpa evitando artefatos de ponto flutuante (ex: 76139000.0001 -> round 4)
    rounded = round(num, 4)
    if rounded == int(rounded):
        return f"{int(rounded)}.0" if not is_int else str(int(rounded))
    return str(rounded)


def parse_monthly_lf_lfs(
    content: bytes,
    col_lf: str,
    col_lfs: str,
) -> list[dict[str, str]]:
    """
    Faz o parse de planilhas mensais com colunas (Mês, LF, LFS):
      - Emissoes.xlsx
      - Estoque.xlsx
      - PrazoEmissoes.xlsx
      - PrazoVencimento.xlsx
    """
    wb = openpyxl.load_workbook(BytesIO(content), data_only=True)
    data_captura, _ = agora_brt()
    registros: list[dict[str, str]] = []

    for sheet_name in wb.sheetnames:
        year_str = sheet_name.strip()
        if not re.match(r"^\d{4}$", year_str):
            continue
        ws = wb[sheet_name]
        header_row = _find_header_row(ws, ("mes",))
        if not header_row:
            continue

        # Mapeia índices de LF e LFS
        lf_col_idx = None
        lfs_col_idx = None
        for c_idx in range(2, ws.max_column + 1):
            tok = normalize_header_token(ws.cell(header_row, c_idx).value)
            if tok == "lf" and lf_col_idx is None:
                lf_col_idx = c_idx
            elif tok == "lfs" and lfs_col_idx is None:
                lfs_col_idx = c_idx

        if not lf_col_idx and not lfs_col_idx:
            continue

        for r_idx in range(header_row + 1, ws.max_row + 1):
            mes_raw = ws.cell(r_idx, 1).value
            tok_mes = normalize_header_token(mes_raw)[:3]
            if tok_mes not in MESES_MAP:
                continue

            mm = MESES_MAP[tok_mes]
            data_ref = f"{year_str}-{mm}-01"
            val_lf = _format_num(ws.cell(r_idx, lf_col_idx).value) if lf_col_idx else ""
            val_lfs = _format_num(ws.cell(r_idx, lfs_col_idx).value) if lfs_col_idx else ""

            if val_lf == "" and val_lfs == "":
                continue

            registros.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": data_ref,
                    col_lf: val_lf,
                    col_lfs: val_lfs,
                }
            )

    return registros


def parse_monthly_segments(
    content: bytes,
    expected_segment_cols: list[str],
) -> list[dict[str, str]]:
    """
    Faz o parse das 4 planilhas mensais por segmento do emissor em formato wide:
      - LFEstoqueSegmento.xlsx
      - LFPrazoVencimento.xlsx
      - LFSEstoqueSegmento.xlsx
      - LFSPrazoVencimento.xlsx
    """
    wb = openpyxl.load_workbook(BytesIO(content), data_only=True)
    data_captura, _ = agora_brt()
    registros: list[dict[str, str]] = []

    for sheet_name in wb.sheetnames:
        year_str = sheet_name.strip()
        if not re.match(r"^\d{4}$", year_str):
            continue
        ws = wb[sheet_name]
        header_row = _find_header_row(ws, ("mes",))
        if not header_row:
            continue

        col_map: dict[str, int] = {}
        for c_idx in range(2, ws.max_column + 1):
            mapped = map_segment_column(ws.cell(header_row, c_idx).value)
            if mapped and mapped != "mes" and mapped not in col_map:
                col_map[mapped] = c_idx

        if not col_map:
            continue

        for r_idx in range(header_row + 1, ws.max_row + 1):
            mes_raw = ws.cell(r_idx, 1).value
            tok_mes = normalize_header_token(mes_raw)[:3]
            if tok_mes not in MESES_MAP:
                continue

            mm = MESES_MAP[tok_mes]
            data_ref = f"{year_str}-{mm}-01"

            row_dict: dict[str, str] = {
                "data_captura": data_captura,
                "data_referencia": data_ref,
            }
            has_any_val = False
            for seg_col in expected_segment_cols:
                c_idx = col_map.get(seg_col)
                val_str = _format_num(ws.cell(r_idx, c_idx).value) if c_idx else ""
                if val_str != "":
                    has_any_val = True
                row_dict[seg_col] = val_str

            if has_any_val:
                registros.append(row_dict)

    return registros


def parse_monthly_secondary_market(content: bytes) -> list[dict[str, str]]:
    """
    Faz o parse da planilha MercadoSecundario.xlsx (Mês, Nº Negócios, Valor).
    """
    wb = openpyxl.load_workbook(BytesIO(content), data_only=True)
    data_captura, _ = agora_brt()
    registros: list[dict[str, str]] = []

    for sheet_name in wb.sheetnames:
        year_str = sheet_name.strip()
        if not re.match(r"^\d{4}$", year_str):
            continue
        ws = wb[sheet_name]
        header_row = _find_header_row(ws, ("mes",))
        if not header_row:
            continue

        neg_col_idx = 2
        val_col_idx = 3
        for c_idx in range(2, ws.max_column + 1):
            tok = normalize_header_token(ws.cell(header_row, c_idx).value)
            if "negocio" in tok:
                neg_col_idx = c_idx
            elif "valor" in tok:
                val_col_idx = c_idx

        for r_idx in range(header_row + 1, ws.max_row + 1):
            mes_raw = ws.cell(r_idx, 1).value
            tok_mes = normalize_header_token(mes_raw)[:3]
            if tok_mes not in MESES_MAP:
                continue

            mm = MESES_MAP[tok_mes]
            data_ref = f"{year_str}-{mm}-01"
            num_neg = _format_num(ws.cell(r_idx, neg_col_idx).value, is_int=True)
            valor = _format_num(ws.cell(r_idx, val_col_idx).value)

            if num_neg == "" and valor == "":
                continue

            registros.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": data_ref,
                    "numero_negocios": num_neg,
                    "valor": valor,
                }
            )

    return registros


def parse_annual_holder_nature(content: bytes) -> list[dict[str, str]]:
    """
    Faz o parse de EstoqueNaturezaDetentor.xlsx:
    (Natureza do Detentor, LF, LFS, Totais, %)
    Remove linhas de 'Total'/'Totais' e converte '%' para escala 0–100.
    """
    wb = openpyxl.load_workbook(BytesIO(content), data_only=True)
    data_captura, _ = agora_brt()
    registros: list[dict[str, str]] = []

    for sheet_name in wb.sheetnames:
        year_str = sheet_name.strip()
        if not re.match(r"^\d{4}$", year_str):
            continue
        ws = wb[sheet_name]
        header_row = _find_header_row(ws, ("natureza",))
        if not header_row:
            continue

        data_ref = _extract_annual_ref_date(ws, year_str)

        for r_idx in range(header_row + 1, ws.max_row + 1):
            raw_label = ws.cell(r_idx, 1).value
            if _is_footer_or_total_label(raw_label):
                continue

            # Remove marcadores de nota de rodapé do nome da natureza (ex: '1/')
            natureza = re.sub(r"\s*\b\d+/\s*$", "", limpar(raw_label)).strip()
            val_lf = _format_num(ws.cell(r_idx, 2).value)
            val_lfs = _format_num(ws.cell(r_idx, 3).value)
            val_tot = _format_num(ws.cell(r_idx, 4).value)
            val_pct = _format_num(ws.cell(r_idx, 5).value, scale=100.0, decimals=4)

            if val_lf == "" and val_lfs == "" and val_tot == "":
                continue

            registros.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": data_ref,
                    "natureza_detentor": natureza,
                    "estoque_lf": val_lf,
                    "estoque_lfs": val_lfs,
                    "estoque_total": val_tot,
                    "participacao_perc": val_pct,
                }
            )

    return registros


def parse_annual_issuer(content: bytes) -> list[dict[str, str]]:
    """
    Faz o parse de EstoquePorEmissor.xlsx:
    Trata o deslocamento de coluna mesclada (None na coluna B entre 2010 e 2018)
    e remove linhas de 'Totais' e legendas.
    """
    wb = openpyxl.load_workbook(BytesIO(content), data_only=True)
    data_captura, _ = agora_brt()
    registros: list[dict[str, str]] = []

    for sheet_name in wb.sheetnames:
        year_str = sheet_name.strip()
        if not re.match(r"^\d{4}$", year_str):
            continue
        ws = wb[sheet_name]
        header_row = _find_header_row(ws, ("if/conglomerado", "if", "instituicao"))
        if not header_row:
            continue

        data_ref = _extract_annual_ref_date(ws, year_str)

        lf_col = None
        lfs_col = None
        tot_col = None
        for c_idx in range(2, ws.max_column + 1):
            tok = normalize_header_token(ws.cell(header_row, c_idx).value)
            if tok == "lf" and lf_col is None:
                lf_col = c_idx
            elif tok == "lfs" and lfs_col is None:
                lfs_col = c_idx
            elif tok in ("totais", "total") and tot_col is None:
                tot_col = c_idx

        if not lf_col:
            continue

        for r_idx in range(header_row + 1, ws.max_row + 1):
            raw_label = ws.cell(r_idx, 1).value
            if _is_footer_or_total_label(raw_label):
                continue

            instituicao = " ".join(limpar(raw_label).split())
            val_lf = _format_num(ws.cell(r_idx, lf_col).value) if lf_col else ""
            val_lfs = _format_num(ws.cell(r_idx, lfs_col).value) if lfs_col else ""
            val_tot = _format_num(ws.cell(r_idx, tot_col).value) if tot_col else ""

            if val_lf == "" and val_lfs == "" and val_tot == "":
                continue

            registros.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": data_ref,
                    "cnpj": resolve_emissor_cnpj14(instituicao),
                    "instituicao_conglomerado": instituicao,
                    "estoque_lf": val_lf,
                    "estoque_lfs": val_lfs,
                    "estoque_total": val_tot,
                }
            )

    return registros


def parse_annual_indexer(content: bytes) -> list[dict[str, str]]:
    """
    Faz o parse de EstoquePorIndexador.xlsx:
    (Indexador, Valor (R$ Mi), %)
    Normaliza a escala das abas 2010–2012 (gravadas em R$ milhões sem máscara ',,')
    multiplicando por 1_000_000 para manter toda a série em Reais (R$).
    Converte '%' para escala 0–100 e remove linhas de 'Totais' / soma sem rótulo.
    """
    wb = openpyxl.load_workbook(BytesIO(content), data_only=True)
    data_captura, _ = agora_brt()
    registros: list[dict[str, str]] = []

    for sheet_name in wb.sheetnames:
        year_str = sheet_name.strip()
        if not re.match(r"^\d{4}$", year_str):
            continue
        ws = wb[sheet_name]
        header_row = _find_header_row(ws, ("indexador",))
        if not header_row:
            continue

        data_ref = _extract_annual_ref_date(ws, year_str)

        # Detecta se os valores da aba estão em R$ milhões (sem ',,' no number_format e magnitude < 1e8)
        sample_cell = ws.cell(header_row + 1, 2)
        num_fmt = str(sample_cell.number_format or "")
        sample_val = sample_cell.value
        scale_val = 1.0
        if (
            isinstance(sample_val, (int, float))
            and 0 < float(sample_val) < 1e8
            and ",," not in num_fmt
        ):
            scale_val = 1_000_000.0

        for r_idx in range(header_row + 1, ws.max_row + 1):
            raw_label = ws.cell(r_idx, 1).value
            if _is_footer_or_total_label(raw_label):
                continue

            indexador = " ".join(limpar(raw_label).split())
            valor = _format_num(ws.cell(r_idx, 2).value, scale=scale_val)
            pct = _format_num(ws.cell(r_idx, 3).value, scale=100.0, decimals=4)

            if valor == "" and pct == "":
                continue

            registros.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": data_ref,
                    "indexador": indexador,
                    "valor": valor,
                    "participacao_perc": pct,
                }
            )

    return registros
