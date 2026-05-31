"""
scrapers/anbima_projecoes.py
-----------------------------
Captura as projeções do IPCA e IGP-M divulgadas pela ANBIMA.

Fonte: https://www.anbima.com.br/pt_br/informar/projecoes-ipca-e-igp-m.htm

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESTRATÉGIAS DE COLETA (com fallback automático)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ESTRATÉGIA A — API Oficial ANBIMA (se credenciais configuradas)
  Endpoint: GET https://api.anbima.com.br/feed/precos-indices/v1/titulos-publicos/projecoes
  Auth:     OAuth 2.0 via client_id + client_secret
  Dados:    JSON estruturado, com nº de instituições e histórico disponível
  Cadastro: https://developers.anbima.com.br
  Produção: anbimafeed@anbima.com.br

ESTRATÉGIA B — Scraping da página de indicadores (fallback sem credenciais)
  Fonte:  https://www.anbima.com.br/informacoes/indicadores/
  Dados:  projeções vigentes do mês corrente e seguinte (atualização 2x/dia)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONFIGURAÇÃO DAS CREDENCIAIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Via variáveis de ambiente ou arquivo .env na raiz do projeto:
  ANBIMA_CLIENT_ID=seu_client_id
  ANBIMA_CLIENT_SECRET=seu_client_secret

No GitHub Actions: Settings → Secrets → ANBIMA_CLIENT_ID e ANBIMA_CLIENT_SECRET

Sem configuração: o scraper usa scraping como fallback automaticamente.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SOBRE AS PROJEÇÕES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IGP-M: coletado nos dias de divulgação das prévias e fechado pela FGV (~3x/mês)
       → projeções para o mês corrente e o posterior

IPCA:  coletado no dia do IPCA fechado e do IPCA-15 pelo IBGE (~2x/mês)
       → projeções para o mês corrente e o seguinte

Dependências:
    pip install requests beautifulsoup4 python-dotenv
"""

import os
import re
import sys
import time
from base64 import b64encode
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Carrega .env se existir (sem obrigar dependência em produção)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv

log = get_logger("anbima_projecoes")

# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────
URL_INDICADORES     = "https://www.anbima.com.br/informacoes/indicadores/"
ANBIMA_OAUTH_URL    = "https://api.anbima.com.br/oauth/access-token"
ANBIMA_PROJECOES_URL = "https://api.anbima.com.br/feed/precos-indices/v1/titulos-publicos/projecoes"

ARQUIVO = Path("data/anbima_projecoes.csv")

CABECALHO = [
    "data_captura",
    "hora_captura",
    "estrategia_coleta",      # "api_oficial" | "scraping_indicadores"
    "indice",                 # IPCA | IGP-M
    "mes_referencia",         # ex: "mai/26"
    "tipo_projecao",          # corrente | seguinte | posterior | fechado
    "valor_pct",              # ex: 0.64 (separador decimal: ponto)
    "data_divulgacao",        # data em que a projeção foi divulgada
    "num_instituicoes",       # nº de instituições (disponível via API)
    "observacao",
]


# ════════════════════════════════════════════════════════
# ESTRATÉGIA A — API Oficial OAuth 2.0
# ════════════════════════════════════════════════════════

def _obter_token(client_id: str, client_secret: str) -> str | None:
    """Troca client_id + client_secret por access_token OAuth 2.0."""
    credencial = b64encode(f"{client_id}:{client_secret}".encode()).decode()
    try:
        resp = requests.post(
            ANBIMA_OAUTH_URL,
            headers={
                "Content-Type":  "application/json",
                "Authorization": f"Basic {credencial}",
            },
            json={"grant_type": "client_credentials"},
            timeout=30,
        )
        resp.raise_for_status()
        token = resp.json().get("access_token")
        if token:
            log.info("[API Oficial] Access token obtido.")
        return token
    except Exception as e:
        log.error(f"[API Oficial] Falha ao obter token: {e}")
        return None


def _mapear_api(item: dict, data_captura: str, hora_captura: str) -> dict:
    return {
        "data_captura":      data_captura,
        "hora_captura":      hora_captura,
        "estrategia_coleta": "api_oficial",
        "indice":            limpar(item.get("indice") or item.get("index", "")).upper(),
        "mes_referencia":    limpar(item.get("referenceMonth") or item.get("mesReferencia") or item.get("mes_referencia", "")),
        "tipo_projecao":     limpar(item.get("projectionType") or item.get("tipoProjecao", "")),
        "valor_pct":         limpar(item.get("projection")     or item.get("projecao") or item.get("value", "")).replace(",", "."),
        "data_divulgacao":   limpar(item.get("releaseDate")    or item.get("dataReferencia", "")),
        "num_instituicoes":  limpar(item.get("numberOfInstitutions") or item.get("numInstituicoes", "")),
        "observacao":        "",
    }


def capturar_via_api(client_id: str, client_secret: str) -> list[dict]:
    log.info("[API Oficial] Iniciando captura...")
    token = _obter_token(client_id, client_secret)
    if not token:
        return []

    data_captura, hora_captura = agora_brt()
    try:
        resp = requests.get(
            ANBIMA_PROJECOES_URL,
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            timeout=30,
        )
        resp.raise_for_status()
        dados = resp.json()
    except Exception as e:
        log.error(f"[API Oficial] Erro ao buscar projeções: {e}")
        return []

    # API pode retornar lista direta ou objeto com chave de dados
    if isinstance(dados, list):
        itens = dados
    elif isinstance(dados, dict):
        itens = dados.get("data", dados.get("projecoes", dados.get("results", [dados])))
    else:
        itens = []

    registros = [_mapear_api(i, data_captura, hora_captura) for i in itens]
    log.info(f"[API Oficial] {len(registros)} projeções capturadas.")
    return registros


# ════════════════════════════════════════════════════════
# ESTRATÉGIA B — Scraping da página de indicadores
# ════════════════════════════════════════════════════════

def capturar_via_scraping() -> list[dict]:
    """
    Extrai projeções vigentes da página de indicadores da ANBIMA.
    Atualizada 2x/dia e inclui projeções do mês corrente e seguinte.
    """
    log.info(f"[Scraping] Acessando {URL_INDICADORES}")
    data_captura, hora_captura = agora_brt()

    for tentativa in range(1, 4):
        try:
            resp = requests.get(
                URL_INDICADORES,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=30,
            )
            resp.encoding = "iso-8859-1"
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"[Scraping] Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error("[Scraping] Todas as tentativas falharam.")
                return []
            time.sleep(5)

    texto = BeautifulSoup(resp.text, "html.parser").get_text(" ", strip=True)
    registros = []

    def add(indice, mes_ref, tipo, valor, data_div="", obs=""):
        registros.append({
            "data_captura":      data_captura,
            "hora_captura":      hora_captura,
            "estrategia_coleta": "scraping_indicadores",
            "indice":            indice,
            "mes_referencia":    mes_ref,
            "tipo_projecao":     tipo,
            "valor_pct":         valor.replace(",", ".").replace("%", "").strip(),
            "data_divulgacao":   data_div,
            "num_instituicoes":  "",
            "observacao":        obs,
        })

    # IGP-M — variação fechada
    m = re.search(r"IGP-M.*?Var\s*%\s*no\s*m[eê]s.*?(\w{3}/\d{2,4}).*?(-?\d+[,\.]\d+)",
                  texto, re.DOTALL | re.IGNORECASE)
    if m:
        add("IGP-M", m.group(1), "fechado", m.group(2), obs="Var % mês fechado")

    # IGP-M — projeção genérica
    for i, m in enumerate(re.findall(
        r"IGP-M[^%\n]*?proje[cç][aã]o[^%\n]*?(\w{3}/\d{2,4})[^%\n]*?(-?\d+[,\.]\d+\s*%?)",
        texto, re.IGNORECASE
    )[:3]):
        tipos = ["corrente", "seguinte", "posterior"]
        add("IGP-M", m[0], tipos[i], m[1].replace("%", "").strip(),
            obs=f"Projeção ANBIMA {tipos[i]}")

    # IPCA — variação fechada
    m = re.search(r"IPCA.*?Var\s*%\s*no\s*m[eê]s.*?(\w{3}/\d{2,4}).*?(-?\d+[,\.]\d+)",
                  texto, re.DOTALL | re.IGNORECASE)
    if m:
        add("IPCA", m.group(1), "fechado", m.group(2), obs="Var % mês fechado")

    # IPCA — projeção genérica
    for i, m in enumerate(re.findall(
        r"IPCA[^%\n]*?proje[cç][aã]o[^%\n]*?(\w{3}/\d{2,4})[^%\n]*?(-?\d+[,\.]\d+\s*%?)",
        texto, re.IGNORECASE
    )[:2]):
        tipos = ["corrente", "seguinte"]
        add("IPCA", m[0], tipos[i], m[1].replace("%", "").strip(),
            obs=f"Projeção ANBIMA {tipos[i]}")

    # Remove duplicatas por (indice, mes_referencia, tipo_projecao)
    vistos, unicos = set(), []
    for r in registros:
        chave = (r["indice"], r["mes_referencia"], r["tipo_projecao"])
        if chave not in vistos:
            vistos.add(chave)
            unicos.append(r)

    log.info(f"[Scraping] {len(unicos)} projeções capturadas.")
    return unicos


# ════════════════════════════════════════════════════════
# Orquestrador com fallback automático
# ════════════════════════════════════════════════════════

def capturar() -> list[dict]:
    client_id     = os.getenv("ANBIMA_CLIENT_ID", "").strip()
    client_secret = os.getenv("ANBIMA_CLIENT_SECRET", "").strip()

    if client_id and client_secret:
        log.info("Credenciais encontradas → usando API oficial.")
        registros = capturar_via_api(client_id, client_secret)
        if registros:
            return registros
        log.warning("API oficial sem dados → usando scraping como fallback.")

    log.info("Usando scraping da página de indicadores.")
    return capturar_via_scraping()


def main():
    log.info("=== ANBIMA Projeções IPCA e IGP-M ===")
    registros = capturar()
    if not registros:
        log.error("Nenhuma projeção capturada.")
        sys.exit(1)
    salvar_csv(ARQUIVO, registros, CABECALHO,
               chaves_dedup=["data_captura", "indice", "mes_referencia", "tipo_projecao"])


if __name__ == "__main__":
    main()
