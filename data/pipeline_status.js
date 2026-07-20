window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-20T11:48:26.355773",
  "elapsed_seconds": 466.6603262424469,
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
      "elapsed_seconds": 62.285638093948364,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.5829224586486816,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.1203467845916748,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.5907607078552246,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.650263786315918,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 4.3477349281311035,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.880490779876709,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.879035472869873,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.835635185241699,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.4153871536254883,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 2.2717998027801514,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 33.14814734458923,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 6.071225881576538,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.0437188148498535,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.2803056240081787,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
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
      "elapsed_seconds": 1.5797622203826904,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.2282159328460693,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 71.25490283966064,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 5.296243667602539,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.496906518936157,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.4452695846557617,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.7104003429412842,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.5592174530029297,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.3869566917419434,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.5204107761383057,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.53035569190979,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.5223331451416016,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.3345661163330078,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 9.625861167907715,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 104.93184971809387,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 212.4630274772644,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 97.27411890029907,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 5.741098165512085,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 7.227589845657349,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 2.171126365661621,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.731277942657471,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 48.45403528213501,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 54.49218511581421,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 20.93162488937378,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 140.9101424217224,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 35.14686131477356,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.028113603591919,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 12.327834606170654,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 9.148786306381226,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.791590690612793,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 10.993843793869019,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.930224418640137,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 5.297121524810791,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 6.4278717041015625,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 10.440052509307861,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 132.3208613395691,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 9.906277179718018,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 7.239783525466919,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 14.60534119606018,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 67.78139853477478,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 165.41546297073364,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 6.854226112365723,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 4.575541734695435,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 5.864245414733887,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 37.77695608139038,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 110.53167724609375,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 5.408901214599609,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.6726796627044678,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 4.492142677307129,
      "error": null,
      "timestamp": "2026-07-20T11:48:26.355961"
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
      "timestamp": "2026-07-20T11:40:49.384035"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-20T11:41:12.194917"
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
      "timestamp": "2026-07-20T11:41:55.691054"
    }
  }
};
