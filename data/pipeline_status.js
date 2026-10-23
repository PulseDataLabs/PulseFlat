window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-23T15:05:59.504421",
  "elapsed_seconds": 511.5213963985443,
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
      "elapsed_seconds": 75.65783786773682,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.7238917350769043,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.9487130641937256,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.9589781761169434,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 11.17588472366333,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.4225707054138184,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.886710166931152,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.312818288803101,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 13.396794557571411,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.2895185947418213,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 62.204073429107666,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 49.86709427833557,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 270.9565670490265,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 7.426910877227783,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 5.3294878005981445,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.6784946918487549,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.0821197032928467,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 487.19982147216797,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 8.319835901260376,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.4658844470977783,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 4.448469161987305,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.340739488601685,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 5.24388313293457,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 4.259204864501953,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 3.7563369274139404,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 2.893016815185547,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 3.2917845249176025,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 3.14518666267395,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 18.02618718147278,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 2.1784684658050537,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 10.292968988418579,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 22.96912145614624,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 5.329403400421143,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 236.67459273338318,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 79.04591369628906,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "ibge_sidra": {
      "status": "error",
      "elapsed_seconds": 111.44714331626892,
      "error": "SystemExit(1)",
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 89.24407482147217,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 72.14975595474243,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 27.735997438430786,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 20.155798196792603,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 80.33800601959229,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.5024631023406982,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 6.252094507217407,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.095824956893921,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 25.114975214004517,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 17.86059021949768,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 15.521652221679688,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 15.906753301620483,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 7.655697822570801,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 7.840528249740601,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 73.15290832519531,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 15.247786283493042,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 6.680197715759277,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 29.42186951637268,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 87.79910492897034,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 100.82805371284485,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 8.285452842712402,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 5.056724786758423,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.8800437450408936,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 39.760804414749146,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 73.81660914421082,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 6.66265082359314,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 4.152735710144043,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 16.330010652542114,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 38.57218813896179,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 33.990898847579956,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 425.5567002296448,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 195.29803729057312,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 35.46831202507019,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 30.809812784194946,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 19.630264043807983,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 7.467948913574219,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 7.362547874450684,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 7.414819717407227,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 2.854865312576294,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 3.8022003173828125,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 9.68222451210022,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.6325061321258545,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 3.172166109085083,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 2.702507734298706,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 4.049416542053223,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 4.693582773208618,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 7.4598708152771,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 3.010558605194092,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 99.98414492607117,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 15.907711267471313,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 19.34865927696228,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 13.754889726638794,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 6.497309446334839,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.645322799682617,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 11.74838638305664,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 4.335251092910767,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 24.876402139663696,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 34.540441036224365,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 23.943538427352905,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 35.09372019767761,
      "error": null,
      "timestamp": "2026-10-23T15:05:59.504901"
    }
  },
  "drifts": {}
};
