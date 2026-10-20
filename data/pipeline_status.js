window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-20T13:41:28.788964",
  "elapsed_seconds": 431.39591550827026,
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
      "elapsed_seconds": 66.00046133995056,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.818410634994507,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 3.6473021507263184,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.1822285652160645,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 11.092856168746948,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.309391975402832,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 9.35509705543518,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 7.6530609130859375,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 12.708295822143555,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.4930005073547363,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 48.822083473205566,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 27.093000888824463,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 151.51258611679077,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 6.2873618602752686,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 5.688886642456055,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.8535020351409912,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.3134987354278564,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 410.29100227355957,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 9.784437656402588,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.3483948707580566,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 6.28777003288269,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.228264570236206,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 11.383153915405273,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 4.071096897125244,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 4.251702070236206,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 2.920269250869751,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 4.204755544662476,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 4.654375076293945,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 7.45194673538208,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 3.3420281410217285,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 68.94360327720642,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 22.62109088897705,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.21014666557312,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 190.144380569458,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 67.68270659446716,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 6.681915998458862,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 72.10405230522156,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 50.79267930984497,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 23.000858068466187,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 27.161101579666138,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 84.75671696662903,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 4.093573808670044,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 5.746968030929565,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 3.707545518875122,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.77992057800293,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 17.568846464157104,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 15.50424337387085,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 14.59252381324768,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 15.989300966262817,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 7.143181562423706,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 61.76984477043152,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 6.128462791442871,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 15.233550071716309,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 10.846284627914429,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 61.67947340011597,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 98.43639135360718,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.206496000289917,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.5692849159240723,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.611218214035034,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 26.508782148361206,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 76.81001806259155,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 3.911374092102051,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.8648138046264648,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 10.5150625705719,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 27.942326545715332,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 19.262511014938354,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 279.32771277427673,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 120.9828851222992,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 35.16693067550659,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 11.990427732467651,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 13.121408700942993,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 9.493211030960083,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 10.245646953582764,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 11.074993371963501,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 3.0170176029205322,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 3.4727025032043457,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.3014750480651855,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.4024128913879395,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 3.7130558490753174,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 3.1174094676971436,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 4.466587066650391,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 4.676886320114136,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 8.629634618759155,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 3.5912811756134033,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 54.35244274139404,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 5.023904323577881,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 3.797590970993042,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 3.129901647567749,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 2.9547367095947266,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.1255416870117188,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 10.732576608657837,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 3.127443313598633,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 30.9859139919281,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 36.6005699634552,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 3.892080783843994,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 7.573164463043213,
      "error": null,
      "timestamp": "2026-10-20T13:41:28.789224"
    }
  },
  "drifts": {}
};
