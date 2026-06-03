import csv
from pathlib import Path

def _limpar_int(valor) -> str:
    if valor is None:
        return ""
    texto = str(valor).strip()
    clean = texto.replace(".", "").replace(" ", "")
    if "," in clean:
        clean = clean.split(",")[0]
    return clean

def _limpar_float(valor) -> str:
    if valor is None:
        return ""
    texto = str(valor).strip()
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    return texto.replace("%", "").strip()

def process_file(file_path: Path):
    if not file_path.exists():
        print(f"File {file_path} does not exist.")
        return
    
    print(f"Processing {file_path}...")
    
    # Read existing rows
    rows = []
    headers = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            # Clean values
            if "quantidade_teorica" in row:
                row["quantidade_teorica"] = _limpar_int(row["quantidade_teorica"])
            if "participacao_pct" in row:
                row["participacao_pct"] = _limpar_float(row["participacao_pct"])
            if "reducao_capital" in row:
                row["reducao_capital"] = _limpar_float(row["reducao_capital"])
            rows.append(row)
            
    # Write back clean rows
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Finished processing {file_path}. Cleaned {len(rows)} rows.")

def main():
    data_dir = Path(__file__).resolve().parents[1] / "data"
    
    # Clean main compiled portfolios CSV
    compiled_file = data_dir / "b3_carteiras_teoricas.csv"
    process_file(compiled_file)
    
    # Clean individual portfolio CSVs
    for file_path in data_dir.glob("b3_carteira_teorica_*.csv"):
        process_file(file_path)

if __name__ == "__main__":
    main()
