import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class B3CarteiraTeoricaIbxlScraper(GenericScraper):
    title = "B3 — Carteira Teórica IBX 50"
    description = "Composição e pesos das 50 ações mais negociadas da bolsa brasileira (IBrX-50)."
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
