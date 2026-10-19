window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-19T14:35:03.133927",
  "elapsed_seconds": 517.9467389583588,
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
      "elapsed_seconds": 68.45617127418518,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 3.0816287994384766,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 3.2396883964538574,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.915328025817871,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 12.511160850524902,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 3.5522069931030273,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 10.420376062393188,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 11.359356164932251,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 15.340733289718628,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 4.055654048919678,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 65.16641664505005,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 54.436293840408325,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 266.4167218208313,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 6.895939350128174,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 5.349151372909546,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.4968252182006836,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.2644124031066895,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 494.3234407901764,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 8.044100999832153,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.562913656234741,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 6.369822263717651,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.955080270767212,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 5.779520273208618,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 5.43859338760376,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 5.715356349945068,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 4.222686767578125,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 3.924286365509033,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 4.170072078704834,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 16.614670276641846,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 2.180046796798706,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 10.701267719268799,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 27.342774152755737,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 11.215616226196289,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 251.94142484664917,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 115.20451164245605,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 9.241076707839966,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 107.50589203834534,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 202.70225739479065,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 29.898812532424927,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 5.934217929840088,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 83.89707946777344,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 4.0215067863464355,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 5.887691259384155,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 3.4326775074005127,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 26.447211742401123,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 20.77509641647339,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 15.944022178649902,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 15.736148118972778,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.638465166091919,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 30.471688747406006,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 68.6920838356018,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 6.2825682163238525,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 14.643390893936157,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 8.859249353408813,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 80.27464199066162,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 107.328852891922,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 5.0580291748046875,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 5.857734441757202,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 10.772460222244263,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 42.436901330947876,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 75.76565074920654,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 5.557511806488037,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 2.930147886276245,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 8.965200185775757,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 42.19369435310364,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 34.824514865875244,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 416.75462007522583,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 197.99891114234924,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 51.87576222419739,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 14.72141408920288,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 17.57023787498474,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.811233997344971,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 11.45659613609314,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 11.563258647918701,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 2.8764209747314453,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 4.893342971801758,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 10.936135292053223,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 4.153276205062866,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 5.648272275924683,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 2.9138245582580566,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 4.817383050918579,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 5.805345058441162,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 9.198753356933594,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 3.797133445739746,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 104.6463680267334,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 12.234357595443726,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 14.42045259475708,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 17.175183296203613,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 3.4502527713775635,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.7653164863586426,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 9.801245927810669,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 6.021028757095337,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 32.960686683654785,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 29.91184687614441,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 13.88414716720581,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 19.313558101654053,
      "error": null,
      "timestamp": "2026-10-19T14:35:03.134400"
    }
  },
  "drifts": {}
};
