import io
import sys
import zipfile
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.utils.base import BaseScraper
from utils.base import nova_session, get_logger
from utils.parsers import decode_bytes

log = get_logger("b3_titulos_negociaveis")

URL = "https://bvmf.bmfbovespa.com.br/suplemento/ExecutaAcaoDownload.asp?arquivo=Titulos_Negociaveis.zip&server=L"


class B3TitulosNegociaveisScraper(BaseScraper):
    name = "b3_titulos_negociaveis"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = False
    chaves_dedup = ["data_captura", "codigo_ativo", "codigo_isin"]

    title = "B3 Títulos Negociáveis"
    description = "Cadastro de todos os títulos e instrumentos negociáveis no mercado da B3, incluindo BDRs, ações e outros ativos."
    icon = "📋"
    icon_class = "icon-b3"
    badge = "Snapshot"
    badge_class = "badge-snapshot"
    tags = ["cadastro", "instrumentos", "bdr", "ações", "b3"]
    source = "B3"

    def fetch(self) -> pd.DataFrame:
        log.info("Baixando arquivo de títulos negociáveis...")
        session = nova_session()
        resp = session.get(URL, timeout=180)
        resp.raise_for_status()

        records = []
        current_company = {}

        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            for info in zf.infolist():
                if info.is_dir() or info.file_size == 0:
                    continue
                filename = info.filename
                log.info(f"Processando arquivo {filename}...")
                raw_text = decode_bytes(zf.read(filename))
                
                for line in raw_text.splitlines():
                    if not line:
                        continue
                    if line.startswith("01"):
                        # Registro de emissor/companhia
                        root = line[2:6].strip()
                        name = line[6:66].strip()
                        short_name = line[66:78].strip()
                        current_company = {
                            "root": root,
                            "nome_emissor": name,
                            "nome_curto": short_name
                        }
                    elif line.startswith("02"):
                        # Registro de ativo negociável
                        ticker = line[2:14].strip()
                        root = line[14:18].strip()
                        desc = line[21:81].strip()
                        isin = line[81:93].strip()
                        market_type = line[111:126].strip()
                        title_type = line[133:143].strip()

                        records.append({
                            "codigo_ativo": ticker,
                            "nome_emissor": current_company.get("nome_emissor", ""),
                            "nome_curto": current_company.get("nome_curto", ""),
                            "codigo_isin": isin,
                            "tipo_ativo": desc,
                            "tipo_mercado": market_type,
                            "tipo_titulo": title_type,
                            "arquivo_origem": filename,
                        })

        log.info(f"Total de {len(records)} registros extraídos.")
        return pd.DataFrame(records)


def main():
    B3TitulosNegociaveisScraper().run()


if __name__ == "__main__":
    main()
