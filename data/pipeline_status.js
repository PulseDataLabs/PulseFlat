window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-07T05:27:16.266607",
  "elapsed_seconds": 884.7943768501282,
  "status": "error",
  "summary": {
    "total": 96,
    "success": 92,
    "failed": 4,
    "drifts": 2
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 71.33557057380676,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.0254969596862793,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.6216049194335938,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.9819157123565674,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 10.371280670166016,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 1.951566457748413,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 7.017984628677368,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 8.07560682296753,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 9.35450792312622,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 4.2493577003479,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 52.640257358551025,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 54.274877309799194,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 245.99719500541687,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.996959686279297,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 4.46503210067749,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.22027158737182617,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 3.497626781463623,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 413.11862874031067,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 7.276431083679199,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.320040702819824,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 4.314095735549927,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 4.738713026046753,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 5.361896276473999,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 4.00310492515564,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 3.8654844760894775,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 3.291520833969116,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 3.4131217002868652,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 3.7844388484954834,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 16.65958333015442,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 2.5536701679229736,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 11.15530276298523,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 20.160241842269897,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "bacen_conglomerados": {
      "status": "error",
      "elapsed_seconds": 0.8480756282806396,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_conglomerados.py\", line 75, in fetch\n    print_warn(\n    ~~~~~~~~~~^\n        f\"{yyyymm}CONGLOMERADO.zip não disponível\", elapsed=time.time() - t0\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\nTypeError: print_warn() got an unexpected keyword argument 'elapsed'\n",
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 5.88497519493103,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 148, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 24.991872549057007,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.4316747188568115,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 13.320441961288452,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 171.26958012580872,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 21.556617259979248,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 14.11677885055542,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 47.587695598602295,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.6390790939331055,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 4.978713035583496,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 4.771862983703613,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "error",
      "elapsed_seconds": 61.20779085159302,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 540, in _make_request\n    response = conn.getresponse()\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 638, in getresponse\n    httplib_response = super().getresponse()\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 1478, in getresponse\n    response.begin()\n    ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 343, in begin\n    version, status, reason = self._read_status()\n                              ~~~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/http/client.py\", line 304, in _read_status\n    line = str(self.fp.readline(_MAXLINE + 1), \"iso-8859-1\")\n               ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/socket.py\", line 723, in readinto\n    return self._sock.recv_into(b)\n           ~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/ssl.py\", line 1304, in recv_into\n    return self.read(nbytes, buffer)\n           ~~~~~~~~~^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/ssl.py\", line 1138, in read\n    return self._sslobj.read(len, buffer)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^\nTimeoutError: The read operation timed out\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 847, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 510, in increment\n    raise reraise(type(error), error, _stacktrace)\n          ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/util/util.py\", line 39, in reraise\n    raise value\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 793, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 542, in _make_request\n    self._raise_timeout(err=e, url=url, timeout_value=read_timeout)\n    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 373, in _raise_timeout\n    raise ReadTimeoutError(\n        self, url, f\"Read timed out. (read timeout={timeout_value})\"\n    ) from err\nurllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='www.b3.com.br', port=443): Read timed out. (read timeout=30)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 98, in fetch\n    rows, header = capturar(self.target_date)\n                   ~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 55, in capturar\n    resp = session.get(url, timeout=180)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 92, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 83, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.15/x64/lib/python3.13/site-packages/requests/adapters.py\", line 742, in send\n    raise ReadTimeout(e, request=request)\nrequests.exceptions.ReadTimeout: HTTPSConnectionPool(host='www.b3.com.br', port=443): Read timed out. (read timeout=30)\n",
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 16.374013423919678,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.409497976303101,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 15.950422048568726,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 16.203777313232422,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 8.428160190582275,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 64.26347064971924,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 17.911298036575317,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 7.176743507385254,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 12.458965301513672,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 67.27795696258545,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 89.63323736190796,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 6.3990888595581055,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 4.380794286727905,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 12.471062183380127,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 20.926135778427124,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 46.831976890563965,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 3.4222686290740967,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.4659757614135742,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 13.553812026977539,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 28.230841159820557,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 18.795976877212524,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 349.2594759464264,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 185.65363454818726,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 45.88159251213074,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 32.396629095077515,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 22.592236518859863,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 8.192931890487671,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 8.61688756942749,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 7.6771814823150635,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 3.8479230403900146,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 4.627188205718994,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 10.988560438156128,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.3861207962036133,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 4.5031654834747314,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 2.522209405899048,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 3.507384777069092,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 5.586378574371338,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 7.959671974182129,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 3.1243295669555664,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 54.96528339385986,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 6.8715925216674805,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 5.112981081008911,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 5.546683073043823,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 2.8789565563201904,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 2.2902262210845947,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 95.27291584014893,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 4.979304790496826,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 7.195552349090576,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 815.344596862793,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 5.00130033493042,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 7.4630866050720215,
      "error": null,
      "timestamp": "2026-10-07T05:27:16.267168"
    }
  },
  "drifts": {
    "anbima_ranking_global.csv": {
      "added": [],
      "removed": [
        "clubes_carteiras_administradas_cotas_fundos_proprios",
        "clubes_carteiras_administradas_cotas_fundos_terceiros",
        "fundos_em_cotas_cotas_fundos_proprios",
        "fundos_em_cotas_cotas_fundos_terceiros",
        "fundos_investimento_cotas_fundos_proprios",
        "fundos_investimento_cotas_fundos_terceiros",
        "origem_recursos_clientes",
        "renda_fixa_oper_compromissada_tit_estaduais_municipais_privados",
        "renda_fixa_tit_publicos_federais",
        "renda_fixa_cdb_rdb",
        "renda_fixa_notas_promissorias",
        "renda_fixa_debentures",
        "renda_fixa_direitos_creditorios",
        "renda_fixa_dpge",
        "renda_fixa_ccb_cccb",
        "renda_fixa_titulos_imobiliarios",
        "renda_fixa_letras_financeiras",
        "renda_fixa_investimento_exterior",
        "renda_fixa_outros",
        "renda_fixa_sub_total",
        "renda_variavel_opcoes",
        "renda_variavel_outros",
        "renda_variavel_sub_total"
      ],
      "timestamp": "2026-10-07T05:12:46.917273"
    },
    "b3_bdi_etfrf.csv.gz": {
      "added": [],
      "removed": [
        "preco_referencia_d1",
        "oferta_compra",
        "oferta_venda"
      ],
      "timestamp": "2026-10-07T05:13:18.484716"
    }
  }
};
