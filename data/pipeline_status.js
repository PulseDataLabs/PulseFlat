window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-22T15:17:18.768351",
  "elapsed_seconds": 537.5657255649567,
  "status": "error",
  "summary": {
    "total": 96,
    "success": 94,
    "failed": 2,
    "drifts": 0
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 71.17954993247986,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.3531641960144043,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 3.6589250564575195,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.860917568206787,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 11.762672424316406,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 1.9533171653747559,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.966034412384033,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.678570747375488,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 16.154682636260986,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 5.64120888710022,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 84.05450558662415,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 53.860079765319824,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 228.93170070648193,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 7.284660339355469,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 5.420135974884033,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.5159568786621094,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.851672649383545,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 512.5359189510345,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 8.695539951324463,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.3633975982666016,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 4.948045015335083,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.482895374298096,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 6.333512544631958,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 3.964660167694092,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 4.27009129524231,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 3.4828317165374756,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 4.642514944076538,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 4.047062158584595,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 9.019016742706299,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 3.0463953018188477,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 45.975332260131836,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 37.04722332954407,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.2239155769348145,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 259.1809072494507,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 141.6201491355896,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "ibge_sidra": {
      "status": "error",
      "elapsed_seconds": 111.16497778892517,
      "error": "SystemExit(1)",
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 151.4688138961792,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 160.3499608039856,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 41.924638509750366,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 13.187740325927734,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 128.5232446193695,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 4.740004062652588,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 5.1165993213653564,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.6091651916503906,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.693351984024048,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 38.224491119384766,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.860835313796997,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 16.688843250274658,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 4.7959043979644775,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 18.86686420440674,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 51.0644052028656,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 21.80855655670166,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 14.89330244064331,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 8.480143070220947,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 73.47039198875427,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 108.85697102546692,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 6.228382110595703,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 5.342824220657349,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 10.55310606956482,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 34.27156066894531,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 70.44277882575989,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.623319864273071,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.9042799472808838,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 8.533750534057617,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 67.81751894950867,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 53.7051317691803,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 434.68806076049805,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 185.88073539733887,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 40.70909357070923,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 28.315279960632324,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 17.701014041900635,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.373051166534424,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 7.230637788772583,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 7.644583463668823,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 3.2856271266937256,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 3.8240649700164795,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.598799228668213,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 2.88822603225708,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 4.972920179367065,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 3.157451868057251,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 5.068416118621826,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 5.773225784301758,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 6.652433395385742,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 3.3587911128997803,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 96.04296731948853,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 11.02275538444519,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 5.959407329559326,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 5.2924723625183105,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 2.5708773136138916,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.319608211517334,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 11.701872825622559,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 4.412279844284058,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 41.57459545135498,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 39.081989765167236,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 4.115070104598999,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 5.454206466674805,
      "error": null,
      "timestamp": "2026-10-22T15:17:18.768600"
    }
  },
  "drifts": {}
};
