window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-15T00:17:33.792188",
  "elapsed_seconds": 1467.550853252411,
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
      "elapsed_seconds": 55.177624464035034,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 4.213091611862183,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 0.8445835113525391,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 9.840437889099121,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 6.658800363540649,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.2130577564239502,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (14/08/2026) não corresponde ao D-1 útil (13/08/2026).\n",
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 4.050715923309326,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.526459455490112,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 3.3722188472747803,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 6.774944305419922,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 221.36013889312744,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 84.25822687149048,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 3.9350061416625977,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 2.757925510406494,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
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
      "elapsed_seconds": 1.0536952018737793,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.0619091987609863,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 237.2491159439087,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 5.39766526222229,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.109617233276367,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 2.2023911476135254,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 2.2169482707977295,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 2.187835216522217,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.904940128326416,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.9363901615142822,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.753525972366333,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.9211938381195068,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.7985646724700928,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 198.70392227172852,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 75.1147837638855,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 299.67017674446106,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 67.63280200958252,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.1457388401031494,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 2.459200620651245,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 143, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 45.81983804702759,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 6.395348787307739,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 1137.7612299919128,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 38.78624773025513,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 19.033490657806396,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 96.08995246887207,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 52.079384326934814,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 1.5852718353271484,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 3.4541678428649902,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 4.407543659210205,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 21.561517000198364,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 9.724740505218506,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 3.238731622695923,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 13.796379566192627,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 14.734999656677246,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 19.714259386062622,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 103.36545920372009,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 19.89927649497986,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.9577250480651855,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 22.483558893203735,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 30.250606536865234,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 70.845538854599,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 2.548048496246338,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.542583703994751,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.1792819499969482,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 15.257336616516113,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 40.779566526412964,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.711747169494629,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.378922462463379,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 2.4007949829101562,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 43.46463465690613,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 5.3882787227630615,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 158.81025958061218,
      "error": null,
      "timestamp": "2026-08-15T00:17:33.792452"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-14T23:53:12.113621"
    },
    "b3_bdi_etfrf.csv.gz": {
      "added": [],
      "removed": [
        "preco_referencia_d1",
        "oferta_compra",
        "oferta_venda"
      ],
      "timestamp": "2026-08-14T06:58:08.964756"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-08-14T23:54:46.669434"
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
      "timestamp": "2026-08-14T23:57:16.369111"
    }
  }
};
