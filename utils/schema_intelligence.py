"""
utils/schema_intelligence.py
----------------------------
Motor de inteligência para detecção semântica de equivalência entre colunas,
reconciliação automática de Schema Drift e unificação de campos variantes.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Sequence
import pandas as pd

# Preposições e conectivos em português que costumam variar em nomes de colunas
STOPWORDS_PT = frozenset({"de", "da", "do", "dos", "das", "e", "o", "a", "em", "no", "na"})

# Mapeamento de abreviações e variações conhecidas
ABBREVIATION_MAP = {
    "du": "du",
    "d_u": "du",
    "dc": "dc",
    "d_c": "dc",
    "dt": "data",
    "num": "numero",
    "nr": "numero",
    "nu": "numero",
    "no": "numero",
    "qtd": "quantidade",
    "quant": "quantidade",
    "vl": "valor",
    "vlr": "valor",
    "val": "valor",
    "cod": "codigo",
    "ref": "referencia",
    "desc": "descricao",
    "pct": "percentual",
    "perc": "percentual",
    "tx": "taxa",
}

# Modificadores e termos excludentes (antônimos/dimensões distintas) que NUNCA devem ser unificados
EXCLUSIVE_MODIFIERS = frozenset({
    "min", "max", "inf", "sup", "minimo", "maximo", "inferior", "superior",
    "compra", "venda", "bid", "ask", "aberto", "fechado", "coberta", "descoberta",
    "brl", "usd", "eur", "ano", "mes", "dia", "diaria", "mensal", "anual",
    "anterior", "atual", "d0", "d1", "dma1", "terceiros", "proprios",
    "acoes", "opcoes", "novo", "antigo", "primario", "secundario",
    "ativo", "passivo", "credito", "debito", "ig", "hy",
    "sub", "sub_total", "subtotal", "total", "reer", "neer", "taxa", "cada",
    "prazo", "tipo", "criterio", "unidade", "carencia", "snd", "fora",
})


def _extract_digits(name: str) -> list[str]:
    """Extrai todas as sequências numéricas de uma string."""
    return re.findall(r"\d+", name)


def _tokenize(col: str) -> list[str]:
    """Divide a coluna em tokens limpos e normalizados."""
    col = unicodedata.normalize("NFKD", col.lower())
    col = "".join(c for c in col if not unicodedata.combining(c))
    tokens = [t for t in re.split(r"[^a-z0-9]+", col) if t]
    return tokens


def normalize_to_core(col: str) -> str:
    """
    Normaliza a coluna para sua raiz unificada:
    - Converte acentos
    - Remove underscores e conectivos em português
    - Trata sequências como d_u -> du
    """
    tokens = _tokenize(col)
    filtered = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        # Detecta sequência de letras soltas como 'd' e 'u'
        if i + 1 < len(tokens) and len(t) == 1 and len(tokens[i + 1]) == 1:
            combined = t + tokens[i + 1]
            if combined in ("du", "dc"):
                filtered.append(combined)
                i += 2
                continue
        if t in STOPWORDS_PT and len(tokens) > 1:
            i += 1
            continue
        # Aplica abreviações comuns
        filtered.append(ABBREVIATION_MAP.get(t, t))
        i += 1
    return "".join(filtered)


def are_columns_equivalent(col_a: str, col_b: str) -> bool:
    """
    Determina se duas colunas representam semanticamente o mesmo campo,
    com guard-rails rigorosos contra falsos positivos.
    """
    if col_a == col_b:
        return True

    # 1. Guard-rail numérico: Se números diferem (ex: 12_meses vs 24_meses, d0 vs d1), NUNCA são iguais
    digits_a = _extract_digits(col_a)
    digits_b = _extract_digits(col_b)
    if digits_a != digits_b:
        return False

    tokens_a = _tokenize(col_a)
    tokens_b = _tokenize(col_b)

    # Aplica abreviações conhecidas aos tokens antes de avaliar modificadores
    mapped_tokens_a = [ABBREVIATION_MAP.get(t, t) for t in tokens_a]
    mapped_tokens_b = [ABBREVIATION_MAP.get(t, t) for t in tokens_b]

    # 2. Guard-rail de modificadores exclusivos (ex: min vs max, compra vs venda, cada vs taxa)
    mods_a = set(mapped_tokens_a) & EXCLUSIVE_MODIFIERS
    mods_b = set(mapped_tokens_b) & EXCLUSIVE_MODIFIERS
    if mods_a != mods_b:
        return False

    # 3. Tratamento de sufixos espúrios de parsing como '_nan' (ex: total_global_ativos_nan vs total_global_ativos)
    clean_nan_a = re.sub(r"_nan$", "", col_a.lower())
    clean_nan_b = re.sub(r"_nan$", "", col_b.lower())
    if clean_nan_a == clean_nan_b and (col_a.endswith("_nan") or col_b.endswith("_nan")):
        return True

    # 4. Guard-rail Data vs Código/Valor: Se apenas uma coluna contém termo 'data'/'dt' no início
    has_date_a = any(t in ("data", "dt") for t in tokens_a[:2])
    has_date_b = any(t in ("data", "dt") for t in tokens_b[:2])
    if has_date_a != has_date_b:
        col_without_date = col_b if has_date_a else col_a
        tokens_no_date = _tokenize(col_without_date)
        id_or_val_terms = {"registro", "codigo", "numero", "patrimonio", "valor", "taxa", "preco", "volume", "saldo"}
        if any(t in tokens_no_date for t in id_or_val_terms):
            return False
        date_terms = {"data", "date", "dt", "dia", "mes", "ano", "vencimento", "referencia", "liquidacao"}
        if not any(t in tokens_no_date for t in date_terms):
            return False

    # 5. Regra de colapso de underscores simples (ex: duration_d_u vs duration_du)
    simple_a = re.sub(r"[^a-z0-9]", "", col_a.lower())
    simple_b = re.sub(r"[^a-z0-9]", "", col_b.lower())
    if simple_a == simple_b:
        return True

    # 4. Regra de raiz com remoção de conectivos PT e abreviações (ex: data_de_referencia vs data_referencia)
    core_a = normalize_to_core(col_a)
    core_b = normalize_to_core(col_b)
    if core_a == core_b:
        return True

    # 5. Tratamento de corrupção por perda de acentuação / caracteres faltantes (ex: pu_m_dio vs pu_medio)
    from difflib import SequenceMatcher
    if SequenceMatcher(None, core_a, core_b).ratio() >= 0.88:
        return True

    return False


def reconcile_columns(
    incoming_cols: Sequence[str], reference_cols: Sequence[str]
) -> dict[str, str]:
    """
    Compara as colunas recebidas (incoming) com uma lista de referência (canonical).
    Retorna um dicionário {col_variante_em_incoming: col_canonica_em_reference}.
    """
    mapping: dict[str, str] = {}
    ref_set = set(reference_cols)

    for inc in incoming_cols:
        if inc in ref_set:
            continue
        for ref in reference_cols:
            if are_columns_equivalent(inc, ref):
                mapping[inc] = ref
                break
    return mapping


def find_internal_duplicate_aliases(cols: Sequence[str]) -> dict[str, str]:
    """
    Varre uma lista de colunas para encontrar pares redundantes presentes
    simultaneamente (ex: duration_du E duration_d_u, data_referencia E data_de_referencia).
    Retorna {variante_redundante: canonica_preferida}.
    """
    mapping: dict[str, str] = {}
    col_list = list(cols)

    for i, c1 in enumerate(col_list):
        if c1 in mapping:
            continue
        for j in range(i + 1, len(col_list)):
            c2 = col_list[j]
            if c2 in mapping:
                continue
            if are_columns_equivalent(c1, c2):
                # Escolhe o nome canônico preferido:
                # 1. O que não tiver caracteres fragmentados por underscore como _d_u_ ou _m_
                # 2. O mais conciso e padronizado (ex: duration_du sobre duration_d_u)
                frag_1 = bool(re.search(r"_[a-z]_[a-z](_|$)", c1))
                frag_2 = bool(re.search(r"_[a-z]_[a-z](_|$)", c2))
                stop_1 = any(f"_{w}_" in f"_{c1}_" for w in STOPWORDS_PT)
                stop_2 = any(f"_{w}_" in f"_{c2}_" for w in STOPWORDS_PT)

                if frag_1 and not frag_2:
                    canonical, variant = c2, c1
                elif frag_2 and not frag_1:
                    canonical, variant = c1, c2
                elif stop_1 and not stop_2:
                    canonical, variant = c2, c1
                elif stop_2 and not stop_1:
                    canonical, variant = c1, c2
                elif len(c1) <= len(c2):
                    canonical, variant = c1, c2
                else:
                    canonical, variant = c2, c1

                mapping[variant] = canonical
    return mapping


def unify_dataframe_columns(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    """
    Unifica colunas de um DataFrame a partir de um mapeamento {variante: canonica}.
    Faz a mesclagem aditiva (coalesce) dos dados sem nenhuma perda de valor,
    removendo a coluna variante obsoleta.
    """
    if not mapping or df.empty:
        return df

    df_out = df.copy()
    for variant, canonical in mapping.items():
        if variant not in df_out.columns:
            continue

        if canonical in df_out.columns:
            canon_s = df_out[canonical].astype(str).replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
            var_s = df_out[variant].astype(str).replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
            merged_s = canon_s.combine_first(var_s).fillna("")
            df_out[canonical] = merged_s
            df_out = df_out.drop(columns=[variant])
        else:
            df_out = df_out.rename(columns={variant: canonical})

    return df_out
