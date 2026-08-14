window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-08-13T23:47:47.192911",
  "elapsed_seconds": 2719.124831199646,
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
      "elapsed_seconds": 57.941967248916626,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 4.066488027572632,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.8240017890930176,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 9.731282711029053,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 7.505685091018677,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.3113832473754883,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (13/08/2026) não corresponde ao D-1 útil (12/08/2026).\n",
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.557126522064209,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 4.547015428543091,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.97007417678833,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 7.050052165985107,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 211.5935251712799,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 109.22241401672363,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 2.1045339107513428,
      "error": null,
      "timestamp": "2026-08-01T01:25:04.029451"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.285668611526489,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 2.814340353012085,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
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
      "elapsed_seconds": 1.0528340339660645,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.2018001079559326,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 245.7787868976593,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 5.31144905090332,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.211390256881714,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.9035582542419434,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 2.818528652191162,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.8924353122711182,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.9047954082489014,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.7957851886749268,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.7519817352294922,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 2.226252317428589,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 2.025400161743164,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 192.2518081665039,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 72.19916319847107,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 335.06632685661316,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 68.10777544975281,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 3.1479334831237793,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 2457.636438369751,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 34.49731111526489,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 17.404767513275146,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 917.2311401367188,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 92.7378613948822,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 18.44448184967041,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 87.49896693229675,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 70.60286092758179,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 1.8164072036743164,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 46.49532461166382,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 5.040932893753052,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "error",
      "elapsed_seconds": 20.264793395996094,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 81, in fetch\n    rows, header = capturar()\n                   ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/b3_indicadores_economicos_fwf.py\", line 48, in capturar\n    parsed = fwf_rows(text, INDICADORES_FIELDS, INDICADORES_WIDTHS)\n  File \"/home/runner/work/PulseFlat/PulseFlat/utils/parsers.py\", line 197, in fwf_rows\n    casas = int(row[\"num_casas_decimais\"])\nValueError: invalid literal for int() with base 10: '¹²'\n",
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 9.576897621154785,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 3.3336987495422363,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 13.833823204040527,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 14.687728881835938,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 7.832669019699097,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 113.0720283985138,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 17.218724727630615,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.485246658325195,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 12.370521068572998,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 33.193931341171265,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 71.11990165710449,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 2.2478370666503906,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.256011962890625,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 3.1505842208862305,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 15.42686152458191,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 43.162909746170044,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.6345736980438232,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.3480932712554932,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 3.683053970336914,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_bdi_etfrf": {
      "status": "success",
      "elapsed_seconds": 41.2228627204895,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_cotahist_diario": {
      "status": "success",
      "elapsed_seconds": 5.436781883239746,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    },
    "b3_cotahist_anual": {
      "status": "success",
      "elapsed_seconds": 162.33787608146667,
      "error": null,
      "timestamp": "2026-08-13T23:47:47.193145"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-08-13T23:02:34.470795"
    },
    "b3_bdi_etfrf.csv.gz": {
      "added": [],
      "removed": [
        "preco_referencia_d1",
        "oferta_compra",
        "oferta_venda"
      ],
      "timestamp": "2026-08-12T10:59:44.008263"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-08-13T23:04:07.967085"
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
      "timestamp": "2026-08-13T23:06:47.548092"
    }
  }
};
