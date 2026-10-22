window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-22T08:35:36.528198",
  "elapsed_seconds": 501.08158016204834,
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
      "elapsed_seconds": 62.94074988365173,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.5003750324249268,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 4.678457498550415,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.7813446521759033,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 11.188691139221191,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.8725829124450684,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 7.14478874206543,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.67233943939209,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 14.614309787750244,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 6.223040342330933,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 60.350438833236694,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 56.177542209625244,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 211.40731287002563,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 7.95786190032959,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 5.494107961654663,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.2867710590362549,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.440197229385376,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 475.35509490966797,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 8.40079116821289,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.21769642829895,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 5.123375177383423,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 5.211204767227173,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 4.639540195465088,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 5.062403440475464,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 4.481104612350464,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 3.7926700115203857,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 3.797297239303589,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 4.150137901306152,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 9.085197925567627,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 3.556584119796753,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 13.590329885482788,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 33.2918484210968,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 5.683956623077393,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 4.264536142349243,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 148, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 177.13810873031616,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 9.307520151138306,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 159.72016954421997,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 177.12240767478943,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 30.210379362106323,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 11.675056457519531,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 157.54672527313232,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 5.269558668136597,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 10.69962191581726,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.726775646209717,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.272528648376465,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 18.375281810760498,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 15.144829750061035,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 16.42036461830139,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 6.495652914047241,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 21.021158456802368,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 44.398380756378174,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 12.41178274154663,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 16.83627963066101,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 10.100929260253906,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 41.323633909225464,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 57.061230182647705,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.268489360809326,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.482496500015259,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.849858522415161,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 16.246634244918823,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 40.19919943809509,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 3.2596752643585205,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.920926809310913,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 9.678927183151245,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 39.73639249801636,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 31.60767364501953,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 349.9092400074005,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 172.14759492874146,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 58.07780861854553,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 26.2742018699646,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 16.340766668319702,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.812095403671265,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 7.573660135269165,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 8.537712574005127,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 4.08262300491333,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 4.373685598373413,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.10637354850769,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.1117188930511475,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 4.801784515380859,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 4.428985595703125,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 7.2093424797058105,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 6.107011318206787,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 7.270727872848511,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 3.1048591136932373,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 69.82412552833557,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 9.154574155807495,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 9.386835098266602,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 6.176626682281494,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 2.666353225708008,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.6614062786102295,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 8.666703224182129,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 3.964404821395874,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 3.0793275833129883,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 29.325928211212158,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 7.9380528926849365,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 8.03447937965393,
      "error": null,
      "timestamp": "2026-10-22T08:35:36.528752"
    }
  },
  "drifts": {}
};
