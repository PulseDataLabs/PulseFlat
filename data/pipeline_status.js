window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-23T11:17:52.170721",
  "elapsed_seconds": 347.31261134147644,
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
      "elapsed_seconds": 64.08222198486328,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.7496578693389893,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 3.139291763305664,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.413618326187134,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 9.613022804260254,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.1919846534729004,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 7.958607912063599,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.267776966094971,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 11.77034068107605,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.575511932373047,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 37.17363095283508,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 28.84523367881775,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 157.95326948165894,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 6.121777534484863,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 5.35186505317688,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.3899571895599365,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.969639778137207,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 313.7146530151367,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 7.134948015213013,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 3.0689220428466797,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 3.6329703330993652,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.669190406799316,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 2.6882686614990234,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 4.7358784675598145,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 4.2948362827301025,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 3.3973731994628906,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 2.1877822875976562,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 3.5626273155212402,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 13.579920291900635,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 2.665163993835449,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 141.93292570114136,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 16.152127742767334,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.5499565601348877,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 138.23877000808716,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 49.78468632698059,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "ibge_sidra": {
      "status": "error",
      "elapsed_seconds": 111.44739413261414,
      "error": "SystemExit(1)",
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 54.35010528564453,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 42.612284421920776,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 20.833210945129395,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 16.913854837417603,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 39.48866105079651,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 4.024283170700073,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 5.633831024169922,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 3.03135347366333,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 26.587361574172974,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 17.818260669708252,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 14.64294147491455,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 14.592334508895874,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.434880018234253,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 6.766257286071777,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 43.27712440490723,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 8.809002876281738,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.728879451751709,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 19.161556005477905,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 53.24663543701172,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 93.42657089233398,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 5.54748272895813,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 8.588236093521118,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 10.9528489112854,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 29.002193689346313,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 79.68543457984924,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.454484701156616,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.6632485389709473,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.4269540309906006,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 25.888102531433105,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 18.788076400756836,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 263.9524881839752,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 121.39030337333679,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 6.867809295654297,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 10.54986572265625,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 10.30603575706482,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 6.293394565582275,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 8.440993547439575,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 8.581389904022217,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 2.7287518978118896,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 3.565544843673706,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 5.530431747436523,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 2.505711317062378,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 3.991151809692383,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 3.219085216522217,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 4.23313570022583,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 5.276046991348267,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 8.396090030670166,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 2.878617525100708,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 42.527992486953735,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 4.1807639598846436,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 5.270197153091431,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 5.120190382003784,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 2.2514162063598633,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.716858148574829,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 13.628265619277954,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 5.57015585899353,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 12.60542893409729,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 22.802973985671997,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 3.059222459793091,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 5.833084344863892,
      "error": null,
      "timestamp": "2026-10-23T11:17:52.171223"
    }
  },
  "drifts": {}
};
