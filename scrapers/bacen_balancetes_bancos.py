#!/usr/bin/env python
# coding: utf-8
"""
Scraper: BACEN – Balancetes de Bancos (COSIF)
Fonte:   https://www.bcb.gov.br/api/servico/sitebcb/Documentos/byListGuid
Saída:   data/bacen_balancetes_bancos.csv

Busca o documento de balancetes mais recente do BCB, faz o download do arquivo ZIP,
extrai o CSV interno, trata os campos (limpeza de cabeçalhos e formatação de saldo)
e salva o arquivo final tratado.
"""
import os
import sys
import zipfile
import csv
from io import BytesIO

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper


DOCS_API_URL = (
    "https://www.bcb.gov.br/api/servico/sitebcb/Documentos/byListGuid"
    "?tronco=estabilidadefinanceira"
    "&guidLista=a11917e4-c729-4259-bd4e-0266827b6acd"
    "&ordem=DataDocumento%20desc"
    "&pasta=/Bancos"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


class BacenBalancetesBancosScraper(BaseScraper):
    name = "bacen_balancetes_bancos"
    accumulate = False  # Sobrescreve diariamente para manter apenas o balancete mais recente

    def fetch(self) -> pd.DataFrame:
        self.logger.info("Buscando lista de documentos de balancetes no BCB...")
        resp = requests.get(DOCS_API_URL, headers=HEADERS, timeout=60)
        resp.raise_for_status()

        data = resp.json()
        conteudo = data.get("conteudo", [])
        if not conteudo:
            raise RuntimeError("Nenhum documento retornado pela API do BCB.")

        # O primeiro documento é o mais recente devido à ordenação da API
        doc = conteudo[0]
        relative_url = doc.get("Url")
        doc_name = doc.get("Nome", "balancete")
        self.logger.info(f"Documento mais recente encontrado: {doc_name} (data: {doc.get('DataDocumento')})")

        if not relative_url:
            raise RuntimeError("URL do documento não informada na resposta da API.")

        download_url = "https://www.bcb.gov.br" + relative_url
        self.logger.info(f"Baixando arquivo zip do balancete: {download_url}")

        resp_file = requests.get(download_url, headers=HEADERS, timeout=120)
        resp_file.raise_for_status()

        self.logger.info("Download concluído. Processando arquivo ZIP...")
        with zipfile.ZipFile(BytesIO(resp_file.content)) as zf:
            filenames = zf.namelist()
            if not filenames:
                raise RuntimeError("Arquivo ZIP baixado está vazio.")
            
            csv_filename = filenames[0]
            self.logger.info(f"Extraindo e tratando CSV: {csv_filename}")
            with zf.open(csv_filename) as f:
                content = f.read().decode("iso-8859-1")

        lines = content.splitlines()
        if len(lines) < 4:
            raise RuntimeError("O arquivo CSV extraído está vazio ou corrompido.")

        # O cabeçalho real está na quarta linha (índice 3)
        header_line = lines[3].strip()
        if header_line.startswith("#"):
            header_line = header_line[1:]
        headers = [h.lower().strip() for h in header_line.split(";")]

        self.logger.info(f"Colunas identificadas: {headers}")

        reader = csv.reader(lines[4:], delimiter=";")
        rows = []
        for r in reader:
            if not r or not any(cell.strip() for cell in r):
                continue
            row_dict = {}
            for idx, val in enumerate(r):
                if idx < len(headers):
                    col_name = headers[idx]
                    val_clean = val.strip()
                    if col_name == "saldo":
                        # Formata o saldo convertendo de "2409477025240,00" para "2409477025240.00"
                        val_clean = val_clean.replace(".", "").replace(",", ".")
                    row_dict[col_name] = val_clean
            rows.append(row_dict)

        self.logger.info(f"Total de {len(rows)} linhas processadas com sucesso.")
        return pd.DataFrame(rows)


if __name__ == "__main__":
    scraper = BacenBalancetesBancosScraper()
    scraper.run()
