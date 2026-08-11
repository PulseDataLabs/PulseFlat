window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-10T23:04:18.660861",
  "elapsed_seconds": 851.8442440032959,
  "status": "error",
  "summary": {
    "total": 66,
    "success": 62,
    "failed": 6,
    "drifts": 3
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 60.15367794036865,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 4.980674505233765,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.1654367446899414,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 12.174816608428955,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 9.415527820587158,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.5214009284973145,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (10/08/2026) não corresponde ao D-1 útil (07/08/2026).\n",
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.8197691440582275,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.458142280578613,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 3.135023593902588,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 8.970032215118408,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 241.39161229133606,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 14.425476551055908,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.4031596183776855,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.351198673248291,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
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
      "elapsed_seconds": 1.9329392910003662,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.8877434730529785,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 257.7110197544098,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 6.69546914100647,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 27.624155282974243,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 2.6812362670898438,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 2.3039140701293945,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 2.696488857269287,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 2.106106996536255,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 2.4101366996765137,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.8923776149749756,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 2.065749406814575,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 2.075448989868164,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 267.83566093444824,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "bcb_ptax": {
      "status": "error",
      "elapsed_seconds": 15.225428342819214,
      "error": "SystemExit(1)",
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "bcb_sgs": {
      "status": "error",
      "elapsed_seconds": 97.7299211025238,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bcb_sgs.py\", line 127, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bcb_sgs.py\", line 104, in capturar\n    raise RuntimeError(\"Nenhum dado capturado do BCB SGS.\")\nRuntimeError: Nenhum dado capturado do BCB SGS.\n",
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "bacen_balancetes_bancos": {
      "status": "error",
      "elapsed_seconds": 3.0931437015533447,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_balancetes_bancos.py\", line 68, in fetch\n    resp_file.raise_for_status()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/requests/models.py\", line 1167, in raise_for_status\n    raise HTTPError(http_error_msg, response=self)\nrequests.exceptions.HTTPError: 502 Server Error: Bad Gateway for url: https://www.bcb.gov.br/content/estabilidadefinanceira/cosif/Bancos/202603BANCOS.csv.zip\n",
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "bacen_conglomerados": {
      "status": "error",
      "elapsed_seconds": 2.262465238571167,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_conglomerados.py\", line 71, in fetch\n    print_warn(f\"{yyyymm}CONGLOMERADO.zip não disponível\", elapsed=time.time() - t0)\n    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nTypeError: print_warn() got an unexpected keyword argument 'elapsed'\n",
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 12.268546342849731,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 143, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 3.9123852252960205,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.8804848194122314,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 513.2491993904114,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 36.784194469451904,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 37.9496591091156,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 121.37572050094604,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 48.416927099227905,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.126185417175293,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 4.577337741851807,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.3692121505737305,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 56.180015563964844,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 11.681094408035278,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 8.92443585395813,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 18.38814377784729,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 11.12268590927124,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 15.78863000869751,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 140.85234546661377,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 22.51456093788147,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 17.489585399627686,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 18.226252555847168,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 45.06971526145935,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 102.68021941184998,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.4616804122924805,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 3.269224166870117,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 4.574414491653442,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 31.421187162399292,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 64.7281801700592,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 3.740494966506958,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.4724218845367432,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 4.767777919769287,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 44.666322231292725,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 7.4885334968566895,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 194.16214179992676,
      "error": null,
      "timestamp": "2026-08-10T23:04:18.661078"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-10T22:50:14.714528"
    },
    "b3_bdi_etfrf.csv.gz": {
      "added": [],
      "removed": [
        "preco_referencia_d1",
        "oferta_compra",
        "oferta_venda"
      ],
      "timestamp": "2026-08-10T07:14:27.068637"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-08-10T22:52:55.852611"
    }
  }
};
