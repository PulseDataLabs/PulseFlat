"""
scrapers/b3_fundos_listados.py
-------------------------------
Captura a lista completa de fundos listados na B3 via API interna (GetListFunds)
e enriquece com dados cadastrais via cadeia ISIN → CNPJ → CVM.

Cobre todos os tipos de fundo disponíveis no endpoint:
  FII, FIAGRO, FIDC, FIP, ETF, ETF-RF, Fundo Setorial

Endpoint: GET https://sistemaswebb3-listados.b3.com.br/fundsListedProxy/Search/
                GetListFunds/<base64>

Enriquecimento:
  ticker → b3_titulos_negociaveis → ISIN → b3_isin_ativos → emissor
  → b3_isin_emissores → CNPJ → registro_fundo_classe → dados completos
"""

import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd

from scrapers.utils.base import BaseScraper
from utils import agora_brt, b64_encode_params, get_logger, limpar, nova_session

log = get_logger("b3_fundos_listados")

BASE_URL = (
    "https://sistemaswebb3-listados.b3.com.br/fundsListedProxy/Search/GetListFunds/"
)
PAGE_SIZE = 100

CATEGORIAS = [
    ("FII", "FII"),
    ("FIAGRO", "FIAGRO"),
    ("FIDC", "FIDC"),
    ("FIP", "FIP"),
    ("ETF", "ETF Renda Variável"),
    ("ETF-RF", "ETF Renda Fixa"),
    ("SETORIAL", "Fundo Setorial"),
]

CABECALHO = [
    "data_captura",
    "tipo_fundo",
    "codigo_fundo",
    "nome_fundo",
    "cnpj",
    "cnpj_classe",
    "administrador",
    "gestor",
    "classificacao",
    "classificacao_anbima",
    "situacao",
    "patrimonio_liquido",
    "data_patrimonio_liquido",
    "data_encerramento",
    "data_inicio",
    "publico_alvo",
    "forma_condominio",
    "codigo_cvm",
    "custodiante",
    "auditor",
    "isin_codigo_cfi",
    "isin_situacao",
    "isin_data_expiracao",
    "isin_data_emissao",
    "isin_exchange",
    "isin_moeda",
    "isin_codigo_categoria",
    "isin_codigo_especie",
    "id_b3",
]


def _url(funds_type: str, page: int) -> str:
    return BASE_URL + b64_encode_params(
        {
            "language": "pt-br",
            "pageNumber": page,
            "pageSize": PAGE_SIZE,
            "typeFund": funds_type,
        }
    )


def _pagina(session, funds_type: str, page: int) -> tuple[list, int, int | None]:
    try:
        resp = session.get(_url(funds_type, page), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        resultados = data.get("results") or data.get("result") or data.get("data") or []
        page_info = data.get("page") or {}
        total = (
            data.get("total")
            or page_info.get("totalRecords")
            or page_info.get("totalResults")
            or page_info.get("total")
            or len(resultados)
        )
        total_pages = page_info.get("totalPages")
        return resultados, int(total or 0), int(total_pages) if total_pages else None
    except Exception as e:
        log.error(f"[{funds_type}] Página {page}: {e}")
        return [], 0, None


def _mapear(item: dict, data_captura: str, tipo_label: str) -> dict:
    codigo = limpar(
        item.get("fundTicker")
        or item.get("ticker")
        or item.get("code")
        or item.get("symbol")
    )
    if not codigo:
        acronym = limpar(item.get("acronym") or item.get("fundAcronym"))
        if acronym:
            codigo = acronym if any(c.isdigit() for c in acronym) else f"{acronym}11"
    return {
        "data_captura": data_captura,
        "tipo_fundo": tipo_label,
        "codigo_fundo": codigo,
        "nome_fundo": limpar(item.get("fundName") or item.get("tradingName")),
        "cnpj": "",
        "cnpj_classe": "",
        "administrador": "",
        "gestor": "",
        "classificacao": "",
        "classificacao_anbima": "",
        "situacao": "",
        "patrimonio_liquido": "",
        "data_patrimonio_liquido": "",
        "data_encerramento": "",
        "data_inicio": "",
        "publico_alvo": "",
        "forma_condominio": "",
        "codigo_cvm": "",
        "custodiante": "",
        "auditor": "",
        "isin_codigo_cfi": "",
        "isin_situacao": "",
        "isin_data_expiracao": "",
        "isin_data_emissao": "",
        "isin_exchange": "",
        "isin_moeda": "",
        "isin_codigo_categoria": "",
        "isin_codigo_especie": "",
        "id_b3": str(item.get("id", "")),
    }


def _enriquecer(registros: list[dict]) -> list[dict]:
    root_dir = Path(__file__).resolve().parents[1]

    titulos_path = root_dir / "data" / "b3_titulos_negociaveis.csv"
    isin_path = root_dir / "data" / "b3_isin_ativos.csv"
    emissores_path = root_dir / "data" / "b3_isin_emissores.csv"
    cvm_path = root_dir / "data" / "registro_fundo_classe.csv"

    if not all(p.exists() for p in [titulos_path, isin_path, emissores_path, cvm_path]):
        log.warning("Arquivos de enriquecimento ausentes — retornando dados básicos.")
        return registros

    try:
        titulos = pd.read_csv(titulos_path, dtype=str, keep_default_na=False)
        isin_ativos = pd.read_csv(isin_path, dtype=str, keep_default_na=False)
        isin_emissores = pd.read_csv(emissores_path, dtype=str, keep_default_na=False)
        cvm = pd.read_csv(cvm_path, dtype=str, keep_default_na=False)
    except Exception as e:
        log.warning(f"Erro ao ler CSVs de enriquecimento: {e}")
        return registros

    # ── Fase 0: cadeia ticker → ISIN → emissor → CNPJ → CVM ──────────────
    ticker_to_isin = titulos.set_index("codigo_ativo")["codigo_isin"].dropna().to_dict()
    isin_to_emissor = (
        isin_ativos.set_index("codigo_isin")["codigo_emissor"].dropna().to_dict()
    )
    emissor_to_cnpj = (
        isin_emissores.set_index("codigo_emissor")["cnpj_emissor"].dropna().to_dict()
    )

    cvm["cnpj_clean"] = cvm["cnpj_fundo"].str.replace(r"\D", "", regex=True)
    cvm_dedup = cvm.drop_duplicates(subset="cnpj_clean").set_index("cnpj_clean")

    enriquecidos = 0
    for rec in registros:
        ticker = rec.get("codigo_fundo", "")
        cod_isin = ticker_to_isin.get(ticker)
        if not cod_isin:
            continue
        emissor = isin_to_emissor.get(cod_isin)
        if not emissor:
            continue
        cnpj = emissor_to_cnpj.get(emissor)
        if not cnpj:
            continue

        cnpj_clean = re.sub(r"\D", "", cnpj)
        if cnpj_clean not in cvm_dedup.index:
            continue

        row = cvm_dedup.loc[cnpj_clean]
        rec["cnpj"] = cnpj
        rec["administrador"] = str(row.get("administrador", ""))
        rec["gestor"] = str(row.get("gestor", ""))
        rec["classificacao"] = str(row.get("classificacao", ""))
        rec["classificacao_anbima"] = str(row.get("classificacao_anbima", ""))
        rec["situacao"] = str(row.get("situacao", ""))
        rec["patrimonio_liquido"] = str(row.get("patrimonio_liquido", ""))
        rec["data_patrimonio_liquido"] = str(row.get("data_patrimonio_liquido", ""))
        rec["data_encerramento"] = str(row.get("data_cancelamento", ""))
        rec["publico_alvo"] = str(row.get("publico_alvo", ""))
        rec["forma_condominio"] = str(row.get("forma_condominio", ""))
        enriquecidos += 1

    # ── Fase 1: dados complementares do ISIN (para todo fundo com ISIN) ─
    isin_idx = isin_ativos.drop_duplicates(subset="codigo_isin").set_index(
        "codigo_isin"
    )

    campos_isin = [
        ("codigo_cfi", "isin_codigo_cfi"),
        ("situacao_isin", "isin_situacao"),
        ("data_expiracao", "isin_data_expiracao"),
        ("data_emissao", "isin_data_emissao"),
        ("exchange", "isin_exchange"),
        ("moeda", "isin_moeda"),
        ("codigo_categoria", "isin_codigo_categoria"),
        ("codigo_especie", "isin_codigo_especie"),
    ]

    for rec in registros:
        cod_isin = ticker_to_isin.get(rec.get("codigo_fundo", ""))
        if not cod_isin or cod_isin not in isin_idx.index:
            continue
        row = isin_idx.loc[cod_isin]
        for src_col, dst_col in campos_isin:
            rec[dst_col] = str(row.get(src_col, ""))

    # ── Fase 2: match por nome na CVM (ETF Renda Fixa) ─────────────────
    cvm_nome = cvm.drop_duplicates(subset="denominacao_social").set_index(
        "denominacao_social"
    )

    enriquecidos_nome = 0
    for rec in registros:
        if rec.get("cnpj"):
            continue
        if rec.get("tipo_fundo") != "ETF Renda Fixa":
            continue
        nome = str(rec.get("nome_fundo", "")).strip()
        if not nome or nome not in cvm_nome.index:
            continue

        row = cvm_nome.loc[nome]
        rec["situacao"] = str(row.get("situacao", ""))
        rec["patrimonio_liquido"] = str(row.get("patrimonio_liquido", ""))
        rec["data_patrimonio_liquido"] = str(row.get("data_patrimonio_liquido", ""))
        rec["forma_condominio"] = str(row.get("forma_condominio", ""))
        rec["codigo_cvm"] = str(row.get("codigo_cvm", ""))
        rec["custodiante"] = str(row.get("custodiante", ""))
        rec["auditor"] = str(row.get("auditor", ""))
        rec["cnpj_classe"] = str(row.get("cnpj_classe", ""))
        rec["data_inicio"] = str(row.get("data_inicio", ""))
        enriquecidos_nome += 1

    log.info(
        f"Enriquecimento: {enriquecidos} via cadeia CVM + "
        f"{enriquecidos_nome} via nome CVM + "
        f"{len(registros) - enriquecidos - enriquecidos_nome} básicos"
    )
    return registros


def _capturar_categoria(
    session, funds_type: str, label: str, data_captura: str
) -> list[dict]:
    log.info(f"[{label}] Buscando página 1...")
    primeira, total, total_pages = _pagina(session, funds_type, 1)
    if not primeira:
        log.warning(f"[{label}] Sem dados.")
        return []

    n_pag = total_pages or (total + PAGE_SIZE - 1) // PAGE_SIZE
    log.info(f"[{label}] {total} fundos | {n_pag} páginas")

    todos = list(primeira)
    for p in range(2, n_pag + 1):
        log.info(f"[{label}] Página {p}/{n_pag}...")
        resultados, *_ = _pagina(session, funds_type, p)
        todos.extend(resultados)
        time.sleep(0.3)

    return [_mapear(i, data_captura, label) for i in todos]


def capturar() -> list[dict]:
    data_captura, _ = agora_brt()
    session = nova_session()
    todos = []
    for funds_type, label in CATEGORIAS:
        todos.extend(_capturar_categoria(session, funds_type, label, data_captura))
        time.sleep(0.5)
    log.info(f"{len(todos)} fundos capturados ao total.")

    registros = _enriquecer(todos)
    return registros


class B3FundosListadosScraper(BaseScraper):
    name = "b3_fundos_listados"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = False
    chaves_dedup = None

    title = "B3 Fundos Listados"
    description = "Lista completa de fundos listados na B3: FII, FIAGRO, FIDC, FIP, ETFs (RV e RF) e Fundos Setoriais. Inclui dados cadastrais e patrimônio líquido via CVM."
    icon = "🏢"
    icon_class = "icon-b3"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = [
        "ticker",
        "fundos",
        "fii",
        "fiagro",
        "fidc",
        "fip",
        "etf",
        "setorial",
        "cnpj",
        "administrador",
        "pl",
    ]
    source = "B3 API + CVM"

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 Fundos Listados ===")
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3FundosListadosScraper().run()
