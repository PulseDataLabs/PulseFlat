"""
scrapers/cvm_fundos_cadastro.py
--------------------------------
Cadastro de fundos de investimento (CAD/FI) da CVM — dados abertos.

Fonte: https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv
Campos principais: TP_FUNDO, CNPJ_FUNDO, DENOM_SOCIAL, DT_REG, SIT,
                   CLASSE, ADMIN, GESTOR, CUSTODIANTE, CLASSE_ANBIMA
"""

import sys
import time
from io import StringIO
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv

log = get_logger("cvm_fundos_cadastro")

ARQUIVO = Path("data/cvm_fundos_cadastro.csv")
URL = "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"

CABECALHO = [
    "data_captura",
    
    "tp_fundo",
    "cnpj_fundo",
    "denom_social",
    "dt_reg",
    "dt_const",
    "cd_cvm",
    "dt_cancel",
    "sit",
    "dt_ini_sit",
    "dt_ini_ativ",
    "classe",
    "rentab_fundo",
    "condom",
    "fundo_cotas",
    "fundo_exclusivo",
    "trib_lprazo",
    "publico_alvo",
    "entid_invest",
    "taxa_perfm",
    "taxa_adm",
    "vl_patrim_liq",
    "dt_patrim_liq",
    "admin",
    "gestor",
    "auditor",
    "custodiante",
    "controlador",
    "classe_anbima",
]


def capturar() -> list[dict]:
    log.info(f"Baixando cadastro de fundos CVM: {URL}")

    for tentativa in range(1, 4):
        try:
            resp = requests.get(URL, timeout=60)
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error("Falha ao baixar cad_fi.csv da CVM.")
                sys.exit(1)
            time.sleep(10)

    # Detecta encoding
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            texto = resp.content.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        texto = resp.content.decode("utf-8", errors="replace")

    import csv
    reader = csv.DictReader(StringIO(texto), delimiter=";")
    data_captura, _ = agora_brt()

    # Mapeamento de colunas do CSV para nosso schema (lowercase)
    CAMPOS_CSV = {
        "TP_FUNDO": "tp_fundo",
        "CNPJ_FUNDO": "cnpj_fundo",
        "DENOM_SOCIAL": "denom_social",
        "DT_REG": "dt_reg",
        "DT_CONST": "dt_const",
        "CD_CVM": "cd_cvm",
        "DT_CANCEL": "dt_cancel",
        "SIT": "sit",
        "DT_INI_SIT": "dt_ini_sit",
        "DT_INI_ATIV": "dt_ini_ativ",
        "CLASSE": "classe",
        "RENTAB_FUNDO": "rentab_fundo",
        "CONDOM": "condom",
        "FUNDO_COTAS": "fundo_cotas",
        "FUNDO_EXCLUSIVO": "fundo_exclusivo",
        "TRIB_LPRAZO": "trib_lprazo",
        "PUBLICO_ALVO": "publico_alvo",
        "ENTID_INVEST": "entid_invest",
        "TAXA_PERFM": "taxa_perfm",
        "TAXA_ADM": "taxa_adm",
        "VL_PATRIM_LIQ": "vl_patrim_liq",
        "DT_PATRIM_LIQ": "dt_patrim_liq",
        "ADMIN": "admin",
        "GESTOR": "gestor",
        "AUDITOR": "auditor",
        "CUSTODIANTE": "custodiante",
        "CONTROLADOR": "controlador",
        "CLASSE_ANBIMA": "classe_anbima",
    }

    registros = []
    for row in reader:
        for campo_csv, campo_nosso in CAMPOS_CSV.items():
            registro[campo_nosso] = limpar(row.get(campo_csv, ""))
        registros.append(registro)

    if not registros:
        log.error("Nenhum fundo extraído do cad_fi.csv.")
        sys.exit(1)

    log.info(f"{len(registros)} fundos capturados do cadastro CVM.")
    return registros


def main():
    log.info("=== CVM — Cadastro de Fundos (cad_fi.csv) ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "cnpj_fundo"])


if __name__ == "__main__":
    main()
