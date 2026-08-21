import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class B3CarteiraTeoricaBdrxScraper(GenericScraper):
    title = "B3 — Carteira Teórica BDRX"
    description = "Composição teórica e pesos ponderados dos Brazilian Depositary Receipts (BDRs Não Patrocinados e Patrocinados) integrantes do Índice de BDRs da B3 (BDRX)."
    badge = "Quadrimestral"
    source = "B3"
    tags = ['b3', 'carteira_teorica', 'bdrx', 'indices']
    group = "b3"
    enabled = True
    phase = 1
    resource_name = "B3 - Carteira Teórica - BDRX"


def main():
    B3CarteiraTeoricaBdrxScraper().run()


if __name__ == "__main__":
    main()
