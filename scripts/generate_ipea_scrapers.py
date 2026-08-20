#!/usr/bin/env python
"""
scripts/generate_ipea_scrapers.py
---------------------------------
Gera programaticamente os arquivos de scrapers para a segunda rodada de séries mensais do Ipeadata.
"""

import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRAPERS_DIR = ROOT / "scrapers"

SERIES = [
    {
        "code": "FUNCEX12_XPT12",
        "name": "ipea_exportacoes_precos",
        "title": "Exportações Preços Índice",
        "desc": "Índice de preços das exportações gerais (média 2018 = 100).",
        "icon": "🚢",
        "class_name": "IpeaExportacoesPrecosScraper",
        "tags": ["exportacao", "precos", "comercio_exterior", "ipea"],
    },
    {
        "code": "FUNCEX12_MDPT12",
        "name": "ipea_importacoes_precos",
        "title": "Importações Preços Índice",
        "desc": "Índice de preços das importações gerais (média 2018 = 100).",
        "icon": "🚢",
        "class_name": "IpeaImportacoesPrecosScraper",
        "tags": ["importacao", "precos", "comercio_exterior", "ipea"],
    },
    {
        "code": "IGP12_IGPDI12",
        "name": "ipea_igp_di_indice",
        "title": "IGP-DI Índice Geral",
        "desc": "Índice Geral de Preços - Disponibilidade Interna (IGP-DI) - índice (ago 1994 = 100).",
        "icon": "📊",
        "class_name": "IpeaIgpDiIndiceScraper",
        "tags": ["igp_di", "inflacao", "precos", "ipea"],
    },
    {
        "code": "IGP12_INCC12",
        "name": "ipea_incc_di_indice",
        "title": "INCC-DI Índice Geral",
        "desc": "Índice Nacional de Custo da Construção - Disponibilidade Interna (INCC-DI) - índice (ago 1994 = 100).",
        "icon": "🏗",
        "class_name": "IpeaInccDiIndiceScraper",
        "tags": ["incc_di", "construcao", "precos", "ipea"],
    },
    {
        "code": "GAC12_INDFBCF12",
        "name": "ipea_fbcf_indice",
        "title": "Indicador FBCF Índice Real",
        "desc": "Indicador IPEA de Formação Bruta de Capital Fixo (FBCF) - índice real (média 1995 = 100).",
        "icon": "🏗",
        "class_name": "IpeaFbcfIndiceScraper",
        "tags": ["fbcf", "investimento", "macroeconomia", "ipea"],
    },
    {
        "code": "GAC12_INDFBCFDESSAZ12",
        "name": "ipea_fbcf_dessaz_indice",
        "title": "Indicador FBCF Dessazonalizado",
        "desc": "Indicador IPEA de FBCF - índice real dessazonalizado (média 1995 = 100).",
        "icon": "🏗",
        "class_name": "IpeaFbcfDessazIndiceScraper",
        "tags": ["fbcf", "investimento", "macroeconomia", "ipea"],
    },
    {
        "code": "GAC12_INDFBCFCC12",
        "name": "ipea_fbcf_construcao_indice",
        "title": "Indicador FBCF Construção Civil",
        "desc": "Indicador IPEA de FBCF - construção civil - índice real (média 1995 = 100).",
        "icon": "🏗",
        "class_name": "IpeaFbcfConstrucaoIndiceScraper",
        "tags": ["fbcf", "construcao", "investimento", "ipea"],
    },
    {
        "code": "GAC12_INDFBCFCCDESSAZ12",
        "name": "ipea_fbcf_construcao_dessaz_indice",
        "title": "Indicador FBCF Construção Dessazonalizado",
        "desc": "Indicador IPEA de FBCF - construção civil - índice real dessazonalizado (média 1995 = 100).",
        "icon": "🏗",
        "class_name": "IpeaFbcfConstrucaoDessazIndiceScraper",
        "tags": ["fbcf", "construcao", "investimento", "ipea"],
    },
    {
        "code": "PRECOS12_INPC12",
        "name": "ipea_inpc_indice",
        "title": "INPC Índice Geral",
        "desc": "Índice Nacional de Preços ao Consumidor (INPC) - geral - índice (dez 1993 = 100).",
        "icon": "📊",
        "class_name": "IpeaInpcIndiceScraper",
        "tags": ["inpc", "inflacao", "precos", "ipea"],
    },
    {
        "code": "PRECOS12_INPCBR12",
        "name": "ipea_inpc_variacao",
        "title": "INPC Taxa de Variação",
        "desc": "Índice Nacional de Preços ao Consumidor (INPC) - geral - taxa de variação (% a.m.).",
        "icon": "📈",
        "class_name": "IpeaInpcVariacaoScraper",
        "tags": ["inpc", "inflacao", "precos", "ipea"],
    },
    {
        "code": "GAC12_SALMINRE12",
        "name": "ipea_salario_minimo_real",
        "title": "Salário Mínimo Real",
        "desc": "Salário mínimo real mensal (em R$ do último mês).",
        "icon": "💰",
        "class_name": "IpeaSalarioMinimoRealScraper",
        "tags": ["salario_minimo", "renda", "trabalho", "ipea"],
    },
    {
        "code": "MTE12_SALMIN12",
        "name": "ipea_salario_minimo_vigente",
        "title": "Salário Mínimo Vigente",
        "desc": "Salário mínimo mensal vigente nominal (em R$).",
        "icon": "💰",
        "class_name": "IpeaSalarioMinimoVigenteScraper",
        "tags": ["salario_minimo", "renda", "trabalho", "ipea"],
    },
    {
        "code": "IBSIE12_QSCFG12",
        "name": "ipea_mineral_ferro_gusa",
        "title": "Produção de Ferro-Gusa",
        "desc": "Produção mensal de ferro-gusa pela indústria de transformação mineral (em toneladas).",
        "icon": "🧱",
        "class_name": "IpeaMineralFerroGusaScraper",
        "tags": ["mineracao", "ferro_gusa", "producao", "ipea"],
    },
    {
        "code": "IBSIE12_QSCAB12",
        "name": "ipea_mineral_aco_bruto",
        "title": "Produção de Aço Bruto",
        "desc": "Produção mensal de aço bruto pela indústria de transformação mineral (em toneladas).",
        "icon": "🧱",
        "class_name": "IpeaMineralAcoBrutoScraper",
        "tags": ["mineracao", "aco_bruto", "producao", "ipea"],
    },
    {
        "code": "IBSIE12_QSCL12",
        "name": "ipea_mineral_laminados",
        "title": "Produção de Laminados",
        "desc": "Produção mensal de laminados pela indústria de transformação mineral (em toneladas).",
        "icon": "🧱",
        "class_name": "IpeaMineralLaminadosScraper",
        "tags": ["mineracao", "laminados", "producao", "ipea"],
    },
]

TEMPLATE = """#!/usr/bin/env python
# coding: utf-8
\"\"\"
Scraper: IPEADATA – {title}
Fonte:   http://www.ipeadata.gov.br/api/odata4/
Saída:   data/{name}.csv
\"\"\"

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.utils.base import BaseScraper

CODIGO_SERIE = "{code}"
API_URL = f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{{CODIGO_SERIE}}')"


class {class_name}(BaseScraper):
    name = "{name}"
    group = "misc"
    enabled = True
    phase = 1

    # Catálogo de Metadados
    title = "{title}"
    description = "{desc}"
    icon = "{icon}"
    icon_class = "icon-{name}"
    badge = "Mensal"
    badge_class = "badge-monthly"
    tags = {tags}
    source = "IPEADATA"

    def fetch(self) -> pd.DataFrame:
        session = self.get_session()
        resp = session.get(API_URL, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        session.close()

        values = data.get("value", [])
        if not values:
            raise RuntimeError("Nenhum dado retornado para {title}.")

        records = []
        for item in values:
            raw_date = item.get("VALDATA", "")
            if "T" in raw_date:
                date_ref = raw_date.split("T")[0]
            else:
                date_ref = raw_date[:10]

            val = item.get("VALVALOR")
            if val is None:
                continue

            records.append({{
                "data_referencia": date_ref,
                "valor": float(val),
            }})

        return pd.DataFrame(records)


if __name__ == "__main__":
    {class_name}().run()
"""


def generate():
    for item in SERIES:
        file_path = SCRAPERS_DIR / f"{item['name']}.py"
        content = TEMPLATE.format(
            code=item["code"],
            name=item["name"],
            title=item["title"],
            desc=item["desc"],
            icon=item["icon"],
            class_name=item["class_name"],
            tags=str(item["tags"]),
        )
        file_path.write_text(content, encoding="utf-8")
        # chmod +x
        file_path.chmod(file_path.stat().st_mode | stat.S_IEXEC)
        print(f"Gerado: {file_path.name}")


if __name__ == "__main__":
    generate()
