window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-17T09:12:52.858235",
  "elapsed_seconds": 379.2014558315277,
  "status": "error",
  "summary": {
    "total": 64,
    "success": 64,
    "failed": 1,
    "drifts": 0
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 57.753798961639404,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.381066083908081,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.6745896339416504,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.2617135047912598,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.481324195861816,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 4.754277944564819,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.891699552536011,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 4.359344244003296,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 1.8732407093048096,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.465296506881714,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 1.2367098331451416,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 19.982228755950928,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 4.729204416275024,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.549170255661011,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.0480849742889404,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
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
      "elapsed_seconds": 1.286306381225586,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 4.13321328163147,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 76.12900757789612,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 5.1169517040252686,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.996505498886108,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.1863458156585693,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.4654779434204102,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.6038427352905273,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.191042184829712,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.1797857284545898,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.207481861114502,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.3623344898223877,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.1519079208374023,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 6.453223466873169,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 78.83727836608887,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 165.49443554878235,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 83.10457110404968,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.133843421936035,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 11.537471055984497,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 2.119081497192383,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.611134052276611,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 31.135488986968994,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 35.42160701751709,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 19.214638710021973,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 118.37423253059387,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 23.706244945526123,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 1.973170518875122,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 11.475089311599731,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.531137466430664,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.881133317947388,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 10.120485067367554,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.289492845535278,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.751201629638672,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.758590221405029,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 9.442100763320923,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 110.791818857193,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 9.551513195037842,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.945828676223755,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 13.512365818023682,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 42.05660390853882,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 128.95989871025085,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.433105945587158,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.9195797443389893,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.820425033569336,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 35.389134645462036,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 90.93470239639282,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.926837682723999,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.3346083164215088,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.5961503982543945,
      "error": null,
      "timestamp": "2026-07-17T09:12:52.858433"
    }
  },
  "drifts": {}
};
