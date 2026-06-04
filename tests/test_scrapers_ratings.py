import sys
from pathlib import Path
import pytest
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.fitch_ratings_brasil import FitchRatingsBrasilScraper


def test_fitch_ratings_brasil_scraper_fetch():
    """Deve testar o método fetch da classe FitchRatingsBrasilScraper e verificar as colunas e formato."""
    scraper = FitchRatingsBrasilScraper()
    df = scraper.fetch()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    expected_cols = [
        "nome",
        "link",
        "Tipo de Rating",
        "Rating",
        "Data da Ação de Rating",
        "CreditWatch/ Perspectiva",
        "Data do CreditWatch/ Perspectiva",
    ]
    for col in expected_cols:
        assert col in df.columns
