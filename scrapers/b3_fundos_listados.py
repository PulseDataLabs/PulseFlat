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
from utils import get_logger, agora_brt, limpar, b64_encode_params, nova_session
import pandas as pd
from scrapers.utils.base import BaseScraper

log = get_logger("b3_fundos_listados")

BASE_URL  = "https://sistemaswebb3-listados.b3.com.br/fundsListedProxy/Search/GetListFunds/"
PAGE_SIZE = 100

CATEGORIAS = [
    ("FII",      "FII"),
    ("FIAGRO",   "FIAGRO"),
    ("FIDC",     "FIDC"),
    ("FIP",      "FIP"),
    ("ETF",      "ETF Renda Variável"),
    ("ETF-RF",   "ETF Renda Fixa"),
    ("SETORIAL", "Fundo Setorial"),
]

CABECALHO = [
    "data_captura",
    "tipo_fundo",
    "codigo_fundo",
    "nome_fundo",
    "cnpj",
    "administrador",
    "gestor",
    "classificacao",
    "classificacao_anbima",
    "situacao",
    "patrimonio_liquido",
    "data_patrimonio_liquido",
    "data_encerramento",
    "publico_alvo",
    "forma_condominio",
    "id_b3",
]


def _url(funds_type: str, page: int) -> str:
    return BASE_URL + b64_encode_params({
        "language": "pt-br", "pageNumber": page,
        "pageSize": PAGE_SIZE, "typeFund": funds_type,
    })


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
    codigo = limpar(item.get("fundTicker") or item.get("ticker") or item.get("code") or item.get("symbol"))
    if not codigo:
        acronym = limpar(item.get("acronym") or item.get("fundAcronym"))
        if acronym:
            codigo = acronym if any(c.isdigit() for c in acronym) else f"{acronym}11"
    return {
        "data_captura":  data_captura,
        "tipo_fundo":    tipo_label,
        "codigo_fundo":  codigo,
        "nome_fundo":    limpar(item.get("fundName") or item.get("tradingName")),
        "cnpj":          "",
        "administrador": "",
        "gestor":        "",
        "classificacao": "",
        "classificacao_anbima": "",
        "situacao":      "",
        "patrimonio_liquido": "",
        "data_patrimonio_liquido": "",
        "data_encerramento": "",
        "publico_alvo":  "",
        "forma_condominio": "",
        "id_b3":         str(item.get("id", "")),
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

    ticker_to_isin = titulos.set_index("codigo_ativo")["codigo_isin"].dropna().to_dict()
    isin_to_emissor = isin_ativos.set_index("codigo_isin")["codigo_emissor"].dropna().to_dict()
    emissor_to_cnpj = isin_emissores.set_index("codigo_emissor")["cnpj_emissor"].dropna().to_dict()

    cvm["cnpj_clean"] = cvm["cnpj_fundo"].str.replace(r"\D", "", regex=True)
    cvm_dedup = cvm.drop_duplicates(subset="cnpj_clean").set_index("cnpj_clean")

    enriquecidos = 0
    for rec in registros:
        ticker = rec.get("codigo_fundo", "")
        isin = ticker_to_isin.get(ticker)
        if not isin:
            continue
        emissor = isin_to_emissor.get(isin)
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

    log.info(f"Registros enriquecidos via CVM: {enriquecidos}/{len(registros)}")
    return registros


def _capturar_categoria(session, funds_type: str, label: str,
                         data_captura: str) -> list[dict]:
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

    title = 'B3 Fundos Listados'
    description = 'Lista completa de fundos listados na B3: FII, FIAGRO, FIDC, FIP, ETFs (RV e RF) e Fundos Setoriais. Inclui dados cadastrais e patrimônio líquido via CVM.'
    icon = '🏢'
    icon_class = 'icon-b3'
    badge = 'Diário'
    badge_class = 'badge-daily'
    tags = ['ticker', 'fundos', 'fii', 'fiagro', 'fidc', 'fip', 'etf', 'setorial', 'cnpj', 'administrador', 'pl']
    source = 'B3 API + CVM'

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 Fundos Listados ===")
        df = pd.DataFrame(capturar())
        if not df.empty:
            colunas = [c for c in CABECALHO if c in df.columns]
            return df[colunas]
        return df


if __name__ == "__main__":
    B3FundosListadosScraper().run()
