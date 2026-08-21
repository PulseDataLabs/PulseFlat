import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class B3CarteiraTeoricaIseeScraper(GenericScraper):
    title = "B3 — Carteira Teórica ISEE (Sustentabilidade)"
    description = "Composição do Índice de Sustentabilidade Empresarial (ISE B3)."
    badge = "Quadrimestral"
    source = "B3"
    tags = ['b3', 'carteira_teorica', 'isee', 'sustentabilidade', 'indices']
    group = "b3"
    enabled = True
    phase = 1
    resource_name = "B3 - Carteira Teórica - ISEE"


def main():
    B3CarteiraTeoricaIseeScraper().run()


if __name__ == "__main__":
    main()
