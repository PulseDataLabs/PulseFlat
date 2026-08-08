window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-07T23:23:41.748927",
  "elapsed_seconds": 2368.8011622428894,
  "status": "error",
  "summary": {
    "total": 66,
    "success": 67,
    "failed": 1,
    "drifts": 4
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 56.95988202095032,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 5.458638429641724,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.9429841041564941,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 10.799150705337524,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.557907819747925,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.4945833683013916,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (07/08/2026) não corresponde ao D-1 útil (06/08/2026).\n",
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 4.719691276550293,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.4731035232543945,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.364504814147949,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 7.809540033340454,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 194.8684437274933,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 123.79965162277222,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.762181758880615,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.124171018600464,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
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
      "elapsed_seconds": 1.4836235046386719,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.9258713722229004,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 250.0107822418213,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 6.493478536605835,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.216422080993652,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.985337495803833,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 2.0909743309020996,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.886406421661377,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.783315658569336,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.8141098022460938,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 2.1939635276794434,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.713000774383545,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.6820085048675537,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 241.26249361038208,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 179.51446294784546,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 344.75801181793213,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 87.02432632446289,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.7483177185058594,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 2100.8471381664276,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 11.898548603057861,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 20.410534381866455,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 212.6710352897644,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 32.913347244262695,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 19.94216251373291,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 111.49180769920349,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 43.09187293052673,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.8907132148742676,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 28.96088933944702,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 5.798924684524536,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.211236715316772,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 10.860492944717407,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.416907548904419,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.88815975189209,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 16.011576175689697,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 9.506319999694824,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 120.35446095466614,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 9.945509433746338,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 6.943534851074219,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 23.331880569458008,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 58.47797918319702,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 134.62419438362122,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 4.637321710586548,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 4.4226977825164795,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 5.858000040054321,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 34.15899443626404,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 92.01838660240173,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 5.222757577896118,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.424743890762329,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.58449387550354,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 30.964226961135864,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 6.261624336242676,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 126.58320140838623,
      "error": null,
      "timestamp": "2026-08-07T23:23:41.749103"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-07T22:44:18.905211"
    },
    "b3_bdi_etfrf.csv.gz": {
      "added": [],
      "removed": [
        "preco_referencia_d1",
        "oferta_compra",
        "oferta_venda"
      ],
      "timestamp": "2026-08-07T06:59:26.007691"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-08-07T22:46:01.487803"
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
      "timestamp": "2026-08-07T22:48:38.602671"
    }
  }
};
