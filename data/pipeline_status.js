window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-04T20:53:57.102549",
  "elapsed_seconds": 6319.7106149196625,
  "status": "error",
  "summary": {
    "total": 66,
    "success": 66,
    "failed": 2,
    "drifts": 3
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 54.42145919799805,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 4.8646650314331055,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.9994938373565674,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 9.331971645355225,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 7.264244794845581,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.19803237915039062,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (04/08/2026) não corresponde ao D-1 útil (03/08/2026).\n",
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 4.31734037399292,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 4.213330030441284,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.4824442863464355,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 6.522278070449829,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 144.39430260658264,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 65.92277717590332,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.711782693862915,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.143869638442993,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
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
      "elapsed_seconds": 1.1691904067993164,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 34.66925024986267,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 217.00429463386536,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 33.42090392112732,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.300764322280884,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 0.9636728763580322,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.0910258293151855,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.2144968509674072,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.0666632652282715,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 0.9640297889709473,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 0.937920093536377,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.0859289169311523,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 0.9555709362030029,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 184.10309052467346,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 149.35356426239014,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 250.727454662323,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 67.85652303695679,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "bacen_conglomerados": {
      "status": "error",
      "elapsed_seconds": 0.6231164932250977,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_conglomerados.py\", line 71, in fetch\n    print_warn(f\"{yyyymm}CONGLOMERADO.zip não disponível\", elapsed=time.time() - t0)\n    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nTypeError: print_warn() got an unexpected keyword argument 'elapsed'\n",
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 1168.2976174354553,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 24.216379165649414,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 13.41036581993103,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 5906.941281080246,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 60.71727418899536,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 17.531291007995605,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 108.01046371459961,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 71.74982118606567,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 1.6013901233673096,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 18.735907316207886,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 7.624959230422974,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 21.706664085388184,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 10.68090009689331,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 3.6001555919647217,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.42822003364563,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 5.550891160964966,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 8.127243041992188,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 105.3783175945282,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 9.133707523345947,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.556107759475708,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 12.480430126190186,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 31.018306016921997,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 75.20544767379761,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 2.2337443828582764,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.312333345413208,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.2303736209869385,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 15.440207242965698,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 48.35793662071228,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 11.819732666015625,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 0.9907090663909912,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.679001569747925,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 39.99810075759888,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 4.583218336105347,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 160.86734437942505,
      "error": null,
      "timestamp": "2026-08-04T20:53:57.102827"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-04T19:08:43.432900"
    },
    "b3_bdi_etfrf.csv.gz": {
      "added": [],
      "removed": [
        "preco_referencia_d1",
        "oferta_compra",
        "oferta_venda"
      ],
      "timestamp": "2026-08-03T23:40:42.555907"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-08-04T19:10:40.783553"
    }
  }
};
