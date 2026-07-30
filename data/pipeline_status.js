window.PULSEFLAT_PIPELINE_STATUS = {
  "timestamp": "2026-07-30T20:52:30.831404",
  "elapsed_seconds": 6249.071563482285,
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
      "elapsed_seconds": 62.978761434555054,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "anbima_indicadores": {
      "status": "success",
      "elapsed_seconds": 5.516944408416748,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "anbima_projecoes": {
      "status": "success",
      "elapsed_seconds": 1.682616949081421,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "anbima_titulos_publicos": {
      "status": "success",
      "elapsed_seconds": 3.5397932529449463,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "anbima_debentures": {
      "status": "success",
      "elapsed_seconds": 9.514891147613525,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "anbima_ima_completo": {
      "status": "error",
      "elapsed_seconds": 0.45487022399902344,
      "error": "Traceback (most recent call last):\n  File \"/home/runner/work/PulseFlat/PulseFlat/run_all.py\", line 213, in run_scraper\n    getattr(mod, class_name)().run()\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 183, in run\n    raise e\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/utils/base.py\", line 93, in run\n    df = self.fetch()\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 176, in fetch\n    df = pd.DataFrame(capturar())\n                      ~~~~~~~~^^\n  File \"/home/runner/work/PulseFlat/PulseFlat/scrapers/anbima_ima_completo.py\", line 127, in capturar\n    raise ValueError(f\"Abortando: data do arquivo ({file_date}) não corresponde ao D-1 útil ({d1_util_str}).\")\nValueError: Abortando: data do arquivo (30/07/2026) não corresponde ao D-1 útil (29/07/2026).\n",
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "anbima_550": {
      "status": "success",
      "elapsed_seconds": 8.487464427947998,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "anbima_idka": {
      "status": "success",
      "elapsed_seconds": 6.028806447982788,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "anbima_ranking_global": {
      "status": "success",
      "elapsed_seconds": 3.132579803466797,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "anbima_matriz_probabilidade_resgate": {
      "status": "success",
      "elapsed_seconds": 5.099882364273071,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "anbima_indice_imab": {
      "status": "success",
      "elapsed_seconds": 154.19539093971252,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "debentures_emissoes_caracteristicas": {
      "status": "success",
      "elapsed_seconds": 114.04146027565002,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "debentures_mercado_secundario_precos_negociacao": {
      "status": "success",
      "elapsed_seconds": 19.09724259376526,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_fiis": {
      "status": "success",
      "elapsed_seconds": 5.059810400009155,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_etfs": {
      "status": "success",
      "elapsed_seconds": 3.467167854309082,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
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
      "elapsed_seconds": 1.4069633483886719,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_bdi_di_over": {
      "status": "success",
      "elapsed_seconds": 2.841017723083496,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_bdi_trades_acoes": {
      "status": "error",
      "elapsed_seconds": 19.59832453727722,
      "error": "SystemExit(1)",
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_bmf_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 36.92009973526001,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_series_historicas": {
      "status": "success",
      "elapsed_seconds": 6.250798463821411,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_carteira_teorica_ibov": {
      "status": "success",
      "elapsed_seconds": 1.572765827178955,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_carteira_teorica_smll": {
      "status": "success",
      "elapsed_seconds": 1.5832173824310303,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_carteira_teorica_bdrx": {
      "status": "success",
      "elapsed_seconds": 1.7592086791992188,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_carteira_teorica_isee": {
      "status": "success",
      "elapsed_seconds": 1.391038417816162,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_carteira_teorica_ibxl": {
      "status": "success",
      "elapsed_seconds": 1.775709867477417,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_carteira_teorica_ifnc": {
      "status": "success",
      "elapsed_seconds": 1.363586664199829,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_carteira_teorica_agfs_iagro": {
      "status": "success",
      "elapsed_seconds": 2.1930923461914062,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_carteira_teorica_ibsd": {
      "status": "success",
      "elapsed_seconds": 1.3825585842132568,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_titulos_negociaveis": {
      "status": "success",
      "elapsed_seconds": 258.2429111003876,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "bcb_ptax": {
      "status": "success",
      "elapsed_seconds": 118.81358098983765,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "bcb_sgs": {
      "status": "success",
      "elapsed_seconds": 322.5307865142822,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "bacen_balancetes_bancos": {
      "status": "success",
      "elapsed_seconds": 161.91056084632874,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "bacen_conglomerados": {
      "status": "success",
      "elapsed_seconds": 37.00908422470093,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "bacen_parcelas_capital_basileia": {
      "status": "success",
      "elapsed_seconds": 1070.214554309845,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "bacen_negociacao_tpf": {
      "status": "success",
      "elapsed_seconds": 53.157078981399536,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "ibge_sidra": {
      "status": "success",
      "elapsed_seconds": 7.842872142791748,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "cvm_fundos_informe_diario": {
      "status": "success",
      "elapsed_seconds": 5882.042576789856,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "cvm_fundos_classe": {
      "status": "success",
      "elapsed_seconds": 73.09326839447021,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "yahoo_finance_series": {
      "status": "success",
      "elapsed_seconds": 2.2871804237365723,
      "error": null,
      "timestamp": "2026-06-27T17:00:25.236835"
    },
    "b3_carteiras_teoricas": {
      "status": "success",
      "elapsed_seconds": 20.59779953956604,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_isin_emissores": {
      "status": "success",
      "elapsed_seconds": 141.229754447937,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_isin_ativos": {
      "status": "success",
      "elapsed_seconds": 29.71498727798462,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_classificacao_setorial": {
      "status": "success",
      "elapsed_seconds": 2.5343685150146484,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "cvm_cadastro_companhias_abertas": {
      "status": "success",
      "elapsed_seconds": 26.95627236366272,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_limites_garantias": {
      "status": "success",
      "elapsed_seconds": 8.676299095153809,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_indicadores_economicos_fwf": {
      "status": "success",
      "elapsed_seconds": 23.783838987350464,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "b3_fundos_listados": {
      "status": "success",
      "elapsed_seconds": 11.74685025215149,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "ipea_calendario": {
      "status": "success",
      "elapsed_seconds": 4.851781129837036,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "ipea_comercio_exterior": {
      "status": "success",
      "elapsed_seconds": 5.410179853439331,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "ipea_fbcf": {
      "status": "success",
      "elapsed_seconds": 6.396486282348633,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "ipea_macroeconomia": {
      "status": "success",
      "elapsed_seconds": 10.919278383255005,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "ipea_mercados_diarios": {
      "status": "success",
      "elapsed_seconds": 167.5778501033783,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "ipea_precos_inflacao": {
      "status": "success",
      "elapsed_seconds": 10.55011534690857,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "ipea_producao_mineral": {
      "status": "success",
      "elapsed_seconds": 9.067401885986328,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "ipea_taxas_juros": {
      "status": "success",
      "elapsed_seconds": 18.55668020248413,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "yahoo_acoes_brasileiras": {
      "status": "success",
      "elapsed_seconds": 28.513118982315063,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "yahoo_acoes_internacionais": {
      "status": "success",
      "elapsed_seconds": 73.57657241821289,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "yahoo_cambio_moedas": {
      "status": "success",
      "elapsed_seconds": 2.6748499870300293,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "yahoo_commodities": {
      "status": "success",
      "elapsed_seconds": 2.3820645809173584,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "yahoo_criptoativos": {
      "status": "success",
      "elapsed_seconds": 2.807276487350464,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "yahoo_etfs": {
      "status": "success",
      "elapsed_seconds": 14.506078243255615,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "yahoo_fiis_fiagros": {
      "status": "success",
      "elapsed_seconds": 44.16266179084778,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "yahoo_indices_globais": {
      "status": "success",
      "elapsed_seconds": 18.413369178771973,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "yahoo_renda_fixa": {
      "status": "success",
      "elapsed_seconds": 1.2415273189544678,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    },
    "wikipedia_global_indices": {
      "status": "success",
      "elapsed_seconds": 5.303366184234619,
      "error": null,
      "timestamp": "2026-07-30T20:52:30.831608"
    }
  },
  "drifts": {
    "anbima_indice_imab.csv.gz": {
      "added": [],
      "removed": [
        "data_referencia",
        "duration_du"
      ],
      "timestamp": "2026-07-30T19:08:29.942836"
    },
    "b3_indicadores_financeiros.csv": {
      "added": [],
      "removed": [
        "last_update"
      ],
      "timestamp": "2026-07-30T19:09:12.709969"
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
      "timestamp": "2026-07-30T19:11:03.255576"
    }
  }
};
