window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-29T20:25:46.530519",
  "elapsed_seconds": 5310.55152797699,
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
      "elapsed_seconds": 58.30473756790161,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 6.733681678771973,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.2074081897735596,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.8670594692230225,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 6.8332579135894775,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.6194231510162354,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (29/07/2026) não corresponde ao D-1 útil (28/07/2026).\n",
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.9085400104522705,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.998786211013794,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 4.8271825313568115,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.8702683448791504,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 138.43738889694214,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 17.381622791290283,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 4.74525785446167,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.5581419467926025,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 4.0049238204956055,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
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
      "elapsed_seconds": 1.3389408588409424,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 8.475000858306885,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 183.5372142791748,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 7.3769965171813965,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.212530136108398,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.3463621139526367,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.5124104022979736,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.5197229385375977,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.4053189754486084,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.3263604640960693,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.3479759693145752,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.3707249164581299,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.3651340007781982,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 252.44661712646484,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 190.8325698375702,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 302.1927914619446,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 96.09634327888489,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.815078020095825,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 924.4011781215668,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 10.29736042022705,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 8.4984130859375,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 4913.695972919464,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 128.8555724620819,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 20.886481046676636,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 121.10532474517822,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 23.077921152114868,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.2328872680664062,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 25.226206302642822,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 6.091476202011108,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "error",
      "elapsed_seconds": 61.11776900291443,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 534, in _make_request\n    response = conn.getresponse()\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 571, in getresponse\n    httplib_response = super().getresponse()\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/http/client.py\", line 1459, in getresponse\n    response.begin()\n    ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/http/client.py\", line 336, in begin\n    version, status, reason = self._read_status()\n                              ~~~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/http/client.py\", line 297, in _read_status\n    line = str(self.fp.readline(_MAXLINE + 1), \"iso-8859-1\")\n               ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/socket.py\", line 723, in readinto\n    return self._sock.recv_into(b)\n           ~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/ssl.py\", line 1304, in recv_into\n    return self.read(nbytes, buffer)\n           ~~~~~~~~~^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/ssl.py\", line 1138, in read\n    return self._sslobj.read(len, buffer)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^\nTimeoutError: The read operation timed out\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 842, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 498, in increment\n    raise reraise(type(error), error, _stacktrace)\n          ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/urllib3/util/util.py\", line 39, in reraise\n    raise value\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 788, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 536, in _make_request\n    self._raise_timeout(err=e, url=url, timeout_value=read_timeout)\n    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 367, in _raise_timeout\n    raise ReadTimeoutError(\n        self, url, f\"Read timed out. (read timeout={timeout_value})\"\n    ) from err\nurllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='www.b3.com.br', port=443): Read timed out. (read timeout=30)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 81, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 39, in capturar\n    resp = session.get(url, timeout=180)\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 85, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 76, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/requests/adapters.py\", line 742, in send\n    raise ReadTimeout(e, request=request)\nrequests.exceptions.ReadTimeout: HTTPSConnectionPool(host='www.b3.com.br', port=443): Read timed out. (read timeout=30)\n",
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 12.00568151473999,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 5.613473176956177,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 5.263025760650635,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 6.295043230056763,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 10.389524698257446,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 161.63255500793457,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 13.762525796890259,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 8.123112201690674,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 18.16915988922119,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 35.48984885215759,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 87.72091126441956,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.2489371299743652,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.7536373138427734,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.231572389602661,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 18.087756633758545,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 62.60274314880371,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 18.032235622406006,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.2619173526763916,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 5.1489715576171875,
      "error": null,
      "timestamp": "2026-07-29T20:25:46.530714"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-07-29T18:57:24.154685"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-29T18:58:06.143599"
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
      "timestamp": "2026-07-29T19:00:32.687469"
    }
  }
};
