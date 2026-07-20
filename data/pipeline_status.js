window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-20T11:06:46.387987",
  "elapsed_seconds": 466.1122872829437,
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
      "elapsed_seconds": 61.259117126464844,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.7472970485687256,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 0.9659850597381592,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.4894614219665527,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.568207025527954,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 7.45152473449707,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.920253276824951,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.257228374481201,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 3.4055991172790527,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.6695220470428467,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 1.5139501094818115,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 20.339434385299683,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 4.6391661167144775,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.575811147689819,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.8350770473480225,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
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
      "elapsed_seconds": 1.5242550373077393,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 4.146132230758667,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 64.64921951293945,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 5.013648509979248,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.242871284484863,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.4438962936401367,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.6252954006195068,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.5557820796966553,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.503706693649292,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.324171781539917,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.3235464096069336,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.9893603324890137,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.3818016052246094,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 8.484037637710571,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 99.72987270355225,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 202.57229852676392,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 92.0529100894928,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 4.293851137161255,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 6.7916014194488525,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 1.578838586807251,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.4217071533203125,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 36.693153858184814,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 45.572285652160645,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 19.566734552383423,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 123.274742603302,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 31.65095329284668,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.8524770736694336,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 5.374774217605591,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 7.963841915130615,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.673665046691895,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 11.521906614303589,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.52141547203064,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.259381294250488,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.9277870655059814,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 10.043255805969238,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 121.5765061378479,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 8.926161527633667,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.842087268829346,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 14.608227729797363,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 76.93689894676208,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 181.09167051315308,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 6.202762842178345,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 4.507535219192505,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 7.017390012741089,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 41.76496434211731,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 125.16028070449829,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 5.7794740200042725,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.7368903160095215,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 5.268421173095703,
      "error": null,
      "timestamp": "2026-07-20T11:06:46.388162"
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
      "timestamp": "2026-07-20T10:59:09.734552"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-20T10:59:33.924105"
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
      "timestamp": "2026-07-20T11:00:13.187980"
    }
  }
};
