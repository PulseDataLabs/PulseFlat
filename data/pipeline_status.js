window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-22T08:10:35.301244",
  "elapsed_seconds": 261.15157747268677,
  "status": "error",
  "summary": {
    "total": 64,
    "success": 64,
    "failed": 1,
    "drifts": 2
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 59.2460401058197,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 1.88423752784729,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.034900188446045,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.2333333492279053,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 5.5509185791015625,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 4.282787561416626,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 3.9554364681243896,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.822451591491699,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 1.9565856456756592,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.400270938873291,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 1.5356371402740479,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 21.532111883163452,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 4.401103734970093,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.524134635925293,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.391666889190674,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
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
      "elapsed_seconds": 1.3137919902801514,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 4.013483047485352,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 25.559318780899048,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 4.149522066116333,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.83660101890564,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.2652239799499512,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.209019422531128,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.206681489944458,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.1914019584655762,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.201836109161377,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.182661771774292,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.1833853721618652,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.2678618431091309,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 14.025952577590942,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 39.99141478538513,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 145.9577398300171,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 76.75200366973877,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 5.586449384689331,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 8.691086053848267,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 1.716245174407959,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 6.1095592975616455,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 33.42024874687195,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 36.42615628242493,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 17.587515115737915,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 21.28868556022644,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 34.84673023223877,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 1.5511586666107178,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 3.456223964691162,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.497880458831787,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.05529475212097,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 9.652332305908203,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 3.980426549911499,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 3.7905852794647217,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.470669746398926,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 8.212502241134644,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 91.28160619735718,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 7.742983818054199,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.522385120391846,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 11.21496868133545,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 27.65871572494507,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 73.258131980896,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 2.622875690460205,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.269148588180542,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 2.731663942337036,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 13.86879301071167,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 37.32727098464966,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.8573837280273438,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.3238770961761475,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 2.801276445388794,
      "error": null,
      "timestamp": "2026-07-22T08:10:35.301450"
    }
  },
  "drifts": {
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-22T08:06:41.966499"
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
      "timestamp": "2026-07-22T08:07:09.006183"
    }
  }
};
