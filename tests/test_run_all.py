"""
tests/test_run_all.py
---------------------
Testes unitários para o orquestrador run_all.py e sua descoberta dinâmica de scrapers.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run_all import discover_scrapers


def test_discover_scrapers_structure():
    """Garante que a descoberta dinâmica de scrapers retorna a estrutura de dados correta."""
    scrapers = discover_scrapers()

    assert isinstance(scrapers, dict)
    assert len(scrapers) > 0

    # Valida se alguns dos scrapers principais estão presentes
    assert "bcb_ptax" in scrapers
    assert "bcb_sgs" in scrapers

    # Valida estrutura de chaves internas
    for module_name, info in scrapers.items():
        assert "group" in info
        assert "enabled" in info
        assert "phase" in info
        assert "class_name" in info
        assert "title" in info

        assert isinstance(info["group"], str)
        assert isinstance(info["enabled"], bool)
        assert isinstance(info["phase"], int)


def test_discover_scrapers_phases():
    """Garante que as fases de precedência de dependências foram carregadas corretamente."""
    scrapers = discover_scrapers()

    # Todos os scrapers remanescentes devem ser da Fase 1
    for name, info in scrapers.items():
        assert info["phase"] == 1


def test_save_pipeline_status_prunes_obsolete(tmp_path, monkeypatch):
    """Garante que save_pipeline_status remove scrapers excluídos/inativos e não infla o total/sucesso."""
    import json

    from run_all import discover_scrapers, save_pipeline_status

    status_dir = tmp_path / "data"
    status_dir.mkdir(parents=True, exist_ok=True)
    status_json = status_dir / "pipeline_status.json"
    status_js = status_dir / "pipeline_status.js"

    # Simula status anterior contendo um scraper obsoleto com status success
    old_data = {
        "scrapers": {
            "scraper_obsoleto_inexistente": {
                "status": "success",
                "elapsed_seconds": 1.5,
                "error": None,
                "timestamp": "2025-01-01T10:00:00",
            }
        },
        "drifts": {},
    }
    with status_json.open("w", encoding="utf-8") as f:
        json.dump(old_data, f)

    save_pipeline_status(
        results={},
        total_elapsed=10.0,
        status_path=status_json,
        status_js_path=status_js,
    )

    with status_json.open("r", encoding="utf-8") as f:
        saved = json.load(f)

    active = {k: v for k, v in discover_scrapers().items() if v["enabled"]}
    assert "scraper_obsoleto_inexistente" not in saved["scrapers"]
    assert saved["summary"]["total"] == len(active)
    assert saved["summary"]["success"] <= saved["summary"]["total"]

