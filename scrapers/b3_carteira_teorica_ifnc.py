import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class B3CarteiraTeoricaIfncScraper(GenericScraper):
    title = "B3 — Carteira Teórica IFNC (Financeiro)"
    description = "Composição do Índice Financeiro da B3 com bancos e instituições financeiras."
    badge = "Quadrimestral"
    source = "B3"
    tags = ['b3', 'carteira_teorica', 'ifnc', 'financeiro', 'indices']
    group = "b3"
    enabled = True
    phase = 1
    resource_name = "B3 - Carteira Teórica - IFNC"


def main():
    B3CarteiraTeoricaIfncScraper().run()


if __name__ == "__main__":
    main()
