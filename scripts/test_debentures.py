import pandas as pd
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parents[1]
csv_file = ROOT_DIR / "data" / "debentures_mercado_secundario_precos_negociacao.csv.gz"
df = pd.read_csv(csv_file, dtype=str, keep_default_na=False)

print(f"Original row count: {len(df)}")

def is_valid_date(val):
    val_strip = str(val).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            datetime.strptime(val_strip, fmt)
            return True
        except ValueError:
            continue
    return False

# Filter out rows with invalid data_referencia
mask_valid = df["data_referencia"].apply(is_valid_date)
df_clean = df[mask_valid]

print(f"Cleaned row count: {len(df_clean)}")
print(f"Removed rows: {len(df) - len(df_clean)}")

# Let's inspect some of the removed rows
df_removed = df[~mask_valid]
print("Removed rows samples:")
print(df_removed.head())

# Overwrite CSV with cleaned data
df_clean.to_csv(csv_file, index=False, encoding="utf-8")
print("Cleaned CSV saved.")
