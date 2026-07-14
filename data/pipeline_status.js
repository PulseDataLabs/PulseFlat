window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-14T11:32:16.090603",
  "elapsed_seconds": 374.28246307373047,
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
      "elapsed_seconds": 59.961742877960205,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.595543622970581,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.2506885528564453,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 1.8457860946655273,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.16134786605835,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 5.472578525543213,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 4.163142681121826,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.149113416671753,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.103673219680786,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.455543041229248,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 1.7198600769042969,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 27.68475103378296,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 4.0716636180877686,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.564838171005249,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.0809788703918457,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
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
      "elapsed_seconds": 1.4421718120574951,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.9132723808288574,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 68.83534836769104,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 4.708739757537842,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.492269515991211,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.2811048030853271,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.4205193519592285,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.3265841007232666,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.3102107048034668,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.1528489589691162,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.298905611038208,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.3205063343048096,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.151918888092041,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 11.176187515258789,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 82.59013748168945,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 138.13922810554504,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 79.19722628593445,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 4.316141843795776,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 6.2185304164886475,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 1.5569672584533691,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.392364978790283,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 38.48616671562195,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 50.54134488105774,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 19.298682928085327,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 121.16719269752502,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 49.675814628601074,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.450963020324707,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 5.0475029945373535,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 8.414344787597656,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.18354058265686,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 7.400648355484009,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.274789810180664,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 5.043354749679565,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.823468923568726,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 8.979585886001587,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 105.88954162597656,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 8.293664932250977,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 6.100936651229858,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 12.941487789154053,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 66.26673817634583,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 145.8899941444397,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.186258316040039,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.7026233673095703,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.034150838851929,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 23.33444333076477,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 19.70145559310913,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.8404154777526855,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.3577873706817627,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.770900249481201,
      "error": null,
      "timestamp": "2026-07-14T11:32:16.090822"
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
      "timestamp": "2026-07-14T11:26:09.809036"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-14T11:26:28.100013"
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
      "timestamp": "2026-07-14T11:27:20.232007"
    }
  }
};
