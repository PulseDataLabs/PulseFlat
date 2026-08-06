window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-06T00:15:51.699159",
  "elapsed_seconds": 2137.618987560272,
  "status": "error",
  "summary": {
    "total": 66,
    "success": 66,
    "failed": 2,
    "drifts": 3
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 61.037883043289185,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 5.796584844589233,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.2691898345947266,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 10.792155981063843,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 9.263451099395752,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.5984349250793457,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (05/08/2026) não corresponde ao D-1 útil (04/08/2026).\n",
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.706996440887451,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.171065092086792,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.7637453079223633,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 8.558614730834961,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 185.0688247680664,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 12.183085203170776,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.611794948577881,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.279139995574951,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
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
      "elapsed_seconds": 1.64345383644104,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.838109016418457,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 203.07108855247498,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 6.464326858520508,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.442580223083496,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.749077558517456,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 2.8799445629119873,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 2.1509761810302734,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 2.200148582458496,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 2.4688897132873535,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.6752562522888184,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.885840654373169,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.6509132385253906,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 248.06446194648743,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 79.02070236206055,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 325.5389177799225,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 88.78055953979492,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "bacen_conglomerados": {
      "status": "error",
      "elapsed_seconds": 0.6888754367828369,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_conglomerados.py\", line 71, in fetch\n    print_warn(f\"{yyyymm}CONGLOMERADO.zip não disponível\", elapsed=time.time() - t0)\n    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nTypeError: print_warn() got an unexpected keyword argument 'elapsed'\n",
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 1873.8696446418762,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 45.75046682357788,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.904607057571411,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 35.69921922683716,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 38.318124532699585,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 21.01649570465088,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 118.27069044113159,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 26.635616064071655,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.137516498565674,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 104.06409287452698,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.030595779418945,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 25.69825053215027,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 11.748113870620728,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.470587253570557,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.970410108566284,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 6.762174129486084,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 9.895044326782227,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 138.38278102874756,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 12.461538076400757,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 7.6145734786987305,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 16.944786548614502,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 44.693989515304565,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 100.14225888252258,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.6742427349090576,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.2294676303863525,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.451249122619629,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 23.621115922927856,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 63.32499146461487,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 3.753310441970825,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.3085224628448486,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 4.8506340980529785,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 39.56060719490051,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 6.660219192504883,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 162.09865427017212,
      "error": null,
      "timestamp": "2026-08-06T00:15:51.699348"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-05T23:40:21.260806"
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
      "timestamp": "2026-08-05T23:42:11.776565"
    }
  }
};
