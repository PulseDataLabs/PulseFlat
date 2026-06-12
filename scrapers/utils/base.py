import sys
import time
from pathlib import Path
import pandas as pd
from utils import salvar_csv, agora_brt

from scripts.utils.ux import ColorLogger, banner, print_start, print_done, print_fail


class BaseScraper:
    name: str = ""
    accumulate: bool = True
    chaves_dedup: list[str] | None = None

    # Metadados para o catálogo global
    title: str = ""
    description: str = ""
    icon: str = "📊"
    icon_class: str = ""
    badge: str = ""
    badge_class: str = ""
    tags: list[str] = []
    source: str = ""

    # Controle do Pipeline
    group: str = ""
    enabled: bool = True
    phase: int = 1

    def __init__(self):
        if not self.name:
            self.name = self.__class__.__name__.lower().replace("scraper", "")
        self.logger = ColorLogger(self.name)
        root_dir = Path(__file__).resolve().parents[2]
        self.output_file = root_dir / "data" / f"{self.name}.csv"

    def fetch(self) -> pd.DataFrame:
        raise NotImplementedError("Cada scraper deve implementar o método fetch.")

    def run(self) -> None:
        is_pipeline = any("run_all" in str(getattr(m, "__file__", "")) for m in sys.modules.values())

        if not is_pipeline:
            banner(self.title or self.name.replace("_", " ").title())

        t0 = time.time()
        try:
            df = self.fetch()
            if df is None or (isinstance(df, pd.DataFrame) and df.empty):
                self.logger.warning("Nenhum dado retornado para salvar.")
                return

            if "data_captura" not in df.columns and "dt_captura" not in df.columns:
                data_captura, _ = agora_brt()
                df.insert(0, "data_captura", data_captura)

            df_cleaned = df.fillna("")

            def clean_series_vectorized(s: pd.Series) -> pd.Series:
                s_str = s.astype(str).str.strip()
                result = s_str.copy()
                
                # DD/MM/YYYY
                mask_date1 = s_str.str.match(r'^\d{2}/\d{2}/\d{4}$')
                if mask_date1.any():
                    result.loc[mask_date1] = s_str.loc[mask_date1].str.replace(
                        r'^(\d{2})/(\d{2})/(\d{4})$', r'\3-\2-\1', regex=True
                    )
                    
                # DD/MM/YY
                mask_date2 = s_str.str.match(r'^\d{2}/\d{2}/\d{2}$')
                if mask_date2.any():
                    result.loc[mask_date2] = s_str.loc[mask_date2].str.replace(
                        r'^(\d{2})/(\d{2})/(\d{2})$', r'20\3-\2-\1', regex=True
                    )
                    
                # YYYYMMDD
                mask_date3 = s_str.str.match(r'^\d{8}$')
                if mask_date3.any():
                    result.loc[mask_date3] = s_str.loc[mask_date3].str.replace(
                        r'^(\d{4})(\d{2})(\d{2})$', r'\1-\2-\3', regex=True
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

                result = result.fillna("").replace({"nan": "", "None": ""})
                return result

            for col in df_cleaned.columns:
                if pd.api.types.is_datetime64_any_dtype(df_cleaned[col]):
                    df_cleaned[col] = df_cleaned[col].dt.strftime("%Y-%m-%d")
                elif pd.api.types.is_numeric_dtype(df_cleaned[col]):
                    continue
                else:
                    df_cleaned[col] = clean_series_vectorized(df_cleaned[col])

            cabecalho = list(df_cleaned.columns)

            data_captura, _ = agora_brt()
            if "data_captura" not in df_cleaned.columns:
                df_cleaned.insert(0, "data_captura", data_captura)
            if "data_captura" not in cabecalho:
                cabecalho.insert(0, "data_captura")

            salvar_csv(
                arquivo=self.output_file,
                registros=df_cleaned,  # Passa o DataFrame diretamente
                cabecalho=cabecalho,
                chaves_dedup=self.chaves_dedup,
                acumular=self.accumulate,
            )

            elapsed = time.time() - t0
            if not is_pipeline:
                print_done(f"{len(df_cleaned)} registros salvos em {self.output_file.name}", elapsed=elapsed)

        except Exception as e:
            elapsed = time.time() - t0
            self.logger.error(f"Erro ao executar scraper {self.name}: {e}")
            raise e
