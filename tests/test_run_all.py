"""
tests/test_run_all.py
---------------------
Testes unitários para o orquestrador run_all.py e sua descoberta dinâmica de scrapers.
"""

import sys
from pathlib import Path
import pytest

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
