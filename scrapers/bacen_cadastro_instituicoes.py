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


def _gerar_trimestres_desde(ano_inicio: int = 2020) -> list[str]:
    """Retorna lista de todos os trimestres desde ano_inicio até a data atual (ex.: ['202606', '202603', ...])."""
    hoje = datetime.date.today()
    trimestres = []
    for ano in range(ano_inicio, hoje.year + 1):
        for mes in [3, 6, 9, 12]:
            if ano == hoje.year and mes > hoje.month:
                break
            trimestres.append(f"{ano}{mes:02d}")
    return sorted(trimestres, reverse=True)


def _gerar_trimestres_recentes(n_trimestres: int = 4) -> list[str]:
    """Retorna lista dos últimos períodos trimestrais (ex.: ['202606', '202603', ...])."""
    return _gerar_trimestres_desde()[:n_trimestres]


def _obter_datas_bases_existentes(arquivo: Path) -> set[str]:
    """Lê as datas-base (ISO 'YYYY-MM-DD') já presentes no arquivo CSV."""
    if not arquivo.exists() or arquivo.stat().st_size == 0:
        return set()
    try:
        df_existente = pd.read_csv(arquivo, usecols=["data_base"], dtype=str)
        return set(df_existente["data_base"].dropna().unique())
    except Exception as e:
        log.warning(f"Não foi possível ler datas-base existentes de {arquivo}: {e}")
        return set()


def capturar_cadastro_trimestre(anomes: str) -> list[dict]:
    """
    Busca o cadastro de instituições financeiras para o trimestre informado na API Olinda BCB.
    Retorna lista de dicionários normalizados com enriquecimento semântico.
    """
    url = ODATA_URL_TEMPLATE.format(anomes=anomes)
    log.info(f"Requisitando cadastro IFData para o período {anomes}...")

    try:
        resp = requests.get(url, headers=HEADERS, timeout=45)
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


def capturar(ano_inicio: int = 2020, recalcular_tudo: bool = False) -> list[dict]:
    """
    Busca o cadastro de instituições financeiras no Olinda BCB.
    Se recalcular_tudo for False, identifica os trimestres faltantes no arquivo data/bacen_cadastro_instituicoes.csv
    desde ano_inicio, além de garantir a atualização dos 2 trimestres mais recentes.
    """
    todos_trimestres = _gerar_trimestres_desde(ano_inicio=ano_inicio)
    datas_existentes = set() if recalcular_tudo else _obter_datas_bases_existentes(ARQUIVO)

    trimestres_alvo = []
    for anomes in todos_trimestres:
        dt_iso = _formatar_data_base(anomes)
        # Sempre busca os 2 trimestres mais recentes (para revisões) ou se não estiver no CSV
        if recalcular_tudo or dt_iso not in datas_existentes or anomes in todos_trimestres[:2]:
            trimestres_alvo.append(anomes)

    if not trimestres_alvo:
        log.info("Todos os trimestres desde 2020 já estão presentes no dataset. Buscando o mais recente para checagem.")
        trimestres_alvo = todos_trimestres[:1]

    log.info(f"Trimestres a capturar ({len(trimestres_alvo)}): {trimestres_alvo}")
    todos_registros = []

    for anomes in trimestres_alvo:
        regs = capturar_cadastro_trimestre(anomes)
        if regs:
            todos_registros.extend(regs)

    return todos_registros


class BacenCadastroInstituicoesScraper(BaseScraper):
    name = "bacen_cadastro_instituicoes"
    group = "bcb"
    enabled = True
    phase = 1
    accumulate = True
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

    def __init__(self, ano_inicio: int = 2020, recalcular_tudo: bool = False):
        super().__init__()
        self.ano_inicio = ano_inicio
        self.recalcular_tudo = recalcular_tudo

    def fetch(self) -> pd.DataFrame:
        log.info(f"=== BACEN — Cadastro de Instituições Financeiras (IFData desde {self.ano_inicio}) ===")
        dados = capturar(ano_inicio=self.ano_inicio, recalcular_tudo=self.recalcular_tudo)
        if not dados:
            return pd.DataFrame(columns=CABECALHO)

        df = pd.DataFrame(dados)
        df = df.sort_values(by=["data_base", "nome_instituicao", "codigo_instituicao"])
        colunas = [c for c in CABECALHO if c in df.columns]
        return df[colunas]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scraper BACEN Cadastro de Instituições (IF.data)")
    parser.add_argument("--desde", type=int, default=2020, help="Ano inicial para a carga histórica (padrão: 2020)")
    parser.add_argument("--recalcular-tudo", action="store_true", help="Força a recarga completa de todos os trimestres")
    args = parser.parse_args()

    scraper = BacenCadastroInstituicoesScraper(ano_inicio=args.desde, recalcular_tudo=args.recalcular_tudo)
    scraper.run()
