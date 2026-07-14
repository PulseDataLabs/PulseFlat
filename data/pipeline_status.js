window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-14T07:46:33.063493",
  "elapsed_seconds": 249.56726360321045,
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
      "elapsed_seconds": 53.934617042541504,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 1.9721152782440186,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.2472245693206787,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 1.9325752258300781,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 5.669118404388428,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 3.7635135650634766,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 4.25579047203064,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.8499839305877686,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.169198989868164,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.1417269706726074,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 1.6930453777313232,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 12.275441884994507,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 3.337449312210083,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.298957824707031,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.0483953952789307,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
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
      "elapsed_seconds": 2.1390492916107178,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.511913299560547,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 70.68306303024292,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 4.414229869842529,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.3452842235565186,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.2774004936218262,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.2996160984039307,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.431596040725708,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.2210917472839355,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.1843514442443848,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.2218852043151855,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.1991424560546875,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.306410789489746,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 10.763113498687744,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 27.72532057762146,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 102.1082329750061,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 72.51344585418701,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.176529884338379,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 6.252046585083008,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 1.5861968994140625,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.369599342346191,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 23.582942247390747,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 45.13444256782532,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 18.528326272964478,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 32.786895513534546,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 40.80648183822632,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 1.492790937423706,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 3.421123743057251,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.1025519371032715,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.268900871276855,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 10.237165927886963,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.108906984329224,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 3.7282984256744385,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 4.600989818572998,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 7.659933090209961,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 93.00729179382324,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 8.929654121398926,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.102913856506348,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 11.207249402999878,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 27.53140950202942,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 71.19217085838318,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 2.563040256500244,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.4550702571868896,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 2.764561891555786,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 13.436597347259521,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 35.98635506629944,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.541746139526367,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.3874821662902832,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.1697731018066406,
      "error": null,
      "timestamp": "2026-07-14T07:46:33.063713"
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
      "timestamp": "2026-07-14T07:42:30.117518"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-14T07:42:51.735869"
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
      "timestamp": "2026-07-14T07:43:30.489221"
    }
  }
};
