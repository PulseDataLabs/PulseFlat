import sys
import time
import datetime
import calendar
import pandas as pd
from pathlib import Path
import io
import csv

# Adiciona o diretório raiz ao sys.path para importar os módulos locais
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.base import salvar_csv, agora_brt, nova_session
from utils.parsers import csv_rows, enriquecer, decode_bytes

def clean_csv_text(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ""
    
    idx = 0
    for i, line in enumerate(lines[:10]):
        num_delimiters = sum(line.count(d) for d in (";", ",", "\t", "|"))
        if num_delimiters >= 4:
            idx = i
            break
    else:
        idx = 0
    
    if idx > 0:
        return "\n".join(lines[idx:])
    return "\n".join(lines)

def get_last_day_of_month(year, month):
    last_day = calendar.monthrange(year, month)[1]
    return datetime.date(year, month, last_day)

def run():
    print("=== DEBÊNTURES MERCADO SECUNDÁRIO - Importador de Histórico ===")
    
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date.today()
    
    output_file = ROOT_DIR / "data" / "debentures_mercado_secundario_precos_negociacao.csv.gz"
    session = nova_session()
    
    data_captura, _ = agora_brt()
    
    curr = start_date
    dfs = []
    
    column_mapping = {
        "data": "data_referencia",
        "codigo_do_ativo": "codigo_ativo"
    }
    
    while curr <= end_date:
        dt_ini = curr.strftime("%Y%m%0d")
        # Último dia do mês ou hoje se for o mês corrente
        last_day = get_last_day_of_month(curr.year, curr.month)
        if last_day > end_date:
            last_day = end_date
            
        dt_fim = last_day.strftime("%Y%m%0d")
        
        print(f"Buscando de {curr} até {last_day}...")
        url = f"https://www.debentures.com.br/exploreosnd/consultaadados/mercadosecundario/precosdenegociacao_e.asp?op_exc=Nada&emissor=&isin=&ativo=&dt_ini={dt_ini}&dt_fim={dt_fim}"
        
        for tentativa in range(1, 4):
            try:
                resp = session.get(url, timeout=60)
                resp.raise_for_status()
                break
            except Exception as e:
                print(f"  Tentativa {tentativa}/3 falhou: {e}")
                if tentativa == 3:
                    print("  Falha definitiva para este período.")
                    resp = None
                else:
                    time.sleep(5)
        
        if resp and resp.content:
            try:
                decoded_text = decode_bytes(resp.content)
                decoded_text = clean_csv_text(decoded_text)
                rows = csv_rows(decoded_text)
                
                if rows:
                    # Aplicar mapeamento de colunas
                    mapped_rows = []
                    for r in rows:
                        new_r = {}
                        is_valid = True
                        for k, v in r.items():
                            new_key = column_mapping.get(k, k)
                            val = v
                            if new_key == "data_referencia":
                                if not val:
                                    is_valid = False
                                    break
                                val_strip = val.strip()
                                parsed_date = None
                                for fmt in ("%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d"):
                                    try:
                                        parsed_date = datetime.datetime.strptime(val_strip, fmt).strftime("%Y-%m-%d")
                                        break
                                    except ValueError:
                                        continue
                                if not parsed_date:
                                    is_valid = False
                                    break
                                val = parsed_date
                            new_r[new_key] = val
                        if is_valid:
                            mapped_rows.append(new_r)
                    
                    dataset_id = "debêntures___preços_de_negociação"
                    enriched, _ = enriquecer(dataset_id, mapped_rows, data_captura_override=data_captura)
                    
                    df_periodo = pd.DataFrame(enriched)
                    if not df_periodo.empty:
                        dfs.append(df_periodo)
                        print(f"  Sucesso: {len(df_periodo)} registros capturados.")
                else:
                    print("  Nenhum registro encontrado no CSV.")
            except Exception as e:
                print(f"  Erro ao processar dados deste período: {e}")
        else:
            print("  Resposta vazia.")
            
        # Ir para o próximo mês
        if curr.month == 12:
            curr = datetime.date(curr.year + 1, 1, 1)
        else:
            curr = datetime.date(curr.year, curr.month + 1, 1)
            
        time.sleep(1) # Intervalo amigável de 1 segundo
        
    if not dfs:
        print("Nenhum histórico foi baixado com sucesso.")
        return
        
    print("\nConcatenando todos os períodos...")
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df = combined_df.fillna("")
    
    # Colunas no cabeçalho do arquivo original (na mesma ordem do arquivo atual)
    cabecalho = [
        "data_referencia", "emissor", "codigo_ativo", "isin", "quantidade", 
        "numero_de_negocios", "pu_minimo", "pu_medio", "pu_maximo", 
        "pu_da_curva", "data_captura", "conjunto", "arquivo_origem", "registro_hash"
    ]
    
    chaves_dedup = ["data_referencia", "codigo_ativo", "isin"]
    
    # Garante que as colunas existem
    for col in cabecalho:
        if col not in combined_df.columns:
            combined_df[col] = ""
            
    print(f"\nSalvando/Concatenando {len(combined_df)} registros no arquivo de destino: {output_file}...")
    
    salvar_csv(
        arquivo=output_file,
        registros=combined_df[cabecalho],
        cabecalho=cabecalho,
        chaves_dedup=chaves_dedup,
        acumular=True
    )
    
    print("\nImportação de histórico finalizada com sucesso!")

if __name__ == "__main__":
    run()
