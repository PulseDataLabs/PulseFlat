window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-23T10:55:42.717518",
  "elapsed_seconds": 374.52565121650696,
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
      "elapsed_seconds": 56.81056594848633,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 1.893681526184082,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 0.9873182773590088,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 1.9695684909820557,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 4.651830196380615,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 4.61803674697876,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 4.158445358276367,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.82809853553772,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 1.567742109298706,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.0472805500030518,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 1.6917200088500977,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 11.848608255386353,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 6.183318614959717,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.571386098861694,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 2.7784857749938965,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
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
      "elapsed_seconds": 0.9745681285858154,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.422161102294922,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 234.41467809677124,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 3.7940821647644043,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.118420839309692,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 0.9924819469451904,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.0901808738708496,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.102806568145752,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.3157060146331787,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 0.951059103012085,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 0.9382386207580566,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.0335676670074463,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 0.9368596076965332,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 7.263353586196899,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 40.14820146560669,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 188.7638087272644,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 66.8376886844635,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 2.798893928527832,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 7.093010425567627,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 1.257453203201294,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 5.9556496143341064,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 40.160738706588745,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 48.44009184837341,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 17.64922285079956,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 100.55505394935608,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 28.57663369178772,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 1.6671762466430664,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 3.488309621810913,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 7.580728530883789,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.12501049041748,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 9.901167869567871,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 3.459956407546997,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 3.8894805908203125,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.466910123825073,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 7.986175537109375,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 92.1218478679657,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 7.445543527603149,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.044862270355225,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 11.214742422103882,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 40.70032000541687,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 96.24467658996582,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.369060039520264,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.244737148284912,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.291607618331909,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 19.358986139297485,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 52.43099808692932,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.9935176372528076,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 0.9362292289733887,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.1205554008483887,
      "error": null,
      "timestamp": "2026-07-23T10:55:42.717732"
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
      "timestamp": "2026-07-23T10:49:34.882070"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-23T10:49:53.736049"
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
      "timestamp": "2026-07-23T10:50:31.391665"
    }
  }
};
