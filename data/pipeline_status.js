window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-11T21:00:29.582737",
  "elapsed_seconds": 2333.0867443084717,
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
      "elapsed_seconds": 56.484848499298096,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 3.402780294418335,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.6340861320495605,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 8.598483800888062,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 7.2862937450408936,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.20990824699401855,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (11/08/2026) não corresponde ao D-1 útil (10/08/2026).\n",
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.172767639160156,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.073681831359863,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.4207394123077393,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 6.407458305358887,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 177.67814564704895,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 87.47922539710999,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.020867347717285,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 2.896973133087158,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
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
      "elapsed_seconds": 1.07759690284729,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_bdi_di_over": {
      "status": "error",
      "elapsed_seconds": 61.34409952163696,
      "error": "SystemExit(1)",
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 124.9161388874054,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 71.6746666431427,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.474289894104004,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.5547678470611572,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.8852062225341797,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 2.096342086791992,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.5020525455474854,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.3182449340820312,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.3268978595733643,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.6271250247955322,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.3556504249572754,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 205.81698489189148,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 68.63207697868347,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 285.5166575908661,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 77.8620958328247,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 14.79524850845337,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 2057.509363412857,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 44.89257502555847,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 101.2935140132904,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 513.3832640647888,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 48.60281825065613,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 18.895787000656128,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 103.99966168403625,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 42.93990397453308,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.090214729309082,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 3.539275646209717,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 7.058052062988281,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.37485408782959,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 9.382426023483276,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 17.35527753829956,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 3.7679848670959473,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 4.707235097885132,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 17.834929704666138,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 114.17903232574463,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 6.965536832809448,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.492353200912476,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 22.940090656280518,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 29.59717321395874,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 69.84923434257507,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 2.339778423309326,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.144190549850464,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.2087271213531494,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 15.502162218093872,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 40.12131595611572,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.2868597507476807,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.1927733421325684,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.6241273880004883,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 83.94808578491211,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 5.359778642654419,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 131.69522428512573,
      "error": null,
      "timestamp": "2026-08-11T21:00:29.582954"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-11T09:56:07.062989"
    },
    "b3_bdi_etfrf.csv.gz": {
      "added": [],
      "removed": [
        "preco_referencia_d1",
        "oferta_compra",
        "oferta_venda"
      ],
      "timestamp": "2026-08-11T09:56:38.519914"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-08-11T20:24:12.274273"
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
      "timestamp": "2026-08-11T20:25:58.028315"
    }
  }
};
