window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-15T09:18:22.059012",
  "elapsed_seconds": 336.96934700012207,
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
      "elapsed_seconds": 61.20901274681091,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.289090633392334,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 0.9919140338897705,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.711013078689575,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 6.882577657699585,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 4.486692190170288,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.302948713302612,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 4.084224700927734,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 1.775113821029663,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 2.5747084617614746,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 1.5370466709136963,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 31.315564155578613,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 4.036414861679077,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.839879035949707,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 2.944011688232422,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
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
      "elapsed_seconds": 1.2013499736785889,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.8618061542510986,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 66.250155210495,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 4.173518657684326,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.449636697769165,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.2054588794708252,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.2295994758605957,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.2577307224273682,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.105149507522583,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.0909569263458252,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.0683033466339111,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.261446237564087,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.194443941116333,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 10.311784029006958,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 81.01432085037231,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 136.58898878097534,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 77.20075178146362,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.4567372798919678,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 7.419778108596802,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 1.585623025894165,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 8.174041271209717,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 41.85459518432617,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 52.34497380256653,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 18.004882097244263,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 125.23320174217224,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 43.844364404678345,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.2991907596588135,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 12.531979084014893,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.5742363929748535,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.95019841194153,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 9.898214101791382,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.251080751419067,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.888708591461182,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.369363307952881,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 8.873653173446655,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 103.0305507183075,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 8.170351028442383,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.763296365737915,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 13.341601133346558,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 37.12235879898071,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 93.61877202987671,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.185938596725464,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.676600694656372,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 2.794257402420044,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 18.35249638557434,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 56.02119541168213,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 3.7036054134368896,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.0721657276153564,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.639855146408081,
      "error": null,
      "timestamp": "2026-07-15T09:18:22.059247"
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
      "timestamp": "2026-07-15T09:12:52.225358"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-15T09:13:12.672529"
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
      "timestamp": "2026-07-15T09:13:58.577224"
    }
  }
};
