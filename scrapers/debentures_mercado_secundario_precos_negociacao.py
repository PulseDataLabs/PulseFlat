import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class DebenturesMercadoSecundarioPrecosNegociacaoScraper(GenericScraper):
    title = "Debêntures — Mercado Secundário e Preços de Negociação"
    description = "Preços médios, quantidades, volumes e negócios diários de debêntures no mercado secundário."
    badge = "Diário"
    source = "Debêntures"
    tags = ['debentures', 'mercado_secundario', 'precos', 'negociacao', 'anbima', 'snd']
    group = "anbima"
    enabled = True
    phase = 1
    resource_name = "Debêntures - Preços de Negociação"

    def __init__(self):
        super().__init__()
        self.chaves_dedup = ["data_referencia", "codigo_ativo", "isin"]

    def fetch(self) -> pd.DataFrame:
        df = super().fetch()
        if not df.empty:

            from utils.parsers import hash_row

            def clean_float(val):
                if pd.isna(val) or val == "" or str(val).strip() in ("-", ""):
                    return ""
                val_str = str(val).strip()
                if "," in val_str:
                    val_str = val_str.replace(".", "").replace(",", ".")
                try:
                    f = float(val_str)
                    if f.is_integer():
                        return str(int(f))
                    return f"{f:.8f}".rstrip("0").rstrip(".")
                except ValueError:
                    return val_str

            def clean_int(val):
                if pd.isna(val) or val == "" or str(val).strip() in ("-", ""):
                    return ""
                val_str = str(val).strip()
                if "," in val_str:
                    val_str = val_str.split(",")[0]
                val_str = val_str.replace(".", "")
                try:
                    return str(int(val_str))
                except ValueError:
                    return val_str

            float_cols = ["pu_minimo", "pu_medio", "pu_maximo", "pu_da_curva"]
            int_cols = ["quantidade", "numero_de_negocios"]

            for col in float_cols:
                if col in df.columns:
                    df[col] = df[col].apply(clean_float)

            for col in int_cols:
                if col in df.columns:
                    df[col] = df[col].apply(clean_int)

            # Recalculate hashes
            records = df.to_dict(orient="records")
            new_hashes = []
            for item in records:
                hash_input = {
                    k: v
                    for k, v in item.items()
                    if k not in ("data_captura", "registro_hash")
                }
                new_hashes.append(hash_row(hash_input))
            df["registro_hash"] = new_hashes

        return df


def main():
    DebenturesMercadoSecundarioPrecosNegociacaoScraper().run()


if __name__ == "__main__":
    main()
