import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class B3CarteiraTeoricaIbxlScraper(GenericScraper):
    title = "B3 — Carteira Teórica IBX 50"
    description = "Composição teórica e pesos relativos das 50 ações de maior liquidez e negociabilidade no mercado à vista da B3 integrantes do Índice Brasil 50 (IBrX 50 / IBXL)."
    badge = "Quadrimestral"
    source = "B3"
    tags = ['b3', 'carteira_teorica', 'ibxl', 'ibrx50', 'indices']
    group = "b3"
    enabled = True
    phase = 1
    resource_name = "B3 - Carteira Teórica - IBXL"


def main():
    B3CarteiraTeoricaIbxlScraper().run()


if __name__ == "__main__":
    main()
