window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-11T23:13:50.306734",
  "elapsed_seconds": 674.3614947795868,
  "status": "error",
  "summary": {
    "total": 66,
    "success": 54,
    "failed": 14,
    "drifts": 4
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 55.678104639053345,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 3.998702049255371,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.7816236019134521,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 9.447050094604492,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 8.143006801605225,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.40198516845703125,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (11/08/2026) não corresponde ao D-1 útil (10/08/2026).\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 6.025160551071167,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 5.907795429229736,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.300546169281006,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 6.483568429946899,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 187.113698720932,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 12.040365219116211,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.18815016746521,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 2.8814730644226074,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
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
      "elapsed_seconds": 1.070016622543335,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.375699520111084,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 428.9221522808075,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 67.22802662849426,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 47.23463535308838,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.364366054534912,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.239318609237671,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.1850144863128662,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.005798578262329,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.0038552284240723,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.4176113605499268,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.0067760944366455,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 0.9722247123718262,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 196.0683331489563,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 68.7578456401825,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 306.95769238471985,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 68.15665650367737,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 2.4215943813323975,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 2.362269163131714,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 143, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 13.037764310836792,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "ibge_sidra": {
      "status": "error",
      "elapsed_seconds": 109.13238143920898,
      "error": "SystemExit(1)",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "cvm_fundos_informe_diario": {
      "status": "error",
      "elapsed_seconds": 146.17909574508667,
      "error": "SystemExit(1)",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "cvm_fundos_classe": {
      "status": "error",
      "elapsed_seconds": 73.25946545600891,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 204, in _new_conn\n    sock = connection.create_connection(\n        (self._dns_host, self.port),\n    ...<2 lines>...\n        socket_options=self.socket_options,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 85, in create_connection\n    raise err\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 73, in create_connection\n    sock.connect(sa)\n    ~~~~~~~~~~~~^^^^\nOSError: [Errno 101] Network is unreachable\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 788, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 488, in _make_request\n    raise new_e\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 464, in _make_request\n    self._validate_conn(conn)\n    ~~~~~~~~~~~~~~~~~~~^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 1106, in _validate_conn\n    conn.connect()\n    ~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 759, in connect\n    self.sock = sock = self._new_conn()\n                       ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 219, in _new_conn\n    raise NewConnectionError(\n        self, f\"Failed to establish a new connection: {e}\"\n    ) from e\nurllib3.exceptions.NewConnectionError: HTTPSConnection(host='dados.cvm.gov.br', port=443): Failed to establish a new connection: [Errno 101] Network is unreachable\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 842, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 543, in increment\n    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nurllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='dados.cvm.gov.br', port=443): Max retries exceeded with url: /dados/FI/CAD/DADOS/registro_fundo_classe.zip (Caused by NewConnectionError(\"HTTPSConnection(host='dados.cvm.gov.br', port=443): Failed to establish a new connection: [Errno 101] Network is unreachable\"))\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/generic_scraper.py\", line 140, in fetch\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/generic_scraper.py\", line 133, in fetch\n    resp = session.get(url, timeout=120)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 85, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 76, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 729, in send\n    raise ConnectionError(e, request=request)\nrequests.exceptions.ConnectionError: HTTPSConnectionPool(host='dados.cvm.gov.br', port=443): Max retries exceeded with url: /dados/FI/CAD/DADOS/registro_fundo_classe.zip (Caused by NewConnectionError(\"HTTPSConnection(host='dados.cvm.gov.br', port=443): Failed to establish a new connection: [Errno 101] Network is unreachable\"))\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 17.78567099571228,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 93.54596400260925,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 63.654114723205566,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 1.6068620681762695,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "error",
      "elapsed_seconds": 21.16679573059082,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 204, in _new_conn\n    sock = connection.create_connection(\n        (self._dns_host, self.port),\n    ...<2 lines>...\n        socket_options=self.socket_options,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 85, in create_connection\n    raise err\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 73, in create_connection\n    sock.connect(sa)\n    ~~~~~~~~~~~~^^^^\nOSError: [Errno 101] Network is unreachable\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 788, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 488, in _make_request\n    raise new_e\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 464, in _make_request\n    self._validate_conn(conn)\n    ~~~~~~~~~~~~~~~~~~~^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 1106, in _validate_conn\n    conn.connect()\n    ~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 759, in connect\n    self.sock = sock = self._new_conn()\n                       ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 219, in _new_conn\n    raise NewConnectionError(\n        self, f\"Failed to establish a new connection: {e}\"\n    ) from e\nurllib3.exceptions.NewConnectionError: HTTPSConnection(host='dados.cvm.gov.br', port=443): Failed to establish a new connection: [Errno 101] Network is unreachable\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 842, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 543, in increment\n    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nurllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='dados.cvm.gov.br', port=443): Max retries exceeded with url: /dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv (Caused by NewConnectionError(\"HTTPSConnection(host='dados.cvm.gov.br', port=443): Failed to establish a new connection: [Errno 101] Network is unreachable\"))\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/cvm_cadastro_companhias_abertas.py\", line 58, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/cvm_cadastro_companhias_abertas.py\", line 27, in capturar\n    resp = session.get(URL, timeout=180)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 85, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 76, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 729, in send\n    raise ConnectionError(e, request=request)\nrequests.exceptions.ConnectionError: HTTPSConnectionPool(host='dados.cvm.gov.br', port=443): Max retries exceeded with url: /dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv (Caused by NewConnectionError(\"HTTPSConnection(host='dados.cvm.gov.br', port=443): Failed to establish a new connection: [Errno 101] Network is unreachable\"))\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 5.052922964096069,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 21.70662522315979,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 9.781738042831421,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "ipea_calendario": {
      "status": "error",
      "elapsed_seconds": 20.315398454666138,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 204, in _new_conn\n    sock = connection.create_connection(\n        (self._dns_host, self.port),\n    ...<2 lines>...\n        socket_options=self.socket_options,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 85, in create_connection\n    raise err\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 73, in create_connection\n    sock.connect(sa)\n    ~~~~~~~~~~~~^^^^\nTimeoutError: timed out\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 788, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 493, in _make_request\n    conn.request(\n    ~~~~~~~~~~~~^\n        method,\n        ^^^^^^^\n    ...<6 lines>...\n        enforce_content_length=enforce_content_length,\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 500, in request\n    self.endheaders()\n    ~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1381, in endheaders\n    self._send_output(message_body, encode_chunked=encode_chunked)\n    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1141, in _send_output\n    self.send(msg)\n    ~~~~~~~~~^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1085, in send\n    self.connect()\n    ~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 331, in connect\n    self.sock = self._new_conn()\n                ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 213, in _new_conn\n    raise ConnectTimeoutError(\n    ...<2 lines>...\n    ) from e\nurllib3.exceptions.ConnectTimeoutError: (<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75925e46e0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)')\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 842, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 543, in increment\n    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nurllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='SGS12_NDIASUTEISFUT12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75925e46e0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_calendario.py\", line 34, in fetch\n    resp = session.get(url, timeout=60)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 82, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 76, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 717, in send\n    raise ConnectTimeout(e, request=request)\nrequests.exceptions.ConnectTimeout: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='SGS12_NDIASUTEISFUT12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75925e46e0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "ipea_comercio_exterior": {
      "status": "error",
      "elapsed_seconds": 20.298285484313965,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 204, in _new_conn\n    sock = connection.create_connection(\n        (self._dns_host, self.port),\n    ...<2 lines>...\n        socket_options=self.socket_options,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 85, in create_connection\n    raise err\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 73, in create_connection\n    sock.connect(sa)\n    ~~~~~~~~~~~~^^^^\nTimeoutError: timed out\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 788, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 493, in _make_request\n    conn.request(\n    ~~~~~~~~~~~~^\n        method,\n        ^^^^^^^\n    ...<6 lines>...\n        enforce_content_length=enforce_content_length,\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 500, in request\n    self.endheaders()\n    ~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1381, in endheaders\n    self._send_output(message_body, encode_chunked=encode_chunked)\n    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1141, in _send_output\n    self.send(msg)\n    ~~~~~~~~~^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1085, in send\n    self.connect()\n    ~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 331, in connect\n    self.sock = self._new_conn()\n                ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 213, in _new_conn\n    raise ConnectTimeoutError(\n    ...<2 lines>...\n    ) from e\nurllib3.exceptions.ConnectTimeoutError: (<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75922eac10>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)')\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 842, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 543, in increment\n    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nurllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='FUNCEX12_XPT12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75922eac10>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_comercio_exterior.py\", line 34, in fetch\n    resp = session.get(url, timeout=60)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 82, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 76, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 717, in send\n    raise ConnectTimeout(e, request=request)\nrequests.exceptions.ConnectTimeout: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='FUNCEX12_XPT12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75922eac10>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "ipea_fbcf": {
      "status": "error",
      "elapsed_seconds": 20.34597134590149,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 204, in _new_conn\n    sock = connection.create_connection(\n        (self._dns_host, self.port),\n    ...<2 lines>...\n        socket_options=self.socket_options,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 85, in create_connection\n    raise err\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 73, in create_connection\n    sock.connect(sa)\n    ~~~~~~~~~~~~^^^^\nTimeoutError: timed out\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 788, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 493, in _make_request\n    conn.request(\n    ~~~~~~~~~~~~^\n        method,\n        ^^^^^^^\n    ...<6 lines>...\n        enforce_content_length=enforce_content_length,\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 500, in request\n    self.endheaders()\n    ~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1381, in endheaders\n    self._send_output(message_body, encode_chunked=encode_chunked)\n    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1141, in _send_output\n    self.send(msg)\n    ~~~~~~~~~^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1085, in send\n    self.connect()\n    ~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 331, in connect\n    self.sock = self._new_conn()\n                ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 213, in _new_conn\n    raise ConnectTimeoutError(\n    ...<2 lines>...\n    ) from e\nurllib3.exceptions.ConnectTimeoutError: (<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75922e9f90>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)')\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 842, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 543, in increment\n    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nurllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='GAC12_INDFBCF12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75922e9f90>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_fbcf.py\", line 34, in fetch\n    resp = session.get(url, timeout=60)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 82, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 76, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 717, in send\n    raise ConnectTimeout(e, request=request)\nrequests.exceptions.ConnectTimeout: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='GAC12_INDFBCF12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75922e9f90>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "ipea_macroeconomia": {
      "status": "error",
      "elapsed_seconds": 20.303396224975586,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 204, in _new_conn\n    sock = connection.create_connection(\n        (self._dns_host, self.port),\n    ...<2 lines>...\n        socket_options=self.socket_options,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 85, in create_connection\n    raise err\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 73, in create_connection\n    sock.connect(sa)\n    ~~~~~~~~~~~~^^^^\nTimeoutError: timed out\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 788, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 493, in _make_request\n    conn.request(\n    ~~~~~~~~~~~~^\n        method,\n        ^^^^^^^\n    ...<6 lines>...\n        enforce_content_length=enforce_content_length,\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 500, in request\n    self.endheaders()\n    ~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1381, in endheaders\n    self._send_output(message_body, encode_chunked=encode_chunked)\n    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1141, in _send_output\n    self.send(msg)\n    ~~~~~~~~~^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1085, in send\n    self.connect()\n    ~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 331, in connect\n    self.sock = self._new_conn()\n                ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 213, in _new_conn\n    raise ConnectTimeoutError(\n    ...<2 lines>...\n    ) from e\nurllib3.exceptions.ConnectTimeoutError: (<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f7591592fd0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)')\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 842, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 543, in increment\n    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nurllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='BM12_PIBAC12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f7591592fd0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_macroeconomia.py\", line 34, in fetch\n    resp = session.get(url, timeout=60)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 82, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 76, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 717, in send\n    raise ConnectTimeout(e, request=request)\nrequests.exceptions.ConnectTimeout: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='BM12_PIBAC12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f7591592fd0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "ipea_mercados_diarios": {
      "status": "error",
      "elapsed_seconds": 20.312795639038086,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 204, in _new_conn\n    sock = connection.create_connection(\n        (self._dns_host, self.port),\n    ...<2 lines>...\n        socket_options=self.socket_options,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 85, in create_connection\n    raise err\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 73, in create_connection\n    sock.connect(sa)\n    ~~~~~~~~~~~~^^^^\nTimeoutError: timed out\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 788, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 493, in _make_request\n    conn.request(\n    ~~~~~~~~~~~~^\n        method,\n        ^^^^^^^\n    ...<6 lines>...\n        enforce_content_length=enforce_content_length,\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 500, in request\n    self.endheaders()\n    ~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1381, in endheaders\n    self._send_output(message_body, encode_chunked=encode_chunked)\n    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1141, in _send_output\n    self.send(msg)\n    ~~~~~~~~~^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1085, in send\n    self.connect()\n    ~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 331, in connect\n    self.sock = self._new_conn()\n                ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 213, in _new_conn\n    raise ConnectTimeoutError(\n    ...<2 lines>...\n    ) from e\nurllib3.exceptions.ConnectTimeoutError: (<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f759232d0f0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)')\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 842, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 543, in increment\n    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nurllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='EIA366_PBRENT366') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f759232d0f0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_mercados_diarios.py\", line 34, in fetch\n    resp = session.get(url, timeout=60)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 82, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 76, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 717, in send\n    raise ConnectTimeout(e, request=request)\nrequests.exceptions.ConnectTimeout: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='EIA366_PBRENT366') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f759232d0f0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "ipea_precos_inflacao": {
      "status": "error",
      "elapsed_seconds": 20.342528581619263,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 204, in _new_conn\n    sock = connection.create_connection(\n        (self._dns_host, self.port),\n    ...<2 lines>...\n        socket_options=self.socket_options,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 85, in create_connection\n    raise err\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 73, in create_connection\n    sock.connect(sa)\n    ~~~~~~~~~~~~^^^^\nTimeoutError: timed out\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 788, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 493, in _make_request\n    conn.request(\n    ~~~~~~~~~~~~^\n        method,\n        ^^^^^^^\n    ...<6 lines>...\n        enforce_content_length=enforce_content_length,\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 500, in request\n    self.endheaders()\n    ~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1381, in endheaders\n    self._send_output(message_body, encode_chunked=encode_chunked)\n    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1141, in _send_output\n    self.send(msg)\n    ~~~~~~~~~^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1085, in send\n    self.connect()\n    ~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 331, in connect\n    self.sock = self._new_conn()\n                ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 213, in _new_conn\n    raise ConnectTimeoutError(\n    ...<2 lines>...\n    ) from e\nurllib3.exceptions.ConnectTimeoutError: (<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75900c0290>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)')\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 842, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 543, in increment\n    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nurllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='IGP12_IGPDI12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75900c0290>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_precos_inflacao.py\", line 34, in fetch\n    resp = session.get(url, timeout=60)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 82, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 76, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 717, in send\n    raise ConnectTimeout(e, request=request)\nrequests.exceptions.ConnectTimeout: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='IGP12_IGPDI12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f75900c0290>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "ipea_producao_mineral": {
      "status": "error",
      "elapsed_seconds": 20.362149238586426,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 204, in _new_conn\n    sock = connection.create_connection(\n        (self._dns_host, self.port),\n    ...<2 lines>...\n        socket_options=self.socket_options,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 85, in create_connection\n    raise err\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 73, in create_connection\n    sock.connect(sa)\n    ~~~~~~~~~~~~^^^^\nTimeoutError: timed out\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 788, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 493, in _make_request\n    conn.request(\n    ~~~~~~~~~~~~^\n        method,\n        ^^^^^^^\n    ...<6 lines>...\n        enforce_content_length=enforce_content_length,\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 500, in request\n    self.endheaders()\n    ~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1381, in endheaders\n    self._send_output(message_body, encode_chunked=encode_chunked)\n    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1141, in _send_output\n    self.send(msg)\n    ~~~~~~~~~^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1085, in send\n    self.connect()\n    ~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 331, in connect\n    self.sock = self._new_conn()\n                ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 213, in _new_conn\n    raise ConnectTimeoutError(\n    ...<2 lines>...\n    ) from e\nurllib3.exceptions.ConnectTimeoutError: (<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f758964bdf0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)')\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 842, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 543, in increment\n    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nurllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='IBSIE12_QSCFG12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f758964bdf0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_producao_mineral.py\", line 34, in fetch\n    resp = session.get(url, timeout=60)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 82, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 76, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 717, in send\n    raise ConnectTimeout(e, request=request)\nrequests.exceptions.ConnectTimeout: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='IBSIE12_QSCFG12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f758964bdf0>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "ipea_taxas_juros": {
      "status": "error",
      "elapsed_seconds": 20.332740545272827,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 204, in _new_conn\n    sock = connection.create_connection(\n        (self._dns_host, self.port),\n    ...<2 lines>...\n        socket_options=self.socket_options,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 85, in create_connection\n    raise err\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/connection.py\", line 73, in create_connection\n    sock.connect(sa)\n    ~~~~~~~~~~~~^^^^\nTimeoutError: timed out\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 788, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 493, in _make_request\n    conn.request(\n    ~~~~~~~~~~~~^\n        method,\n        ^^^^^^^\n    ...<6 lines>...\n        enforce_content_length=enforce_content_length,\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 500, in request\n    self.endheaders()\n    ~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1381, in endheaders\n    self._send_output(message_body, encode_chunked=encode_chunked)\n    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1141, in _send_output\n    self.send(msg)\n    ~~~~~~~~~^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1085, in send\n    self.connect()\n    ~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 331, in connect\n    self.sock = self._new_conn()\n                ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 213, in _new_conn\n    raise ConnectTimeoutError(\n    ...<2 lines>...\n    ) from e\nurllib3.exceptions.ConnectTimeoutError: (<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f758964bf00>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)')\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 842, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 543, in increment\n    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nurllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='ANBIMA12_TJPOUP12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f758964bf00>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/ipea_taxas_juros.py\", line 34, in fetch\n    resp = session.get(url, timeout=60)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 82, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 76, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 717, in send\n    raise ConnectTimeout(e, request=request)\nrequests.exceptions.ConnectTimeout: HTTPConnectionPool(host='www.ipeadata.gov.br', port=80): Max retries exceeded with url: /api/odata4/ValoresSerie(SERCODIGO='ANBIMA12_TJPOUP12') (Caused by ConnectTimeoutError(<HTTPConnection(host='www.ipeadata.gov.br', port=80) at 0x7f758964bf00>, 'Connection to www.ipeadata.gov.br timed out. (connect timeout=10)'))\n",
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 31.716161489486694,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 71.53576993942261,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 2.3893868923187256,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.7288014888763428,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.317728042602539,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 16.40471625328064,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 42.76954507827759,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.390913248062134,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.0391120910644531,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.1051437854766846,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 56.27509331703186,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 4.822258710861206,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 149.5516381263733,
      "error": null,
      "timestamp": "2026-08-11T23:13:50.306993"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-11T23:02:41.889703"
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
      "timestamp": "2026-08-11T23:04:55.186893"
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
      "timestamp": "2026-08-11T23:07:21.633438"
    }
  }
};
