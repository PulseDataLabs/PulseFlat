window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-04T01:02:42.554223",
  "elapsed_seconds": 5012.827727794647,
  "status": "error",
  "summary": {
    "total": 66,
    "success": 65,
    "failed": 3,
    "drifts": 3
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 60.8536913394928,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 5.416632652282715,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.35929012298584,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 10.77062726020813,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 9.069168090820312,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.599949836730957,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (03/08/2026) não corresponde ao D-1 útil (31/07/2026).\n",
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.54037618637085,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 4.970366954803467,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.761343002319336,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 8.242164373397827,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 153.85221576690674,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 13.04346513748169,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.3477864265441895,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.4221813678741455,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
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
      "elapsed_seconds": 1.88187837600708,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 64.44339323043823,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 165.3409857749939,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 67.2518835067749,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.532055616378784,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.2187180519104004,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.355118751525879,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.3891804218292236,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.3275561332702637,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.6232595443725586,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.3050923347473145,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.8467352390289307,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.2020156383514404,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 250.6068308353424,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 69.94328713417053,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 296.51220750808716,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 83.2799129486084,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "bacen_conglomerados": {
      "status": "error",
      "elapsed_seconds": 0.4192619323730469,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_conglomerados.py\", line 71, in fetch\n    print_warn(f\"{yyyymm}CONGLOMERADO.zip não disponível\", elapsed=time.time() - t0)\n    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nTypeError: print_warn() got an unexpected keyword argument 'elapsed'\n",
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 2.1592679023742676,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 143, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 49.85300135612488,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.279012203216553,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 4644.210921287537,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 35.119364976882935,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 19.099247694015503,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 144.70431804656982,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 74.12491059303284,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.552487373352051,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 4.501948595046997,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.907203912734985,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.919484615325928,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 11.464284420013428,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 5.231305360794067,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 5.477391004562378,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 6.617476463317871,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 9.811105728149414,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 126.9252941608429,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 8.727569818496704,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 6.901126384735107,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 15.51844048500061,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 48.55228352546692,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 104.63437581062317,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 5.081949472427368,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 4.3033766746521,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 5.444276571273804,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 36.94325852394104,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 92.86182236671448,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.62126350402832,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.5560238361358643,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 4.677042484283447,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 80.10347580909729,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 6.624866485595703,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 150.44163513183594,
      "error": null,
      "timestamp": "2026-08-04T01:02:42.554459"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-03T23:39:17.039466"
    },
    "b3_bdi_etfrf.csv.gz": {
      "added": [],
      "removed": [
        "preco_referencia_d1",
        "oferta_compra",
        "oferta_venda"
      ],
      "timestamp": "2026-08-03T23:40:42.555907"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-08-03T23:42:00.390742"
    }
  }
};
