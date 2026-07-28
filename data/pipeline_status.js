window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-28T20:15:21.709513",
  "elapsed_seconds": 4449.348983049393,
  "status": "error",
  "summary": {
    "total": 64,
    "success": 63,
    "failed": 2,
    "drifts": 1
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 64.10984253883362,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 6.003180980682373,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.2532222270965576,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.120120048522949,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 10.11281156539917,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.6492083072662354,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (28/07/2026) não corresponde ao D-1 útil (27/07/2026).\n",
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.522026777267456,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.64414119720459,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 3.2044715881347656,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 4.829723119735718,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 130.9600534439087,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 102.73359489440918,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 17.279910564422607,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.206284284591675,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.4530014991760254,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
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
      "elapsed_seconds": 1.491029977798462,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.8021857738494873,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 23.3393771648407,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 6.211418628692627,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.330014944076538,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.931046962738037,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.998335838317871,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.6933708190917969,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 2.091670274734497,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 2.3707549571990967,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.9009668827056885,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.4984424114227295,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.740035057067871,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 252.29614806175232,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 115.36728692054749,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 293.4772171974182,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 154.5670530796051,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 33.97937798500061,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 694.7406423091888,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 54.263465881347656,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.727018117904663,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 4111.3277592659,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 60.71575212478638,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 20.650429725646973,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 125.04953241348267,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 30.019854307174683,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.455261468887329,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 23.940847396850586,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 8.683878898620605,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "error",
      "elapsed_seconds": 0.393172025680542,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 81, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 43, in capturar\n    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:\n         ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/zipfile/__init__.py\", line 1407, in __init__\n    self._RealGetContents()\n    ~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/zipfile/__init__.py\", line 1474, in _RealGetContents\n    raise BadZipFile(\"File is not a zip file\")\nzipfile.BadZipFile: File is not a zip file\n",
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 11.106663227081299,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.556568622589111,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 5.3319010734558105,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 6.329121351242065,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 10.5488760471344,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 161.2339322566986,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 14.135636806488037,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 8.13055682182312,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 18.26515507698059,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 37.110209465026855,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 84.88378190994263,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.2691588401794434,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.661612033843994,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.1652557849884033,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 18.023650884628296,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 67.48358726501465,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 17.34133553504944,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.2763285636901855,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 5.254120349884033,
      "error": null,
      "timestamp": "2026-07-28T20:15:21.709739"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-07-28T19:01:20.302323"
    }
  }
};
