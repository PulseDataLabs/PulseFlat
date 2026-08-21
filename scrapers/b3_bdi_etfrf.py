"""
scrapers/b3_bdi_etfrf.py
------------------------
Negócios diários de ETF de Renda Fixa extraídos do Boletim Diário de Informações (BDI) da B3.

Fonte: https://arquivos.b3.com.br/bdi/
       https://arquivos.b3.com.br/bdi/download/bdi/{YYYY-MM-DD}/BDI_00_{YYYYMMDD}.pdf

O BDI diário traz a seção "Negócios de VM de renda fixa realizados no Puma" com o resumo
diário por ativo (preços, quantidade, negócios e volume) dos ETF de Renda Fixa.

Formato antigo (BDI_00, único PDF): cada campo em uma linha própria, na ordem
  código → preços (abertura, mínimo, máximo, médio, último) → preço referência D1 →
  oferta compra → oferta venda → quantidade → negócios → volume.
Formato novo (BDI_02-1, capítulo "Resumo de ações"): linhas com
  código / ISIN / FORWARD / valores, onde quantidade de negócios, quantidade de
  contratos e volume financeiro são os 3 últimos valores (índices 14, 15 e 16).

Quando o BDI_00 do dia ainda não foi publicado, usa o capítulo BDI_02-1 como fallback.

Códigos normalizados: remove o sufixo "11" para casar com `codigo_fundo` de
data/b3_fundos_listados.csv (ETF Renda Fixa).
"""

import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd

from scrapers.utils.base import BaseScraper
from utils import get_logger, nova_session
from utils.parsers import _CAL

log = get_logger("b3_bdi_etfrf")

ARQUIVO = Path("data/b3_bdi_etfrf.csv.gz")

CABECALHO = [
    "data_referencia",
    "codigo_ativo",
    "preco_abertura",
    "preco_minimo",
    "preco_maximo",
    "preco_medio",
    "preco_fechamento",
    "preco_referencia_d1",
    "oferta_compra",
    "oferta_venda",
    "quantidade",
    "negocios",
    "volume",
    "arquivo_origem",
]

VALUE_RE = re.compile(r"^[\d.,\-]+$")
OLD_SECTION_START = "realizados no Puma"

MIRROR = "https://arquivos.b3.com.br/bdi/download/bdi/{data}/{nome}_{ymd}.pdf"

FORMATOS = [
    ("BDI_00", "old"),
    ("BDI_02-1", "forward"),
]


def _normalizar_valor(v: str) -> str:
    v = v.strip()
    if v in ("", "-"):
        return ""
    if "," in v:
        return v.replace(".", "").replace(",", ".")
    return v.replace(".", "")


def _base(code: str) -> str:
    return code[:-2] if code.endswith("11") else code


def _page_lines(page) -> list[str]:
    d = page.get_text("dict")
    out = []
    for block in d.get("blocks", []):
        if not isinstance(block, dict):
            continue
        for line in block.get("lines", []):
            if not isinstance(line, dict):
                continue
            spans = line.get("spans", [])
            if not isinstance(spans, list):
                continue
            text = "".join(s.get("text", "") for s in spans if isinstance(s, dict))
            if not text.strip():
                continue
            y = line.get("bbox", [0, 0, 0, 0])
            out.append((y[1], text))
    out.sort(key=lambda t: t[0])
    return [txt for _, txt in out]


def _parse_old_format(doc, valid: set[str]) -> list[dict]:
    """Seção 'Negócios de VM de renda fixa realizados no Puma' do BDI_00."""
    rows = []
    for page in doc:
        lines = _page_lines(page)
        start = None
        for i, ln in enumerate(lines):
            if (
                OLD_SECTION_START in ln
                and i + 1 < len(lines)
                and lines[i + 1].strip()
                and not re.fullmatch(r"\d+", lines[i + 1].strip())
            ):
                start = i
                break
        if start is None:
            continue
        j = start + 1
        while j < len(lines) and lines[j].strip() != "Volume":
            j += 1
        cur = None
        for ln in lines[j + 1 :]:
            toks = ln.split()
            if not toks:
                continue
            first = toks[0]
            if first in valid:
                cur = {
                    "code": _base(first),
                    "values": [t for t in toks[1:] if VALUE_RE.match(t)],
                }
                continue
            if cur is not None:
                cur["values"].extend(t for t in toks if VALUE_RE.match(t))
                if len(cur["values"]) >= 11:
                    v = cur["values"][:11]
                    rows.append(
                        {
                            "codigo_ativo": cur["code"],
                            "preco_abertura": v[0],
                            "preco_minimo": v[1],
                            "preco_maximo": v[2],
                            "preco_medio": v[3],
                            "preco_fechamento": v[4],
                            "preco_referencia_d1": v[5],
                            "oferta_compra": v[6],
                            "oferta_venda": v[7],
                            "quantidade": v[8],
                            "negocios": v[9],
                            "volume": v[10],
                        }
                    )
                    cur = None
    return rows


def _parse_forward_format(doc, valid: set[str]) -> list[dict]:
    """Linhas FORWARD do capítulo 'Resumo de ações' (BDI_02-1)."""
    rows = []
    cur = None
    for page in doc:
        for ln in _page_lines(page):
            toks = ln.split()
            if not toks:
                continue
            first = toks[0]
            if first in valid:
                cur = {"code": _base(first), "values": [], "expect": "isin"}
                continue
            if cur is None:
                continue
            if cur["expect"] == "isin":
                cur["expect"] = "seg"
            elif cur["expect"] == "seg":
                if toks[0] == "FORWARD":
                    cur["expect"] = "vals"
                else:
                    cur = None
            elif cur["expect"] == "vals":
                if not VALUE_RE.match(toks[0]):
                    cur = None
                    continue
                cur["values"].extend(t for t in toks if VALUE_RE.match(t))
                if len(cur["values"]) >= 17:
                    v = cur["values"][:17]
                    rows.append(
                        {
                            "codigo_ativo": cur["code"],
                            "preco_abertura": v[0],
                            "preco_minimo": v[1],
                            "preco_maximo": v[2],
                            "preco_medio": v[3],
                            "preco_fechamento": v[4],
                            "negocios": v[14],
                            "quantidade": v[15],
                            "volume": v[16],
                        }
                    )
                    cur = None
    return rows


def _ler_etfrf_base() -> list[str]:
    root = Path(__file__).resolve().parents[1]
    csv_path = root / "data" / "b3_fundos_listados.csv"
    if not csv_path.exists():
        return []
    df = pd.read_csv(csv_path, dtype=str)
    if "tipo_fundo" in df.columns and "codigo_fundo" in df.columns:
        df = df[df["tipo_fundo"].astype(str).str.strip() == "ETF Renda Fixa"]
        codigos = {
            str(c).strip().upper()
            for c in df["codigo_fundo"].dropna()
            if str(c).strip()
        }
        return sorted({_base(c) for c in codigos})
    return []


def _dias_uteis(start: date, end: date) -> list[date]:
    if start > end:
        start, end = end, start
    return list(_CAL.seq(start, end))


def _baixar_e_parsear(session, dt: date, valid: set[str], parser: str) -> list[dict]:
    import fitz

    data = dt.strftime("%Y-%m-%d")
    ymd = dt.strftime("%Y%m%d")
    for nome, modo in FORMATOS:
        if parser != modo and parser != "any":
            continue
        url = MIRROR.format(data=data, nome=nome, ymd=ymd)
        try:
            resp = session.get(url, timeout=180)
            if resp.status_code != 200:
                continue
        except Exception as e:
            log.warning(f"  {nome} {data}: erro no download: {e}")
            continue
        with fitz.open(stream=resp.content, filetype="pdf") as doc:
            if modo == "old":
                rows = _parse_old_format(doc, valid)
                if not rows:
                    rows = _parse_forward_format(doc, valid)
            else:
                rows = _parse_forward_format(doc, valid)
        if rows:
            for r in rows:
                r["data_referencia"] = data
                r["arquivo_origem"] = f"{nome}_{ymd}.pdf"
                for campo in (
                    "preco_abertura",
                    "preco_minimo",
                    "preco_maximo",
                    "preco_medio",
                    "preco_fechamento",
                    "preco_referencia_d1",
                    "oferta_compra",
                    "oferta_venda",
                    "quantidade",
                    "negocios",
                    "volume",
                ):
                    if campo in r:
                        r[campo] = _normalizar_valor(r[campo])
            log.info(f"  {data}: {len(rows)} registros via {nome}")
            return rows
        log.info(f"  {nome} {data}: seção ETF-RF vazia")
    return []


def capturar(
    start_date: date | None,
    end_date: date | None,
    target_date: date | None,
    parser: str = "any",
) -> list[dict]:
    if target_date:
        dias = [target_date]
    elif start_date and end_date:
        dias = _dias_uteis(start_date, end_date)
    elif start_date:
        dias = _dias_uteis(start_date, date.today())
    else:
        dias = [_CAL.offset(date.today(), -1)]

    base = _ler_etfrf_base()
    if not base:
        log.error(
            "Lista de ETF Renda Fixa não encontrada (data/b3_fundos_listados.csv)."
        )
        return []
    valid = {c + "11" for c in base}

    session = nova_session()
    todos = []
    for dt in dias:
        rows = _baixar_e_parsear(session, dt, valid, parser)
        todos.extend(rows)
    return todos


class B3BdiEtfrfScraper(BaseScraper):
    name = "b3_bdi_etfrf"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = True
    compress = True
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    # Catálogo de Metadados
    title = "B3 BDI — ETFs de Renda Fixa"
    description = "Negociação e cotações de fechamento dos ETFs de Renda Fixa na B3."
    icon = "📊"
    icon_class = "icon-b3"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = ["ETF", "renda fixa", "bdi", "volume", "negócios", "preço"]
    source = "B3 BDI"

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 BDI — ETF de Renda Fixa ===")
        rows = capturar(self.start_date, self.end_date, self.target_date)
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            df = df[colunas].sort_values(["data_referencia", "codigo_ativo"])
        return df


if __name__ == "__main__":
    B3BdiEtfrfScraper().run()
