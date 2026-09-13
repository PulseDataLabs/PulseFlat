"""
scrapers/bacen_cadastro_instituicoes.py
---------------------------------------
Cadastro Geral de Instituições Financeiras e demais entidades autorizadas a funcionar
pelo Banco Central do Brasil (SFN / IF.data).

Consome os dados oficiais da API OData Olinda do Banco Central do Brasil:
https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataCadastro

Saída:
- data/bacen_cadastro_instituicoes.csv (Snapshot cadastral com enriquecimento semântico)
"""

import datetime
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.base import BaseScraper
from utils import agora_brt, get_logger, limpar

log = get_logger("bacen_cadastro_instituicoes")

ARQUIVO = Path("data/bacen_cadastro_instituicoes.csv")

CABECALHO = [
    "data_captura",
    "data_base",
    "codigo_instituicao",
    "nome_instituicao",
    "cnpj_instituicao_lider",
    "situacao",
    "situacao_desc",
    "segmento_prudencial",
    "tipo_consolidacao",
    "tipo_consolidacao_desc",
    "tipo_detalhamento",
    "tipo_detalhamento_desc",
    "tipo_controle",
    "tipo_controle_desc",
    "atividade",
    "uf",
    "municipio",
    "ano_mes_inicio_atividade",
    "codigo_conglomerado_financeiro",
    "codigo_conglomerado_prudencial",
]

ODATA_URL_TEMPLATE = (
    "https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/"
    "IfDataCadastro(AnoMes=@AnoMes)?@AnoMes={anomes}&$format=json"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
}

# Dicionários de mapeamento e enriquecimento semântico
MAPA_TCB = {
    "B1": "Bancos Comerciais e Múltiplos com Carteira Comercial",
    "B2": "Bancos Múltiplos sem Carteira Comercial, Investimento e Desenvolvimento",
    "B3S": "Cooperativas de Crédito Singulares",
    "B3C": "Cooperativas Centrais e Confederações",
    "B4": "Outras Instituições Bancárias",
    "N1": "Sociedades Distribuidoras e Corretoras de Títulos e Câmbio",
    "N2": "Sociedades de Crédito, Financiamento e Investimento e Arrendamento Mercantil",
    "N3": "Sociedades de Crédito Imobiliário e Associações de Poupança",
    "N4": "Instituições de Pagamento, SCDs, SEPs e Outras Não Bancárias",
}

MAPA_TC = {
    1: "Público",
    2: "Privado Nacional",
    3: "Controle Estrangeiro",
}

MAPA_TD = {
    "C": "Consolidado",
    "I": "Individual",
}

MAPA_SITUACAO = {
    "A": "Ativa",
    "I": "Inativa / Cancelada",
    "F": "Fase de Liquidação",
    "LE": "Liquidação Extrajudicial",
    "LO": "Liquidação Ordinária",
    "RAET": "Regime de Administração Especial Temporária",
}


def _formatar_data_base(anomes: str) -> str:
    """Converte 'YYYYMM' (mês de fim de trimestre) para data ISO 'YYYY-MM-DD'."""
    s = str(anomes or "").strip()
    if len(s) == 6 and s.isdigit():
        ano = s[:4]
        mes = s[4:6]
        dias_fim = {"03": "31", "06": "30", "09": "30", "12": "31"}
        dia = dias_fim.get(mes, "28")
        return f"{ano}-{mes}-{dia}"
    return s


def _formatar_inicio_atividade(val) -> str:
    """Converte 'YYYYMM' (início da atividade) para 'YYYY-MM'."""
    s = str(val or "").strip()
    if len(s) == 6 and s.isdigit():
        return f"{s[:4]}-{s[4:6]}"
    return s


def _formatar_cnpj_raiz(cnpj_str: str) -> str:
    """Formata o CNPJ de 8 dígitos para XX.XXX.XXX."""
    s = str(cnpj_str or "").strip()
    if len(s) == 8 and s.isdigit():
        return f"{s[:2]}.{s[2:5]}.{s[5:8]}"
    return s


def _gerar_trimestres_recentes(n_trimestres: int = 4) -> list[str]:
    """Retorna lista dos últimos períodos trimestrais (ex.: ['202606', '202603', ...])."""
    hoje = datetime.date.today()
    ano = hoje.year
    mes = hoje.month

    # Meses padrão de divulgação do IFData: 3, 6, 9, 12
    meses_trimestre = [3, 6, 9, 12]
    # Determina o trimestre corrente ou anterior
    trimestres = []
    curr_ano = ano
    # Encontra o último trimestre fechado
    curr_mes = max([m for m in meses_trimestre if m <= mes] or [12])
    if mes < 3:
        curr_ano -= 1
        curr_mes = 12

    for _ in range(n_trimestres):
        trimestres.append(f"{curr_ano}{curr_mes:02d}")
        idx = meses_trimestre.index(curr_mes)
        if idx == 0:
            curr_mes = 12
            curr_ano -= 1
        else:
            curr_mes = meses_trimestre[idx - 1]

    return trimestres


def capturar_cadastro_trimestre(anomes: str) -> list[dict]:
    """
    Busca o cadastro de instituições financeiras para o trimestre informado na API Olinda BCB.
    Retorna lista de dicionários normalizados com enriquecimento semântico.
    """
    url = ODATA_URL_TEMPLATE.format(anomes=anomes)
    log.info(f"Requisitando cadastro IFData para o período {anomes}...")

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            log.warning(f"Status HTTP {resp.status_code} ao buscar período {anomes}.")
            return []

        dados_json = resp.json()
        itens = dados_json.get("value", [])
        if not itens:
            log.warning(f"Nenhum registro no array 'value' para o período {anomes}.")
            return []

        data_captura, _ = agora_brt()
        data_base_iso = _formatar_data_base(anomes)
        registros = []

        for item in itens:
            cod_inst = limpar(str(item.get("CodInst") or ""))
            if not cod_inst:
                continue

            tcb = limpar(str(item.get("Tcb") or ""))
            tc = item.get("Tc")
            td = limpar(str(item.get("Td") or ""))
            sit = limpar(str(item.get("Situacao") or ""))
            sr = limpar(str(item.get("Sr") or ""))

            registros.append(
                {
                    "data_captura": data_captura,
                    "data_base": data_base_iso,
                    "codigo_instituicao": cod_inst,
                    "nome_instituicao": limpar(str(item.get("NomeInstituicao") or "")),
                    "cnpj_instituicao_lider": _formatar_cnpj_raiz(item.get("CnpjInstituicaoLider")),
                    "situacao": sit,
                    "situacao_desc": MAPA_SITUACAO.get(sit, sit),
                    "segmento_prudencial": sr,
                    "tipo_consolidacao": tcb,
                    "tipo_consolidacao_desc": MAPA_TCB.get(tcb, tcb),
                    "tipo_detalhamento": td,
                    "tipo_detalhamento_desc": MAPA_TD.get(td, td),
                    "tipo_controle": tc if tc is not None else "",
                    "tipo_controle_desc": MAPA_TC.get(tc, str(tc or "")),
                    "atividade": limpar(str(item.get("Atividade") or "")),
                    "uf": limpar(str(item.get("Uf") or "")),
                    "municipio": limpar(str(item.get("Municipio") or "")),
                    "ano_mes_inicio_atividade": _formatar_inicio_atividade(item.get("DataInicioAtividade")),
                    "codigo_conglomerado_financeiro": limpar(str(item.get("CodConglomeradoFinanceiro") or "")),
                    "codigo_conglomerado_prudencial": limpar(str(item.get("CodConglomeradoPrudencial") or "")),
                }
            )

        log.info(f"{len(registros)} instituições capturadas para a data-base {data_base_iso}.")
        return registros

    except Exception as e:
        log.error(f"Erro ao requisitar cadastro IFData ({url}): {e}")
        return []


def capturar() -> list[dict]:
    """
    Busca o período trimestral mais recente disponível no Olinda BCB.
    Tenta os trimestres mais recentes em ordem decrescente até obter sucesso.
    """
    periodos = _gerar_trimestres_recentes(n_trimestres=4)
    for anomes in periodos:
        regs = capturar_cadastro_trimestre(anomes)
        if regs:
            return regs
    log.warning("Nenhum dado retornado em nenhum dos trimestres recentes testados.")
    return []


class BacenCadastroInstituicoesScraper(BaseScraper):
    name = "bacen_cadastro_instituicoes"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = False
    compress = False
    chaves_dedup = ["data_base", "codigo_instituicao"]

    # Catálogo de Metadados
    title = "BACEN — Cadastro de Instituições Financeiras (IF.data)"
    description = (
        "Cadastro completo de instituições financeiras e entidades autorizadas pelo Banco Central do Brasil "
        "no Sistema Financeiro Nacional (SFN / IF.data). Inclui classificação prudencial (S1-S5), tipo de consolidação, "
        "conglomerados, atividade regulatória, tipo de controle, localização e situação cadastral."
    )
    icon = "🏛️"
    icon_class = "icon-bcb"
    badge = "Trimestral"
    badge_class = "badge-quarterly"
    tags = [
        "bacen",
        "bcb",
        "instituições financeiras",
        "bancos",
        "cooperativas",
        "ifdata",
        "sfn",
        "regulação",
        "fintech",
    ]
    source = "BACEN"

    def fetch(self) -> pd.DataFrame:
        log.info("=== BACEN — Cadastro de Instituições Financeiras (IFData) ===")
        dados = capturar()
        if not dados:
            return pd.DataFrame(columns=CABECALHO)

        df = pd.DataFrame(dados)
        # Ordena por nome da instituição
        df = df.sort_values(by=["nome_instituicao", "codigo_instituicao"])
        colunas = [c for c in CABECALHO if c in df.columns]
        return df[colunas]


if __name__ == "__main__":
    BacenCadastroInstituicoesScraper().run()
