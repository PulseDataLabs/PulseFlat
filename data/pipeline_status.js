window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-21T08:10:36.050109",
  "elapsed_seconds": 295.7337522506714,
  "status": "error",
  "summary": {
    "total": 64,
    "success": 63,
    "failed": 2,
    "drifts": 3
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 54.826523780822754,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.002469539642334,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.155951738357544,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.6128897666931152,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 5.463842868804932,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 4.5396568775177,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.4068520069122314,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.696522951126099,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.811906576156616,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.2142422199249268,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "anbima_indice_imab": {
      "status": "error",
      "elapsed_seconds": 1.9618382453918457,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 60, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_indice_imab.py\", line 32, in capturar\n    header_existente = read_existing_header(ARQUIVO)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 336, in read_existing_header\n    first = f.readline().strip()\n            ~~~~~~~~~~^^\n  File \"<frozen codecs>\", line 325, in decode\nUnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte\n",
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 21.799782276153564,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 4.239764213562012,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.654315233230591,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.6692705154418945,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
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
      "elapsed_seconds": 1.575223684310913,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.411332130432129,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 22.880080461502075,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 4.6250834465026855,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.350857496261597,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.3994791507720947,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.9371802806854248,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.45528244972229,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 2.2296853065490723,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.8638100624084473,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.8700275421142578,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.3448750972747803,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.5497868061065674,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 15.59014344215393,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 43.02219867706299,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 158.36373829841614,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 86.04682350158691,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 5.838551044464111,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 2.683375597000122,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 143, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 1.975820541381836,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 22.530859231948853,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 30.429931163787842,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 38.73936128616333,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 17.923011302947998,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 22.779876947402954,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 35.00595760345459,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.207097053527832,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 3.6976280212402344,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 5.094268798828125,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.997040510177612,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 10.203549146652222,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.478226900100708,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.148794412612915,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.373273611068726,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 8.772399187088013,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 103.27866983413696,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 8.282320976257324,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.315265893936157,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 14.158276081085205,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 33.488691329956055,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 87.21748995780945,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.668269634246826,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.046675682067871,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.198762893676758,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 18.84363627433777,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 49.13656568527222,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.9334943294525146,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.411280870437622,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.5091142654418945,
      "error": null,
      "timestamp": "2026-07-21T08:10:36.050309"
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
      "timestamp": "2026-07-21T08:05:47.995937"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-21T08:06:11.077978"
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
      "timestamp": "2026-07-21T08:06:37.543598"
    }
  }
};
