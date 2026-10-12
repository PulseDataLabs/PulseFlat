window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-12T18:12:29.302646",
  "elapsed_seconds": 467.9916467666626,
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
      "elapsed_seconds": 90.87328815460205,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.0355615615844727,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.41153621673584,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 1.8660824298858643,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 9.885059356689453,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.2135777473449707,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.443167448043823,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.821062326431274,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 9.045921802520752,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.0398612022399902,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 48.91905426979065,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 53.06317186355591,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 211.0108242034912,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.776185035705566,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.620424270629883,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.36589813232421875,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.0721569061279297,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 446.71032905578613,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 7.244872093200684,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.143643856048584,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 4.814560174942017,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 3.4055042266845703,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 5.580216407775879,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 3.444608211517334,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 4.1334388256073,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 2.851813793182373,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 2.674203872680664,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 3.3017168045043945,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 12.77494502067566,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 1.8289248943328857,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 8.626321792602539,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 26.347847938537598,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 9.99345850944519,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 224.34537887573242,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 96.52127408981323,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 8.42909836769104,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 84.79083132743835,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 154.87093329429626,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 21.627669095993042,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 19.579380750656128,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 55.629526138305664,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.240269660949707,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 7.7501983642578125,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.604296922683716,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.86881971359253,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 15.861816883087158,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 5.986335754394531,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 10.102102041244507,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 10.912596464157104,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 10.922547817230225,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 62.167393922805786,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 7.1512064933776855,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 4.378695964813232,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 8.899750232696533,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 86.09710431098938,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 102.1387026309967,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 5.215083837509155,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 4.234050750732422,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.721415281295776,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 41.02455711364746,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 64.57247972488403,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 5.15361475944519,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 2.582709550857544,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 13.559847593307495,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 23.17831015586853,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 13.642227172851562,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 374.6946768760681,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 184.43999361991882,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 40.109601974487305,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 42.13689160346985,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 29.41261124610901,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.316112995147705,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 7.783255100250244,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 7.087209463119507,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 3.2173256874084473,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 3.582021713256836,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 10.883039474487305,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.0958826541900635,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 3.6608214378356934,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 2.268979072570801,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 3.005474805831909,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 4.78375244140625,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 7.775944232940674,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 2.580209970474243,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 54.04367542266846,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 5.3715500831604,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 3.584688186645508,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 3.329108238220215,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 3.561343193054199,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.8291268348693848,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 9.399556636810303,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 4.734303951263428,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 75.27517533302307,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 159.78779816627502,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 3.3158087730407715,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 3.818544626235962,
      "error": null,
      "timestamp": "2026-10-12T18:12:29.302908"
    }
  },
  "drifts": {}
};
