import os
import sys
import datetime
import calendar
import pandas as pd
import requests
from io import StringIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import salvar_csv, agora_brt

BASE_URL = "https://databricks-reports.anbima.com.br/fliq"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}

from pathlib import Path
output_file = Path("data/anbima_matriz_probabilidade_resgate.csv")

def get_last_day_of_month(year, month):
    last_day = calendar.monthrange(year, month)[1]
    return datetime.date(year, month, last_day)

def run():
    print("=== ANBIMA FLIQ - Matriz de Resgate - Importador de Histórico ===")
    
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date.today()
    
    data_captura, _ = agora_brt()
    
    curr = start_date
    dfs = []
    
    while curr <= end_date:
        ym_str = curr.strftime("%Y%m")
        file_name = f"report_fliq_{ym_str}.csv"
        url = f"{BASE_URL}/{file_name}"
        
        # Obter data de referência do último dia do mês
        data_ref = get_last_day_of_month(curr.year, curr.month)
        
        print(f"Downloading {file_name}...")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=60)
            if resp.status_code == 200 and "NoSuchKey" not in resp.text:
                df = pd.read_csv(StringIO(resp.text), sep=",", encoding="utf-8")
                df.insert(0, "data_referencia", data_ref.strftime("%Y-%m-%d"))
                df.insert(0, "data_captura", data_captura)
                
                # Garantir coluna data mesmo vazia
                if 'data' not in df.columns:
                    df['data'] = ""
                
                dfs.append(df)
                print(f"  Sucesso: {len(df)} registros")
            else:
                print(f"  Não encontrado: {ym_str}")
        except Exception as e:
            print(f"  Erro ao baixar {ym_str}: {e}")
            
        # Ir para o próximo mês
        if curr.month == 12:
            curr = datetime.date(curr.year + 1, 1, 1)
        else:
            curr = datetime.date(curr.year, curr.month + 1, 1)
            
    if not dfs:
        print("Nenhum histórico foi baixado.")
        return
        
    print("\nConcatenando todos os meses...")
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Tratar valores vazios
    combined_df = combined_df.fillna("")
    
    # Limpeza básica de strings
    for col in combined_df.columns:
        if col not in ["data_captura", "data_referencia", "valor", "prazo"]:
            combined_df[col] = combined_df[col].astype(str).str.strip()
            
    print(f"\nSalvando base consolidada: {len(combined_df)} registros em {output_file}...")
    
    cabecalho = [
        "data_captura", "data_referencia", "periodo", "classe", 
        "segmento_investidor", "tipo_metodologia", "metrica", "prazo", "valor", "data"
    ]
    
    chaves_dedup = ["data_referencia", "classe", "segmento_investidor", "tipo_metodologia", "metrica", "prazo"]
    
    salvar_csv(
        arquivo=output_file,
        registros=combined_df[cabecalho],
        cabecalho=cabecalho,
        chaves_dedup=chaves_dedup,
        acumular=True
    )
    
    print("\nHistórico importado com sucesso!")

if __name__ == "__main__":
    run()
