"""
tests/test_scrapers.py
-----------------------
Testes unitários para scrapers genéricos e utilitários de scraping.
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_generic_scraper_json(requests_mock, tmp_path, monkeypatch):
    """Deve baixar, processar e salvar corretamente dados de um recurso json genérico."""
    import yaml
    from scrapers.generic_scraper import run_resource

    mock_config = {
        "resources": [
            {
                "name": "teste_json",
                "url": "https://jsonplaceholder.typicode.com/posts/",
                "file_name": "teste_json.json",
                "type_response": "json"
            }
        ]
    }
    monkeypatch.setattr(yaml, "safe_load", lambda f: mock_config)

    mock_data = [
        {"id": 1, "title": "Post 1", "body": "Body 1", "userId": 10},
        {"id": 2, "title": "Post 2", "body": "Body 2", "userId": 20}
    ]

    requests_mock.get(
        "https://jsonplaceholder.typicode.com/posts/",
        json=mock_data,
        status_code=200
    )

    out_file = tmp_path / "teste_json.csv"
    run_resource("teste_json", output_file_override=out_file)

    assert out_file.exists()
    import csv
    with open(out_file, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert rows[0]["id"] == "1"
    assert rows[0]["title"] == "Post 1"
    assert rows[0]["body"] == "Body 1"
    assert rows[0]["userid"] == "10"
