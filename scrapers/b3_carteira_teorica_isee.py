import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class B3CarteiraTeoricaIseeScraper(GenericScraper):
    resource_name = "B3 - Carteira Teórica - ISEE"


def main():
    B3CarteiraTeoricaIseeScraper().run()


if __name__ == "__main__":
    main()
