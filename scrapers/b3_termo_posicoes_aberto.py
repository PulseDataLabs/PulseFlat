"""
scrapers/b3_termo_posicoes_aberto.py
--------------------------------------
Posições em Aberto e Totais Consolidados do Mercado a Termo negociado na B3.
Captura diariamente todos os contratos em aberto por ativo (ações, BDRs, units)
e consolida os volumes globais de contratos, ativos e volume financeiro em Reais.

Fonte:
- B3 Market Data / Mercado a Vista / Termo / Posições em Aberto
- Endpoint: GET https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-a-vista/termo/posicoes-em-aberto/posicoes-em-aberto-8AE490C99D724062019D7901CD91500D.htm?data={DD/MM/YYYY}&f=0
Saída:
- data/b3_termo_posicoes_aberto.csv (Posições detalhadas por código/empresa)
- data/b3_termo_posicoes_resumo.csv (Resumo consolidado diário do mercado a termo)
"""

import re
import sys
import time
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.base import BaseScraper
from utils import agora_brt, get_logger, limpar, salvar_csv
from utils.parsers import _CAL

log = get_logger("b3_termo_posicoes_aberto")

ROOT_DIR = Path(__file__).resolve().parents[1]
ARQUIVO_POSICOES = ROOT_DIR / "data" / "b3_termo_posicoes_aberto.csv"
ARQUIVO_RESUMO = ROOT_DIR / "data" / "b3_termo_posicoes_resumo.csv"

CABECALHO_POSICOES = [
    "data_captura",
    "data_referencia",
    "codigo",
    "empresa",
    "tipo",
    "quantidade_contratos",
    "quantidade_ativos",
    "valor_contratos",
    "preco_medio_termo",
]

CABECALHO_RESUMO = [
    "data_captura",
    "data_referencia",
    "total_empresas_termo",
    "quantidade_contratos",
    "quantidade_ativos",
    "valor_contratos",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}


def _parse_float_br(val) -> float:
    """Converte '4.678.626.251,93' para 4678626251.93."""
    s = str(val or "").strip()
    if not s or s == "-":
        return 0.0
    s = s.replace(".", "").replace(",", ".")
    try:
        return round(float(s), 2)
    except (ValueError, TypeError):
        return 0.0


def _parse_int_br(val) -> int:
    """Converte '320.752.049' para 320752049."""
    s = str(val or "").strip()
    if not s or s == "-":
        return 0
    s = s.replace(".", "").replace(",", "")
    try:
        return int(s)
    except (ValueError, TypeError):
        return 0


def _extrair_data_referencia_html(soup: BeautifulSoup, default_iso: str) -> str:
    """Extrai data no formato DD/MM/YYYY do texto 'Dados de Fechamento do Pregão de DD/MM/YYYY'."""
    text = soup.get_text()
    match = re.search(r"Dados de Fechamento do Pregão de\s*(\d{2}/\d{2}/\d{4})", text, re.IGNORECASE)
    if match:
        d, m, y = match.group(1).split("/")
        return f"{y}-{m}-{d}"
    return default_iso


def capturar_dia(data_alvo: date) -> tuple[list[dict], dict | None, str]:
    """
    Captura dados de termo para uma data específica da B3.
    Retorna (linhas_posicoes, linha_resumo, data_referencia_iso).
    """
    str_br = data_alvo.strftime("%d/%m/%Y")
    str_iso = data_alvo.strftime("%Y-%m-%d")
    data_captura, _ = agora_brt()

    url = (
        "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/"
        f"mercado-a-vista/termo/posicoes-em-aberto/posicoes-em-aberto-8AE490C99D724062019D7901CD91500D.htm?data={str_br}&f=0"
    )

    resp = None
    for tentativa in range(3):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 200 and "table" in resp.text.lower():
                break
        except Exception as e:
            log.warning(f"Tentativa {tentativa + 1} falhou para {str_br}: {e}")
            time.sleep(1.5)

    if not resp or resp.status_code != 200 or "table" not in resp.text.lower():
        log.warning(f"Nenhum dado ou erro HTTP na consulta de termo para {str_br}.")
        return [], None, str_iso

    soup = BeautifulSoup(resp.text, "html.parser")
    tables = soup.find_all("table")
    if not tables:
        return [], None, str_iso

    data_ref_iso = _extrair_data_referencia_html(soup, str_iso)

    # Tabela 0: Resumo Geral
    linha_resumo = None
    if len(tables) >= 1:
        t0_rows = tables[0].find_all("tr")
        if len(t0_rows) >= 2:
            tds = [td.get_text(strip=True) for td in t0_rows[1].find_all(["th", "td"])]
            if len(tds) >= 3:
                linha_resumo = {
                    "data_captura": data_captura,
                    "data_referencia": data_ref_iso,
                    "quantidade_contratos": _parse_int_br(tds[0]),
                    "quantidade_ativos": _parse_int_br(tds[1]),
                    "valor_contratos": _parse_float_br(tds[2]),
                }

    # Tabela 1: Posições por Ativo
    linhas_posicoes = []
    if len(tables) >= 2:
        t1_rows = tables[1].find_all("tr")
        for tr in t1_rows[1:]:
            cols = [limpar(td.get_text(strip=True)) for td in tr.find_all(["th", "td"])]
            if len(cols) < 6:
                continue

            codigo = cols[0]
            empresa = cols[1]
            tipo = " ".join(cols[2].split())
            qtd_contratos = _parse_int_br(cols[3])
            qtd_ativos = _parse_int_br(cols[4])
            val_contratos = _parse_float_br(cols[5])

            preco_medio = (
                round(val_contratos / qtd_ativos, 2)
                if qtd_ativos > 0 and val_contratos > 0
                else 0.0
            )

            linhas_posicoes.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": data_ref_iso,
                    "codigo": codigo,
                    "empresa": empresa,
                    "tipo": tipo,
                    "quantidade_contratos": qtd_contratos,
                    "quantidade_ativos": qtd_ativos,
                    "valor_contratos": val_contratos,
                    "preco_medio_termo": preco_medio,
                }
            )

    if linha_resumo:
        linha_resumo["total_empresas_termo"] = len(linhas_posicoes)

    return linhas_posicoes, linha_resumo, data_ref_iso


class B3TermoPosicoesAbertoScraper(BaseScraper):
    name = "b3_termo_posicoes_aberto"
    title = "B3 Posições em Aberto de Termo"
    description = (
        "Posições em aberto e volumes financeiros no mercado a termo da B3 "
        "por empresa/ativo e totalizadores consolidados do mercado."
    )
    icon = "🤝"
    tags = ["b3", "termo", "mercado a termo", "posicoes em aberto", "acoes", "bdrs"]
    group = "b3"
    source = "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-a-vista/termo/posicoes-em-aberto/"

    accumulate = True
    chaves_dedup = ["data_referencia", "codigo"]
    compress = False

    def __init__(self):
        super().__init__()
        self.output_file = ARQUIVO_POSICOES
        self.output_resumo = ARQUIVO_RESUMO

    def fetch(self) -> pd.DataFrame:
        """
        Executa a extração das posições em aberto de termo.
        Se target_date for especificado, busca apenas essa data.
        Caso contrário, busca as datas úteis recentes disponíveis para garantir histórico.
        """
        log.info("Iniciando captura de posições em aberto no mercado a termo da B3...")
        todas_posicoes = []
        todos_resumos = []

        if self.target_date:
            datas = [pd.to_datetime(self.target_date).date()]
        else:
            # Buscar os últimos 5 dias úteis para garantir histórico consistente
            data_base = _CAL.offset(date.today(), -1)
            datas = [_CAL.offset(data_base, -i) for i in range(5)]

        for d in datas:
            log.info(f"Consultando mercado a termo B3 para {d}...")
            posicoes, resumo, ref_iso = capturar_dia(d)
            if posicoes:
                log.info(f"[{ref_iso}] {len(posicoes)} ativos encontrados no mercado a termo.")
                todas_posicoes.extend(posicoes)
                if resumo:
                    todos_resumos.append(resumo)
            time.sleep(0.5)

        if not todas_posicoes:
            log.warning("Nenhum dado de termo retornado para as datas consultadas.")
            return pd.DataFrame(columns=CABECALHO_POSICOES)

        df_posicoes = pd.DataFrame(todas_posicoes, columns=CABECALHO_POSICOES)

        # Salvar o resumo consolidado
        if todos_resumos:
            df_resumo = pd.DataFrame(todos_resumos, columns=CABECALHO_RESUMO)
            salvar_csv(
                arquivo=self.output_resumo,
                registros=df_resumo,
                cabecalho=CABECALHO_RESUMO,
                chaves_dedup=["data_referencia"],
                acumular=True,
            )
            log.info(f"Resumo consolidado salvo em {self.output_resumo} ({len(df_resumo)} linhas).")

        return df_posicoes


if __name__ == "__main__":
    scraper = B3TermoPosicoesAbertoScraper()
    scraper.run()
