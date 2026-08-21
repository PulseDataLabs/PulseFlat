import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class B3CarteiraTeoricaSmllScraper(GenericScraper):
    title = "B3 — Carteira Teórica SMLL (Small Caps)"
    description = "Composição e ponderação do Índice Small Cap da B3."
    badge = "Quadrimestral"
    source = "B3"
    tags = ['b3', 'carteira_teorica', 'smll', 'small_caps', 'indices']
    group = "b3"
    enabled = True
    phase = 1
    resource_name = "B3 - Carteira Teórica - SMLL"


def main():
    B3CarteiraTeoricaSmllScraper().run()


if __name__ == "__main__":
    main()
