window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-14T22:50:23.780589",
  "elapsed_seconds": 1956.509196281433,
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
      "elapsed_seconds": 62.126420974731445,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 4.82911229133606,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.3690533638000488,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 11.871635437011719,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.33236813545227,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.5322675704956055,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (14/08/2026) não corresponde ao D-1 útil (13/08/2026).\n",
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 4.738641738891602,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.646514654159546,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.584584951400757,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 12.479602575302124,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 270.7522497177124,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 63.04143047332764,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.935595512390137,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.4196736812591553,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
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
      "elapsed_seconds": 1.9703617095947266,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.832749843597412,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 225.10906291007996,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 6.0430004596710205,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.6151580810546875,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 2.1727209091186523,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 2.446545124053955,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 3.194777727127075,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.9911043643951416,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 2.0727059841156006,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 2.0458343029022217,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 2.043976306915283,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.8752405643463135,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 258.6310932636261,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 103.5018744468689,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 410.63928413391113,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 106.50648951530457,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 54.7565016746521,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 3.435703754425049,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 143, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 28.091288805007935,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.5546863079071045,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 1565.870065689087,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 28.741072416305542,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 20.221603631973267,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 113.88812851905823,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 69.59233403205872,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.8655474185943604,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 3.9747133255004883,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.5413432121276855,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 53.46277713775635,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 11.016966104507446,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 14.457731246948242,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.72717022895813,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.933213949203491,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 9.903116941452026,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 144.02062726020813,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 9.552289485931396,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 10.900059461593628,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 26.40687870979309,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 43.918389081954956,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 100.56916117668152,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.4543471336364746,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.1686766147613525,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.0701963901519775,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 23.96932291984558,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 64.32343626022339,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 4.251692056655884,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.8154733180999756,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 4.823673725128174,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 34.833980560302734,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 7.228672742843628,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 184.20671892166138,
      "error": null,
      "timestamp": "2026-08-14T22:50:23.780798"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-14T22:17:53.779184"
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
      "timestamp": "2026-08-14T22:20:12.475507"
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
      "timestamp": "2026-08-14T22:22:24.076003"
    }
  }
};
