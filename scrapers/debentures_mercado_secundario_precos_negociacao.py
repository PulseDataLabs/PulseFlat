import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class DebenturesMercadoSecundarioPrecosNegociacaoScraper(GenericScraper):
    group = "anbima"
    enabled = True
    phase = 1
    resource_name = "Debêntures - Preços de Negociação"


def main():
    DebenturesMercadoSecundarioPrecosNegociacaoScraper().run()


if __name__ == "__main__":
    main()
