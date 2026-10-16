window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-16T14:47:20.826639",
  "elapsed_seconds": 461.19290828704834,
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
      "elapsed_seconds": 64.05400156974792,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 1.6813974380493164,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 3.1525490283966064,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.9378533363342285,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 10.774617433547974,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.3725697994232178,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.97179913520813,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 8.739589929580688,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 8.916373014450073,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 2.948058605194092,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 65.77845025062561,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 48.00596785545349,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 213.674565076828,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 6.3669273853302,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 5.027665615081787,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.35358524322509766,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.847134590148926,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 438.35700273513794,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 8.006644248962402,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.303898572921753,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 4.426515102386475,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.417628526687622,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 4.850744247436523,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 3.9153952598571777,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 3.899137258529663,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 3.3667116165161133,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 3.644587516784668,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 3.5686941146850586,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 16.99108648300171,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 2.0637383460998535,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 10.878798007965088,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 19.984052896499634,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 6.027776002883911,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 200.1659436225891,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 97.25404834747314,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.4355573654174805,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 90.73569822311401,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 150.70925450325012,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 34.82638907432556,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 29.35043692588806,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 64.118581533432,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 4.3033974170684814,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 5.680772304534912,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.5280075073242188,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 25.128223180770874,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 23.637980937957764,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.42515230178833,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 14.84844708442688,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 16.8383686542511,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 13.691277980804443,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 48.660585165023804,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 7.075058460235596,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 14.971460103988647,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 21.663114309310913,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 74.98784613609314,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 114.16597747802734,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 6.38095760345459,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 6.806041955947876,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 7.802668571472168,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 43.53085899353027,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 86.52810144424438,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.0740766525268555,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.8465535640716553,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 6.33029580116272,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 42.65079951286316,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 38.26897096633911,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 366.1360948085785,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 174.82645773887634,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 41.12988567352295,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 22.821149110794067,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 16.00320839881897,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 8.473137140274048,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 9.128546476364136,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 8.69448971748352,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 3.0599801540374756,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 3.888803243637085,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 8.384973287582397,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.3092613220214844,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 4.3869948387146,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 2.321523427963257,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 4.260066032409668,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 5.28118896484375,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 8.398900508880615,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 3.1658060550689697,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 98.34770894050598,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 13.79248595237732,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 11.880801916122437,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 6.732804775238037,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 2.842360258102417,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.422589063644409,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 8.56532597541809,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 3.633115530014038,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 53.88025975227356,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 28.915161848068237,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 5.132774591445923,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 13.188520908355713,
      "error": null,
      "timestamp": "2026-10-16T14:47:20.827377"
    }
  },
  "drifts": {}
};
