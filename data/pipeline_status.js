window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-21T10:46:54.180553",
  "elapsed_seconds": 356.742155790329,
  "status": "error",
  "summary": {
    "total": 64,
    "success": 63,
    "failed": 2,
    "drifts": 2
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 58.58539152145386,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.381795883178711,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 0.9889588356018066,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.1659860610961914,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 6.390819549560547,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 5.266278982162476,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.459449529647827,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 4.1115028858184814,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 1.909682035446167,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.4042909145355225,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 1.5349678993225098,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 29.892856121063232,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 5.39878249168396,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.271752834320068,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.6440744400024414,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_carteiras": {
      "status": "unknown",
      "elapsed_seconds": 0.0,
      "error": null,
      "timestamp": null
    },
    "b3_futuros_ajustes": {
      "status": "unknown",
      "elapsed_seconds": 0.0,
      "error": null,
      "timestamp": null
    },
    "b3_indicadores_financeiros": {
      "status": "success",
      "elapsed_seconds": 1.1321966648101807,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.8769471645355225,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 22.81056809425354,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 4.904207944869995,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.157252311706543,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.1115617752075195,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 2.040343999862671,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.354485273361206,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.6966185569763184,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.286144733428955,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.2816166877746582,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.0831162929534912,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.1666836738586426,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 9.492528200149536,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 42.82104754447937,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 207.71617364883423,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 85.92943167686462,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 9.392375707626343,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 10.866022825241089,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 2.191714286804199,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 11.850517988204956,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 44.72722148895264,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 59.4358868598938,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 18.8884596824646,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 105.13015246391296,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 41.858922481536865,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.4760665893554688,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 3.7116942405700684,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 5.318425178527832,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "error",
      "elapsed_seconds": 0.21814441680908203,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 81, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 43, in capturar\n    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:\n         ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/zipfile/__init__.py\", line 1407, in __init__\n    self._RealGetContents()\n    ~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/zipfile/__init__.py\", line 1474, in _RealGetContents\n    raise BadZipFile(\"File is not a zip file\")\nzipfile.BadZipFile: File is not a zip file\n",
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 9.861618041992188,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.4521164894104,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.09891676902771,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.213819980621338,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 10.135117053985596,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 107.41074180603027,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 8.552573680877686,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.841712951660156,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 13.56621503829956,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 44.21943664550781,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 105.15207052230835,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.918147087097168,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.6510629653930664,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.016052722930908,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 22.47987174987793,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 61.051997661590576,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 3.5304064750671387,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.1701815128326416,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.5762345790863037,
      "error": null,
      "timestamp": "2026-07-21T10:46:54.180771"
    }
  },
  "drifts": {
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-21T10:41:21.680961"
    },
    "bacen_conglomerados.csv": {
      "added": [],
      "removed": [
        "departamento",
        "secao_1",
        "secao_2",
        "secao_3",
        "tipo_documento",
        "data_documento",
        "detalhe"
      ],
      "timestamp": "2026-07-21T10:41:46.252773"
    }
  }
};
