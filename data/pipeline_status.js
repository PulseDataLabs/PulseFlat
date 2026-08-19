window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-19T00:39:04.261061",
  "elapsed_seconds": 2435.4899940490723,
  "status": "error",
  "summary": {
    "total": 66,
    "success": 66,
    "failed": 2,
    "drifts": 4
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 54.265809059143066,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 4.191884994506836,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.9954423904418945,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 11.137687683105469,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.789616107940674,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.40167975425720215,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (18/08/2026) não corresponde ao D-1 útil (17/08/2026).\n",
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.43989896774292,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.700947046279907,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.28136944770813,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 7.620267629623413,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 268.15024852752686,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 13.587117671966553,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.821854829788208,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.1047556400299072,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
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
      "elapsed_seconds": 2.475461959838867,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.7359988689422607,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 206.64753770828247,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 6.477648973464966,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.3737711906433105,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.813887119293213,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.7811968326568604,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 2.316845178604126,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.7105052471160889,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.6936395168304443,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.8312904834747314,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.9901351928710938,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.7215361595153809,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 21.82965064048767,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 100.0526225566864,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 389.5856866836548,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 87.59745740890503,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.225637197494507,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 2.8386542797088623,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 143, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 54.16094446182251,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 6.980028390884399,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 2135.357654809952,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 34.691082239151,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 19.72503113746643,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 18.844275951385498,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 56.42969822883606,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.5391716957092285,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 4.026829957962036,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.059531927108765,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.098888874053955,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 10.669282674789429,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 14.12256383895874,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 14.706977605819702,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 18.910826444625854,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 12.178197622299194,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 131.07063555717468,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 19.01951003074646,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 8.790194749832153,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 15.579976558685303,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 53.12652611732483,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 113.90897130966187,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.589300870895386,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.938210964202881,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.526408433914185,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 24.002152919769287,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 68.30171060562134,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 14.690165996551514,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.6667473316192627,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 2.828556776046753,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 32.507713317871094,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 6.988047361373901,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 164.42487502098083,
      "error": null,
      "timestamp": "2026-08-19T00:39:04.261335"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-18T23:58:35.088143"
    },
    "b3_bdi_etfrf.csv.gz": {
      "added": [],
      "removed": [
        "preco_referencia_d1",
        "oferta_compra",
        "oferta_venda"
      ],
      "timestamp": "2026-08-18T06:29:17.654754"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-08-19T00:00:18.262789"
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
      "timestamp": "2026-08-19T00:02:09.924172"
    }
  }
};
