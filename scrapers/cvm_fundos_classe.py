import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import run_resource


def main():
    run_resource("CVM - Fundos de Investimento, Classes e Subclasses de Cotas CVM175")


if __name__ == "__main__":
    main()
