window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-01T01:25:04.029206",
  "elapsed_seconds": 5426.014402389526,
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
      "elapsed_seconds": 56.5970618724823,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 4.172820806503296,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.8402814865112305,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.7686548233032227,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.111571311950684,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.38504934310913086,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (31/07/2026) não corresponde ao D-1 útil (30/07/2026).\n",
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 4.3184144496917725,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.860890626907349,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.1029653549194336,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.914702892303467,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 126.44756007194519,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 50.20634055137634,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.2267746925354,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.2511961460113525,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
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
      "elapsed_seconds": 1.061049222946167,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.455439329147339,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 121.18297481536865,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 4.051955699920654,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.1491539478302,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.2011706829071045,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.241098403930664,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.3520123958587646,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.164419412612915,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.0752067565917969,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.2654941082000732,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.7289047241210938,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.4541311264038086,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 207.5819549560547,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 59.89224052429199,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 261.7935128211975,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 74.24711608886719,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.3658766746520996,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 5.214076042175293,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 143, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 31.09721350669861,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 6.716030597686768,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 5200.668665409088,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 47.35382795333862,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 18.121887683868408,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 93.52550983428955,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 26.716026306152344,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.2894606590270996,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 3.717259407043457,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 4.856781244277954,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 52.89223527908325,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 10.546225547790527,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 3.7785844802856445,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.165282964706421,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 4.594872951507568,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 8.306980609893799,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 113.48207426071167,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 8.60973572731018,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 10.321292638778687,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 13.875893831253052,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 35.16399025917053,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 89.10993599891663,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.6940102577209473,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.0144970417022705,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.258192777633667,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 19.685465097427368,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 53.6661593914032,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.065257787704468,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.4589693546295166,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 4.259996175765991,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-07-31T19:01:49.706952"
    }
  }
};
