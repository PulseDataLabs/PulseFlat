"""
tests/test_utils.py
-------------------
Testes básicos dos utilitários compartilhados.

Rodar: python -m pytest tests/ -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import agora_brt, limpar, b64_encode_params
import json
from base64 import b64decode


def test_agora_brt_formato():
    data, hora = agora_brt()
    assert len(data) == 10 and data[4] == "-" and data[7] == "-", "Data deve ser YYYY-MM-DD"
    assert len(hora) == 8 and hora[2] == ":" and hora[5] == ":", "Hora deve ser HH:MM:SS"


def test_limpar_none():
    assert limpar(None) == ""


def test_limpar_espacos():
    assert limpar("  PETR4  ") == "PETR4"


def test_limpar_numero():
    assert limpar(123) == "123"


def test_b64_encode_params_decodificavel():
    params = {"language": "pt-br", "pageNumber": 1, "pageSize": 100, "fundsType": "FII"}
    encoded = b64_encode_params(params)
    decoded = json.loads(b64decode(encoded).decode("utf-8"))
    assert decoded == params


def test_b64_encode_sem_espacos():
    """A B3 exige JSON sem espaços nos separadores."""
    params = {"a": 1, "b": 2}
    encoded = b64_encode_params(params)
    decoded_str = b64decode(encoded).decode("utf-8")
    assert " " not in decoded_str
