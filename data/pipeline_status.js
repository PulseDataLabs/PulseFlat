window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-19T17:13:54.900737",
  "elapsed_seconds": 369.0673632621765,
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
      "elapsed_seconds": 62.766114950180054,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.576889991760254,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 3.2882301807403564,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.5389533042907715,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 9.033333539962769,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.165006637573242,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.945953369140625,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 7.047262668609619,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 9.078641653060913,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 4.409460783004761,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 16.65758514404297,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 34.323378562927246,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 155.6949052810669,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 6.077989816665649,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 4.813760042190552,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.7407889366149902,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.569430112838745,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 329.2651526927948,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 5.092400550842285,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.284590244293213,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 2.9281046390533447,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 3.8418266773223877,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 3.1285271644592285,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 3.2174441814422607,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 2.5635082721710205,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 2.814770460128784,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 2.3362174034118652,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 2.47900128364563,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 6.807759046554565,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 3.1566147804260254,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 14.349612712860107,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 18.37625026702881,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 2.592146158218384,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 164.52754878997803,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 87.48300981521606,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 5.490562438964844,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 72.10379219055176,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 94.43729615211487,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 33.11679458618164,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 17.66910719871521,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 95.72412037849426,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.6750006675720215,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 8.091665267944336,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.066849946975708,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 25.258270502090454,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 29.141709566116333,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 14.030069589614868,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.235955715179443,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 4.820751667022705,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 6.96935772895813,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 44.93229937553406,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 7.926021575927734,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 16.270012617111206,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 20.046401500701904,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 70.84285879135132,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 109.15347862243652,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 5.3301100730896,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 5.265284061431885,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 9.228206157684326,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 38.77806115150452,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 77.93395495414734,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.698972702026367,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.7280762195587158,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 7.340880632400513,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 42.33655405044556,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 35.803837060928345,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 268.4695782661438,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 130.76709246635437,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 37.452016830444336,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 10.675535678863525,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 9.836726188659668,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.795097351074219,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 8.277456283569336,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 9.052155494689941,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 2.6854546070098877,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 5.014524936676025,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 4.712753534317017,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 2.430405378341675,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 3.7327003479003906,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 2.536501407623291,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 4.136923551559448,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 4.411118984222412,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 7.9844512939453125,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 2.4794626235961914,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 56.426185131073,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 10.873779058456421,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 18.45858383178711,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 3.5404720306396484,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 2.0232090950012207,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 1.8757994174957275,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 7.920006513595581,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 2.9655587673187256,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 26.628108024597168,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 20.654757499694824,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 12.511137008666992,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 12.5465726852417,
      "error": null,
      "timestamp": "2026-10-19T17:13:54.900991"
    }
  },
  "drifts": {}
};
