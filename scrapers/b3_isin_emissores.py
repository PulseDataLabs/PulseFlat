import sys
import time
import requests
import zipfile
import io
import base64
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, nova_session, salvar_csv
from utils.b3_helpers import get_isin_zip
from scrapers.utils.base import BaseScraper

log = get_logger("b3_isin_emissores")

class B3IsinEmissoresScraper(BaseScraper):
    name = "b3_isin_emissores"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = False  # Snapshot completo, não acumular
    chaves_dedup = None

    # Metadados para o catálogo global
    title = "B3 ISIN Emissores"
    description = "Banco de dados completo de emissores de códigos ISIN da B3."
    icon = "🏢"
    icon_class = "icon-b3"
    badge = "Semanal"
    badge_class = "badge-weekly"
    tags = ["isin", "emissores", "cadastro"]
    source = "B3"

    def fetch(self) -> pd.DataFrame:
        session = nova_session()
        zip_content = get_isin_zip(session)
        
        log.info("Lendo EMISSOR.TXT de dentro do arquivo ZIP...")
        import csv
        
        data_captura, _ = agora_brt()
        records = []
        
        with zipfile.ZipFile(io.BytesIO(zip_content)) as zf:
            with zf.open("EMISSOR.TXT") as f:
                # TextIOWrapper para ler linha a linha de forma eficiente
                text_stream = io.TextIOWrapper(f, encoding="latin1")
                reader = csv.reader(text_stream)
                for row in reader:
                    if len(row) < 4:
                        continue
                    records.append({
                        "data_captura": data_captura,
                        "codigo_emissor": limpar(row[0]),
                        "nome_emissor": limpar(row[1]),
                        "cnpj_emissor": limpar(row[2]),
                        "data_criacao_emissor": limpar(row[3])
                    })
                    
        log.info(f"{len(records)} emissores capturados.")
        return pd.DataFrame(records)

    def run(self) -> None:
        is_pipeline = any("run_all" in str(getattr(m, "__file__", "")) for m in sys.modules.values())
        if not is_pipeline:
            from scripts.utils.ux import banner
            banner(self.title or self.name.replace("_", " ").title())

        t0 = time.time()
        try:
            df = self.fetch()
            if df is None or df.empty:
                self.logger.warning("Nenhum dado retornado para salvar.")
                return

            if "data_captura" not in df.columns:
                data_captura, _ = agora_brt()
                df.insert(0, "data_captura", data_captura)

            df_cleaned = df.fillna("")

            # Formatação de datas vetorizada e rápida
            col = "data_criacao_emissor"
            if col in df_cleaned.columns:
                s = df_cleaned[col].astype(str)
                mask = s.str.match(r'^\d{8}$')
                df_cleaned.loc[mask, col] = s.str.slice(0, 4) + "-" + s.str.slice(4, 6) + "-" + s.str.slice(6, 8)

            registros = df_cleaned.to_dict(orient="records")
            cabecalho = list(df_cleaned.columns)

            data_captura, _ = agora_brt()
            for r in registros:
                if "data_captura" not in r:
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

            elapsed = time.time() - t0
            if not is_pipeline:
                from scripts.utils.ux import print_done
                print_done(f"{len(registros)} registros salvos em {self.output_file.name}", elapsed=elapsed)

        except Exception as e:
            elapsed = time.time() - t0
            self.logger.error(f"Erro ao executar scraper {self.name}: {e}")
            raise e


if __name__ == "__main__":
    B3IsinEmissoresScraper().run()
