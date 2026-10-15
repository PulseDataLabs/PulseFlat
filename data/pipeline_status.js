window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-15T15:00:30.676229",
  "elapsed_seconds": 505.15934586524963,
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
      "elapsed_seconds": 78.9399642944336,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 1.61966872215271,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.5573525428771973,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.9580559730529785,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 13.058856010437012,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 1.8458373546600342,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.005135536193848,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.688192367553711,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 10.214854001998901,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.7424240112304688,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 82.995281457901,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 75.96468019485474,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 190.68508434295654,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 6.392121315002441,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 5.1069793701171875,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.4827263355255127,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.761699676513672,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 482.27191948890686,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 5.639346361160278,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.300400495529175,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 3.4007785320281982,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.087670564651489,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 4.051952600479126,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 3.393480062484741,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 3.6494364738464355,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 2.93157696723938,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.8718490600585938,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 2.7130494117736816,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 19.597418069839478,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 2.126335620880127,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 11.256932020187378,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 28.593480587005615,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 7.657903432846069,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 280.74630856513977,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 154.60660791397095,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.6003029346466064,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 122.31099963188171,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 136.91882610321045,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 39.55435919761658,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 35.903847455978394,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 146.50553965568542,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.0624120235443115,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 11.026596307754517,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.239830732345581,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.484609842300415,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 39.39339280128479,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 15.209376811981201,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.272143602371216,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 6.493124723434448,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 8.706036567687988,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 95.11146330833435,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 7.611055612564087,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 16.90124535560608,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 10.299201488494873,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 85.69429326057434,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 75.43760633468628,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.655797243118286,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.826253890991211,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 5.627207040786743,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 23.635176181793213,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 59.953320026397705,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 3.2291438579559326,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.5812900066375732,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 14.419700860977173,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 65.37325429916382,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 51.80901575088501,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 410.20464396476746,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 160.26916313171387,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 44.41592836380005,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 33.558648109436035,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 19.461714029312134,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.204102516174316,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 6.712378263473511,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 6.728096961975098,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 3.487349033355713,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 4.518912076950073,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 10.613970756530762,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.538306951522827,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 3.58803653717041,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 2.187368631362915,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 3.101989984512329,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 5.562503337860107,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 6.976027965545654,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 2.515012741088867,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 99.57298564910889,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 6.499489784240723,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 4.034111976623535,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 3.4031240940093994,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 3.212528944015503,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.0297927856445312,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 7.614477872848511,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 2.6887855529785156,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 77.02152299880981,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 51.40361309051514,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 2.8429887294769287,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 4.328407526016235,
      "error": null,
      "timestamp": "2026-10-15T15:00:30.676497"
    }
  },
  "drifts": {}
};
