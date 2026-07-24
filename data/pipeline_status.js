window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-24T00:03:00.424346",
  "elapsed_seconds": 998.682293176651,
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
      "elapsed_seconds": 55.36160349845886,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 3.688746452331543,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.6005418300628662,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 2.3166396617889404,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 7.220239877700806,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.20894718170166016,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (23/07/2026) não corresponde ao D-1 útil (22/07/2026).\n",
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 5.110448598861694,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 4.910935401916504,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 2.311326742172241,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 3.712881326675415,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 68.48448705673218,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 36.2529022693634,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 6.431266784667969,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 4.374965667724609,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 2.741682767868042,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
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
      "elapsed_seconds": 0.9420568943023682,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.353170156478882,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_bdi_trades_acoes": {
      "status": "success",
      "elapsed_seconds": 123.86256718635559,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 4.237699031829834,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.096209287643433,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 0.962346076965332,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.0953538417816162,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.2195789813995361,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 0.9763305187225342,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 0.9410390853881836,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 0.9520955085754395,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 1.0931642055511475,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 0.945023775100708,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 16.828668355941772,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 41.79729461669922,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 195.42354202270508,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 67.74850177764893,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 2.0704805850982666,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "error",
      "elapsed_seconds": 2.09955096244812,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/bacen_parcelas_capital_basileia.py\", line 143, in fetch\n    raise RuntimeError(\n    ...<2 lines>...\n    )\nRuntimeError: Nenhum dado retornado da API OData do BCB (IFData). Verifique se a API está disponível.\n",
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 8.466719388961792,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 6.086106061935425,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 855.0107188224792,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 54.2721643447876,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 17.98888850212097,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 84.73695397377014,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 26.83470368385315,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 1.5836145877838135,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 4.155491828918457,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 4.845970392227173,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 22.28049373626709,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 9.276432991027832,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 3.450479030609131,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 3.559757947921753,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 4.530188798904419,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 7.629249572753906,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 102.44148087501526,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 7.1488261222839355,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 5.53400731086731,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 12.388233184814453,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 26.702861309051514,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 67.73582816123962,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 2.214066743850708,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 1.9347362518310547,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 2.2872977256774902,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 13.222194194793701,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 36.035454988479614,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 2.2974398136138916,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 0.949878454208374,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 4.941233396530151,
      "error": null,
      "timestamp": "2026-07-24T00:03:00.424569"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-07-23T23:46:27.361346"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-23T23:46:56.702268"
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
      "timestamp": "2026-07-23T23:47:51.686619"
    }
  }
};
