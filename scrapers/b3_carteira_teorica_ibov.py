import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class B3CarteiraTeoricaIbovScraper(GenericScraper):
    title = "B3 — Carteira Teórica IBOVESPA"
    description = "Composição oficial, quantidade teórica e participação percentual ponderada de todas as ações e units componentes do Índice Bovespa (IBOVESPA), o principal benchmark de renda variável da B3."
    badge = "Quadrimestral"
    source = "B3"
    tags = ['b3', 'carteira_teorica', 'ibov', 'ibovespa', 'indices']
    group = "b3"
    enabled = True
    phase = 1
    resource_name = "B3 - Carteira Teórica - IBOV"


def main():
    B3CarteiraTeoricaIbovScraper().run()


if __name__ == "__main__":
    main()
