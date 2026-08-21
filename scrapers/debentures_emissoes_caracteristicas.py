import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrapers.generic_scraper import GenericScraper


class DebenturesEmissoesCaracteristicasScraper(GenericScraper):
    title = "Debêntures — Emissões e Características"
    description = "Cadastro detalhado de todas as emissões públicas e privadas de debêntures registradas no Brasil, com taxa de remuneração (spread), indexador, data de emissão, vencimento e garantias."
    badge = "Diário"
    source = "Debêntures"
    tags = ['debentures', 'emissoes', 'caracteristicas', 'anbima', 'snd']
    group = "anbima"
    enabled = True
    phase = 1
    resource_name = "Debêntures - Características de Emissões"


def main():
    DebenturesEmissoesCaracteristicasScraper().run()


if __name__ == "__main__":
    main()
