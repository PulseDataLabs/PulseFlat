window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-20T14:33:54.882380",
  "elapsed_seconds": 430.2977137565613,
  "status": "error",
  "summary": {
    "total": 96,
    "success": 95,
    "failed": 1,
    "drifts": 0
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 61.960113763809204,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.510258436203003,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 3.6102874279022217,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.606473445892334,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 9.708606243133545,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.7114548683166504,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.622186899185181,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.394456386566162,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 10.921291589736938,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 5.943998336791992,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 46.31861448287964,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 40.35322165489197,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 162.06924271583557,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 6.472554445266724,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 5.491244077682495,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.5357320308685303,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.2940893173217773,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 409.1324815750122,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 7.385502099990845,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.333616018295288,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 5.0570807456970215,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 5.842850685119629,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 6.204885244369507,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 4.638160228729248,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 4.4844090938568115,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 3.623135805130005,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 3.775864601135254,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 3.24930739402771,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 8.122341871261597,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 2.2600655555725098,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 16.123830795288086,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 27.307299852371216,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 11.11717963218689,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 191.53191614151,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 88.44371819496155,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 8.966726779937744,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 89.82044506072998,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 130.92134189605713,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 24.82672429084778,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 23.636027574539185,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 60.085317850112915,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 5.041533708572388,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 6.033705234527588,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 3.377342939376831,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 24.266014575958252,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 15.8908212184906,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 15.54893159866333,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 26.169179677963257,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 16.02192974090576,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 8.623708248138428,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 50.475847482681274,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 16.745208740234375,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 15.723548412322998,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 19.401453495025635,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 52.15060329437256,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 102.51093077659607,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.774894952774048,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.265432119369507,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.627795219421387,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 26.871956825256348,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 76.47767686843872,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.1218421459198,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.7559535503387451,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 5.3579792976379395,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 30.86365795135498,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 22.685688257217407,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 286.3055090904236,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 131.66958093643188,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 42.15817308425903,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 19.738070011138916,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 12.869145393371582,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.101037502288818,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 6.857007265090942,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 8.380131244659424,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 3.0735130310058594,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 4.625676155090332,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 5.821110248565674,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 2.6767449378967285,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 3.9306671619415283,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 3.1701745986938477,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 4.79066801071167,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 5.178830862045288,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 6.851894855499268,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 2.6655139923095703,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 50.36235308647156,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 7.288212060928345,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 6.169785737991333,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 4.860783100128174,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 2.432889461517334,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.285034418106079,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 9.333470582962036,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 3.5684478282928467,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 27.7371084690094,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 39.08074951171875,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 3.340820550918579,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 5.235321283340454,
      "error": null,
      "timestamp": "2026-10-20T14:33:54.882621"
    }
  },
  "drifts": {}
};
