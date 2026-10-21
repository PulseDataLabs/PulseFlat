window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-21T08:47:13.128764",
  "elapsed_seconds": 1203.9271442890167,
  "status": "error",
  "summary": {
    "total": 96,
    "success": 86,
    "failed": 10,
    "drifts": 0
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 59.99698758125305,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.198385000228882,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.5768697261810303,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.325443744659424,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 11.390811920166016,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 1.8237390518188477,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 9.438215017318726,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 8.193739414215088,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 8.053986549377441,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.8246591091156006,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 63.8520712852478,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 56.72759509086609,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 205.93517065048218,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 6.298473358154297,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 4.3325605392456055,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.38539910316467285,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.212692975997925,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 455.2000105381012,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 6.682861566543579,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.276474952697754,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 4.730530500411987,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.725377559661865,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 5.976704359054565,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 4.016041040420532,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 4.212508678436279,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 2.9046616554260254,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 3.129495620727539,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 3.2352256774902344,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 15.581140995025635,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 2.069154739379883,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 75.67732119560242,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 23.581949949264526,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 12.231327295303345,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 212.47242736816406,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 112.17318916320801,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "ibge_sidra": {
      "status": "error",
      "elapsed_seconds": 109.4203634262085,
      "error": "SystemExit(1)",
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 134.3347887992859,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 170.15024375915527,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 27.149007320404053,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 5.802839279174805,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 65.11036133766174,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.368608236312866,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 4.846269845962524,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.937636137008667,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 28.292539596557617,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 20.378945112228394,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "ipea_calendario": {
      "status": "error",
      "elapsed_seconds": 143.3387005329132,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_calendario.py\", line 46, in fetch\n    return self.fetch_series_list(SERIES)\n           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/ipea_base.py\", line 118, in fetch_series_list\n    raise RuntimeError(\"Nenhum dado retornado para as séries do IPEA.\")\nRuntimeError: Nenhum dado retornado para as séries do IPEA.\n",
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "ipea_comercio_exterior": {
      "status": "error",
      "elapsed_seconds": 142.56776642799377,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_comercio_exterior.py\", line 46, in fetch\n    return self.fetch_series_list(SERIES)\n           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/ipea_base.py\", line 118, in fetch_series_list\n    raise RuntimeError(\"Nenhum dado retornado para as séries do IPEA.\")\nRuntimeError: Nenhum dado retornado para as séries do IPEA.\n",
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "ipea_fbcf": {
      "status": "error",
      "elapsed_seconds": 284.9760468006134,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_fbcf.py\", line 60, in fetch\n    return self.fetch_series_list(SERIES)\n           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/ipea_base.py\", line 118, in fetch_series_list\n    raise RuntimeError(\"Nenhum dado retornado para as séries do IPEA.\")\nRuntimeError: Nenhum dado retornado para as séries do IPEA.\n",
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "ipea_macroeconomia": {
      "status": "error",
      "elapsed_seconds": 354.5370750427246,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_macroeconomia.py\", line 67, in fetch\n    return self.fetch_series_list(SERIES)\n           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/ipea_base.py\", line 118, in fetch_series_list\n    raise RuntimeError(\"Nenhum dado retornado para as séries do IPEA.\")\nRuntimeError: Nenhum dado retornado para as séries do IPEA.\n",
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "ipea_mercados_diarios": {
      "status": "error",
      "elapsed_seconds": 284.7253227233887,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_mercados_diarios.py\", line 60, in fetch\n    return self.fetch_series_list(SERIES)\n           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/ipea_base.py\", line 118, in fetch_series_list\n    raise RuntimeError(\"Nenhum dado retornado para as séries do IPEA.\")\nRuntimeError: Nenhum dado retornado para as séries do IPEA.\n",
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "ipea_precos_inflacao": {
      "status": "error",
      "elapsed_seconds": 284.1322889328003,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_precos_inflacao.py\", line 60, in fetch\n    return self.fetch_series_list(SERIES)\n           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/ipea_base.py\", line 118, in fetch_series_list\n    raise RuntimeError(\"Nenhum dado retornado para as séries do IPEA.\")\nRuntimeError: Nenhum dado retornado para as séries do IPEA.\n",
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "ipea_producao_mineral": {
      "status": "error",
      "elapsed_seconds": 213.18165802955627,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_producao_mineral.py\", line 53, in fetch\n    return self.fetch_series_list(SERIES)\n           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/ipea_base.py\", line 118, in fetch_series_list\n    raise RuntimeError(\"Nenhum dado retornado para as séries do IPEA.\")\nRuntimeError: Nenhum dado retornado para as séries do IPEA.\n",
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "ipea_taxas_juros": {
      "status": "error",
      "elapsed_seconds": 782.5068485736847,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_taxas_juros.py\", line 109, in fetch\n    return self.fetch_series_list(SERIES)\n           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/ipea_base.py\", line 118, in fetch_series_list\n    raise RuntimeError(\"Nenhum dado retornado para as séries do IPEA.\")\nRuntimeError: Nenhum dado retornado para as séries do IPEA.\n",
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 31.62824845314026,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 63.86436223983765,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 2.9298224449157715,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.3601772785186768,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.316899299621582,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 17.330588340759277,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 44.421441316604614,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.6214184761047363,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.2923283576965332,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.107083320617676,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 36.42199349403381,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 34.161890268325806,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 383.75755763053894,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 159.82530879974365,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 37.083057165145874,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 19.271601915359497,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 18.86275315284729,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 8.357347965240479,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 10.536752223968506,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 10.53587794303894,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 2.8723790645599365,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 5.475727081298828,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 10.325217247009277,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.688354730606079,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 5.661104440689087,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 1.9354946613311768,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 5.863530397415161,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 6.856806755065918,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 10.272433280944824,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 2.6915571689605713,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 102.69156789779663,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 5.446725845336914,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 12.992222785949707,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 7.405119180679321,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 3.532550811767578,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.5192530155181885,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 9.77156400680542,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 4.017568826675415,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 27.357045888900757,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 73.5389952659607,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 5.794166088104248,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 13.210386037826538,
      "error": null,
      "timestamp": "2026-10-21T08:47:13.129073"
    }
  },
  "drifts": {}
};
