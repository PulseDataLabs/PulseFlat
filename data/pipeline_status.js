window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-18T22:53:48.178161",
  "elapsed_seconds": 2123.454617500305,
  "status": "error",
  "summary": {
    "total": 66,
    "success": 66,
    "failed": 2,
    "drifts": 2
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 52.3662269115448,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 3.7180910110473633,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.710500717163086,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 10.180991649627686,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 7.521439075469971,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.22121381759643555,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (18/08/2026) não corresponde ao D-1 útil (17/08/2026).\n",
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.01029896736145,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.762953758239746,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.281534194946289,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 6.573632001876831,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 235.1702013015747,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 19.363973379135132,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.265777826309204,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 2.8061001300811768,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
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
      "elapsed_seconds": 1.087003469467163,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.335357904434204,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 312.4422860145569,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 5.961474657058716,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.2292561531066895,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.9213590621948242,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 2.313370704650879,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 2.429126262664795,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.9373466968536377,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.7765898704528809,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.5973918437957764,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.852968692779541,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.600510835647583,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 205.8474736213684,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 82.15956997871399,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 329.76768159866333,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 76.23827195167542,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.0547149181365967,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 2.6620750427246094,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 143, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 29.859078884124756,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 23.45985746383667,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 1747.2713763713837,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 49.0003719329834,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 18.888612508773804,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 85.83525919914246,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 69.36949563026428,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 1.7891502380371094,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 3.5490570068359375,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 4.622014760971069,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 21.74186873435974,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 9.554689645767212,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 13.500914812088013,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 13.858332633972168,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 14.311783790588379,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 18.311654090881348,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 98.39713478088379,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 18.277379274368286,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 17.05229616165161,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 13.62637996673584,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 103.16148710250854,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 74.82062005996704,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 2.455172300338745,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.3314106464385986,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.293245315551758,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 18.88598132133484,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 58.68245005607605,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.534601926803589,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 0.9989809989929199,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 2.8800785541534424,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 39.23944330215454,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 5.797782897949219,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 152.59807920455933,
      "error": null,
      "timestamp": "2026-08-18T22:53:48.178400"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-18T22:18:30.285280"
    },
    "b3_bdi_etfrf.csv.gz": {
      "added": [],
      "removed": [
        "preco_referencia_d1",
        "oferta_compra",
        "oferta_venda"
      ],
      "timestamp": "2026-08-18T06:29:17.654754"
    }
  }
};
