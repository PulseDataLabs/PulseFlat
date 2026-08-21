import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class CvmFundosClasseScraper(GenericScraper):
    title = "CVM — Registro de Classes e Subclasses de Fundos (RCVM 175)"
    description = "Estrutura moderna de classes e subclasses de cotas sob a Resolução CVM 175."
    badge = "Diário"
    source = "CVM"
    tags = ['cvm', 'fundos', 'classes', 'subclasses', 'rcvm175']
    group = "cvm"
    enabled = True
    phase = 1
    resource_name = "CVM - Fundos de Investimento, Classes e Subclasses de Cotas CVM175"


def main():
    CvmFundosClasseScraper().run()


if __name__ == "__main__":
    main()
