import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class CvmFundosClasseScraper(GenericScraper):
    resource_name = "CVM - Fundos de Investimento, Classes e Subclasses de Cotas CVM175"


def main():
    CvmFundosClasseScraper().run()


if __name__ == "__main__":
    main()
