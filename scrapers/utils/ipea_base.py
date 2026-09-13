"""
scrapers/utils/ipea_base.py
---------------------------
Classe base para todos os scrapers que consomem dados OData v4 do IPEADATA.
Integra-se nativamente ao BaseScraper e ao orquestrador run_all.py.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scrapers.utils.base import BaseScraper
from scrapers.utils.ipea_client import IpeaClient
from utils.base import get_logger

log = get_logger("ipea_base")


class BaseIpeaScraper(BaseScraper):
    """
    Classe base especializada para scrapers de séries temporais do IPEADATA.
    Herda todas as funcionalidades de BaseScraper (deduplicação, particionamento,
    gravação CSV/Parquet, catálogo de metadados e concorrência).
    """

    group: str = "ipea"
    source: str = "IPEA — Ipeadata (ipeadata.gov.br)"
    icon: str = "🏛️"
    icon_class: str = "icon-ipea"
    badge: str = "IPEA"
    badge_class: str = "badge-monthly"
    enabled: bool = True
    phase: int = 1
    accumulate: bool = True

    # Subclasses podem definir um código único ou uma lista de séries estruturadas
    series_code: str = ""

    def __init__(self, client: IpeaClient | None = None):
        super().__init__()
        self.client = client or IpeaClient()

    def fetch_serie(
        self,
        sercodigo: str,
        top: int | None = None,
        filter_str: str | None = None,
        orderby: str | None = "VALDATA asc",
    ) -> list[dict[str, Any]]:
        """
        Executa requisição para obter os valores históricos de uma série.
        """
        try:
            records = self.client.get_serie_values(
                sercodigo, top=top, filter_str=filter_str, orderby=orderby
            )
            self.logger.info(
                f"[IPEA] {len(records)} registros retornados para a série {sercodigo}"
            )
            return records
        except Exception as e:
            self.logger.error(f"Erro ao requisitar série IPEA {sercodigo}: {e}")
            raise

    def fetch_series_list(
        self,
        series_list: list[dict[str, Any]],
        top: int | None = None,
    ) -> pd.DataFrame:
        """
        Coleta e concatena uma lista estruturada de séries do IPEADATA contendo 'code' e 'title'.
        Aplica filtros de data_referencia caso start_date, end_date ou target_date estejam definidos.
        """
        frames = []
        for item in series_list:
            code = item["code"]
            title = item.get("title", code)
            try:
                values = self.client.get_serie_values(code, top=top)
            except Exception as e:
                self.logger.warning(f"[IPEA] Falha ao coletar série {code}: {e}")
                continue

            records = []
            for val_item in values:
                raw_date = val_item.get("VALDATA", "")
                date_ref = (
                    raw_date.split("T")[0].strip()
                    if "T" in raw_date
                    else raw_date[:10].strip()
                )
                val = val_item.get("VALVALOR")
                if val is None:
                    continue
                try:
                    num_val = float(val)
                except (ValueError, TypeError):
                    continue

                records.append(
                    {
                        "data_referencia": date_ref,
                        "codigo_ativo": code,
                        "label": title,
                        "valor": num_val,
                    }
                )

            if records:
                frames.append(pd.DataFrame(records))

        if not frames:
            raise RuntimeError("Nenhum dado retornado para as séries do IPEA.")

        df = pd.concat(frames, ignore_index=True)
        if self.target_date:
            target_str = self.target_date.strftime("%Y-%m-%d")
            df = df[df["data_referencia"] == target_str]
        elif self.start_date or self.end_date:
            if self.start_date:
                df = df[df["data_referencia"] >= self.start_date.strftime("%Y-%m-%d")]
            if self.end_date:
                df = df[df["data_referencia"] <= self.end_date.strftime("%Y-%m-%d")]

        return df.sort_values(by=["data_referencia", "codigo_ativo"]).reset_index(drop=True)

    def normalize_dataframe(
        self,
        records: list[dict[str, Any]],
        codigo: str = "",
        nome: str = "",
    ) -> pd.DataFrame:
        """
        Padroniza os registros brutos do IPEA (VALDATA, VALVALOR) no formato padrão PulseFlat:
        - data_referencia: YYYY-MM-DD
        - valor: float
        - data_captura: data atual em formato ISO
        - codigo_ativo: código da série ou ticker
        - nome_ativo: descrição legível
        """
        if not records:
            return pd.DataFrame()

        df = pd.DataFrame(records)
        hoje = datetime.now().strftime("%Y-%m-%d")

        # Tratamento da data de referência
        if "VALDATA" in df.columns:
            df["data_referencia"] = (
                df["VALDATA"].astype(str).str.split("T").str[0].str.strip()
            )
        elif "data_referencia" not in df.columns:
            df["data_referencia"] = hoje

        # Tratamento do valor numérico
        if "VALVALOR" in df.columns:
            df["valor"] = pd.to_numeric(df["VALVALOR"], errors="coerce")
        elif "valor" in df.columns:
            df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

        df["data_captura"] = hoje

        if codigo and "codigo_ativo" not in df.columns:
            df["codigo_ativo"] = codigo
        elif "SERCODIGO" in df.columns and "codigo_ativo" not in df.columns:
            df["codigo_ativo"] = df["SERCODIGO"]

        if nome and "nome_ativo" not in df.columns:
            df["nome_ativo"] = nome

        # Seleciona e organiza colunas essenciais
        colunas_ordenadas = ["data_captura", "data_referencia", "codigo_ativo", "nome_ativo", "valor"]
        cols_finais = [c for c in colunas_ordenadas if c in df.columns]
        outros_campos = [c for c in df.columns if c not in cols_finais and c not in ("VALDATA", "VALVALOR", "SERCODIGO", "NIVNOME", "TERCODIGO")]

        df = df[cols_finais + outros_campos]
        df = df.dropna(subset=["data_referencia", "valor"])
        df = df.sort_values(by=["data_referencia"]).drop_duplicates(
            subset=["data_referencia", "codigo_ativo"] if "codigo_ativo" in df.columns else ["data_referencia"]
        )

        return df
