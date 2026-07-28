window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-28T08:55:57.847744",
  "elapsed_seconds": 2492.5278503894806,
  "status": "error",
  "summary": {
    "total": 64,
    "success": 64,
    "failed": 1,
    "drifts": 2
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 55.56595802307129,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.073486089706421,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.536243200302124,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.068358898162842,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 6.5361127853393555,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 4.248798370361328,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.11624813079834,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 4.4703733921051025,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 3.02071213722229,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 4.040730714797974,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 88.17029118537903,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 67.59900951385498,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 11.081306457519531,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.033387899398804,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.0494332313537598,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
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
      "status": "error",
      "elapsed_seconds": 0.32997918128967285,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 123, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 80, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.451908588409424,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 23.534453868865967,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 4.605281829833984,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.263271808624268,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.53452467918396,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 2.1581082344055176,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.4708244800567627,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.7681457996368408,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.7583723068237305,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.7373924255371094,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.264901876449585,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.7228803634643555,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 19.4184467792511,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 44.99166560173035,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 205.57525205612183,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 70.12248611450195,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 2.2112863063812256,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 363.15161395072937,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 12.319953918457031,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 6.336200714111328,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 2354.4990894794464,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 82.00817322731018,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 16.77096438407898,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 24.108561277389526,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 30.859718084335327,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 1.6308152675628662,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 9.758714437484741,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.472964286804199,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.915638208389282,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 9.456987142562866,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 3.267085313796997,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 4.216805934906006,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 4.672841787338257,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 7.5611279010772705,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 102.28334426879883,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 7.450262784957886,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.652377605438232,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 12.660424709320068,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 27.95020365715027,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 71.5969717502594,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.029447078704834,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.3463103771209717,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 2.7690436840057373,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 15.101006507873535,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 39.509302616119385,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.70627498626709,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.3020105361938477,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.817383050918579,
      "error": null,
      "timestamp": "2026-07-28T08:55:57.848019"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-07-27T23:38:10.987110"
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
      "timestamp": "2026-07-28T08:15:34.555864"
    }
  }
};
