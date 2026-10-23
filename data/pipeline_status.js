window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-22T21:04:31.004212",
  "elapsed_seconds": 539.2277081012726,
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
      "elapsed_seconds": 80.217764377594,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.5987043380737305,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 4.341354131698608,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.4426238536834717,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 11.601189136505127,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 29.62154221534729,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 8.968942165374756,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 9.20219349861145,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 17.24514079093933,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 6.003965854644775,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 97.43580222129822,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 55.17645883560181,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 252.67693758010864,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 7.402819395065308,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 5.170643329620361,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.952345609664917,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.6521997451782227,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 501.88791942596436,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 9.17293930053711,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.286020278930664,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 5.192188739776611,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 5.482004165649414,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 5.570325136184692,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 5.599890947341919,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 5.291731834411621,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 4.249075174331665,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 3.196115732192993,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 3.588655710220337,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 19.511215448379517,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 2.6828579902648926,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 12.148934125900269,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 27.369142055511475,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 10.270310878753662,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 231.3774003982544,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 125.9237654209137,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "ibge_sidra": {
      "status": "error",
      "elapsed_seconds": 110.2520272731781,
      "error": "SystemExit(1)",
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 148.27341055870056,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 162.8293297290802,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 41.98996376991272,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 17.808000802993774,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 98.31692051887512,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 4.799586772918701,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 7.303876876831055,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 4.208423614501953,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 24.14297080039978,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 35.99676728248596,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 5.671477556228638,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 14.764111757278442,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.550858974456787,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 6.460193395614624,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 42.70437526702881,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 16.19672441482544,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 15.111555337905884,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 21.71764874458313,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 58.50416898727417,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 70.65780735015869,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.880630731582642,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 4.441389799118042,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 10.450613021850586,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 27.429954767227173,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 43.500014305114746,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 3.1984505653381348,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 2.1741628646850586,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 11.512405633926392,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 66.82556772232056,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 53.171854734420776,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 427.7020483016968,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 166.19030737876892,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 42.85601592063904,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 37.164228439331055,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 29.50576663017273,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 9.794148206710815,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 10.744251728057861,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 9.02376389503479,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 4.275439739227295,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 5.640583276748657,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 16.41569948196411,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 4.963199138641357,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 5.844082355499268,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 3.2689621448516846,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 5.083871126174927,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 7.474040508270264,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 7.88118314743042,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 3.532595634460449,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 113.86180305480957,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 37.78154945373535,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 46.03363227844238,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 23.252588510513306,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 4.310184717178345,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.90433406829834,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 9.664812326431274,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 6.012346029281616,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 9.298312187194824,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 32.44148921966553,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 7.648597955703735,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 38.453195571899414,
      "error": null,
      "timestamp": "2026-10-22T21:04:31.004483"
    }
  },
  "drifts": {}
};
