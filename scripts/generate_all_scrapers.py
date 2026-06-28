#!/usr/bin/env python
# coding: utf-8
"""
scripts/generate_all_scrapers.py
---------------------------------
Gera programaticamente os 16 novos scrapers divididos por categorias (8 Yahoo, 8 Ipea)
e remove os arquivos antigos de scrapers e dados individuais de forma limpa.
"""

import os
import stat
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRAPERS_DIR = ROOT / "scrapers"
DATA_DIR = ROOT / "data"

YAHOO_SECTIONS = {
    "yahoo_acoes_brasileiras": {
        "title": "Ações Brasileiras",
        "class_name": "YahooAcoesBrasileirasScraper",
        "dynamic_csv": "b3_carteiras_teoricas.csv",
        "dynamic_suffix": ".SA",
    },
    "yahoo_acoes_internacionais": {
        "title": "Ações Internacionais",
        "class_name": "YahooAcoesInternacionaisScraper",
        "dynamic_csv": "wikipedia_global_indices.csv",
        "dynamic_suffix": "",
    },
    "yahoo_cambio_moedas": {
        "title": "Câmbio e Moedas",
        "class_name": "YahooCambioMoedasScraper",
    },
    "yahoo_criptoativos": {
        "title": "Criptoativos",
        "class_name": "YahooCriptoativosScraper",
    },
    "yahoo_commodities": {
        "title": "Commodities Globais",
        "class_name": "YahooCommoditiesScraper",
    },
    "yahoo_indices_globais": {
        "title": "Índices de Ações Globais",
        "class_name": "YahooIndicesGlobaisScraper",
    },
    "yahoo_renda_fixa": {
        "title": "Renda Fixa & Treasuries",
        "class_name": "YahooRendaFixaScraper",
    },
    "yahoo_etfs": {
        "title": "ETFs Globais e Setoriais",
        "class_name": "YahooEtfsScraper",
        "dynamic_csv": "b3_fundos_listados.csv",
        "dynamic_filters": ["ETF Renda Variável", "ETF Renda Fixa"],
        "dynamic_suffix": ".SA",
    },
    "yahoo_fiis_fiagros": {
        "title": "FIIs e Fiagros B3",
        "class_name": "YahooFiisFiagrosScraper",
        "dynamic_csv": "b3_fundos_listados.csv",
        "dynamic_filters": ["FII", "FIAGRO"],
        "dynamic_suffix": ".SA",
    }
}

IPEADATA_SECTIONS = {
    "ipea_macroeconomia": {
        "title": "Macroeconomia Geral",
        "class_name": "IpeaMacroeconomiaScraper",
        "series": [
            {"code": "BM12_PIBAC12", "title": "PIB Acumulado 12m", "desc": "PIB acumulado em 12 meses (R$)", "icon": "📈", "tags": ["pib", "macroeconomia", "ipea"]},
            {"code": "PNADC12_TDESOC12", "title": "Taxa de Desocupação", "desc": "Taxa de desocupação da PNAD Contínua (%)", "icon": "👥", "tags": ["desemprego", "trabalho", "ipea"]},
            {"code": "GAC12_SALMINRE12", "title": "Salário Mínimo Real", "desc": "Salário mínimo real mensal (em R$ do último mês)", "icon": "💰", "tags": ["salario_minimo", "renda", "ipea"]},
            {"code": "MTE12_SALMIN12", "title": "Salário Mínimo Vigente", "desc": "Salário mínimo vigente nominal (R$)", "icon": "💰", "tags": ["salario_minimo", "renda", "ipea"]},
            {"code": "SGS12_7836", "title": "Saldo da Poupança", "desc": "Saldo total de depósitos em poupança SBPE e rural (R$ milhões)", "icon": "🏦", "tags": ["poupanca", "saldo", "ipea"]}
        ]
    },
    "ipea_mercados_diarios": {
        "title": "Mercados Globais Diários",
        "class_name": "IpeaMercadosDiariosScraper",
        "series": [
            {"code": "EIA366_PBRENT366", "title": "Petróleo Brent", "desc": "Preço do petróleo bruto Brent (FOB, US$)", "icon": "🛢", "tags": ["petroleo", "brent", "commodities", "ipea"]},
            {"code": "EIA366_PWTI366", "title": "Petróleo WTI", "desc": "Preço do petróleo bruto WTI (FOB, US$)", "icon": "🛢", "tags": ["petroleo", "wti", "commodities", "ipea"]},
            {"code": "GM366_DOW366", "title": "Índice Dow Jones", "desc": "Índice de ações Dow Jones (fechamento)", "icon": "📈", "tags": ["dow_jones", "acoes", "ipea"]},
            {"code": "SGS366_NASDAQ366", "title": "Índice NASDAQ", "desc": "Índice de ações NASDAQ (fechamento)", "icon": "📈", "tags": ["nasdaq", "acoes", "ipea"]}
        ]
    },
    "ipea_taxas_juros": {
        "title": "Taxas de Juros",
        "class_name": "IpeaTaxasJurosScraper",
        "series": [
            {"code": "ANBIMA12_TJPOUP12", "title": "Poupança Rentabilidade Antiga", "desc": "Rentabilidade mensal da poupança para depósitos até 03/05/2012 (% a.m.)", "icon": "💵", "tags": ["juros", "poupanca", "ipea"]},
            {"code": "BM12_RNDPO12", "title": "Poupança Rentabilidade Nova", "desc": "Rentabilidade mensal da poupança para depósitos a partir de 04/05/2012 (% a.m.)", "icon": "💵", "tags": ["juros", "poupanca", "ipea"]},
            {"code": "ANBIMA12_TJTLN112", "title": "Taxa LTN 1m", "desc": "Taxa de juros prefixada - estrutura a termo - LTN - 1 mês (% a.m.)", "icon": "🏛", "tags": ["juros", "ltn", "ipea"]},
            {"code": "ANBIMA12_TJTLN312", "title": "Taxa LTN 3m", "desc": "Taxa de juros prefixada - estrutura a termo - LTN - 3 meses (% a.m.)", "icon": "🏛", "tags": ["juros", "ltn", "ipea"]},
            {"code": "ANBIMA12_TJTLN612", "title": "Taxa LTN 6m", "desc": "Taxa de juros prefixada - estrutura a termo - LTN - 6 meses (% a.m.)", "icon": "🏛", "tags": ["juros", "ltn", "ipea"]},
            {"code": "ANBIMA12_TJTLN1212", "title": "Taxa LTN 12m", "desc": "Taxa de juros prefixada - estrutura a termo - LTN - 12 meses (% a.m.)", "icon": "🏛", "tags": ["juros", "ltn", "ipea"]},
            {"code": "BM12_TJCDI12", "title": "Taxa CDI Mensal", "desc": "Taxa de juros - CDI / Over - acumulada no mês (% a.m.)", "icon": "📊", "tags": ["juros", "cdi", "ipea"]},
            {"code": "BM12_TJLP12", "title": "Taxa TJLP", "desc": "Taxa de Juros de Longo Prazo (TJLP) (% a.m.)", "icon": "🏭", "tags": ["juros", "tjlp", "ipea"]},
            {"code": "BM12_TJOVER12", "title": "Taxa Selic Mensal", "desc": "Taxa de juros - Over / Selic - acumulada no mês (% a.m.)", "icon": "💰", "tags": ["juros", "selic", "ipea"]},
            {"code": "BM12_TJTBF12", "title": "Taxa TBF", "desc": "Taxa Básica Financeira (TBF) - 1º dia do mês (% a.m.)", "icon": "📈", "tags": ["juros", "tbf", "ipea"]},
            {"code": "BM12_TJTR12", "title": "Taxa TR", "desc": "Taxa Referencial (TR) - 1º dia do mês (% a.m.)", "icon": "🏠", "tags": ["juros", "tr", "ipea"]}
        ]
    },
    "ipea_precos_inflacao": {
        "title": "Preços e Inflação",
        "class_name": "IpeaPrecosInflacaoScraper",
        "series": [
            {"code": "IGP12_IGPDI12", "title": "IGP-DI Índice Geral", "desc": "Índice Geral de Preços - Disponibilidade Interna (IGP-DI) - índice (ago 1994 = 100)", "icon": "📊", "tags": ["igp_di", "inflacao", "ipea"]},
            {"code": "IGP12_INCC12", "title": "INCC-DI Índice Geral", "desc": "Índice Nacional de Custo da Construção - Disponibilidade Interna (INCC-DI) - índice (ago 1994 = 100)", "icon": "🏗", "tags": ["incc_di", "construcao", "ipea"]},
            {"code": "PRECOS12_INPC12", "title": "INPC Índice Geral", "desc": "Índice Nacional de Preços ao Consumidor (INPC) - geral - índice (dez 1993 = 100)", "icon": "📊", "tags": ["inpc", "inflacao", "ipea"]},
            {"code": "PRECOS12_INPCBR12", "title": "INPC Taxa de Variação", "desc": "Índice Nacional de Preços ao Consumidor (INPC) - geral - taxa de variação (% a.m.)", "icon": "📈", "tags": ["inpc", "inflacao", "ipea"]}
        ]
    },
    "ipea_fbcf": {
        "title": "Investimento FBCF",
        "class_name": "IpeaFbcfScraper",
        "series": [
            {"code": "GAC12_INDFBCF12", "title": "Indicador FBCF Índice Real", "desc": "Indicador IPEA de FBCF - índice real (média 1995 = 100)", "icon": "🏗", "tags": ["fbcf", "investimento", "ipea"]},
            {"code": "GAC12_INDFBCFDESSAZ12", "title": "Indicador FBCF Dessazonalizado", "desc": "Indicador IPEA de FBCF - índice real dessazonalizado (média 1995 = 100)", "icon": "🏗", "tags": ["fbcf", "investimento", "ipea"]},
            {"code": "GAC12_INDFBCFCC12", "title": "Indicador FBCF Construção Civil", "desc": "Indicador IPEA de FBCF - construção civil - índice real (média 1995 = 100)", "icon": "🏗", "tags": ["fbcf", "construcao", "ipea"]},
            {"code": "GAC12_INDFBCFCCDESSAZ12", "title": "Indicador FBCF Construção Dessazonalizado", "desc": "Indicador IPEA de FBCF - construção civil - índice real dessazonalizado (média 1995 = 100)", "icon": "🏗", "tags": ["fbcf", "construcao", "ipea"]}
        ]
    },
    "ipea_comercio_exterior": {
        "title": "Comércio Exterior",
        "class_name": "IpeaComercioExteriorScraper",
        "series": [
            {"code": "FUNCEX12_XPT12", "title": "Exportações Preços Índice", "desc": "Índice de preços das exportações gerais (média 2018 = 100)", "icon": "🚢", "tags": ["exportacao", "precos", "ipea"]},
            {"code": "FUNCEX12_MDPT12", "title": "Importações Preços Índice", "desc": "Índice de preços das importações gerais (média 2018 = 100)", "icon": "🚢", "tags": ["importacao", "precos", "ipea"]}
        ]
    },
    "ipea_producao_mineral": {
        "title": "Produção Transformação Mineral",
        "class_name": "IpeaProducaoMineralScraper",
        "series": [
            {"code": "IBSIE12_QSCFG12", "title": "Produção de Ferro-Gusa", "desc": "Produção mensal de ferro-gusa (em toneladas)", "icon": "🧱", "tags": ["ferro_gusa", "producao", "ipea"]},
            {"code": "IBSIE12_QSCAB12", "title": "Produção de Aço Bruto", "desc": "Produção mensal de aço bruto (em toneladas)", "icon": "🧱", "tags": ["aco_bruto", "producao", "ipea"]},
            {"code": "IBSIE12_QSCL12", "title": "Produção de Laminados", "desc": "Produção mensal de laminados (em toneladas)", "icon": "🧱", "tags": ["laminados", "producao", "ipea"]}
        ]
    },
    "ipea_calendario": {
        "title": "Calendário e Dias Úteis",
        "class_name": "IpeaCalendarioScraper",
        "series": [
            {"code": "SGS12_NDIASUTEISFUT12", "title": "Dias Úteis Futuros", "desc": "Número de dias úteis futuros estimados mensalmente", "icon": "📆", "tags": ["dias_uteis", "calendario", "ipea"]},
            {"code": "SGS12_NDIASUTEISPAS12", "title": "Dias Úteis Passados", "desc": "Número de dias úteis passados no mês correspondente", "icon": "📅", "tags": ["dias_uteis", "calendario", "ipea"]}
        ]
    }
}

TEMPLATE_YAHOO = """# coding: utf-8
\"\"\"
Scraper: Yahoo Finance – {title}
Fonte:   https://finance.yahoo.com
Saída:   data/{name}.csv
\"\"\"

import os
import sys
import time
import datetime
import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper

DYNAMIC_CSV = "{dynamic_csv}"
DYNAMIC_FILTERS = {dynamic_filters}
DYNAMIC_SUFFIX = "{dynamic_suffix}"
YAHOO_HEADERS = {{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
    "Referer": "https://finance.yahoo.com/",
    "Origin": "https://finance.yahoo.com",
}}
API_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{{ticker}}"
DAYS_BACK = 30


def _fetch_ticker(session: requests.Session, ticker: str, label: str, dt_ini: int, dt_fim: int) -> pd.DataFrame:
    url = API_URL.format(ticker=ticker)
    params = {{
        "period1": dt_ini,
        "period2": dt_fim,
        "interval": "1d",
        "events": "history",
        "includeAdjustedClose": "true",
    }}
    resp = session.get(url, params=params, headers=YAHOO_HEADERS, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    result = data.get("chart", {{}}).get("result", [])
    if not result:
        return pd.DataFrame()

    timestamps = result[0].get("timestamp", [])
    closes = result[0].get("indicators", {{}}).get("quote", [{{}}])[0].get("close", [])

    df = pd.DataFrame({{"timestamp": timestamps, "close": closes}})
    df["data_referencia"] = pd.to_datetime(df["timestamp"], unit="s").dt.normalize().dt.date
    df["codigo_ativo"] = ticker
    df["label"] = label
    df["preco_fechamento"] = pd.to_numeric(df["close"], errors="coerce")
    df["preco_fechamento"] = df["preco_fechamento"].ffill()

    return df[["data_referencia", "codigo_ativo", "label", "preco_fechamento"]]


class {class_name}(BaseScraper):
    name = "{name}"
    group = "misc"
    enabled = True
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    def fetch(self) -> pd.DataFrame:
        from pathlib import Path

        dt_ini_date = self.start_date
        dt_fim_date = self.end_date

        if dt_ini_date is None:
            hoje = datetime.date.today()
            dt_ini_date = hoje - datetime.timedelta(days=DAYS_BACK)
        if dt_fim_date is None:
            dt_fim_date = datetime.date.today()

        dt_fim = int(datetime.datetime.combine(dt_fim_date, datetime.time()).timestamp())
        dt_ini = int(datetime.datetime.combine(dt_ini_date, datetime.time()).timestamp())

        # Resolve tickers list
        tickers_list = []
        root_dir = Path(__file__).resolve().parents[1]
        custom_csv = root_dir / "data" / "custom_tickers.csv"
        if custom_csv.exists():
            try:
                df_custom = pd.read_csv(custom_csv)
                df_filtered = df_custom[df_custom["category"] == "{name}"]
                for _, row in df_filtered.iterrows():
                    tickers_list.append((str(row["ticker"]).strip(), str(row["label"]).strip()))
            except Exception as e:
                self.logger.warning(f"Erro ao carregar custom_tickers.csv: {{e}}")

        if DYNAMIC_CSV:
            csv_path = root_dir / "data" / DYNAMIC_CSV
            if csv_path.exists():
                try:
                    df_b3 = pd.read_csv(csv_path)
                    if DYNAMIC_FILTERS and "tipo_fundo" in df_b3.columns:
                        df_b3 = df_b3[df_b3["tipo_fundo"].isin(DYNAMIC_FILTERS)]
                    col = "codigo_fundo" if "codigo_fundo" in df_b3.columns else "codigo_ativo"
                    if col in df_b3.columns:
                        codes = df_b3[col].dropna().unique()
                        for code in codes:
                            code_str = str(code).strip()
                            if code_str:
                                ticker_yahoo = f"{{code_str}}{{DYNAMIC_SUFFIX}}" if DYNAMIC_SUFFIX else code_str
                                tickers_list.append((ticker_yahoo, code_str))
                except Exception as e:
                    self.logger.warning(f"Erro ao carregar B3 tickers dinâmicos: {{e}}")

        # Deduplicate tickers_list based on first element (ticker)
        seen = set()
        dedup_tickers = []
        for t, l in tickers_list:
            if t not in seen:
                seen.add(t)
                dedup_tickers.append((t, l))

        session = requests.Session()
        frames = []

        for i, (ticker, label) in enumerate(dedup_tickers, 1):
            try:
                df = _fetch_ticker(session, ticker, label, dt_ini, dt_fim)
                if not df.empty:
                    frames.append(df)
            except Exception:
                pass

        session.close()

        if not frames:
            raise RuntimeError("Nenhuma série baixada do Yahoo Finance.")

        return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    {class_name}().run()
"""

TEMPLATE_IPEA = """# coding: utf-8
\"\"\"
Scraper: IPEADATA – {title}
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/{name}.csv
\"\"\"

import os
import sys
import datetime
import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper

SERIES = {series}
API_URL = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{{code}}')"


class {class_name}(BaseScraper):
    name = "{name}"
    group = "misc"
    enabled = True
    phase = 1
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    def fetch(self) -> pd.DataFrame:
        session = self.get_session()
        frames = []

        for item in SERIES:
            url = API_URL.format(code=item["code"])
            resp = session.get(url, timeout=60)
            resp.raise_for_status()
            data = resp.json()

            values = data.get("value", [])
            if not values:
                continue

            records = []
            for val_item in values:
                raw_date = val_item.get("VALDATA", "")
                if "T" in raw_date:
                    date_ref = raw_date.split("T")[0]
                else:
                    date_ref = raw_date[:10]

                val = val_item.get("VALVALOR")
                if val is None:
                    continue

                records.append({{
                    "data_referencia": date_ref,
                    "codigo_ativo": item["code"],
                    "label": item["title"],
                    "valor": float(val),
                }})
            
            if records:
                frames.append(pd.DataFrame(records))

        session.close()

        if not frames:
            raise RuntimeError("Nenhum dado retornado para as séries do Ipea.")

        df = pd.concat(frames, ignore_index=True)

        # Filtros de data em memória se target_date ou start/end_date estiverem definidos
        if self.target_date:
            target_str = self.target_date.strftime("%Y-%m-%d")
            df = df[df["data_referencia"] == target_str]
        elif self.start_date or self.end_date:
            if self.start_date:
                df = df[df["data_referencia"] >= self.start_date.strftime("%Y-%m-%d")]
            if self.end_date:
                df = df[df["data_referencia"] <= self.end_date.strftime("%Y-%m-%d")]

        return df


if __name__ == "__main__":
    {class_name}().run()
"""

def clean_old():
    # Remove scrapers antigos do Yahoo
    old_files = [str(SCRAPERS_DIR / "yahoo_finance_series.py")]
    for f in old_files:
        try:
            if os.path.exists(f):
                os.remove(f)
                print(f"Removido scraper antigo: {Path(f).name}")
        except Exception:
            pass

    # Remove CSVs antigos do Yahoo
    old_csvs = [str(DATA_DIR / "yahoo_finance_series.csv")]
    for f in old_csvs:
        try:
            if os.path.exists(f):
                os.remove(f)
                print(f"Removido CSV antigo: {Path(f).name}")
        except Exception:
            pass

def generate():
    clean_old()

    # Gera Yahoo
    for name, item in YAHOO_SECTIONS.items():
        file_path = SCRAPERS_DIR / f"{name}.py"
        content = TEMPLATE_YAHOO.format(
            title=item["title"],
            name=name,
            class_name=item["class_name"],
            dynamic_csv=item.get("dynamic_csv", ""),
            dynamic_filters=str(item.get("dynamic_filters", None)),
            dynamic_suffix=item.get("dynamic_suffix", ""),
        )
        file_path.write_text(content, encoding="utf-8")
        file_path.chmod(file_path.stat().st_mode | stat.S_IEXEC)
        print(f"Gerado scraper Yahoo: {file_path.name}")

    # Gera Ipea
    for name, item in IPEADATA_SECTIONS.items():
        file_path = SCRAPERS_DIR / f"{name}.py"
        content = TEMPLATE_IPEA.format(
            title=item["title"],
            name=name,
            class_name=item["class_name"],
            series=str(item["series"]),
        )
        file_path.write_text(content, encoding="utf-8")
        file_path.chmod(file_path.stat().st_mode | stat.S_IEXEC)
        print(f"Gerado scraper Ipea: {file_path.name}")

if __name__ == "__main__":
    generate()
