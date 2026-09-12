"""
scrapers/tesouro_transparente_template.py
-----------------------------------------
Template e guia de referência para criação de novos scrapers baseados
na API CKAN do Tesouro Transparente (Tesouro Nacional).

Fonte: https://www.tesourotransparente.gov.br/ckan/api/3
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.tesouro_transparente_base import BaseTesouroTransparenteScraper
from utils.base import agora_brt, get_logger

log = get_logger("tesouro_transparente_template")


class TesouroTransparenteTemplateScraper(BaseTesouroTransparenteScraper):
    # Identificador único do dataset (gera data/tesouro_transparente_exemplo_template.csv)
    name = "tesouro_transparente_exemplo_template"

    group = "tesouro"
    enabled = False  # Deixar False até configurar o resource_id específico
    phase = 1
    accumulate = True

    # Chaves para evitar duplicatas em coletas diárias
    chaves_dedup = ["data_captura", "data_referencia", "titulo"]

    title = "Tesouro Transparente — Template de Exemplo (CKAN)"
    description = (
        "Scraper modelo demonstrando a estrutura de consulta à API CKAN do Tesouro Nacional. "
        "Utilize este arquivo como base para implementar novas consultas (Tesouro Direto, DPF, etc.)."
    )
    icon = "🪙"
    icon_class = "icon-tesouro"
    badge = "Tesouro Direto"
    badge_class = "badge-dynamic"
    tags = ["tesouro", "ckan", "renda_fixa", "titulos_publicos"]
    source = "Tesouro Transparente — Tesouro Nacional (tesourotransparente.gov.br)"

    # Resource ID de exemplo do CKAN
    resource_id = "exemplo-resource-id"

    def fetch(self) -> pd.DataFrame:
        """
        Executa a coleta e transformação dos dados do CKAN.
        """
        log.info(f"Consultando resource do Tesouro Transparente: {self.resource_id}")

        registros = self.fetch_resource(self.resource_id, limit=50)
        if not registros:
            log.warning("Nenhum dado retornado pelo Tesouro Transparente.")
            return pd.DataFrame()

        data_captura, _ = agora_brt()
        linhas_normalizadas = []

        for item in registros:
            linhas_normalizadas.append(
                {
                    "data_captura": data_captura,
                    "data_referencia": item.get("Data Base") or item.get("data", ""),
                    "titulo": item.get("Tipo Titulo") or item.get("titulo", ""),
                    "vencimento": item.get("Data Vencimento") or item.get("vencimento", ""),
                    "taxa_compra": item.get("Taxa Compra Manha") or item.get("taxa_compra", ""),
                    "pu_compra": item.get("PU Compra Manha") or item.get("pu_compra", ""),
                }
            )

        df = pd.DataFrame(linhas_normalizadas)
        log.info(f"{len(df)} registros preparados com sucesso.")
        return df


if __name__ == "__main__":
    TesouroTransparenteTemplateScraper().run()
