import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class B3CarteiraTeoricaAgfsIagroScraper(GenericScraper):
    title = "B3 — Carteira Teórica AGFS / IAGRO"
    description = "Composição diária e ponderação teórica das ações e ativos elegíveis ao Índice Agro B3 (IAGRO / AGFS), refletindo a representatividade do agronegócio no mercado acionário brasileiro."
    badge = "Quadrimestral"
    source = "B3"
    tags = ['b3', 'carteira_teorica', 'agfs', 'iagro', 'indices']
    group = "b3"
    enabled = True
    phase = 1
    resource_name = "B3 - Carteira Teórica - AGFS - IAGRO"


def main():
    B3CarteiraTeoricaAgfsIagroScraper().run()


if __name__ == "__main__":
    main()
