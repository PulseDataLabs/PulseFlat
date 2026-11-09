
#!/usr/bin/env python
# coding: utf-8
"""
Scraper: BACEN – Conglomerados Financeiros
Fonte:   https://www.bcb.gov.br/content/estabilidadefinanceira/relacao_instituicoes_funcionamento/
Saída:   data/bacen_conglomerados.csv

Baixa o arquivo ZIP mensal (YYYYMMCONGLOMERADO.zip), extrai o XLSX
e retorna o conteúdo normalizado.
"""
import datetime
import os
import sys
import time
import zipfile
from io import BytesIO

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper
from scripts.utils.ux import print_done, print_warn

BASE_URL = (
    "https://www.bcb.gov.br/content/estabilidadefinanceira/"
    "relacao_instituicoes_funcionamento/Conglomerados/"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}


def _try_download(session: requests.Session, ref: datetime.date) -> tuple[bytes | None, str | None]:
    yyyymm = ref.strftime("%Y%m")
    mmyyyy = ref.strftime("%m%Y")
    candidates = [
        f"{mmyyyy}CONGLOMERADO.zip",  # Padrão recente adotado pelo BACEN (MMYYYY)
        f"{yyyymm}CONGLOMERADO.zip",  # Padrão histórico (YYYYMM)
        f"{mmyyyy}conglomerado.zip",
        f"{yyyymm}conglomerado.zip",
    ]
    for file_name in candidates:
        url = BASE_URL + file_name
        try:
            resp = session.get(url, headers=HEADERS, timeout=60)
            if resp.status_code == 200 and resp.content:
                return resp.content, file_name
        except Exception:
            continue
    return None, None


class BacenConglomeradosScraper(BaseScraper):
    name = "bacen_conglomerados"
    group = "bcb"
    enabled = True
    phase = 1
    badge = "Mensal"
    title = "BACEN — Conglomerados Financeiros e Prudenciais"
    description = "Quadro societário, composição patrimonial e demonstrações consolidadas dos Conglomerados Financeiros e Prudenciais regulados pelo Banco Central do Brasil."

    def fetch(self) -> pd.DataFrame:

        session = requests.Session()

        hoje = datetime.date.today()
        content = None
        target_ref = None
        for meses_atras in (1, 2, 3):
            ref = hoje - relativedelta(months=meses_atras)
            t0 = time.time()
            c, fname = _try_download(session, ref)
            if c:
                print_done(
                    f"encontrado {fname}", elapsed=time.time() - t0
                )
                content = c
                target_ref = ref
                break
            print_warn(
                f"conglomerado para {ref.strftime('%m/%Y')} não disponível", elapsed=time.time() - t0
            )
        if not content or target_ref is None:
            raise RuntimeError(
                "Nenhum arquivo de conglomerados disponível nos últimos 3 meses."
            )

        # Extrai XLSX do ZIP em memória
        with zipfile.ZipFile(BytesIO(content)) as zf:
            xlsx_names = [n for n in zf.namelist() if n.endswith(".xlsx")]
            if not xlsx_names:
                raise RuntimeError("Nenhum XLSX encontrado no arquivo ZIP.")
            xlsx_bytes = zf.read(xlsx_names[0])

        df_raw = pd.read_excel(BytesIO(xlsx_bytes), header=None, engine="openpyxl")
        header_idx = None
        for idx in range(min(25, len(df_raw))):
            row_vals = [
                str(x).strip().upper()
                for x in df_raw.iloc[idx].values
                if pd.notna(x) and str(x).strip()
            ]
            if (
                len(row_vals) >= 3
                and any("CONGLOMERADO" in v for v in row_vals)
                and any("CNPJ" in v or "PARTICIPANTE" in v for v in row_vals)
            ):
                header_idx = idx
                break

        if header_idx is not None:
            df = df_raw.iloc[header_idx + 1 :].copy()
            df.columns = [str(c).strip() for c in df_raw.iloc[header_idx].values]
        else:
            df = pd.read_excel(BytesIO(xlsx_bytes), engine="openpyxl")

        df = df.loc[:, ~df.columns.astype(str).str.contains(r"^Unnamed", case=False, na=False)]
        df = df.dropna(how="all", axis=1)
        df = df.dropna(how="all", axis=0)
        df.columns = [str(c).strip() for c in df.columns]
        df.insert(0, "data_referencia", target_ref.replace(day=1))
        return df


if __name__ == "__main__":
    scraper = BacenConglomeradosScraper()
    scraper.run()
