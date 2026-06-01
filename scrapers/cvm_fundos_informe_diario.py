"""
scrapers/cvm_fundos_informe_diario.py
--------------------------------------
Informe diário de fundos de investimento — CVM dados abertos (ZIP com CSV).

Fonte: https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{YYYYMM}.zip
Campos: TP_FUNDO_CLASSE, CNPJ_FUNDO_CLASSE, ID_SUBCLASSE, DT_COMPTC,
        VL_TOTAL, VL_QUOTA, VL_PATRIM_LIQ, CAPTC_DIA, RESG_DIA, NR_COTST
"""

import sys
import time
import zipfile
from datetime import date, timedelta
from io import BytesIO, StringIO
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import get_logger, agora_brt, limpar, salvar_csv

log = get_logger("cvm_fundos_informe_diario")

ARQUIVO = Path("data/cvm_fundos_informe_diario.csv")

CABECALHO = [
    "data_captura",
    "hora_captura",
    "tp_fundo_classe",
    "cnpj_fundo_classe",
    "id_subclasse",
    "dt_comptc",
    "vl_total",
    "vl_quota",
    "vl_patrim_liq",
    "captc_dia",
    "resg_dia",
    "nr_cotst",
]

URL_TPL = (
    "https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/"
    "inf_diario_fi_{yyyymm}.zip"
)


def _url_referencia() -> tuple[str, date]:
    """Tenta o mês atual, depois o anterior."""
    ref = date.today() - timedelta(days=4)  # CVM publica com ~4 dias de atraso
    for _ in range(3):
        url = URL_TPL.format(yyyymm=ref.strftime("%Y%m"))
        try:
            resp = requests.head(url, timeout=15)
            if resp.status_code == 200:
                return url, ref
        except Exception:
            pass
        # Tenta mês anterior
        ref = (ref.replace(day=1) - timedelta(days=1))
    return URL_TPL.format(yyyymm=ref.strftime("%Y%m")), ref


def capturar() -> list[dict]:
    url, data_ref = _url_referencia()
    log.info(f"Baixando informe diário CVM: {url}")

    for tentativa in range(1, 4):
        try:
            resp = requests.get(url, timeout=120)  # arquivo pode ser grande
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning(f"Tentativa {tentativa}/3: {e}")
            if tentativa == 3:
                log.error("Falha ao baixar informe diário CVM.")
                sys.exit(1)
            time.sleep(10)

    # Abre ZIP em memória
    try:
        zf = zipfile.ZipFile(BytesIO(resp.content))
    except zipfile.BadZipFile:
        log.error("Arquivo ZIP inválido da CVM.")
        sys.exit(1)

    csv_name = next((n for n in zf.namelist() if n.endswith(".csv")), None)
    if not csv_name:
        log.error("Nenhum CSV no ZIP da CVM.")
        sys.exit(1)

    raw = zf.read(csv_name)
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            texto = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        texto = raw.decode("utf-8", errors="replace")

    import csv
    reader = csv.DictReader(StringIO(texto), delimiter=";")
    data_captura, hora_captura = agora_brt()

    CAMPOS = {
        "TP_FUNDO_CLASSE": "tp_fundo_classe",
        "CNPJ_FUNDO_CLASSE": "cnpj_fundo_classe",
        "ID_SUBCLASSE": "id_subclasse",
        "DT_COMPTC": "dt_comptc",
        "VL_TOTAL": "vl_total",
        "VL_QUOTA": "vl_quota",
        "VL_PATRIM_LIQ": "vl_patrim_liq",
        "CAPTC_DIA": "captc_dia",
        "RESG_DIA": "resg_dia",
        "NR_COTST": "nr_cotst",
    }

    registros = []
    for row in reader:
        registro = {"data_captura": data_captura, "hora_captura": hora_captura}
        for campo_csv, campo_nosso in CAMPOS.items():
            registro[campo_nosso] = limpar(row.get(campo_csv, ""))
        registros.append(registro)

    if not registros:
        log.error("Nenhum registro no informe diário CVM.")
        sys.exit(1)

    log.info(f"{len(registros)} registros do informe diário CVM capturados.")
    return registros


def main():
    log.info("=== CVM — Informe Diário de Fundos ===")
    salvar_csv(ARQUIVO, capturar(), CABECALHO,
               chaves_dedup=["data_captura", "cnpj_fundo_classe", "dt_comptc"])


if __name__ == "__main__":
    main()
