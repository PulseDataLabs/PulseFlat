window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-08T02:07:51.678299",
  "elapsed_seconds": 515.9921057224274,
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
      "elapsed_seconds": 84.07203936576843,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 3.3723745346069336,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 3.5835318565368652,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.7340586185455322,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 12.209514379501343,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.7976489067077637,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 8.934253692626953,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 8.187180519104004,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 15.035808563232422,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 5.0963780879974365,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 43.73050308227539,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 59.68297052383423,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 280.3778123855591,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.7892677783966064,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 4.602771043777466,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.4643900394439697,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 4.2454164028167725,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 491.7334249019623,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 8.455559968948364,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.4138431549072266,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 4.968330144882202,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.937905550003052,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 6.209591627120972,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 4.287357330322266,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 4.290918588638306,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 3.855520248413086,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 5.1353185176849365,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 3.9690072536468506,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 37.31812858581543,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 1.8058133125305176,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 13.108811140060425,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 24.42271876335144,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 9.087624311447144,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 2.2970659732818604,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 148, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 84.3616554737091,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 8.774556159973145,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 74.77652907371521,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 255.9439833164215,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 24.603604078292847,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 38.31712746620178,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 339.3653075695038,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.9298574924468994,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 10.70337176322937,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.973942995071411,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 26.67970108985901,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 18.75335717201233,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 5.29332709312439,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 14.71416711807251,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.765149116516113,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 19.125832319259644,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 88.4590232372284,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 16.669087648391724,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 14.792454719543457,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 30.022088527679443,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 76.31322431564331,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 93.51482391357422,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 6.035728693008423,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 5.694656133651733,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 6.168989896774292,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 34.390610694885254,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 67.66726565361023,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 5.666006803512573,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 2.970109224319458,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 15.616811275482178,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 21.301987171173096,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 14.01604151725769,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 430.6381924152374,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 210.18233489990234,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 48.77705764770508,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 16.05843186378479,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 16.17538070678711,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 10.776708841323853,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 10.588891506195068,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 12.12814974784851,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 3.7182931900024414,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 5.580676317214966,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.197403430938721,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.587210178375244,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 4.386017084121704,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 3.584111452102661,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 5.38893985748291,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 5.9163267612457275,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 10.630594253540039,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 3.751127004623413,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 54.404959201812744,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 4.56913685798645,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 3.9271416664123535,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 3.5504024028778076,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 2.6996262073516846,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.194859743118286,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 17.372755765914917,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 5.584838628768921,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 7.123089790344238,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 39.57046842575073,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 3.0597991943359375,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 4.6234962940216064,
      "error": null,
      "timestamp": "2026-10-08T02:07:51.678851"
    }
  },
  "drifts": {}
};
