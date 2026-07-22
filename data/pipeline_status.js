window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-22T10:51:29.786273",
  "elapsed_seconds": 444.7733817100525,
  "status": "error",
  "summary": {
    "total": 64,
    "success": 64,
    "failed": 1,
    "drifts": 3
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 64.57059741020203,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 3.0836639404296875,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.947235345840454,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.263929843902588,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.734945297241211,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 4.135808944702148,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.231797695159912,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.421581268310547,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.266021966934204,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.0880303382873535,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 2.0452544689178467,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 36.20182204246521,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 6.685742616653442,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.7827394008636475,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.843627691268921,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_carteiras": {
      "status": "unknown",
      "elapsed_seconds": 0.0,
      "error": null,
      "timestamp": null
    },
    "b3_futuros_ajustes": {
      "status": "unknown",
      "elapsed_seconds": 0.0,
      "error": null,
      "timestamp": null
    },
    "b3_indicadores_financeiros": {
      "status": "success",
      "elapsed_seconds": 1.4133703708648682,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.2563085556030273,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 22.170265913009644,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 5.728302717208862,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.47188401222229,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.3752110004425049,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.9362244606018066,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.4917380809783936,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.718869924545288,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.7301342487335205,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.794421911239624,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.4946823120117188,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.7248175144195557,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 12.004384279251099,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 91.00999116897583,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 212.49983882904053,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 86.68811345100403,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.1393871307373047,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 7.506060838699341,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 1.5808489322662354,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 9.13538670539856,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 50.882587909698486,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 55.96352934837341,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 19.64251208305359,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 117.17560577392578,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 32.9482536315918,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.3463993072509766,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 13.777616262435913,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 7.192526578903198,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.156336784362793,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 11.313185691833496,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.616372346878052,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.930410623550415,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 6.204801559448242,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 9.674506664276123,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 115.47376847267151,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 9.189143180847168,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.862512111663818,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 15.181267738342285,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 66.61068511009216,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 159.39036202430725,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.538843870162964,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 4.374792575836182,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 5.187462091445923,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 34.819998264312744,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 98.86716055870056,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.776026010513306,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.4845585823059082,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 4.6974005699157715,
      "error": null,
      "timestamp": "2026-07-22T10:51:29.786450"
    }
  },
  "drifts": {
    "anbima_ranking_global.csv": {
      "added": [],
      "removed": [
        "ordem",
        "administrador",
        "total_global_ativos",
        "clubes_carteiras_administradas_ativos",
        "clubes_carteiras_administradas_cotas_fundos_proprios",
        "clubes_carteiras_administradas_cotas_fundos_terceiros",
        "fundos_em_cotas_ativos",
        "fundos_em_cotas_cotas_fundos_proprios",
        "fundos_em_cotas_cotas_fundos_terceiros",
        "fundos_investimento_ativos",
        "fundos_investimento_cotas_fundos_proprios",
        "fundos_investimento_cotas_fundos_terceiros",
        "sub_total_k",
        "dupla_contagem_l",
        "origem_recursos_do_grupo",
        "origem_recursos_clientes",
        "total_global_ativos_nan",
        "investidor_efpc_emp_publicas",
        "investidor_efpc_emp_privadas",
        "investidor_seguradora",
        "investidor_eapc",
        "investidor_capitalizacao",
        "investidor_corporate",
        "investidor_middle_market",
        "investidor_private",
        "investidor_varejo_alta_renda",
        "investidor_varejo",
        "investidor_poder_publico",
        "investidor_rpps",
        "investidor_fundos_investimento",
        "investidor_estrangeiros",
        "investidor_por_conta_ordem",
        "investidor_outros",
        "renda_fixa_oper_compromissada_tit_publicos_federais",
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
        "renda_variavel_acoes",
        "renda_variavel_opcoes",
        "renda_variavel_outros",
        "renda_variavel_sub_total",
        "clientes_clubes_investimento",
        "clientes_carteiras_administradas",
        "clientes_fundos_em_cotas",
        "clientes_fundos_investimento",
        "clientes_sub_total",
        "clientes_dupla_contagem",
        "clientes_total"
      ],
      "timestamp": "2026-07-22T10:44:13.653574"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-22T10:44:36.969511"
    },
    "bacen_conglomerados.csv": {
      "added": [],
      "removed": [
        "departamento",
        "secao_1",
        "secao_2",
        "secao_3",
        "tipo_documento",
        "data_documento",
        "detalhe"
      ],
      "timestamp": "2026-07-22T10:45:06.436092"
    }
  }
};
