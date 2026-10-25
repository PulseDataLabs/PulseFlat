window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-10-25T08:44:05.478949",
  "elapsed_seconds": 1017.6862225532532,
  "status": "error",
  "summary": {
    "total": 96,
    "success": 93,
    "failed": 3,
    "drifts": 0
  },
  "scrapers": {
    "onu_pacto_global": {
      "status": "success",
      "elapsed_seconds": 69.03618860244751,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 2.7827956676483154,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 2.7837870121002197,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.3237550258636475,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 11.23293161392212,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_ima_completo": {
      "status": "success",
      "elapsed_seconds": 2.1238508224487305,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 7.835122108459473,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 8.06944751739502,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 9.074917554855347,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.204432249069214,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 51.609503984451294,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 51.67420721054077,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 184.77104568481445,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.012333154678345,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 4.407381057739258,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_indicadores_financeiros": {
      "status": "error",
      "elapsed_seconds": 0.29869556427001953,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1116, in json\n    return complexjson.loads(self.text, **kwargs)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/__init__.py\", line 352, in loads\n    return _default_decoder.decode(s)\n           ~~~~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/json/decoder.py\", line 363, in raw_decode\n    raise JSONDecodeError(\"Expecting value\", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 129, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_financeiros.py\", line 81, in capturar\n    dados = resp.json()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/models.py\", line 1120, in json\n    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)\nrequests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.824378728866577,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 489.16970682144165,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 8.39552903175354,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 2.2078566551208496,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 3.531952381134033,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 3.663796901702881,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 3.9275500774383545,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 3.4080283641815186,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 3.6173453330993652,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 3.144320011138916,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 2.0058093070983887,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 2.6800057888031006,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 14.702606439590454,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 2.019091844558716,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 10.047669172286987,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 13.33311915397644,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 2.5990278720855713,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 190.58903431892395,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 120.52992486953735,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "ibge_sidra": {
      "status": "error",
      "elapsed_seconds": 109.54288244247437,
      "error": "SystemExit(1)",
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 156.9239320755005,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 157.56756377220154,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 22.67174482345581,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 27.054064989089966,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 55.325692892074585,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 3.16231369972229,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 4.962819814682007,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 2.078974485397339,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "error",
      "elapsed_seconds": 61.324023723602295,
      "error": "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 540, in _make_request\n    response = conn.getresponse()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/urllib3/connection.py\", line 638, in getresponse\n    httplib_response = super().getresponse()\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/http/client.py\", line 1478, in getresponse\n    response.begin()\n    ~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/http/client.py\", line 343, in begin\n    version, status, reason = self._read_status()\n                              ~~~~~~~~~~~~~~~~~^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/http/client.py\", line 304, in _read_status\n    line = str(self.fp.readline(_MAXLINE + 1), \"iso-8859-1\")\n               ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/socket.py\", line 723, in readinto\n    return self._sock.recv_into(b)\n           ~~~~~~~~~~~~~~~~~~~~^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/ssl.py\", line 1315, in recv_into\n    return self.read(nbytes, buffer)\n           ~~~~~~~~~^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/ssl.py\", line 1149, in read\n    return self._sslobj.read(len, buffer)\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^\nTimeoutError: The read operation timed out\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/adapters.py\", line 696, in send\n    resp = conn.urlopen(\n        method=request.method,\n    ...<9 lines>...\n        chunked=chunked,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 847, in urlopen\n    retries = retries.increment(\n        method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/urllib3/util/retry.py\", line 510, in increment\n    raise reraise(type(error), error, _stacktrace)\n          ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/urllib3/util/util.py\", line 39, in reraise\n    raise value\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 793, in urlopen\n    response = self._make_request(\n        conn,\n    ...<10 lines>...\n        **response_kw,\n    )\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 542, in _make_request\n    self._raise_timeout(err=e, url=url, timeout_value=read_timeout)\n    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/urllib3/connectionpool.py\", line 373, in _raise_timeout\n    raise ReadTimeoutError(\n        self, url, f\"Read timed out. (read timeout={timeout_value})\"\n    ) from err\nurllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='www.b3.com.br', port=443): Read timed out. (read timeout=30)\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 237, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 206, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 109, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 98, in fetch\n    rows, header = capturar(self.target_date)\n                   ~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 55, in capturar\n    resp = session.get(url, timeout=180)\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/sessions.py\", line 671, in get\n    return self.request(\"GET\", url, params=params, **kwargs)\n           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 92, in _patched_request\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/base.py\", line 83, in _patched_request\n    resp = _orig_request(self, method, url, *args, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/sessions.py\", line 651, in request\n    resp = self.send(prep, **send_kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/sessions.py\", line 784, in send\n    r = adapter.send(request, **kwargs)\n  File \"/opt/hostedtoolcache/Python/3.13.16/x64/lib/python3.13/site-packages/requests/adapters.py\", line 742, in send\n    raise ReadTimeout(e, request=request)\nrequests.exceptions.ReadTimeout: HTTPSConnectionPool(host='www.b3.com.br', port=443): Read timed out. (read timeout=30)\n",
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 16.81265878677368,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 13.340607643127441,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 13.20987057685852,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 4.0397350788116455,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 16.168007850646973,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 29.65236186981201,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 16.79436492919922,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 15.233741998672485,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 18.802810668945312,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 53.21906924247742,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 70.77984404563904,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 3.330063819885254,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.5202250480651855,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.833883047103882,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 21.590821743011475,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 45.221604347229004,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.52840256690979,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.324321985244751,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 13.7131986618042,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 23.206422805786133,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 25.451287746429443,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 408.8542242050171,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "debentures_mercado_secundario_precos_negociacao_api": {
      "status": "success",
      "elapsed_seconds": 150.98704385757446,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "debentures_emissoes_caracteristicas_api": {
      "status": "success",
      "elapsed_seconds": 52.04190635681152,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_cri_cra_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 22.535342693328857,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_letras_financeiras": {
      "status": "success",
      "elapsed_seconds": 17.185354948043823,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_fidc_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 9.78377628326416,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_curvas_credito": {
      "status": "success",
      "elapsed_seconds": 10.806674003601074,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_curvas_juros_ettj": {
      "status": "success",
      "elapsed_seconds": 10.934013843536377,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_indice_ida": {
      "status": "success",
      "elapsed_seconds": 3.4269611835479736,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_indices_ima_resultados": {
      "status": "success",
      "elapsed_seconds": 4.063662528991699,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_titulos_publicos_mercado_secundario": {
      "status": "success",
      "elapsed_seconds": 10.233795166015625,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_titulos_publicos_vna": {
      "status": "success",
      "elapsed_seconds": 3.8102643489837646,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_indices_idka_resultados": {
      "status": "success",
      "elapsed_seconds": 4.16042685508728,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_projecoes_inflacao": {
      "status": "success",
      "elapsed_seconds": 2.48002290725708,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_indices_carteira_teorica_ima": {
      "status": "success",
      "elapsed_seconds": 3.652940273284912,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_indices_carteira_teorica_ida": {
      "status": "success",
      "elapsed_seconds": 5.049190521240234,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_curvas_juros_parametros_svensson": {
      "status": "success",
      "elapsed_seconds": 9.11606240272522,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_titulos_publicos_estimativa_selic": {
      "status": "success",
      "elapsed_seconds": 2.3224642276763916,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "anbima_reune_negociacoes": {
      "status": "success",
      "elapsed_seconds": 61.588162422180176,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "fred_us_treasuries_yield_curve": {
      "status": "success",
      "elapsed_seconds": 4.45346474647522,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "fred_global_liquidity_credit_spreads": {
      "status": "success",
      "elapsed_seconds": 4.403898000717163,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "fred_us_macro_indicators": {
      "status": "success",
      "elapsed_seconds": 3.308171510696411,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_bdi_derivativos_resumo": {
      "status": "success",
      "elapsed_seconds": 3.6291728019714355,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_opcoes_posicoes_resumo": {
      "status": "success",
      "elapsed_seconds": 1.7911832332611084,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_opcoes_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 148.45291185379028,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_valor_mercado_empresas": {
      "status": "success",
      "elapsed_seconds": 3.1821508407592773,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "bacen_cadastro_instituicoes": {
      "status": "success",
      "elapsed_seconds": 15.483999013900757,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "b3_termo_posicoes_aberto": {
      "status": "success",
      "elapsed_seconds": 949.9950499534607,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "fred_brazil_export_commodities": {
      "status": "success",
      "elapsed_seconds": 3.127370834350586,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    },
    "fred_brazil_macro_fx_and_cycles": {
      "status": "success",
      "elapsed_seconds": 5.66931939125061,
      "error": null,
      "timestamp": "2026-10-25T08:44:05.479602"
    }
  },
  "drifts": {}
};
