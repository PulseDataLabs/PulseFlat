import logging
from pathlib import Path
import pandas as pd
from utils import salvar_csv, agora_brt

class BaseScraper:
    name: str = ""
    accumulate: bool = True
    chaves_dedup: list[str] | None = None

    def __init__(self):
        if not self.name:
            self.name = self.__class__.__name__.lower().replace("scraper", "")
        self.logger = logging.getLogger(self.name)
        root_dir = Path(__file__).resolve().parents[2]
        self.output_file = root_dir / "data" / f"{self.name}.csv"

    def fetch(self) -> pd.DataFrame:
        raise NotImplementedError("Cada scraper deve implementar o método fetch.")

    def run(self) -> None:
        self.logger.info(f"Iniciando scraper: {self.name}")
        try:
            df = self.fetch()
            if df is None or (isinstance(df, pd.DataFrame) and df.empty):
                self.logger.warning("Nenhum dado retornado para salvar.")
                return

            # Certifica de que a coluna de data de captura existe
            if "data_captura" not in df.columns and "dt_captura" not in df.columns:
                data_captura, _ = agora_brt()
                df.insert(0, "data_captura", data_captura)

            # Limpa NaN para strings vazias
            df_cleaned = df.fillna("")

            # Formata tipos e limpa dados (datas e números BR)
            import re

            def clean_value(val):
                if val is None or pd.isna(val):
                    return ""
                val_str = str(val).strip()
                if not val_str:
                    return ""

                # 1. Limpa formatos de data BR (DD/MM/YYYY -> YYYY-MM-DD)
                match = re.match(r'^(\d{2})/(\d{2})/(\d{4})$', val_str)
                if match:
                    d, m, y = match.groups()
                    return f"{y}-{m}-{d}"
                match_short = re.match(r'^(\d{2})/(\d{2})/(\d{2})$', val_str)
                if match_short:
                    d, m, y = match_short.groups()
                    return f"20{y}-{m}-{d}"

                # 2. Limpa formatos numéricos BR (5,3656 -> 5.3656)
                if ',' in val_str and val_str.count(',') == 1:
                    clean_num = val_str.replace('.', '').replace(',', '').replace('%', '').replace('-', '').replace('+', '').strip()
                    if clean_num.isdigit():
                        parts = val_str.split(',')
                        left = parts[0].replace('.', '')
                        right = parts[1]
                        return f"{left}.{right}"

                return val_str

            for col in df_cleaned.columns:
                if pd.api.types.is_datetime64_any_dtype(df_cleaned[col]):
                    df_cleaned[col] = df_cleaned[col].dt.strftime("%Y-%m-%d")
                else:
                    df_cleaned[col] = df_cleaned[col].apply(clean_value)

            registros = df_cleaned.to_dict(orient="records")
            cabecalho = list(df_cleaned.columns)

            # Garante que data_captura esteja preenchido para salvamento correto
            data_captura, _ = agora_brt()
            for r in registros:
                if "data_captura" not in r:
                    if "dt_captura" in r:
                        r["data_captura"] = r["dt_captura"]
                    else:
                        r["data_captura"] = data_captura

            if "data_captura" not in cabecalho:
                cabecalho.insert(0, "data_captura")

            salvar_csv(
                arquivo=self.output_file,
                registros=registros,
                cabecalho=cabecalho,
                chaves_dedup=self.chaves_dedup,
                acumular=self.accumulate,
            )

        except Exception as e:
            self.logger.error(f"Erro ao executar scraper {self.name}: {e}", exc_info=True)
            raise e
