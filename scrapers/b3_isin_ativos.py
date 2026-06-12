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

log = get_logger("b3_isin_ativos")

class B3IsinAtivosScraper(BaseScraper):
    name = "b3_isin_ativos"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = False  # Snapshot completo, não acumular
    chaves_dedup = None

    # Metadados para o catálogo global
    title = "B3 ISIN Ativos"
    description = "Banco de dados completo de ativos com código ISIN cadastrados na B3."
    icon = "🏷️"
    icon_class = "icon-b3"
    badge = "Semanal"
    badge_class = "badge-weekly"
    tags = ["isin", "ativos", "cadastro"]
    source = "B3"

    def fetch(self) -> pd.DataFrame:
        session = nova_session()
        zip_content = get_isin_zip(session)
        
        log.info("Lendo NUMERACA.TXT de dentro do arquivo ZIP...")
        import csv
        
        data_captura, _ = agora_brt()
        records = []
        
        colunas = [
            "data_geracao", "acao", "codigo_isin", "codigo_emissor", "codigo_cfi", 
            "descricao_ativo", "ano_emissao", "data_emissao", "ano_expiracao", 
            "data_expiracao", "taxa_juros", "moeda", "valor_nominal", "preco_exercicio", 
            "indexador", "percentual_indexador", "data_acao", "codigo_cetip", 
            "codigo_selic", "codigo_pais", "tipo_ativo", "codigo_categoria", 
            "codigo_especie", "data_base", "numero_emissao", "numero_serie", 
            "tipo_emissao", "tipo_ativo_objeto", "tipo_entrega", "tipo_fundo", 
            "tipo_garantias", "tipo_juros", "tipo_mercado", "tipo_status_isin", 
            "tipo_vencimento", "tipo_protecao", "tipo_politica_distribuicao_fundos", 
            "tipo_politica_investimento_fundo", "tipo_forma", "tipo_estilo_opcao", 
            "numero_serie_opcao", "codigo_frequencia_juros", "situacao_isin", 
            "data_primeiro_pagamento_juros", "exchange"
        ]
        
        with zipfile.ZipFile(io.BytesIO(zip_content)) as zf:
            with zf.open("NUMERACA.TXT") as f:
                # TextIOWrapper para ler linha a linha de forma eficiente
                text_stream = io.TextIOWrapper(f, encoding="latin1")
                reader = csv.reader(text_stream)
                for row in reader:
                    if len(row) < 45:
                        continue
                    
                    rec = {"data_captura": data_captura}
                    for idx, col_name in enumerate(colunas):
                        rec[col_name] = row[idx].strip()
                    
                    records.append(rec)
                    
        log.info(f"{len(records)} ativos capturados.")
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

            # 1. Formatação de datas vetorizada e rápida
            date_cols = ["data_geracao", "data_emissao", "data_expiracao", "data_acao", "data_base", "data_primeiro_pagamento_juros"]
            for col in date_cols:
                if col in df_cleaned.columns:
                    s = df_cleaned[col].astype(str)
                    mask = s.str.match(r'^\d{8}$')
                    df_cleaned.loc[mask, col] = s.str.slice(0, 4) + "-" + s.str.slice(4, 6) + "-" + s.str.slice(6, 8)

            # 2. Formatação de decimais vetorizada e rápida
            num_cols = ["taxa_juros", "valor_nominal", "preco_exercicio", "percentual_indexador"]
            for col in num_cols:
                if col in df_cleaned.columns:
                    s = df_cleaned[col].astype(str)
                    mask = s.str.contains(',', regex=False)
                    df_cleaned.loc[mask, col] = s.str.replace('.', '', regex=False).str.replace(',', '.', regex=False)

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
    B3IsinAtivosScraper().run()
