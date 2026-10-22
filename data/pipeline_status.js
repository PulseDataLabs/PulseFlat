window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-22T14:00:59.647319",
  "elapsed_seconds": 545.8726444244385,
  "status": "error",
  "summary": {
    "total": 96,
    "success": 94,
    "failed": 2,
    "drifts": 1
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 67.68993973731995,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.2641475200653076,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.8774538040161133,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.822384834289551,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 10.378554105758667,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.2956221103668213,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 7.848616361618042,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.628337860107422,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 11.822407960891724,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 5.630620241165161,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 88.37540626525879,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 66.81284999847412,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 216.1071126461029,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 7.07021427154541,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 4.617992639541626,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.37337160110473633,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.7552051544189453,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 521.9199798107147,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 6.629418134689331,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.2777440547943115,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 4.04922342300415,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.1447367668151855,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 8.721034288406372,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 4.112091302871704,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 3.4135537147521973,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 2.799506664276123,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 3.270850419998169,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 2.9481327533721924,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 6.666296005249023,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 4.696532249450684,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 27.049174785614014,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 36.9179413318634,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 14.60807180404663,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 254.93342208862305,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 174.88529896736145,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "ibge_sidra": {
      "status": "error",
      "elapsed_seconds": 109.72596311569214,
      "error": "SystemExit(1)",
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 137.04569625854492,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 161.01170229911804,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 41.52208399772644,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 13.6842622756958,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 169.72586011886597,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.263507127761841,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 13.756375312805176,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.355577230453491,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.28445339202881,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 41.15593194961548,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 3.5402374267578125,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 3.746309280395508,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 4.26439642906189,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 6.006119728088379,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 58.756391286849976,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 17.350101947784424,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 6.344037294387817,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 20.73297119140625,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 74.54894018173218,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 98.26767539978027,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 5.258322238922119,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 7.6376471519470215,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 9.758957862854004,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 28.16734480857849,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 59.01708388328552,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 3.437063455581665,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.4797003269195557,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 5.587923765182495,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 71.77665162086487,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 56.15358805656433,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 438.51197361946106,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 170.15693044662476,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 33.97324347496033,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 30.88473129272461,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 20.382041931152344,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 6.946240425109863,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 9.016008615493774,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 7.994154691696167,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 5.214776515960693,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 2.716519355773926,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 11.091261625289917,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.3169589042663574,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 4.814838647842407,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 2.4313223361968994,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 3.80230450630188,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 4.146468162536621,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 7.900542974472046,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 2.8745970726013184,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 112.95304298400879,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 4.28126859664917,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 4.103382349014282,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 3.6171233654022217,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 3.1069087982177734,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.257955312728882,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 7.251659154891968,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 3.1323885917663574,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 74.8560242652893,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 38.448479413986206,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 4.288157939910889,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 5.537179231643677,
      "error": null,
      "timestamp": "2026-10-22T14:00:59.647878"
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
      "timestamp": "2026-10-22T13:52:08.671161"
    }
  }
};
