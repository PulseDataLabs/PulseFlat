import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class B3CarteiraTeoricaSmllScraper(GenericScraper):
    group = "b3"
    enabled = True
    phase = 1
    resource_name = "B3 - Carteira Teórica - SMLL"


def main():
    B3CarteiraTeoricaSmllScraper().run()


if __name__ == "__main__":
    main()
