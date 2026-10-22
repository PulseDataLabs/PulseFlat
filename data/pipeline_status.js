window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-22T13:01:17.945825",
  "elapsed_seconds": 542.4841911792755,
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
      "elapsed_seconds": 67.15983271598816,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.5880274772644043,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 3.052859306335449,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.5746796131134033,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 11.9565908908844,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.149521827697754,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 9.533462047576904,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 7.9899513721466064,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 10.032411098480225,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.880910634994507,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 88.17699384689331,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 65.66558718681335,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 226.38906073570251,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 6.7140796184539795,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 4.897016286849976,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.43153953552246094,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.547240972518921,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 519.9652252197266,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 7.7191057205200195,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.315239667892456,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 4.971941232681274,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.474628686904907,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 5.675069332122803,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 3.743720054626465,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 4.647798538208008,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 3.501091241836548,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 3.220282554626465,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 3.718266248703003,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 8.250405311584473,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 3.3618924617767334,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 11.998087644577026,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 37.100027561187744,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 4.917553424835205,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 252.8624393939972,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 160.31547617912292,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "ibge_sidra": {
      "status": "error",
      "elapsed_seconds": 110.39418506622314,
      "error": "SystemExit(1)",
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 141.19805812835693,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 193.3184244632721,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 40.75466322898865,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 15.636275053024292,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 153.53690481185913,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 4.456480503082275,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 11.094815015792847,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 3.379885196685791,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.51303768157959,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 43.85224676132202,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 15.989100694656372,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 11.955997943878174,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 16.453179836273193,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 17.184957265853882,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 28.003174781799316,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 18.309041500091553,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 4.803859710693359,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 19.318198919296265,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 76.19496417045593,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 113.31644296646118,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 6.802335262298584,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 5.599494695663452,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 12.02379322052002,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 33.70321750640869,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 78.12642526626587,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.0799195766448975,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.8818039894104004,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 7.956937074661255,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 73.50079083442688,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 56.120450019836426,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 432.45079827308655,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 170.17864274978638,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 42.57825827598572,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 17.649738073349,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 17.76207947731018,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 8.446430921554565,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 10.543536186218262,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 10.831355810165405,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 2.9342586994171143,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 4.645190238952637,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 10.905946969985962,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.2924060821533203,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 5.028325319290161,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 2.2936415672302246,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 4.321868419647217,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 5.358749151229858,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 10.463343620300293,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 2.9579761028289795,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 107.91906309127808,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 5.258875370025635,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 5.062286615371704,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 6.515091896057129,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 3.4662816524505615,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.20611834526062,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 9.393598079681396,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 3.076687812805176,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 59.90772557258606,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 62.41150212287903,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 4.978745698928833,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 5.443172931671143,
      "error": null,
      "timestamp": "2026-10-22T13:01:17.946103"
    }
  },
  "drifts": {}
};
