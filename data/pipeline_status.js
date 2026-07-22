window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-22T11:43:49.228664",
  "elapsed_seconds": 486.15938115119934,
  "status": "error",
  "summary": {
    "total": 64,
    "success": 64,
    "failed": 1,
    "drifts": 1
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 64.12568068504333,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 3.068699836730957,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.0518009662628174,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.445751190185547,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.738834857940674,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 7.7123847007751465,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.030496597290039,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.360889911651611,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.6845908164978027,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.3619391918182373,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 2.125828266143799,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 35.08600616455078,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 7.748314142227173,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 7.851781606674194,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.7953593730926514,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
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
      "elapsed_seconds": 1.942448616027832,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.9981706142425537,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 22.03515100479126,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 5.778685569763184,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.715017318725586,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.456312656402588,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 2.147850275039673,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.5640661716461182,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.8291220664978027,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.5933277606964111,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.6980512142181396,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.6606416702270508,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.626422643661499,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 10.94596242904663,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 98.68641471862793,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 224.7326111793518,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 93.21280837059021,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 5.1966705322265625,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 7.578094005584717,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 1.6077032089233398,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 8.27352261543274,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 52.958186626434326,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 58.30718231201172,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 20.63700008392334,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 124.48028373718262,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 33.48623323440552,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.5430703163146973,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 13.219241857528687,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 7.681496858596802,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.18087339401245,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 11.213769674301147,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.494772434234619,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 5.248109579086304,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 7.331573009490967,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 11.401764631271362,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 120.65999627113342,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 9.579915761947632,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 7.16204047203064,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 15.232558727264404,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 79.39632773399353,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 184.63605403900146,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 6.535353183746338,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 5.11383843421936,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 6.033676385879517,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 43.86314272880554,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 122.9354555606842,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 6.548082113265991,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.72340989112854,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 4.759304523468018,
      "error": null,
      "timestamp": "2026-07-22T11:43:49.228878"
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
      "timestamp": "2026-07-22T11:35:53.098949"
    }
  }
};
