window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-15T20:42:39.059531",
  "elapsed_seconds": 454.6390392780304,
  "status": "error",
  "summary": {
    "total": 96,
    "success": 95,
    "failed": 1,
    "drifts": 1
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 62.429059743881226,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.1747031211853027,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.604893445968628,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.6749441623687744,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 10.376811027526855,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 22.528237104415894,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 8.035312414169312,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 8.567159414291382,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 11.542691707611084,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.7055914402008057,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 71.9384880065918,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 38.974534034729004,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 156.15209484100342,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.967864513397217,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 4.940310001373291,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.2848978042602539,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 4.490594148635864,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 425.58198976516724,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 27.342243671417236,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.350343704223633,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 3.8136770725250244,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 3.651376724243164,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 4.81151008605957,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 3.7406020164489746,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 3.96099591255188,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 3.366300344467163,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 3.3683836460113525,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 3.1747992038726807,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 18.178840160369873,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 1.650911808013916,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 13.225314140319824,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 21.26612615585327,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 6.4710540771484375,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 169.84445881843567,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 80.45784425735474,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.27604866027832,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 72.59588384628296,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 134.87109208106995,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 33.17360162734985,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 14.285942792892456,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 50.627055644989014,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.1345102787017822,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 4.641038656234741,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 3.509596824645996,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 24.18101716041565,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 16.297446489334106,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.384137153625488,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 14.925652503967285,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 15.453964233398438,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 7.458867073059082,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 51.6932487487793,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 9.688856840133667,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.002755880355835,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 9.1663818359375,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 43.65412878990173,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 82.02707767486572,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.4738407135009766,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.626206398010254,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.340797185897827,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 24.266125440597534,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 48.055206537246704,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.305853843688965,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 2.007446527481079,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 8.229544401168823,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 47.89365601539612,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 33.903847217559814,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 285.61520314216614,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 130.28679060935974,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 41.78876829147339,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 29.67171859741211,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 23.1225106716156,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 6.5107855796813965,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 8.752315282821655,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 7.51998233795166,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 4.6386778354644775,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 5.1631951332092285,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 12.89479398727417,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 4.537775278091431,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 4.795055389404297,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 2.7192749977111816,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 4.812108755111694,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 5.550578832626343,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 7.9363367557525635,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 3.3963873386383057,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 76.05407547950745,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 10.219021320343018,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 10.537056684494019,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 10.779934167861938,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 3.3444976806640625,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.2901716232299805,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 10.519142866134644,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 4.044482707977295,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 10.705272912979126,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 32.31063508987427,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 12.87614130973816,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 7.579617738723755,
      "error": null,
      "timestamp": "2026-10-15T20:42:39.059867"
    }
  },
  "drifts": {
    "anbima_ranking_global.csv": {
      "added": [],
      "removed": [
        "clubes_carteiras_administradas_cotas_fundos_proprios",
        "clubes_carteiras_administradas_cotas_fundos_terceiros",
        "fundos_em_cotas_cotas_fundos_proprios",
        "fundos_em_cotas_cotas_fundos_terceiros",
        "fundos_investimento_cotas_fundos_proprios",
        "fundos_investimento_cotas_fundos_terceiros",
        "origem_recursos_clientes",
        "renda_fixa_oper_compromissada_tit_estaduais_municipais_privados",
        "renda_fixa_tit_publicos_federais",
        "renda_fixa_cdb_rdb",
        "renda_fixa_notas_promissorias",
        "renda_fixa_debentures",
        "renda_fixa_direitos_creditorios",
        "renda_fixa_dpge",
        "renda_fixa_ccb_cccb",
        "renda_fixa_titulos_imobiliarios",
        "renda_fixa_letras_financeiras",
        "renda_fixa_investimento_exterior",
        "renda_fixa_outros",
        "renda_fixa_sub_total",
        "renda_variavel_opcoes",
        "renda_variavel_outros",
        "renda_variavel_sub_total"
      ],
      "timestamp": "2026-10-15T20:35:23.156193"
    }
  }
};
