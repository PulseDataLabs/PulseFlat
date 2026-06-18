import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class DebenturesEmissoesCaracteristicasScraper(GenericScraper):
    group = "anbima"
    enabled = True
    phase = 1
    resource_name = "Debêntures - Características de Emissões"


def main():
    DebenturesEmissoesCaracteristicasScraper().run()


if __name__ == "__main__":
    main()
