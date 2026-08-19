from collections import defaultdict

#!/usr/bin/env python
# coding: utf-8
"""
scripts/consolidate.py
-----------------------
Gera tabela consolidada com o último valor de cada indicador financeiro
time-series (séries temporais). Exclui contagens e dados transacionais.

Saídas:
  data/consolidated.json  — dados consolidados (formato JSON)
  data/consolidated.csv   — dados consolidados (formato CSV)
  data/consolidated.js    — fallback offline para a página web
"""

import argparse
import csv
import json
import sys
import time
from collections import OrderedDict
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils.ux import (
    ColorLogger,
    add_common_args,
    apply_common_args,
    banner,
    print_done,
    print_info,
    print_start,
    print_summary,
    print_warn,
    section,
)

log = ColorLogger("consolidate")

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


# ── Helpers ────────────────────────────────────────────────────────────


def _read_csv(path: str) -> list[dict]:
    if not Path(path).exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sorted_by(rows: list[dict], col: str, reverse: bool = True) -> list[dict]:
    return sorted(rows, key=lambda r: r.get(col, ""), reverse=reverse)


def _parse_br_float(val: str) -> Optional[float]:
    if not val or not val.strip():
        return None
    try:
        return float(val.strip().replace(",", "."))
    except ValueError:
        return None


def _fmt_val(val: str) -> str:
    f = _parse_br_float(val)
    if f is None:
        return val
    abs_f = abs(f)
    if abs_f >= 1000:
        decimals = 0
    elif abs_f >= 1:
        decimals = 2
    elif abs_f >= 0.01:
        decimals = 4
    else:
        decimals = 6
    return f"{f:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _fmt_pct(val: str, decimals: int = 2) -> str:
    f = _parse_br_float(val)
    if f is None:
        return val
    return f"{f:,.{decimals}f}%".replace(",", "X").replace(".", ",").replace("X", ".")


def _safe(val: str) -> str:
    return (val or "").strip()


# ── Nomes amigáveis de datasets ────────────────────────────────────────

DATASET_LABEL = {
    "bcb_sgs.csv": "BCB SGS",
    "anbima_indicadores.csv": "ANBIMA Indicadores",
    "b3_bdi_di_over.csv": "B3 DI Over",
    "b3_bmf_taxas_juros.csv": "B3 BMF Taxas",
    "b3_indicadores_financeiros.csv": "B3 Indicadores Financeiros",
    "b3_taxa_cambio_referencia.csv": "B3 Taxa Câmbio",
    "bcb_ptax.csv": "BCB PTAX",
    "anbima_indice_imab.csv": "ANBIMA IMA-B",
    "anbima_titulos_publicos.csv": "ANBIMA Títulos Públicos",
    "yahoo_acoes_brasileiras.csv": "Yahoo Ações Brasileiras",
    "yahoo_acoes_internacionais.csv": "Yahoo Ações Internacionais",
    "yahoo_cambio_moedas.csv": "Yahoo Câmbio e Moedas",
    "yahoo_criptoativos.csv": "Yahoo Criptoativos",
    "yahoo_commodities.csv": "Yahoo Commodities",
    "yahoo_indices_globais.csv": "Yahoo Índices Globais",
    "yahoo_renda_fixa.csv": "Yahoo Renda Fixa",
    "yahoo_etfs.csv": "Yahoo ETFs",
    "yahoo_fiis_fiagros.csv": "Yahoo FIIs e Fiagros",
    "ipea_macroeconomia.csv": "IPEA Macroeconomia",
    "ipea_mercados_diarios.csv": "IPEA Mercados Diários",
    "ipea_taxas_juros.csv": "IPEA Taxas de Juros",
    "ipea_precos_inflacao.csv": "IPEA Preços e Inflação",
    "ipea_fbcf.csv": "IPEA FBCF",
    "ipea_comercio_exterior.csv": "IPEA Comércio Exterior",
    "ipea_producao_mineral.csv": "IPEA Produção Mineral",
    "ipea_calendario.csv": "IPEA Calendário",
}


YAHOO_SECTIONS = {
    "Ações Brasileiras (B3)": [
        "VALE3.SA",
        "PETR4.SA",
        "PETR3.SA",
        "ITUB4.SA",
        "BBDC4.SA",
        "BBAS3.SA",
        "B3SA3.SA",
        "ELET3.SA",
        "WEGE3.SA",
        "ABEV3.SA",
        "RENT3.SA",
        "GGBR4.SA",
        "CSNA3.SA",
        "USIM5.SA",
        "JBSS3.SA",
        "MGLU3.SA",
        "LREN3.SA",
        "EQTL3.SA",
        "SBSP3.SA",
        "SUZB3.SA",
        "VIVT3.SA",
        "TIMS3.SA",
        "SANB11.SA",
        "BPAC11.SA",
        "CIEL3.SA",
        "EGIE3.SA",
        "CPFE3.SA",
        "CMIG4.SA",
        "CCRO3.SA",
        "RADL3.SA",
        "HYPE3.SA",
        "CRFB3.SA",
        "ASAI3.SA",
        "NTCO3.SA",
        "BRFS3.SA",
        "COGN3.SA",
        "CYRE3.SA",
        "MRVE3.SA",
        "EZTC3.SA",
        "TEND3.SA",
        "ALOS3.SA",
        "MULT3.SA",
        "IGTI11.SA",
        "BEEF3.SA",
        "MRFG3.SA",
        "CPLE6.SA",
        "ENGI11.SA",
        "TAEE11.SA",
        "TRPL4.SA",
        "PRIO3.SA",
        "RRRP3.SA",
        "RECV3.SA",
        "UGPA3.SA",
        "VBBR3.SA",
        "CSAN3.SA",
        "BRKM5.SA",
        "EMBR3.SA",
        "GOLL4.SA",
        "AZUL4.SA",
        "RUMO3.SA",
        "JHSF3.SA",
        "YDUQ3.SA",
        "CVCB3.SA",
        "SLCE3.SA",
        "SMTO3.SA",
        "FLRY3.SA",
        "HAPV3.SA",
        "QUAL3.SA",
        "ODPV3.SA",
        "BBDC3.SA",
        "ITSA4.SA",
        "BRAP4.SA",
        "CMIN3.SA",
        "KLBN11.SA",
        "PCAR3.SA",
        "IRBR3.SA",
        "ENEV3.SA",
        "LOGN3.SA",
        "MDIA3.SA",
    ],
    "Ações Internacionais": [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "NVDA",
        "META",
        "TSLA",
        "NFLX",
        "JPM",
        "V",
        "WMT",
        "DIS",
        "MA",
        "UNH",
        "HD",
        "BAC",
        "XOM",
        "CVX",
        "KO",
        "PEP",
        "COST",
        "PG",
        "JNJ",
        "MRK",
        "ABBV",
        "LLY",
        "PFE",
        "AMD",
        "INTC",
        "QCOM",
        "ADBE",
        "CRM",
        "ORCL",
        "NKE",
        "MCD",
        "SBUX",
        "NVO",
        "ASML",
        "TSM",
        "BABA",
    ],
    "Câmbio / Moedas": [
        "BRL=X",
        "EURBRL=X",
        "GBPBRL=X",
        "CHFBRL=X",
        "JPYBRL=X",
        "CNYBRL=X",
        "ARSBRL=X",
        "CLPBRL=X",
        "MXNBRL=X",
        "UYUBRL=X",
        "COPBRL=X",
        "PENBRL=X",
        "EURUSD=X",
        "GBPUSD=X",
        "USDJPY=X",
        "AUDUSD=X",
        "USDCAD=X",
        "USDCHF=X",
        "USDCNY=X",
        "USDRUB=X",
        "USDTRY=X",
        "USDINR=X",
        "USDMXN=X",
        "DX-Y.NYB",
    ],
    "Criptoativos": [
        "BTC-USD",
        "ETH-USD",
        "SOL-USD",
        "BNB-USD",
        "XRP-USD",
        "ADA-USD",
        "DOGE-USD",
        "DOT-USD",
        "AVAX-USD",
        "LINK-USD",
        "SHIB-USD",
        "TRX-USD",
        "LTC-USD",
        "UNI-USD",
        "XLM-USD",
        "ATOM-USD",
        "ETC-USD",
        "FIL-USD",
        "HBAR-USD",
        "NEAR-USD",
        "ICP-USD",
        "APT-USD",
        "OP-USD",
        "GRT-USD",
        "IMX-USD",
    ],
    "Commodities Globais": [
        "TIO=F",
        "ZS=F",
        "KC=F",
        "CL=F",
        "BZ=F",
        "GC=F",
        "SI=F",
        "HG=F",
        "NG=F",
        "ZC=F",
        "ZW=F",
        "SB=F",
        "CT=F",
        "CC=F",
        "LH=F",
        "FC=F",
        "PL=F",
        "PA=F",
        "ZO=F",
        "ZR=F",
    ],
    "Índices de Ações Globais": [
        "^BVSP",
        "^GSPC",
        "^IXIC",
        "^DJI",
        "^VIX",
        "^STOXX50E",
        "000001.SS",
        "^N225",
        "^FTSE",
        "^GDAXI",
        "^FCHI",
        "^HSI",
        "^MERV",
        "^IPSA",
        "^MXX",
        "^RUT",
        "^NYA",
        "^AXJO",
        "^BSESN",
        "^KS11",
        "^TWII",
        "^JKSE",
        "^STI",
        "^KLSE",
        "^TA35",
    ],
    "Renda Fixa & Treasuries": ["^IRX", "^FVX", "^TNX", "^TYX"],
    "ETFs & Setoriais": [
        "EWZ",
        "SMLL.SA",
        "BOVA11.SA",
        "SMAL11.SA",
        "IVVB11.SA",
        "HASH11.SA",
        "BND",
        "HYG",
        "LQD",
        "SPY",
        "QQQ",
        "DIA",
        "IWM",
        "EEM",
        "VGK",
        "VWO",
        "XLE",
        "XLF",
        "XLK",
    ],
    "FIIs e Fiagros": [
        "IFIX.SA",
        "MXRF11.SA",
        "HGLG11.SA",
        "XPML11.SA",
        "KNIP11.SA",
        "BTLG11.SA",
        "KNCR11.SA",
        "VISC11.SA",
        "HGRU11.SA",
        "BRCO11.SA",
        "PVBI11.SA",
        "ALZR11.SA",
        "VGIA11.SA",
        "KNCA11.SA",
        "RURA11.SA",
        "CPTR11.SA",
        "FGAA11.SA",
    ],
}


IPEADATA_SECTIONS = {
    "ipea_macroeconomia.csv": [
        {
            "code": "BM12_PIBAC12",
            "label": "PIB (acumulado 12m)",
            "category": "Macroeconomia",
        },
        {
            "code": "PNADC12_TDESOC12",
            "label": "Taxa de desocupação (PNAD Contínua)",
            "category": "Macroeconomia",
            "fmt": "pct",
        },
        {
            "code": "GAC12_SALMINRE12",
            "label": "Salário Mínimo Real",
            "category": "Macroeconomia",
        },
        {
            "code": "MTE12_SALMIN12",
            "label": "Salário Mínimo Vigente",
            "category": "Macroeconomia",
        },
        {
            "code": "SGS12_7836",
            "label": "Saldo Total da Poupança (SBPE/Rural)",
            "category": "Macroeconomia",
        },
    ],
    "ipea_mercados_diarios.csv": [
        {
            "code": "EIA366_PBRENT366",
            "label": "Petróleo Brent",
            "category": "Mercados Globais",
        },
        {
            "code": "EIA366_PWTI366",
            "label": "Petróleo WTI",
            "category": "Mercados Globais",
        },
        {
            "code": "GM366_DOW366",
            "label": "Índice Dow Jones",
            "category": "Mercados Globais",
        },
        {
            "code": "SGS366_NASDAQ366",
            "label": "Índice NASDAQ",
            "category": "Mercados Globais",
        },
    ],
    "ipea_taxas_juros.csv": [
        {
            "code": "ANBIMA12_TJPOUP12",
            "label": "Poupança Rentabilidade Antiga (dep. até 2012)",
            "category": "Taxas de Juros",
            "fmt": "pct",
        },
        {
            "code": "BM12_RNDPO12",
            "label": "Poupança Rentabilidade Nova (dep. pós 2012)",
            "category": "Taxas de Juros",
            "fmt": "pct",
        },
        {
            "code": "ANBIMA12_TJTLN112",
            "label": "Estrutura Termo LTN - 1 mês",
            "category": "Taxas de Juros",
            "fmt": "pct",
        },
        {
            "code": "ANBIMA12_TJTLN312",
            "label": "Estrutura Termo LTN - 3 meses",
            "category": "Taxas de Juros",
            "fmt": "pct",
        },
        {
            "code": "ANBIMA12_TJTLN612",
            "label": "Estrutura Termo LTN - 6 meses",
            "category": "Taxas de Juros",
            "fmt": "pct",
        },
        {
            "code": "ANBIMA12_TJTLN1212",
            "label": "Estrutura Termo LTN - 12 meses",
            "category": "Taxas de Juros",
            "fmt": "pct",
        },
        {
            "code": "BM12_TJCDI12",
            "label": "CDI Acumulado no Mês",
            "category": "Taxas de Juros",
            "fmt": "pct",
        },
        {
            "code": "BM12_TJLP12",
            "label": "Taxa de Juros de Longo Prazo (TJLP)",
            "category": "Taxas de Juros",
            "fmt": "pct",
        },
        {
            "code": "BM12_TJOVER12",
            "label": "Selic Acumulada no Mês",
            "category": "Taxas de Juros",
            "fmt": "pct",
        },
        {
            "code": "BM12_TJTBF12",
            "label": "Taxa Básica Financeira (TBF)",
            "category": "Taxas de Juros",
            "fmt": "pct",
        },
        {
            "code": "BM12_TJTR12",
            "label": "Taxa Referencial (TR)",
            "category": "Taxas de Juros",
            "fmt": "pct",
        },
    ],
    "ipea_precos_inflacao.csv": [
        {
            "code": "IGP12_IGPDI12",
            "label": "IGP-DI - Geral - Índice",
            "category": "Macroeconomia",
        },
        {
            "code": "IGP12_INCC12",
            "label": "INCC-DI - Geral - Índice",
            "category": "Macroeconomia",
        },
        {
            "code": "PRECOS12_INPC12",
            "label": "INPC - Geral - Índice",
            "category": "Macroeconomia",
        },
        {
            "code": "PRECOS12_INPCBR12",
            "label": "INPC - Geral - Taxa de Variação",
            "category": "Macroeconomia",
            "fmt": "pct",
        },
    ],
    "ipea_fbcf.csv": [
        {
            "code": "GAC12_INDFBCF12",
            "label": "Indicador IPEA de FBCF - Índice Real",
            "category": "Macroeconomia",
        },
        {
            "code": "GAC12_INDFBCFDESSAZ12",
            "label": "Indicador IPEA de FBCF - Dessazonalizado",
            "category": "Macroeconomia",
        },
        {
            "code": "GAC12_INDFBCFCC12",
            "label": "Indicador IPEA de FBCF - Construção Civil",
            "category": "Macroeconomia",
        },
        {
            "code": "GAC12_INDFBCFCCDESSAZ12",
            "label": "Indicador IPEA de FBCF - Construção Dessazonalizado",
            "category": "Macroeconomia",
        },
    ],
    "ipea_comercio_exterior.csv": [
        {
            "code": "FUNCEX12_XPT12",
            "label": "Exportações - Preços - Índice",
            "category": "Macroeconomia",
        },
        {
            "code": "FUNCEX12_MDPT12",
            "label": "Importações - Preços - Índice",
            "category": "Macroeconomia",
        },
    ],
    "ipea_producao_mineral.csv": [
        {
            "code": "IBSIE12_QSCFG12",
            "label": "Mineral - Ferro-Gusa - Produção",
            "category": "Produção",
        },
        {
            "code": "IBSIE12_QSCAB12",
            "label": "Mineral - Aço Bruto - Produção",
            "category": "Produção",
        },
        {
            "code": "IBSIE12_QSCL12",
            "label": "Mineral - Laminados - Produção",
            "category": "Produção",
        },
    ],
    "ipea_calendario.csv": [
        {
            "code": "SGS12_NDIASUTEISFUT12",
            "label": "Número de Dias Úteis Futuros",
            "category": "Calendário",
        },
        {
            "code": "SGS12_NDIASUTEISPAS12",
            "label": "Número de Dias Úteis Passados",
            "category": "Calendário",
        },
    ],
}


# ── Definições dos indicadores ─────────────────────────────────────────

INDICATOR_DEFS = [
    # ── B3 DI Over ─────────────────────────────────────────────────
    {
        "dataset": "b3_bdi_di_over.csv",
        "source": "B3",
        "label": "DI Over (SELIC equivalente)",
        "value_col": "average",
        "date_col": "rpt_dt",
        "fmt": "pct",
    },
    {
        "dataset": "b3_bdi_di_over.csv",
        "source": "B3",
        "label": "DI Over — Volume financeiro",
        "value_col": "financial_volume",
        "date_col": "rpt_dt",
        "fmt": "number",
    },
    # ── B3 BMF Taxas de Juros ──────────────────────────────────────
    {
        "dataset": "b3_bmf_taxas_juros.csv",
        "source": "B3",
        "indicator_col": "curva",
        "value_col": "taxa",
        "date_col": "data_referencia",
        "fmt": "pct",
        "note_col": "prazo_dias",
        "category": "Taxas de Juros",
    },
    # ── B3 Indicadores Financeiros ─────────────────────────────────
    {
        "dataset": "b3_indicadores_financeiros.csv",
        "source": "B3",
        "indicator_col": "description",
        "value_col_main": "value",
        "value_col_fallback": "rate",
        "date_col": "last_update",
        "category": "Indicadores B3",
    },
    # ── B3 Taxa de Câmbio ──────────────────────────────────────────
    {
        "dataset": "b3_taxa_cambio_referencia.csv",
        "source": "B3",
        "indicator_col": "description",
        "value_col_main": "value",
        "value_col_fallback": "rate",
        "date_col": "lastupdate",
        "category": "Taxas de Câmbio",
    },
    # ── BCB PTAX ───────────────────────────────────────────────────
    {
        "dataset": "bcb_ptax.csv",
        "source": "BCB",
        "label": "PTAX USD — Compra",
        "value_col": "cotacao_compra",
        "date_col": "data_hora_cotacao",
        "category": "Taxas de Câmbio",
    },
    {
        "dataset": "bcb_ptax.csv",
        "source": "BCB",
        "label": "PTAX USD — Venda",
        "value_col": "cotacao_venda",
        "date_col": "data_hora_cotacao",
        "category": "Taxas de Câmbio",
    },
    # ── BCB SGS ────────────────────────────────────────────────────
    *[
        {
            "dataset": "bcb_sgs.csv",
            "source": "BCB",
            "label": nome,
            "value_col": "valor",
            "date_col": "data",
            "filter_col": "codigo_serie",
            "filter_val": codigo,
            "fmt": "pct",
            "category": "Séries SGS",
        }
        for codigo, nome in [
            ("11", "SELIC (% a.d.)"),
            ("1", "IGP-M"),
            ("189", "IGP-M (índice)"),
            ("190", "IGP-M 12m"),
            ("433", "IPCA 12m"),
        ]
    ],
    # ── ANBIMA Indicadores ─────────────────────────────────────────
    {
        "dataset": "anbima_indicadores.csv",
        "source": "ANBIMA",
        "indicator_col": "indicador",
        "value_col": "valor",
        "date_col": "data_referencia",
        "category_col": "categoria",
        "unit_col": "unidade",
    },
    # ── ANBIMA Títulos Públicos ───────────────────────────────────
    {
        "dataset": "anbima_titulos_publicos.csv",
        "source": "ANBIMA",
        "indicator_col": "codigo_selic",
        "value_cols": [
            ("tx_indicativa", "Taxa indicativa", "pct"),
            ("pu", "PU", "number"),
        ],
        "date_col": "data_referencia",
        "note_col": "titulo",
        "category": "Títulos Públicos",
    },
    # ── ANBIMA IMA-B ───────────────────────────────────────────────
    {
        "dataset": "anbima_indice_imab.csv",
        "source": "ANBIMA",
        "indicator_col": "indice",
        "value_cols": [
            ("numero_indice", "Número-índice", "number"),
            ("variacao_diaria", "Variação diária", "pct"),
            ("duration_du", "Duration (d.u.)", "number"),
        ],
        "date_col": "data_de_referencia",
        "category": "IMA-B",
    },
    # ── Yahoo Finance ──────────────────────────────────────────────
    *[
        {
            "dataset": filename + ".csv",
            "source": "Yahoo Finance",
            "label": ticker,
            "value_col": "preco_fechamento",
            "date_col": "data_referencia",
            "filter_col": "codigo_ativo",
            "filter_val": ticker,
            "category": category,
        }
        for category, filename in [
            ("Ações Brasileiras (B3)", "yahoo_acoes_brasileiras"),
            ("Ações Internacionais", "yahoo_acoes_internacionais"),
            ("Câmbio / Moedas", "yahoo_cambio_moedas"),
            ("Criptoativos", "yahoo_criptoativos"),
            ("Commodities Globais", "yahoo_commodities"),
            ("Índices de Ações Globais", "yahoo_indices_globais"),
            ("Renda Fixa & Treasuries", "yahoo_renda_fixa"),
            ("ETFs & Setoriais", "yahoo_etfs"),
            ("FIIs e Fiagros", "yahoo_fiis_fiagros"),
        ]
        for ticker in YAHOO_SECTIONS[category]
    ],
    # ── IPEADATA ───────────────────────────────────────────────────
    *[
        {
            "dataset": filename,
            "source": "IPEA",
            "label": item["label"],
            "value_col": "valor",
            "date_col": "data_referencia",
            "filter_col": "codigo_ativo",
            "filter_val": item["code"],
            "category": item["category"],
            **({"fmt": item["fmt"]} if "fmt" in item else {}),
        }
        for filename, items in IPEADATA_SECTIONS.items()
        for item in items
    ],
]


# ── Extratores ────────────────────────────────────────────────────────


def _build_base(idef: dict) -> dict:
    return {
        "dataset": idef["dataset"],
        "dataset_label": DATASET_LABEL.get(
            idef["dataset"], idef["dataset"].replace(".csv", "")
        ),
        "fonte": idef["source"],
        "categoria": idef.get("category", ""),
        "tipo": "indicador",
    }


def _fmt(idef: dict, raw_val: str) -> str:
    fmt = idef.get("fmt", "")
    if fmt == "pct":
        return _fmt_pct(raw_val)
    if fmt == "number":
        return _fmt_val(raw_val)
    f = _parse_br_float(raw_val)
    if f is not None:
        return _fmt_val(raw_val)
    return raw_val


def _ref_date(idef: dict, row: dict) -> str:
    date_col = idef["date_col"]
    d = _safe(row.get(date_col, ""))[:10]
    if d:
        return d
    return _safe(row.get("data_captura", ""))[:10]


def _extract_single_value(rows: list[dict], idef: dict) -> Optional[dict]:
    value_col = idef["value_col"]
    rows_sorted = _sorted_by(rows, idef["date_col"])
    if not rows_sorted:
        return None
    latest = rows_sorted[0]
    raw_val = _safe(latest.get(value_col, ""))
    if not raw_val:
        return None
    out = _build_base(idef)
    out["indicador"] = idef.get("label", "")
    out["valor"] = _fmt(idef, raw_val)
    out["unidade"] = idef.get("unit", "")
    out["data_referencia"] = _ref_date(idef, latest)
    out["captura_em"] = _safe(latest.get("data_captura", ""))[:10]
    out["metrica"] = value_col
    return out


def _extract_filtered_value(rows: list[dict], idef: dict) -> Optional[dict]:
    filtered = [
        r for r in rows if _safe(r.get(idef["filter_col"], "")) == idef["filter_val"]
    ]
    if not filtered:
        return None
    res = _extract_single_value(filtered, idef)
    if res and "filter_val" in idef:
        res["metrica"] = idef["filter_val"]
    return res


def _extract_grouped_value(rows: list[dict], idef: dict) -> list[dict]:
    indicator_col = idef["indicator_col"]
    value_col = idef["value_col"]
    category_col = idef.get("category_col", "")
    unit_col = idef.get("unit_col", "")

    groups: dict[str, list[dict]] = {}
    for r in rows:
        key = _safe(r.get(indicator_col, ""))
        if key:
            groups.setdefault(key, []).append(r)

    results = []
    for indicator_name, grp in sorted(groups.items()):
        grp_sorted = _sorted_by(grp, idef["date_col"])
        if not grp_sorted:
            continue
        latest = grp_sorted[0]
        raw_val = _safe(latest.get(value_col, ""))
        if not raw_val:
            continue
        out = _build_base(idef)
        out["indicador"] = indicator_name
        out["valor"] = _fmt(idef, raw_val)
        out["unidade"] = _safe(latest.get(unit_col, "")) if unit_col else ""
        out["categoria"] = (
            (_safe(latest.get(category_col, "")) or idef.get("category", ""))
            if category_col
            else idef.get("category", "")
        )
        out["data_referencia"] = _ref_date(idef, latest)
        out["captura_em"] = _safe(latest.get("data_captura", ""))[:10]
        out["metrica"] = value_col
        results.append(out)
    return results


def _extract_multi_value(rows: list[dict], idef: dict) -> list[dict]:
    indicator_col = idef.get("indicator_col", "")
    value_cols = idef["value_cols"]
    note_col = idef.get("note_col", "")

    if indicator_col:
        groups: dict[str, list[dict]] = {}
        for r in rows:
            key = _safe(r.get(indicator_col, ""))
            if key:
                groups.setdefault(key, []).append(r)
    else:
        groups = {"": rows}

    results = []
    for indicator_name, grp in groups.items():
        grp_sorted = _sorted_by(grp, idef["date_col"])
        if not grp_sorted:
            continue
        latest = grp_sorted[0]
        note = _safe(latest.get(note_col, "")) if note_col else ""
        label_base = indicator_name or idef.get("label", "")
        if note and indicator_name:
            label_base = f"{indicator_name} ({note})"

        for col_name, col_label, col_fmt in value_cols:
            raw_val = _safe(latest.get(col_name, ""))
            if not raw_val:
                continue
            out = _build_base(idef)
            out["indicador"] = label_base
            out["valor"] = _fmt_pct(raw_val) if col_fmt == "pct" else _fmt_val(raw_val)
            out["unidade"] = col_label
            out["data_referencia"] = _ref_date(idef, latest)
            out["captura_em"] = _safe(latest.get("data_captura", ""))[:10]
            out["metrica"] = col_name
            results.append(out)
    return results


def _extract_dual_value(rows: list[dict], idef: dict) -> list[dict]:
    indicator_col = idef.get("indicator_col", "")
    main_col = idef["value_col_main"]
    fallback_col = idef["value_col_fallback"]

    groups: dict[str, list[dict]] = {}
    for r in rows:
        key = _safe(r.get(indicator_col, ""))
        if key:
            groups.setdefault(key, []).append(r)

    results = []
    for indicator_name, grp in groups.items():
        grp_sorted = _sorted_by(grp, idef["date_col"])
        if not grp_sorted:
            continue
        latest = grp_sorted[0]
        raw_val = _safe(latest.get(main_col, ""))
        used_col = main_col
        if not raw_val:
            raw_val = _safe(latest.get(fallback_col, ""))
            used_col = fallback_col
        if not raw_val:
            continue
        out = _build_base(idef)
        out["indicador"] = indicator_name
        out["valor"] = _fmt(idef, raw_val)
        out["unidade"] = ""
        out["data_referencia"] = _ref_date(idef, latest)
        out["captura_em"] = _safe(latest.get("data_captura", ""))[:10]
        out["metrica"] = used_col
        results.append(out)
    return results


# ── Gerador principal ─────────────────────────────────────────────────


def generate(dry_run: bool = False) -> None:
    t0 = time.time()
    banner(
        "Consolidado",
        "Extrai último valor de cada indicador financeiro → consolidated.json/csv",
    )
    section("Processando indicadores", "chart")

    all_results: list[dict] = []
    total = len(INDICATOR_DEFS)

    for idx, idef in enumerate(INDICATOR_DEFS, 1):
        label = idef.get("label", idef.get("indicator_col", idef["dataset"]))
        print_start(f"[{idx}/{total}] {label} ({idef['dataset']})", icon="search")

        csv_path = DATA_DIR / idef["dataset"]
        if not csv_path.exists():
            print_warn(f"{idef['dataset']}: arquivo não encontrado")
            continue

        rows = _read_csv(str(csv_path))
        if not rows:
            print_warn(f"{idef['dataset']}: sem dados")
            continue

        if "value_cols" in idef:
            results = _extract_multi_value(rows, idef)

        elif "filter_col" in idef:
            result = _extract_filtered_value(rows, idef)
            results = [result] if result else []

        elif "indicator_col" in idef and "value_col_main" in idef:
            results = _extract_dual_value(rows, idef)

        elif "indicator_col" in idef:
            results = _extract_grouped_value(rows, idef)

        else:
            result = _extract_single_value(rows, idef)
            results = [result] if result else []

        all_results.extend(results)
        if results:
            print_done(f"{label} → {len(results)} indicador(es)")
        else:
            print_warn(f"{label}: sem dados")

    if not all_results:
        print_warn("Nenhum dado consolidado extraído.")
        return

    all_results.sort(key=lambda r: (r["fonte"], r["dataset"], r["indicador"]))

    if not dry_run:
        section("Escrevendo saída", "package")

        json_path = DATA_DIR / "consolidated.json"
        csv_path = DATA_DIR / "consolidated.csv"
        js_path = DATA_DIR / "consolidated.js"

        json_path.parent.mkdir(parents=True, exist_ok=True)

        json_path.write_text(
            json.dumps(all_results, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print_done(f"consolidated.json — {len(all_results)} registros")

        js_path.write_text(
            f"window.PULSEFLAT_CONSOLIDATED = {json.dumps(all_results, indent=2, ensure_ascii=False)};\n",
            encoding="utf-8",
        )
        print_done(f"consolidated.js — {len(all_results)} registros")

        fieldnames = [
            "dataset",
            "dataset_label",
            "fonte",
            "categoria",
            "tipo",
            "indicador",
            "valor",
            "unidade",
            "data_referencia",
            "captura_em",
            "metrica",
        ]
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        print_done(f"consolidated.csv — {len(all_results)} registros")

    else:
        print_info(f"Dry-run: {len(all_results)} registros seriam gerados.")

    elapsed = time.time() - t0
    print_summary(
        "Consolidado gerado",
        total=total,
        success=len(all_results),
        failed=0,
        elapsed=elapsed,
        details=[
            ("chart", "Indicadores", str(len(all_results))),
            ("info", "Fontes", str(len({r["fonte"] for r in all_results}))),
        ],
    )


# ── Pivoteamento (multivalor → colunas) ───────────────────────────────


def generate_pivoted() -> None:
    """Lê consolidated.json e gera consolidated_pivoted.json/js.
    Cada grupo (dataset_label, fonte, data_referencia, indicador) vira uma
    única linha. Se o grupo tiver 2+ registros com unidades diferentes,
    cada unidade vira uma coluna; caso contrário usa 'Valor'.
    """
    src = DATA_DIR / "consolidated.json"
    if not src.exists():
        return

    raw = json.loads(src.read_text(encoding="utf-8"))
    if not raw:
        return

    # First pass: group raw records
    buckets: dict[tuple, list[dict]] = defaultdict(list)
    for r in raw:
        key = (
            r.get("dataset_label", ""),
            r.get("fonte", ""),
            r.get("data_referencia", ""),
            r.get("indicador", ""),
        )
        buckets[key].append(r)

    pivoted: list[OrderedDict] = []
    all_metrics: set[str] = set()

    for key, recs in buckets.items():
        row = OrderedDict()
        for k in (
            "data_referencia",
            "indicador",
            "fonte",
            "dataset_label",
            "categoria",
        ):
            row[k] = recs[0].get(k, "")

        # Determine metric columns for this group
        units = list(OrderedDict.fromkeys(r.get("unidade", "") or "" for r in recs))
        non_empty = [u for u in units if u]

        if len(non_empty) >= 2:
            # Multi-metric group: use unit labels as columns
            for r in recs:
                metric = r.get("unidade", "") or ""
                row[metric] = r.get("valor", "")
                all_metrics.add(metric)
        else:
            # Single-metric group: use "Valor"
            row["Valor"] = recs[0].get("valor", "")
            all_metrics.add("Valor")

        pivoted.append(row)

    pivoted.sort(key=lambda x: (x.get("data_referencia", ""), x.get("indicador", "")))

    section("Escrevendo pivô", "package")

    json_path = DATA_DIR / "consolidated_pivoted.json"
    js_path = DATA_DIR / "consolidated_pivoted.js"

    json_path.write_text(
        json.dumps(pivoted, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print_done(f"consolidated_pivoted.json — {len(pivoted)} registros")

    js_path.write_text(
        f"window.PULSEFLAT_PIVOTED = {json.dumps(pivoted, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    print_done(f"consolidated_pivoted.js — {len(pivoted)} registros")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="📊 Gera dados consolidados (consolidated.json/csv/js) a partir dos CSVs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
exemplos:
  python scripts/consolidate.py
  python scripts/consolidate.py --dry-run
  python scripts/consolidate.py --quiet
        """,
    )
    add_common_args(parser)
    args = parser.parse_args()
    if args.dry_run:
        log.info("Modo dry-run: arquivos não serão salvos.")
    apply_common_args(args)
    generate(dry_run=args.dry_run)
    if not args.dry_run:
        generate_pivoted()
