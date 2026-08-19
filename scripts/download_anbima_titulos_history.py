import datetime
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

# Adiciona o diretório raiz ao sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.base import get_logger, limpar, nova_session, salvar_csv

log = get_logger("download_anbima_titulos_history")

CABECALHO = [
    "data_captura",
    "titulo",
    "data_referencia",
    "codigo_selic",
    "data_base_emissao",
    "data_vencimento",
    "tx_compra",
    "tx_venda",
    "tx_indicativa",
    "pu",
    "desvio_padrao",
    "interv_ind_inf_d0",
    "interv_ind_sup_d0",
    "interv_ind_inf_dma1",
    "interv_ind_sup_dma1",
    "criterio",
]

COLUNAS = [
    "titulo",
    "data_referencia",
    "codigo_selic",
    "data_base_emissao",
    "data_vencimento",
    "tx_compra",
    "tx_venda",
    "tx_indicativa",
    "pu",
    "desvio_padrao",
    "interv_ind_inf_d0",
    "interv_ind_sup_d0",
    "interv_ind_inf_dma1",
    "interv_ind_sup_dma1",
    "criterio",
]


def fetch_date(date_obj):
    session = nova_session()
    yymmdd = date_obj.strftime("%y%m%d")
    url = f"https://www.anbima.com.br/informacoes/merc-sec/arqs/ms{yymmdd}.txt"
    date_str = date_obj.strftime("%Y-%m-%d")

    try:
        resp = session.get(url, timeout=20)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()

        # Detect encoding
        content = resp.content
        texto = None
        for enc in ("latin-1", "utf-8", "cp1252"):
            try:
                texto = content.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        if texto is None:
            texto = content.decode("utf-8", errors="replace")

        linhas = texto.splitlines()
        dados_linhas = [l for l in linhas[3:] if l.strip() and "@" in l]

        registros = []
        for l in dados_linhas:
            partes = l.split("@")
            if len(partes) < len(COLUNAS):
                partes += [""] * (len(COLUNAS) - len(partes))
            registro = {"data_captura": date_str}
            for col, val in zip(COLUNAS, partes):
                registro[col] = limpar(val.replace(",", "."))
            registros.append(registro)

        return registros
    except Exception as e:
        log.warning(f"Erro ao baixar/processar data {date_str}: {e}")
        return []


def run():
    log.info("=== ANBIMA — Títulos Públicos — Importador de Histórico ===")

    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date.today()

    # Gerar todas as datas de segunda a sexta no intervalo
    dates_to_fetch = []
    curr = start_date
    while curr <= end_date:
        if curr.weekday() < 5:  # Segunda a sexta
            dates_to_fetch.append(curr)
        curr += datetime.timedelta(days=1)

    log.info(
        f"Total de {len(dates_to_fetch)} dias de semana para buscar no histórico desde 2020."
    )

    all_records = []

    # Usar ThreadPoolExecutor para baixar em paralelo
    max_workers = 15
    log.info(f"Iniciando download com {max_workers} threads paralelos...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_date, d): d for d in dates_to_fetch}

        completed_count = 0
        total_count = len(dates_to_fetch)

        for future in as_completed(futures):
            date_val = futures[future]
            completed_count += 1
            res = future.result()
            if res:
                all_records.extend(res)
                if completed_count % 100 == 0 or completed_count == total_count:
                    log.info(
                        f"  Progresso: {completed_count}/{total_count} datas processadas. {len(all_records)} registros carregados."
                    )

    if not all_records:
        log.error("Nenhum histórico foi baixado com sucesso.")
        return

    log.info(f"Concatenando todos os {len(all_records)} registros...")
    df = pd.DataFrame(all_records)
    df = df.fillna("")

    # Padronização de datas e floats vectorizada
    def clean_series_vectorized(s: pd.Series) -> pd.Series:
        s_str = s.astype(str).str.strip()
        result = s_str.copy()

        # DD/MM/YYYY -> YYYY-MM-DD
        mask_date1 = s_str.str.match(r"^\d{2}/\d{2}/\d{4}$")
        if mask_date1.any():
            result.loc[mask_date1] = s_str.loc[mask_date1].str.replace(
                r"^(\d{2})/(\d{2})/(\d{4})$", r"\3-\2-\1", regex=True
            )

        # DD/MM/YY -> YYYY-MM-DD
        mask_date2 = s_str.str.match(r"^\d{2}/\d{2}/\d{2}$")
        if mask_date2.any():
            result.loc[mask_date2] = s_str.loc[mask_date2].str.replace(
                r"^(\d{2})/(\d{2})/(\d{2})$", r"20\3-\2-\1", regex=True
            )

        # YYYYMMDD -> YYYY-MM-DD
        mask_date3 = s_str.str.match(r"^\d{8}$")
        if mask_date3.any():
            result.loc[mask_date3] = s_str.loc[mask_date3].str.replace(
                r"^(\d{4})(\d{2})(\d{2})$", r"\1-\2-\3", regex=True
            )

        # Float
        mask_num = s_str.str.contains(r",") & (s_str.str.count(r",") == 1)
        if mask_num.any():
            s_num = s_str.loc[mask_num]
            clean_num = s_num.str.replace(r"[\.\%\-\+\s]", "", regex=True).str.replace(
                ",", "", regex=False
            )
            is_digit_mask = clean_num.str.isdigit()
            if is_digit_mask.any():
                valid_nums = s_num.loc[is_digit_mask]
                converted = valid_nums.str.replace(".", "", regex=False).str.replace(
                    ",", ".", regex=False
                )
                result.loc[valid_nums.index] = converted

        return result.fillna("").replace({"nan": "", "None": ""})

    for col in df.columns:
        if col == "data_captura":
            continue
        df[col] = clean_series_vectorized(df[col])

    output_file = ROOT_DIR / "data" / "anbima_titulos_publicos.csv"
    log.info(f"Salvando dados históricos no arquivo final: {output_file}...")
    salvar_csv(
        arquivo=output_file,
        registros=df,
        cabecalho=CABECALHO,
        chaves_dedup=["data_captura", "titulo", "data_vencimento"],
        acumular=False,
    )
    log.info("Histórico de títulos públicos finalizado com sucesso!")


if __name__ == "__main__":
    run()
