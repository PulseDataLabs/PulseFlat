"""
scrapers/b3_opcoes_posicoes_aberto.py
--------------------------------------
Posições em Aberto (Open Interest) de Opções negociadas na B3.
Captura todas as séries de opções de ações (empresas) e de índices (Ibovespa, etc.),
detalhando contratos abertos, posições cobertas, descobertas e em travas,
além da contagem de clientes titulares e lançadores.

Fontes:
- Opções sobre Ações: https://www.b3.com.br/json/{YYYYMMDD}/Posicoes/Empresa/SI_C_OPCPOSABEMP.json
- Opções sobre Índices: https://www.b3.com.br/json/{YYYYMMDD}/Posicoes/Indice/SI_C_OPCPOSABIND.json
Saída:
- data/b3_opcoes_posicoes_aberto.csv.gz (Snapshot completo diário de todas as séries)
- data/b3_opcoes_posicoes_resumo.csv (Resumo acumulado por ativo com Put/Call Ratio e Open Interest)
"""

import sys
import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.base import BaseScraper
from utils import agora_brt, get_logger, limpar, salvar_csv
from utils.parsers import _CAL

log = get_logger("b3_opcoes_posicoes_aberto")

ROOT_DIR = Path(__file__).resolve().parents[1]
ARQUIVO_GRANULAR = ROOT_DIR / "data" / "b3_opcoes_posicoes_aberto.csv.gz"
ARQUIVO_RESUMO = ROOT_DIR / "data" / "b3_opcoes_posicoes_resumo.csv"

CABECALHO_GRANULAR = [
    "data_captura",
    "data_referencia",
    "categoria_ativo",
    "empresa",
    "codigo_ativo_objeto",
    "especificacao",
    "serie",
    "tipo_mercado",
    "preco_exercicio",
    "data_vencimento",
    "posicao_coberta",
    "posicao_trava",
    "posicao_descoberta",
    "posicao_total",
    "clientes_titulares",
    "clientes_lancadores",
]

CABECALHO_RESUMO = [
    "data_captura",
    "data_referencia",
    "codigo_ativo_objeto",
    "total_series",
    "posicao_aberta_call",
    "posicao_aberta_put",
    "posicao_aberta_total",
    "put_call_ratio",
    "posicao_coberta",
    "posicao_descoberta",
    "posicao_trava",
    "strike_max_oi_call",
    "strike_max_oi_put",
]

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}


def _formatar_data_iso(d_str: str) -> str:
    """Converte 'YYYYMMDD' para 'YYYY-MM-DD'."""
    s = str(d_str or "").strip()
    if len(s) == 8 and s.isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return s


def _tipo_mercado_str(t_merc) -> str:
    """Mapeia o código tMerc da B3 para CALL, PUT ou código textual."""
    val = str(t_merc or "").strip()
    if val == "70":
        return "CALL"
    if val == "80":
        return "PUT"
    return val or "OUTROS"


def _capturar_json(url: str) -> dict | None:
    """Executa requisição GET ao endpoint JSON da B3 com timeout e retries."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code in (302, 404):
            return None
        log.warning(f"Resposta HTTP {resp.status_code} para {url}")
        return None
    except Exception as e:
        log.warning(f"Erro ao requisitar {url}: {e}")
        return None


def capturar_dia(data_alvo: date) -> tuple[list[dict], str]:
    """
    Captura opções de ações (empresas) e opções de índices para a data especificada.
    Retorna (lista_de_registros_granulares, data_referencia_str).
    """
    ymd = data_alvo.strftime("%Y%m%d")
    str_data = data_alvo.strftime("%Y-%m-%d")
    data_captura, _ = agora_brt()

    url_emp = f"https://www.b3.com.br/json/{ymd}/Posicoes/Empresa/SI_C_OPCPOSABEMP.json"
    url_ind = f"https://www.b3.com.br/json/{ymd}/Posicoes/Indice/SI_C_OPCPOSABIND.json"

    data_emp = _capturar_json(url_emp)
    if not data_emp or "Empresa" not in data_emp:
        return [], str_data

    todos = []

    # 1. Opções sobre Ações / Empresas
    for letra, series_list in data_emp.get("Empresa", {}).items():
        for s in series_list:
            todos.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": str_data,
                    "categoria_ativo": "EMPRESA",
                    "empresa": limpar(str(s.get("nmEmp", ""))),
                    "codigo_ativo_objeto": limpar(str(s.get("mer", ""))),
                    "especificacao": limpar(str(s.get("espPap", ""))),
                    "serie": limpar(str(s.get("ser", ""))),
                    "tipo_mercado": _tipo_mercado_str(s.get("tMerc")),
                    "preco_exercicio": float(s.get("prEx", 0) or 0),
                    "data_vencimento": _formatar_data_iso(s.get("dtVen")),
                    "posicao_coberta": int(s.get("poCob", 0) or 0),
                    "posicao_trava": int(s.get("posTr", 0) or 0),
                    "posicao_descoberta": int(s.get("posDe", 0) or 0),
                    "posicao_total": int(s.get("posTo", 0) or 0),
                    "clientes_titulares": int(s.get("qtdClTit", 0) or 0),
                    "clientes_lancadores": int(s.get("qtdClLan", 0) or 0),
                }
            )

    # 2. Opções sobre Índices
    data_ind = _capturar_json(url_ind)
    if data_ind and "Indice" in data_ind:
        for s in data_ind.get("Indice", []):
            ticker_obj = limpar(str(s.get("mer", "")))
            nome_empresa = f"ÍNDICE {ticker_obj}" if ticker_obj else "ÍNDICE"
            todos.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": str_data,
                    "categoria_ativo": "INDICE",
                    "empresa": nome_empresa,
                    "codigo_ativo_objeto": ticker_obj,
                    "especificacao": "INDICE",
                    "serie": limpar(str(s.get("ser", ""))),
                    "tipo_mercado": _tipo_mercado_str(s.get("tMerc")),
                    "preco_exercicio": float(s.get("prEx", 0) or 0),
                    "data_vencimento": _formatar_data_iso(s.get("dtVen")),
                    "posicao_coberta": int(s.get("poCob", 0) or 0),
                    "posicao_trava": int(s.get("posTr", 0) or 0),
                    "posicao_descoberta": int(s.get("posDe", 0) or 0),
                    "posicao_total": int(s.get("posTo", 0) or 0),
                    "clientes_titulares": int(s.get("qtdClTit", 0) or 0),
                    "clientes_lancadores": int(s.get("qtdClLan", 0) or 0),
                }
            )

    return todos, str_data


def capturar(target_date: date | None = None) -> tuple[list[dict], str]:
    """
    Captura dados de posições em aberto. Se target_date for omitido,
    tenta as últimas datas úteis até encontrar a mais recente disponível na B3.
    """
    if target_date:
        return capturar_dia(target_date)

    data_base = _CAL.offset(date.today(), -1)
    for delta in range(5):
        d = _CAL.offset(data_base, -delta)
        log.info(f"Buscando posições em aberto de opções B3 para {d}...")
        registros, str_ref = capturar_dia(d)
        if registros:
            log.info(
                f"{len(registros)} séries de opções encontradas para a data {str_ref}."
            )
            return registros, str_ref
        time.sleep(0.3)

    log.warning("Nenhum dado de opções retornado nos últimos 5 dias úteis.")
    return [], data_base.strftime("%Y-%m-%d")


def gerar_resumo_por_ativo(df_granular: pd.DataFrame, str_data: str) -> pd.DataFrame:
    """
    Gera dataframe consolidado por ativo-objeto com métricas agregadas:
    Open Interest de CALLs, PUTs, Put/Call Ratio, cobertas vs descobertas e strikes de maior OI.
    """
    if df_granular.empty:
        return pd.DataFrame(columns=CABECALHO_RESUMO)

    data_captura, _ = agora_brt()
    resumo_linhas = []

    for ativo, g in df_granular.groupby("codigo_ativo_objeto"):
        if not ativo:
            continue

        call_mask = g["tipo_mercado"] == "CALL"
        put_mask = g["tipo_mercado"] == "PUT"

        pos_call = int(g.loc[call_mask, "posicao_total"].sum())
        pos_put = int(g.loc[put_mask, "posicao_total"].sum())
        pos_total = int(g["posicao_total"].sum())
        pc_ratio = round(pos_put / pos_call, 4) if pos_call > 0 else 0.0

        call_df = g.loc[call_mask]
        strike_call = (
            float(call_df.loc[call_df["posicao_total"].idxmax()]["preco_exercicio"])
            if not call_df.empty
            else 0.0
        )

        put_df = g.loc[put_mask]
        strike_put = (
            float(put_df.loc[put_df["posicao_total"].idxmax()]["preco_exercicio"])
            if not put_df.empty
            else 0.0
        )

        resumo_linhas.append(
            {
                "data_captura": data_captura,
                "data_referencia": str_data,
                "codigo_ativo_objeto": ativo,
                "total_series": len(g),
                "posicao_aberta_call": pos_call,
                "posicao_aberta_put": pos_put,
                "posicao_aberta_total": pos_total,
                "put_call_ratio": pc_ratio,
                "posicao_coberta": int(g["posicao_coberta"].sum()),
                "posicao_descoberta": int(g["posicao_descoberta"].sum()),
                "posicao_trava": int(g["posicao_trava"].sum()),
                "strike_max_oi_call": strike_call,
                "strike_max_oi_put": strike_put,
            }
        )

    df_resumo = pd.DataFrame(resumo_linhas)
    if not df_resumo.empty:
        df_resumo = df_resumo.sort_values(by="posicao_aberta_total", ascending=False)
        return df_resumo[CABECALHO_RESUMO]
    return pd.DataFrame(columns=CABECALHO_RESUMO)


def atualizar_resumo_acumulado(df_resumo_dia: pd.DataFrame) -> None:
    """Atualiza o arquivo data/b3_opcoes_posicoes_resumo.csv de forma incremental."""
    if df_resumo_dia.empty:
        return
    salvar_csv(
        arquivo=ARQUIVO_RESUMO,
        registros=df_resumo_dia,
        cabecalho=CABECALHO_RESUMO,
        chaves_dedup=["data_referencia", "codigo_ativo_objeto"],
        acumular=True,
    )
    log.info(f"Resumo de opções por ativo atualizado em {ARQUIVO_RESUMO}.")


class B3OpcoesPosicoesAbertoScraper(BaseScraper):
    name = "b3_opcoes_posicoes_aberto"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = False
    compress = True  # Gera data/b3_opcoes_posicoes_aberto.csv.gz

    # Catálogo de Metadados
    title = "B3 Opções — Posições em Aberto (Open Interest)"
    description = (
        "Posições em aberto (Open Interest) de todas as séries de opções de ações e índices da B3, "
        "com detalhamento de posições cobertas, descobertas, em travas e número de clientes titulares e lançadores."
    )
    icon = "🎯"
    icon_class = "icon-b3"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = ["opções", "open interest", "posições em aberto", "call", "put", "derivativos", "B3"]
    source = "B3"

    def fetch(self) -> pd.DataFrame:
        log.info("=== B3 Opções — Posições em Aberto ===")
        dados, str_data = capturar(self.target_date)
        df = pd.DataFrame(dados)

        if not df.empty:
            # Ordena por ativo objeto, vencimento e strike
            df = df.sort_values(by=["codigo_ativo_objeto", "data_vencimento", "preco_exercicio"])

            # Gera e atualiza paralelamente o resumo acumulado
            df_resumo = gerar_resumo_por_ativo(df, str_data)
            atualizar_resumo_acumulado(df_resumo)

            colunas = [c for c in CABECALHO_GRANULAR if c in df.columns]
            return df[colunas]

        return pd.DataFrame(columns=CABECALHO_GRANULAR)


if __name__ == "__main__":
    B3OpcoesPosicoesAbertoScraper().run()
