import sys
import time
import datetime
import calendar
import pandas as pd
from pathlib import Path

# Adiciona o diretório raiz ao sys.path para importar os módulos locais
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.base import salvar_csv, agora_brt, nova_session, get_logger
from utils.parsers import rows_from_zip, enriquecer

log = get_logger("download_bacen_negociacao_history")

def get_last_day_of_month(year, month):
    last_day = calendar.monthrange(year, month)[1]
    return datetime.date(year, month, last_day).strftime("%Y-%m-%d")

def run():
    log.info("=== BCB — Negociacao TPF Extra-grupo — Importador de Histórico ===")
    
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date.today()
    
    output_file = ROOT_DIR / "data" / "bacen_negociacao_tpf_extragrupo.csv.gz"
    session = nova_session()
    
    curr = start_date
    all_enriched = []
    
    while curr <= end_date:
        year_month = curr.strftime("%Y%m")
        url = f"https://www4.bcb.gov.br/pom/demab/negociacoes/download/NegE{year_month}.ZIP"
        
        last_day_str = get_last_day_of_month(curr.year, curr.month)
        
        log.info(f"Buscando dados de {curr.year}-{curr.month:02d} ({url})...")
        resp = None
        for tentativa in range(1, 4):
            try:
                resp = session.get(url, timeout=60)
                if resp.status_code == 404:
                    log.info(f"  [404] Arquivo para {year_month} não encontrado (pulando).")
                    resp = None
                    break
                resp.raise_for_status()
                break
            except Exception as e:
                log.warning(f"  Tentativa {tentativa}/3 falhou: {e}")
                if tentativa == 3:
                    log.error(f"  Falha definitiva para o período {year_month}.")
                    resp = None
                else:
                    time.sleep(5)
                    
        if resp and resp.content:
            try:
                rows = rows_from_zip(resp.content)
                if rows:
                    dataset_id = "bacen_negociacao_tpf_extragrupo"
                    enriched, _ = enriquecer(dataset_id, rows, data_captura_override=last_day_str)
                    all_enriched.extend(enriched)
                    log.info(f"  [OK] {len(enriched)} registros extraídos e enriquecidos.")
                else:
                    log.warning("  Nenhum registro encontrado no ZIP.")
            except Exception as e:
                log.error(f"  Erro ao processar arquivo de {year_month}: {e}")
                
        # Ir para o próximo mês
        if curr.month == 12:
            curr = datetime.date(curr.year + 1, 1, 1)
        else:
            curr = datetime.date(curr.year, curr.month + 1, 1)
            
        time.sleep(0.5) # Intervalo amigável de 500ms
        
    if not all_enriched:
        log.error("Nenhum histórico foi baixado com sucesso.")
        return
        
    log.info(f"Concatenando todos os {len(all_enriched)} registros históricos...")
    df_combined = pd.DataFrame(all_enriched)
    
    # Adicionar higienização e padronização semelhante ao BaseScraper.run
    df_combined = df_combined.fillna("")
    
    def clean_series_vectorized(s: pd.Series) -> pd.Series:
        s_str = s.astype(str).str.strip()
        result = s_str.copy()
        
        # DD/MM/YYYY -> YYYY-MM-DD
        mask_date1 = s_str.str.match(r'^\d{2}/\d{2}/\d{4}$')
        if mask_date1.any():
            result.loc[mask_date1] = s_str.loc[mask_date1].str.replace(
                r'^(\d{2})/(\d{2})/(\d{4})$', r'\3-\2-\1', regex=True
            )
            
        # DD/MM/YY -> YYYY-MM-DD
        mask_date2 = s_str.str.match(r'^\d{2}/\d{2}/\d{2}$')
        if mask_date2.any():
            result.loc[mask_date2] = s_str.loc[mask_date2].str.replace(
                r'^(\d{2})/(\d{2})/(\d{2})$', r'20\3-\2-\1', regex=True
            )
            
        # Números brasileiros
        mask_num = s_str.str.contains(r',') & (s_str.str.count(r',') == 1)
        if mask_num.any():
            s_num = s_str.loc[mask_num]
            clean_num = s_num.str.replace(r'[\.\%\-\+\s]', '', regex=True).str.replace(',', '', regex=False)
            is_digit_mask = clean_num.str.isdigit()
            if is_digit_mask.any():
                valid_nums = s_num.loc[is_digit_mask]
                converted = valid_nums.str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
                result.loc[valid_nums.index] = converted
                
        return result.fillna("").replace({"nan": "", "None": ""})

    for col in df_combined.columns:
        if col in ("data_captura", "conjunto", "arquivo_origem", "registro_hash"):
            continue
        df_combined[col] = clean_series_vectorized(df_combined[col])
        
    cabecalho = list(df_combined.columns)
    chaves_dedup = ["data_captura", "conjunto", "registro_hash"]
    
    log.info(f"Salvando dados históricos no arquivo final: {output_file}...")
    salvar_csv(
        arquivo=output_file,
        registros=df_combined,
        cabecalho=cabecalho,
        chaves_dedup=chaves_dedup,
        acumular=False
    )
    log.info("Histórico de TPF extra-grupo finalizado com sucesso!")

if __name__ == "__main__":
    run()
