window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-23T11:49:54.152903",
  "elapsed_seconds": 464.7981607913971,
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
      "elapsed_seconds": 57.709829568862915,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.7994000911712646,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 0.998647928237915,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.927243232727051,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.331281661987305,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 7.269908666610718,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.6730921268463135,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 4.889899015426636,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 3.433629035949707,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 2.9028234481811523,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 1.5414304733276367,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 16.47084927558899,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 4.7490129470825195,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.1756837368011475,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.2696714401245117,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
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
      "elapsed_seconds": 1.3808186054229736,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 4.237511396408081,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 116.3145215511322,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 5.264920711517334,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.235715389251709,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.8477659225463867,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.5332434177398682,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.808373212814331,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.356740951538086,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.4971261024475098,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.3474581241607666,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.604407787322998,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.433621883392334,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 8.988315105438232,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 57.5086145401001,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 224.2354609966278,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 92.63600945472717,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 2.947505235671997,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 7.709374904632568,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 2.568333148956299,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.699022531509399,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 43.22127151489258,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 47.1640100479126,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 19.724425554275513,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 148.15631413459778,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 33.53021192550659,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.905771493911743,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 19.63173484802246,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 7.197408437728882,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.128914833068848,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 11.44787883758545,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.619608402252197,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 5.673935413360596,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 6.385139226913452,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 10.726778507232666,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 123.89122033119202,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 9.816482305526733,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 7.864187955856323,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 14.71666407585144,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 77.81276369094849,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 177.07176113128662,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 6.40678071975708,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 5.700247049331665,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 6.611553430557251,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 50.539642572402954,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 118.07670426368713,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 6.330916881561279,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.7563936710357666,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.9229040145874023,
      "error": null,
      "timestamp": "2026-07-23T11:49:54.153056"
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
      "timestamp": "2026-07-23T11:42:18.549963"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-23T11:42:42.320045"
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
      "timestamp": "2026-07-23T11:43:20.379016"
    }
  }
};
