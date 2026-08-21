import argparse
import time

from scripts.utils.ux import print_done

"""
scrapers/b3_cotahist_anual.py
-------------------------------
COTAHIST anual da B3 — cotações históricas do ano corrente.

Fonte: https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{year}.ZIP
"""

import io
import sys
import zipfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd

from scrapers.utils.base import BaseScraper
from utils.base import FUSO, get_logger, nova_session
from utils.parsers import decode_bytes, enriquecer, fwf_rows, read_existing_header

log = get_logger("b3_cotahist_anual")

URL_FORMAT = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{year}.ZIP"

COTAHIST_WIDTHS = [
    2,
    8,
    2,
    12,
    3,
    12,
    10,
    3,
    4,
    13,
    13,
    13,
    13,
    13,
    13,
    13,
    5,
    18,
    18,
    13,
    1,
    8,
    7,
    13,
    12,
    3,
]
COTAHIST_FIELDS = [
    "regtype",
    "refdate",
    "bdi_code",
    "symbol",
    "instrument_market",
    "corporation_name",
    "specification_code",
    "days_to_settlement",
    "trading_currency",
    "open",
    "high",
    "low",
    "average",
    "close",
    "best_bid",
    "best_ask",
    "trade_quantity",
    "traded_contracts",
    "volume",
    "strike_price",
    "strike_price_adjustment_indicator",
    "maturity_date",
    "allocation_lot_size",
    "strike_price_in_points",
    "isin",
    "distribution_id",
]

ARQUIVO = Path("data/b3_cotahist_anual.csv.gz")

# Mercados mantidos: 010 (à vista) e 020 (fracionário) — ações, BDRs, ETFs e
# fundos listados. Demais mercados (opções, termos, direitos, leilões) são
# descartados para manter o arquivo pequeno e versionável no GitHub.
MERCADOS_KEEP = ("010", "020")


def capturar(year: int) -> tuple[list[dict], list[str]]:
    session = nova_session()
    url = URL_FORMAT.format(year=year)
    log.info(f"Baixando {url}")
    resp = session.get(url, timeout=180)
    resp.raise_for_status()

    rows = []
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for info in zf.infolist():
            if info.is_dir() or info.file_size == 0:
                continue
            text = decode_bytes(zf.read(info.filename))
            parsed = fwf_rows(
                text, COTAHIST_FIELDS, COTAHIST_WIDTHS, only_regtype_01=True
            )
            for r in parsed:
                if r.get("instrument_market") not in MERCADOS_KEEP:
                    continue
                r["arquivo_origem"] = info.filename
                rows.append(r)

    enriched, header_novo = enriquecer("b3_cotahist_anual", rows)
    header_existente = read_existing_header(ARQUIVO)
    header = []
    for col in header_existente + header_novo:
        if col and col not in header:
            header.append(col)
    return enriched, header


class B3CotahistAnualScraper(BaseScraper):
    name = "b3_cotahist_anual"
    group = "b3"
    enabled = True
    phase = 1
    accumulate = True
    compress = True
    chaves_dedup = ["data_captura", "conjunto", "registro_hash"]

    # Catálogo de Metadados
    title = "B3 — COTAHIST Histórico Anual"
    description = "Série histórica anual completa de cotações de ações, fundos e opções da B3."
    icon = "📅"
    icon_class = "icon-b3"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = ["cotações anual", "histórico", "fwf", "b3"]
    source = "B3 · COTAHIST"

    def _ano_atual(self) -> int:
        return datetime.now(FUSO).year

    def fetch(self, year: int | None = None) -> pd.DataFrame:
        log.info("=== B3 — COTAHIST Anual ===")
        if year is None:
            import argparse

            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument("--year", type=int, default=self._ano_atual())
            args, _ = parser.parse_known_args()
            year = args.year

        log.info(f"Buscando cotações históricas para o ano: {year}")
        rows, header = capturar(year)
        # Reordena para garantir o cabeçalho original
        df = pd.DataFrame(rows)
        if not df.empty:
            colunas = [c for c in header if c in df.columns]
            return df[colunas]
        return df

    def _processar_ano(self, year: int) -> None:
        t0 = time.time()

        # 1. Fetch data
        df = self.fetch(year)
        if df is None or df.empty:
            self.logger.warning(f"Nenhum dado retornado para {year}.")
            return

        # Add data_captura if not present
        if "data_captura" not in df.columns:
            from utils import agora_brt

            data_captura, _ = agora_brt()
            df.insert(0, "data_captura", data_captura)

        # Fillna and clean
        df_cleaned = df.fillna("")
        # Apply standard cleaning logic only to date columns
        for col in df_cleaned.columns:
            if col not in ("refdate", "maturity_date"):
                continue
            s_str = df_cleaned[col].astype(str).str.strip()
            result = s_str.copy()

            # YYYYMMDD -> YYYY-MM-DD
            mask_date = s_str.str.match(r"^\d{8}$")
            if mask_date.any():
                result.loc[mask_date] = s_str.loc[mask_date].str.replace(
                    r"^(\d{4})(\d{2})(\d{2})$", r"\1-\2-\3", regex=True
                )
            df_cleaned[col] = result.fillna("").replace({"nan": "", "None": ""})

        # 2. Write to CSV in a memory-efficient chunked manner
        output_file = self.output_file
        tmp_file = output_file.with_name(output_file.name + ".tmp")

        # Ensure headers are aligned
        cabecalho = list(df_cleaned.columns)

        substituidas = 0
        if output_file.exists():
            from utils.parsers import read_existing_header

            header_existente = read_existing_header(output_file)
            merged_headers = []
            for col in header_existente + cabecalho:
                if col and col not in merged_headers:
                    merged_headers.append(col)
            cabecalho = merged_headers

            # Stream original file, filtering out rows of the current year
            str_year = str(year)
            import gzip

            with gzip.open(tmp_file, "wt", encoding="utf-8", newline="") as out_f:
                # Write header
                out_f.write(",".join(cabecalho) + "\n")

                # Read chunks
                chunk_reader = pd.read_csv(
                    output_file, dtype=str, keep_default_na=False, chunksize=100000
                )
                for chunk in chunk_reader:
                    # Ensure chunk has all cabecalho columns
                    for c in cabecalho:
                        if c not in chunk.columns:
                            chunk[c] = ""

                    # Filter out rows of the same year
                    mask_drop = chunk["refdate"].astype(str).str.startswith(str_year)
                    chunk_filtered = chunk[~mask_drop]
                    substituidas += mask_drop.sum()

                    if not chunk_filtered.empty:
                        chunk_filtered.to_csv(
                            out_f,
                            header=False,
                            index=False,
                            columns=cabecalho,
                            encoding="utf-8",
                        )

            # Append new data
            for c in cabecalho:
                if c not in df_cleaned.columns:
                    df_cleaned[c] = ""
            with gzip.open(tmp_file, "at", encoding="utf-8", newline="") as out_f:
                df_cleaned.to_csv(
                    out_f,
                    header=False,
                    index=False,
                    columns=cabecalho,
                    encoding="utf-8",
                )

            # Rename tmp to output
            tmp_file.replace(output_file)
        else:
            # File does not exist, just write new data
            df_cleaned.to_csv(
                output_file, index=False, columns=cabecalho, encoding="utf-8"
            )

        elapsed = time.time() - t0
        msg = f"[{year}] {len(df_cleaned)} registros salvos em {output_file.name}"
        if substituidas > 0:
            msg += f" ({substituidas} registros antigos substituídos)"
        print_done(msg, elapsed=elapsed)

    def run(self) -> None:
        is_pipeline = any(
            "run_all" in str(getattr(m, "__file__", "")) for m in sys.modules.values()
        )
        if not is_pipeline:
            from scripts.utils.ux import banner

            banner(self.title or self.name.replace("_", " ").title())

        # Parse CLI arguments
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--year", type=int, default=self._ano_atual())
        parser.add_argument("--since", type=int, default=None)
        args, _ = parser.parse_known_args()

        if args.since:
            anos = list(range(args.since, self._ano_atual() + 1))
        else:
            anos = [args.year]

        t0 = time.time()
        try:
            for ano in anos:
                self._processar_ano(ano)
            total_elapsed = time.time() - t0
            if len(anos) > 1:
                from scripts.utils.ux import print_done

                print_done(
                    f"{len(anos)} anos processados ({anos[0]}–{anos[-1]})",
                    elapsed=total_elapsed,
                )
        except Exception as e:
            time.time() - t0
            self.logger.error(f"Erro ao executar scraper {self.name}: {e}")
            raise e


if __name__ == "__main__":
    B3CotahistAnualScraper().run()
