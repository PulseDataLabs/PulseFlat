"""
scrapers/anbima_indicadores.py
-------------------------------
Captura o quadro de indicadores financeiros da ANBIMA:
  Taxa SELIC, DI-B3, IGP-M, IPCA, Dólar, Euro, TR, TBF, FDS.

Fonte: https://www.anbima.com.br/informacoes/indicadores/
"""

import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, nova_session, salvar_csv

log = get_logger("anbima_indicadores")

URL     = "https://www.anbima.com.br/informacoes/indicadores/"
ARQUIVO = Path("data/anbima_indicadores.csv")

CABECALHO = [
    "data_captura",
    "data_referencia",
    "data_referencia_pagina",
    "indicador",
    "categoria",
    "valor",
    "unidade",
]


def _limpar_valor(texto: str) -> str:
    if not texto:
        return ""
    texto_limpo = texto.strip().replace("\xa0", "")
    if "," in texto_limpo:
        texto_limpo = texto_limpo.replace(".", "").replace(",", ".")
    return re.sub(r"[%\s]", "", texto_limpo)


def _extrair_data_ref(soup: BeautifulSoup) -> str:
    texto = soup.get_text(" ", strip=True)
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})\s*[-–]\s*(\d{2}:\d{2})", texto)
    if m:
        dia, mes, ano, hora = m.group(1), m.group(2), m.group(3), m.group(4)
        return f"{ano}-{mes}-{dia} {hora}:00"
    return "N/A"


def capturar() -> list[dict]:
    log.info(f"Acessando {URL}")
    session = nova_session()

    for tentativa in range(1, 4):
        try:
            resp = session.get(URL, timeout=30)
            resp.encoding = "iso-8859-1"
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error("Todas as tentativas falharam.")
                sys.exit(1)
            time.sleep(5)

    soup = BeautifulSoup(resp.text, "html.parser")
    data_captura, _ = agora_brt()
    data_ref_pag = _extrair_data_ref(soup)
    texto    = soup.get_text(" ", strip=True)
    registros = []

    def add(indicador, categoria, valor, data_referencia, unidade=""):
        registros.append({
            "data_captura":           data_captura,
            "data_referencia":        data_referencia,
            "data_referencia_pagina": data_ref_pag,
            "indicador":              indicador,
            "categoria":              categoria,
            "valor":                  _limpar_valor(valor),
            "unidade":                unidade,
        })

    # Mapeamento de abreviações dos meses
    MESES_MAP = {
        "jan": "01", "fev": "02", "mar": "03", "abr": "04",
        "mai": "05", "jun": "06", "jul": "07", "ago": "08",
        "set": "09", "out": "10", "nov": "11", "dez": "12",
    }

    def _converter_mes_ano(texto_mes_ano: str) -> str:
        m = re.search(r"([a-z]{3})[a-z]*\s*/\s*(\d{2})", texto_mes_ano.lower())
        if m:
            mes_str = m.group(1)
            ano_str = "20" + m.group(2)
            mes_num = MESES_MAP.get(mes_str)
            if mes_num:
                return f"{ano_str}-{mes_num}-01"
        return ""

    def _formatar_data_iso(data_str: str) -> str:
        parts = data_str.split("/")
        if len(parts) == 3:
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
        return data_str

    # Extrai referências de mês do IGP-M e IPCA (e suas projeções)
    m_igpm = re.search(r"IGP-M\s*\(([^)]+)\)", texto)
    dt_igpm = _converter_mes_ano(m_igpm.group(1)) if m_igpm else ""

    m_igpm_proj = re.search(r"IGP-M\s*\d*\s*Proje..o\s*\(([^)]+)\)", texto, re.IGNORECASE)
    dt_igpm_proj = _converter_mes_ano(m_igpm_proj.group(1)) if m_igpm_proj else ""

    m_ipca = re.search(r"IPCA\s*\(([^)]+)\)", texto)
    dt_ipca = _converter_mes_ano(m_ipca.group(1)) if m_ipca else ""

    m_ipca_proj = re.search(r"IPCA\s*\d*\s*Proje..o\s*\(([^)]+)\)", texto, re.IGNORECASE)
    dt_ipca_proj = _converter_mes_ano(m_ipca_proj.group(1)) if m_ipca_proj else ""

    # Taxas de Juros
    for nome, padrao in [
        ("Estimativa SELIC", r"Estimativa SELIC.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Taxa SELIC (BC)",  r"Taxa SELIC do BC.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("DI-B3",            r"DI-B3.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]:
        m = re.search(padrao, texto, re.DOTALL)
        if m:
            dt_ref = _formatar_data_iso(m.group(1))
            add(nome, "Taxa de Juros", m.group(2), dt_ref, "% a.a.")

    # Índices de Preços
    for nome, padrao, dt_ref, unidade in [
        ("IGP-M Número Índice", r"IGP-M\s*\([^)]+\)\s*\d*\s*N.mero\s*.ndice\s*([\d\.,]+)", dt_igpm, "índice"),
        ("IGP-M Var % mês",     r"IGP-M\s*\([^)]+\)\s*\d*\s*.*?Var\s*%\s*no\s*m[eê]s\s*(-?\d+[\.,]\d+)", dt_igpm, "%"),
        ("IGP-M Projeção",      r"IGP-M\s*\d*\s*Proje..o\s*\([^)]+\)\s*(-?\d+[\.,]\d+)", dt_igpm_proj, "%"),
        ("IPCA Número Índice",  r"IPCA\s*\([^)]+\)\s*\d*\s*N.mero\s*.ndice\s*([\d\.,]+)", dt_ipca, "índice"),
        ("IPCA Var % mês",      r"IPCA\s*\([^)]+\)\s*\d*\s*.*?Var\s*%\s*no\s*m[eê]s\s*(-?\d+[\.,]\d+)", dt_ipca, "%"),
        ("IPCA Projeção",       r"IPCA\s*\d*\s*Proje..o\s*\([^)]+\)\s*(-?\d+[\.,]\d+)", dt_ipca_proj, "%"),
    ]:
        m = re.search(padrao, texto, re.DOTALL | re.IGNORECASE)
        if m:
            add(nome, "Índice de Preços", m.group(1), dt_ref, unidade)

    # Câmbio
    for nome, padrao in [
        ("Dólar Comercial Compra", r"Dolar Comercial Compra.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Dólar Comercial Venda",  r"D.lar Comercial Venda.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Euro Compra",            r"Euro Compra.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("Euro Venda",             r"Euro Venda.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]:
        m = re.search(padrao, texto, re.DOTALL)
        if m:
            dt_ref = _formatar_data_iso(m.group(1))
            add(nome, "Câmbio", m.group(2), dt_ref, "R$")

    # TR / TBF
    for nome, padrao in [
        ("TR",  r"\bTR\b.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
        ("TBF", r"\bTBF\b.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)"),
    ]:
        m = re.search(padrao, texto, re.DOTALL)
        if m:
            dt_ref = _formatar_data_iso(m.group(1))
            add(nome, "Taxa de Referência", m.group(2), dt_ref, "% mês")

    # FDS
    for i, m in enumerate(
        re.findall(r"FDS.*?(\d{2}/\d{2}/\d{4}).*?(\d+[\.,]\d+)", texto, re.DOTALL)[:2], 1
    ):
        dt_ref = _formatar_data_iso(m[0])
        add(f"FDS (registro {i})", "FDS", m[1], dt_ref, "R$ cota")

    log.info(f"{len(registros)} indicadores capturados (ref: {data_ref_pag})")
    return registros


def main():
    log.info("=== ANBIMA Indicadores ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "indicador"])


if __name__ == "__main__":
    main()
