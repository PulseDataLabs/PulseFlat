window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-19T23:15:58.758685",
  "elapsed_seconds": 3466.122973680496,
  "status": "error",
  "summary": {
    "total": 67,
    "success": 66,
    "failed": 2,
    "drifts": 4
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 67.98234844207764,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 5.164523363113403,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.444483757019043,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 13.883305311203003,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.94170618057251,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.5965752601623535,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 234, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 192, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 140, in capturar\n    raise ValueError(\n        f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\"\n    )\nValueError: Abortando: data do arquivo (19/08/2026) não corresponde ao D-1 útil (18/08/2026).\n",
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.085846900939941,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 7.2644500732421875,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 3.4565720558166504,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 8.514349460601807,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 328.4585874080658,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 22.538337230682373,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 87.66699695587158,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.120607376098633,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.3641486167907715,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
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
      "elapsed_seconds": 1.5845041275024414,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.9648995399475098,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 255.8723156452179,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 6.121903419494629,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.775065183639526,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 2.3614542484283447,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 2.669487476348877,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 2.9545912742614746,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 2.3067071437835693,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 2.25439453125,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 2.004822015762329,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 2.0262012481689453,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.9605727195739746,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 294.4934024810791,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 118.5279688835144,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 476.90636682510376,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 98.52769684791565,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 48.67091369628906,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 2.060753583908081,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 234, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 147, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 47.83231282234192,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 8.447341680526733,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 3011.9841301441193,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 68.92442607879639,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 21.810383319854736,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 130.71531295776367,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 31.487845420837402,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.1966989040374756,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 4.531416654586792,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.656550884246826,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.30041813850403,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 11.562029600143433,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.49359917640686,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 15.067300081253052,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 15.857603311538696,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 19.796579122543335,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 135.73617553710938,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 9.47711730003357,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 112.44938039779663,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 24.1949303150177,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 38.32619500160217,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 86.37792158126831,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.2992942333221436,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.8080673217773438,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.852980136871338,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 19.79655361175537,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 52.198631286621094,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 3.0922510623931885,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.287370204925537,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.9135286808013916,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 51.21128988265991,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 8.635873556137085,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 189.11961913108826,
      "error": null,
      "timestamp": "2026-08-19T23:15:58.758919"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-19T22:18:20.279431"
    },
    "b3_bdi_etfrf.csv.gz": {
      "added": [],
      "removed": [
        "preco_referencia_d1",
        "oferta_compra",
        "oferta_venda"
      ],
      "timestamp": "2026-08-19T08:22:19.295708"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-08-19T22:20:14.019124"
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
      "timestamp": "2026-08-19T22:22:58.926019"
    }
  }
};
