window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-11-23T20:42:57.007361",
  "elapsed_seconds": 421.7995910644531,
  "status": "error",
  "summary": {
    "total": 108,
    "success": 100,
    "failed": 8,
    "drifts": 0
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 59.14883613586426,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 1.998945951461792,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 3.911792278289795,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.028562307357788,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 10.415708065032959,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 19.567252159118652,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.1162025928497314,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 4.59940767288208,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 12.85751461982727,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 5.106692552566528,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 58.83470678329468,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 31.593061923980713,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 179.21206092834473,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.912294626235962,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 4.404250383377075,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_indicadores_financeiros": {
      "status": "success",
      "elapsed_seconds": 1.4748625755310059,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 42.64389228820801,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 393.5660481452942,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 39.65129780769348,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.282987594604492,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_carteira_teorica_ibov": {
      "status": "error",
      "elapsed_seconds": 0.27616429328918457,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 238, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 110, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/generic_scraper.py\", line 150, in fetch\n    raise RuntimeError(\"Resposta vazia recebida do servidor.\")\nRuntimeError: Resposta vazia recebida do servidor.\n",
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_carteira_teorica_smll": {
      "status": "error",
      "elapsed_seconds": 0.5192301273345947,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 238, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 110, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/generic_scraper.py\", line 150, in fetch\n    raise RuntimeError(\"Resposta vazia recebida do servidor.\")\nRuntimeError: Resposta vazia recebida do servidor.\n",
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "error",
      "elapsed_seconds": 0.24649620056152344,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 238, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 110, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/generic_scraper.py\", line 150, in fetch\n    raise RuntimeError(\"Resposta vazia recebida do servidor.\")\nRuntimeError: Resposta vazia recebida do servidor.\n",
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_carteira_teorica_isee": {
      "status": "error",
      "elapsed_seconds": 0.4781782627105713,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 238, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 110, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/generic_scraper.py\", line 150, in fetch\n    raise RuntimeError(\"Resposta vazia recebida do servidor.\")\nRuntimeError: Resposta vazia recebida do servidor.\n",
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "error",
      "elapsed_seconds": 0.36272597312927246,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 238, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 110, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/generic_scraper.py\", line 150, in fetch\n    raise RuntimeError(\"Resposta vazia recebida do servidor.\")\nRuntimeError: Resposta vazia recebida do servidor.\n",
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "error",
      "elapsed_seconds": 0.6878480911254883,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 238, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 110, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/generic_scraper.py\", line 150, in fetch\n    raise RuntimeError(\"Resposta vazia recebida do servidor.\")\nRuntimeError: Resposta vazia recebida do servidor.\n",
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "error",
      "elapsed_seconds": 0.40226244926452637,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 238, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 110, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/generic_scraper.py\", line 150, in fetch\n    raise RuntimeError(\"Resposta vazia recebida do servidor.\")\nRuntimeError: Resposta vazia recebida do servidor.\n",
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "error",
      "elapsed_seconds": 0.5923511981964111,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 238, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 110, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/generic_scraper.py\", line 150, in fetch\n    raise RuntimeError(\"Resposta vazia recebida do servidor.\")\nRuntimeError: Resposta vazia recebida do servidor.\n",
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 12.700514793395996,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 2.265867233276367,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 11.11690616607666,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 15.026742219924927,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.0549018383026123,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 196.18120193481445,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 55.90473198890686,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 5.6997153759002686,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 162.07823777198792,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 49.08143401145935,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 17.95229482650757,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 12.606851577758789,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 33.64998483657837,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.083648681640625,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 5.946153879165649,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.170936107635498,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 27.697952270507812,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 19.00281071662903,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 15.211138248443604,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 14.880781888961792,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 17.06438708305359,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 10.165571212768555,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 74.49887585639954,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 24.921794891357422,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 20.147555351257324,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 23.716768503189087,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 58.64906907081604,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 108.58307027816772,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.71480393409729,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.7604925632476807,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.9683873653411865,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 34.92693567276001,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 75.41109681129456,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 5.317395448684692,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.7227833271026611,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 6.331718444824219,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 25.982887268066406,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 14.353444814682007,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 283.4535186290741,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 151.4562919139862,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 33.49177384376526,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 29.565197944641113,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 19.327995538711548,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.868239641189575,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 5.187833309173584,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 6.04983115196228,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 4.487980842590332,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 5.3740222454071045,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 8.544033288955688,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.410017251968384,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 4.843410968780518,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 3.134355068206787,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 5.425314664840698,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 6.917003870010376,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 5.487474203109741,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 3.402292490005493,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 62.847562074661255,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 5.316515922546387,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 2.6546597480773926,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 2.497459888458252,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 34.87902355194092,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 5.145479679107666,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 10.993647575378418,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 4.818039417266846,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 19.51073384284973,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 34.44209384918213,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 2.6044702529907227,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 4.115615129470825,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lf_emissoes": {
      "status": "success",
      "elapsed_seconds": 2.3984036445617676,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lf_estoque": {
      "status": "success",
      "elapsed_seconds": 3.326639175415039,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lf_estoque_emissor": {
      "status": "success",
      "elapsed_seconds": 4.257180690765381,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lf_estoque_indexador": {
      "status": "success",
      "elapsed_seconds": 3.3007023334503174,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lf_estoque_natureza_detentor": {
      "status": "success",
      "elapsed_seconds": 3.3433921337127686,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lf_estoque_segmento": {
      "status": "success",
      "elapsed_seconds": 3.294870138168335,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lf_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 2.912620782852173,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lf_prazo_emissoes": {
      "status": "success",
      "elapsed_seconds": 2.6444942951202393,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lf_prazo_vencimento": {
      "status": "success",
      "elapsed_seconds": 2.7691078186035156,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lf_prazo_vencimento_segmento": {
      "status": "success",
      "elapsed_seconds": 2.728290557861328,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lfs_estoque_segmento": {
      "status": "success",
      "elapsed_seconds": 2.636384963989258,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    },
    "bacen_lfs_prazo_vencimento_segmento": {
      "status": "success",
      "elapsed_seconds": 2.647383689880371,
      "error": null,
      "timestamp": "2026-11-23T20:42:57.007860"
    }
  },
  "drifts": {}
};
