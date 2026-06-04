<p align="center">
  <img src="logo.png" alt="PulseFlat Logo" width="280">
</p>

# PulseFlat

> 🚀 **Página do Projeto:** [https://royopa.github.io/PulseFlat/](https://royopa.github.io/PulseFlat/)

Pipeline automatizado de captura diária de dados financeiros brasileiros via **GitHub Actions**.  
Sem servidor. Sem custo. Histórico versionado em CSV no próprio repositório.

---

## Scrapers

### Grupo ANBIMA

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `anbima_indicadores` | ANBIMA | Scraping HTML | `anbima_indicadores.csv` |
| `anbima_projecoes` | ANBIMA | API OAuth 2.0 / Scraping | `anbima_projecoes.csv` |
| `anbima_titulos_publicos` | ANBIMA | TXT delimitado (@) | `anbima_titulos_publicos.csv` |
| `anbima_debentures` | ANBIMA | TXT delimitado (@) | `anbima_debentures.csv` |
| `anbima_ima_completo` | ANBIMA | TXT delimitado | `anbima_ima_completo.csv` |
| `anbima_550` | ANBIMA | TXT (Resolução 550) | `anbima_550.csv` |
| `anbima_indice_imab` | ANBIMA | XLS histórico | `anbima_indice_imab.csv` |
| `anbima_idka` | ANBIMA | API pública | `anbima_idka.csv` |
| `anbima_ranking_global` | ANBIMA | API Strapi | `anbima_ranking_global.csv` |
| `anbima_matriz_probabilidade_resgate` | ANBIMA | Scraping HTML | `anbima_matriz_probabilidade_resgate.csv` |

### Grupo BCB

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `bcb_ptax` | BCB | API REST (Olinda) | `bcb_ptax.csv` (sem acúmulo) |
| `bcb_sgs` | BCB | API REST (SGS) | `bcb_sgs.csv` (sem acúmulo) |
| `bacen_negociacao_tpf` | BCB | ZIP + CSV (DEMAB) | `bacen_negociacao_tpf_extragrupo_mes_corrente.csv`, `..._mes_anterior.csv` |
| `bacen_balancetes_bancos` | BCB | API Documentos | `bacen_balancetes_bancos.csv` (sem acúmulo) |
| `bacen_conglomerados` | BCB | API OData | `bacen_conglomerados.csv` |
| `bacen_parcelas_capital_basileia` | BCB | API OData | `bacen_parcelas_capital_basileia.csv` |

### Grupo IBGE

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `ibge_sidra` | IBGE | API REST (SIDRA) | `ibge_sidra.csv` (sem acúmulo) |

### Grupo CVM

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `cvm_cadastro_companhias_abertas` | CVM | CSV direto | `cvm_cadastro_companhias_abertas.csv` (sem acúmulo) |
| `cvm_fundos_cadastro` | CVM | CSV direto | `cvm_fundos_cadastro.csv` (sem acúmulo) |
| `cvm_fundos_informe_diario` | CVM | ZIP + CSV | `cvm_fundos_informe_diario.csv` (sem acúmulo) |
| `cvm_fundos_extrato` | CVM | CSV direto | `cvm_fundos_extrato.csv` (sem acúmulo) |
| `cvm_fundos_classe` | CVM | ZIP + CSV | `cvm_fundos_classe.csv` (sem acúmulo) |

### Grupo SND / Debêntures

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `debentures_emissoes_caracteristicas` | SND | HTML direto | `debentures_emissoes_caracteristicas.csv` (sem acúmulo) |
| `debentures_mercado_secundario_precos_negociacao` | SND | HTML direto | `debentures_mercado_secundario_precos_negociacao.csv` (sem acúmulo) |

### Grupo B3

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `b3_fiis` | B3 | API JSON + Base64 | `b3_fiis_listados.csv` (sem acúmulo) |
| `b3_etfs` | B3 | API JSON + Base64 | `b3_etfs_listados.csv` (sem acúmulo) |
| `b3_etfs_listados_download` | B3 | API JSON + Base64 | `b3_etfs_listados.csv` (sem acúmulo) |
| `b3_carteiras` | B3 | API JSON + Base64 | `b3_carteiras_teoricas.csv` |
| `b3_carteira_teorica_ibov` | B3 | API JSON + Base64 | `b3_carteira_teorica_ibov.csv` |
| `b3_carteira_teorica_smll` | B3 | API JSON + Base64 | `b3_carteira_teorica_smll.csv` |
| `b3_carteira_teorica_bdrx` | B3 | API JSON + Base64 | `b3_carteira_teorica_bdrx.csv` |
| `b3_carteira_teorica_isee` | B3 | API JSON + Base64 | `b3_carteira_teorica_isee.csv` |
| `b3_carteira_teorica_ibxl` | B3 | API JSON + Base64 | `b3_carteira_teorica_ibxl.csv` |
| `b3_carteira_teorica_ifnc` | B3 | API JSON + Base64 | `b3_carteira_teorica_ifnc.csv` |
| `b3_carteira_teorica_agfs_iagro` | B3 | API JSON + Base64 | `b3_carteira_teorica_agfs_iagro.csv` |
| `b3_carteira_teorica_ibsd` | B3 | API JSON + Base64 | `b3_carteira_teorica_ibsd.csv` |
| `b3_indicadores_financeiros` | B3 | API JSON + Base64 | `b3_indicadores_financeiros.csv` |
| `b3_bdi_di_over` | B3 | API POST (BDI) | `b3_bdi_di_over.csv` |
| `b3_taxa_cambio_referencia` | B3 | API JSON + Base64 | `b3_taxa_cambio_referencia.csv` |
| `b3_capital_social_empresas` | B3 | API JSON + Base64 | `b3_capital_social_empresas.csv` |
| `b3_bvbg028` | B3 | ZIP + CSV (BVBG) | `b3_bvbg028.csv` |
| `b3_bvbg086` | B3 | ZIP + CSV (BVBG) | `b3_bvbg086.csv` |
| `b3_bvbg087` | B3 | ZIP + CSV (BVBG) | `b3_bvbg087.csv` |
| `b3_indices_precos_historicos` | B3 | API JSON + Base64 | `b3_indices_precos_historicos.csv` |
| `b3_classificacao_setorial` | B3 | ZIP + XLSX | `b3_classificacao_setorial.csv` (sem acúmulo) |
| `b3_titulos_negociaveis` | B3 | ZIP + CSV | `b3_titulos_negociaveis.csv` (sem acúmulo) |
| `b3_series_historicas` | B3 | API JSON + Download | `b3_series_historicas.csv` |

### Grupo Ratings (Agências de Classificação)

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `s_p_entidades_brasil` | S&P Global | Scraping HTML | `s_p_entidades_brasil.csv` |
| `s_p_ratings_brasil` | S&P Global | Scraping HTML | `s_p_ratings_brasil.csv` |
| `s_p_acoes_ratings` | S&P Global | Scraping HTML | `s_p_acoes_ratings.csv` |
| `moodys_local_ratings` | Moody's Local | Scraping HTML | (Bloqueado por anti-bot) |

### Grupo Outros / Diversos (Misc)

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `yahoo_finance_series` | Yahoo Finance | API yfinance | `yahoo_finance_series.csv` |
| `investing_etf` | Investing.com | Scraping HTML | `investing_etf.csv` |

**Desativados:** `b3_cotahist_diario`, `b3_cotahist_anual`, `b3_indicadores_economicos_fwf`, `b3_negocios_balcao`, `b3_companhias_detalhes`, `b3_companhias_info`, `b3_dividendos_dinheiro`, `b3_futuros_ajustes` (fonte legada descontinuada), `b3_bmf_taxas_juros` (API BDI sem dados).

---

## Dados capturados

### `anbima_indicadores.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| data_referencia | Data de referência do valor/indicador (ex: data do dia para taxas, 1º dia do mês de referência para IGP-M/IPCA) |
| data_referencia_pagina | Data/hora da última atualização na página |
| indicador | Nome do indicador (ex: Taxa SELIC (BC)) |
| categoria | Grupo: Taxa de Juros, Câmbio, Índice de Preços, etc. |
| valor | Valor numérico (ponto como separador decimal) |
| unidade | % a.a., R$, % mês, índice, R$ cota |

**Indicadores:** SELIC (Estimativa e BC), DI-B3, IGP-M (índice, var.%, projeção), IPCA (índice, var.%, projeção), Dólar Comercial (compra/venda), Euro (compra/venda), TR, TBF, FDS.

### `anbima_projecoes.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| data_referencia | Data de referência (1º dia do mês de referência, ex: 2026-06-01 para jun/26) |
| estrategia_coleta | `api_oficial` ou `scraping_indicadores` |
| indice | IPCA ou IGP-M |
| mes_referencia | Mês/ano da projeção (ex: mai/26) |
| tipo_projecao | corrente / seguinte / posterior / fechado |
| valor_pct | Valor em % (separador decimal: ponto) |
| data_divulgacao | Data de divulgação da projeção |
| num_instituicoes | Nº de instituições (disponível via API) |
| observacao | Observação descritiva da projeção |

**IGP-M:** divulgado ~3x/mês nos dias de prévia e fechado pela FGV  
**IPCA:** divulgado ~2x/mês no dia do IPCA fechado e do IPCA-15 pelo IBGE

### `anbima_titulos_publicos.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| titulo | Nome do título público |
| data_referencia | Data de referência da cotação |
| codigo_selic | Código SELIC do ativo |
| data_base_emissao | Data base de emissão |
| data_vencimento | Data de vencimento |
| tx_compra / tx_venda / tx_indicativa | Taxas de compra, venda e indicativa (% a.a.) |
| pu | Preço unitário (R$) |
| desvio_padrao | Desvio padrão das taxas |

### `anbima_debentures.csv`
| Campo | Descrição |
|---|---|
| data_referencia | Data de referência da cotação |
| codigo | Código da debênture |
| nome_emissor | Nome do emissor |
| dt_repactuacao_vencimento | Data de repactuação/vencimento |
| indice_correcao | Índice de correção (CDI, IPCA, etc.) |
| tx_compra / tx_venda / tx_indicativa | Taxas de compra, venda e indicativa |
| pu | Preço unitário (R$) |
| duration | Duration do ativo (dias úteis) |

### `anbima_ima_completo.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| data_referencia | Data de referência |
| indice | Nome do índice (IMA-Geral, IRF-M, IDA, etc.) |
| numero_indice | Número do índice |
| variacao_diaria / _mensal / _anual | Variações percentuais |
| duration_du | Duration em dias úteis |
| peso_geral | Peso do subíndice no índice geral (%) |

### `anbima_550.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| titulo | Nome do ativo |
| vencimento | Data de vencimento |
| preco_unitario | Preço unitário (R$) |
| preco_retorno | Preço de retorno |
| posicao_custodia | Posição em custódia |

### `bcb_ptax.csv`
Cotações do dólar PTAX. Snapshot contendo a série histórica diária de compra e venda completa desde **01/01/2020** (arquivo não acumulativo, reescrito por completo a cada execução).

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| data_hora_cotacao | Data/hora da cotação PTAX |
| cotacao_compra | Cotação de compra (R$/US$) |
| cotacao_venda | Cotação de venda (R$/US$) |

### `bcb_sgs.csv`
Séries temporais do Banco Central via SGS. Snapshot contendo a série histórica diária de compra/venda do dólar e taxas SELIC, CDI, IPCA, IGP-M completa desde **01/01/2020** (arquivo não acumulativo, reescrito por completo a cada execução).

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| codigo_serie | Código da série SGS (ex: 11, 432, 433) |
| nome_serie | Nome descritivo da série |
| data | Data do valor |
| valor | Valor da série |

**Séries:** SELIC diária, SELIC acumulada mês, CDI diário, CDI acumulado mês, IPCA mensal, IPCA acumulado 12m, IGP-M mensal, IGP-M acumulado 12m, Dólar venda.

### `ibge_sidra.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| serie_id | Código da tabela SIDRA |
| nome_serie | Nome da série |
| fonte | Fonte dos dados |
| periodo_referencia | Período de referência |
| data_modificacao | Data da última modificação |

**Tabelas:** 1737 (IPCA), 3065 (IPCA-15), 1621 (INPC).

### `b3_fiis_listados.csv`
Ticker, nome, CNPJ, administrador, segmento, tipo, mandato, prazo, gestão, cotistas, patrimônio líquido.

### `b3_etfs_listados.csv`
Categoria (RV/RF), ticker, nome, CNPJ, administrador, gestor, índice de referência, segmento, cotistas, patrimônio.

### `b3_carteiras_teoricas.csv`
22 índices B3 · ticker, nome, tipo, quantidade teórica, peso (%), segmento — por ativo/índice/data.

**Índices:** IBOV, IBRA, IBrX 100, IBrX 50, IGC, ITAG, MLCX, SMLL, IVBX, IDIV, IFIX, IFNC, ICON, IEEX, IMAT, IMOB, INDX, UTIL, IGCT, IGNM, ISE, ICO2

<!-- ### `b3_futuros_ajustes.csv` — DESATIVADO: fonte legada descontinuada dez/2025 -->
<!-- ### `b3_bmf_taxas_juros.csv` — DESATIVADO: API BDI sem dados -->

### `b3_indicadores_financeiros.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| security_identification_code | Código do indicador |
| description | Descrição do indicador |
| group_description | Grupo (Interest Rates, Exchange Rates, etc.) |
| value | Valor numérico |
| rate | Taxa associada |

### `b3_bdi_di_over.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| rpt_dt | Data de referência |
| number_of_operations | Número de operações |
| financial_volume | Volume financeiro (R$) |
| average | Taxa média (% a.d.) |
| daily_factor | Fator diário |
| selic_rate | Taxa SELIC no período |

### `bacen_negociacao_tpf_extragrupo_mes_corrente.csv` / `..._mes_anterior.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| data_negocio | Data de negociação |
| titulo | Código do título público |
| tipo_operacao | Tipo de operação (Compra, Venda) |
| quantidade | Quantidade negociada |
| preco | Preço de negociação |
| valor | Valor financeiro da operação |

### `b3_taxa_cambio_referencia.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| codigo_moeda | Código da moeda (ex: USD) |
| taxa_compra | Taxa de câmbio de compra (R$) |
| taxa_venda | Taxa de câmbio de venda (R$) |

### `b3_capital_social_empresas.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| cnpj | CNPJ da empresa |
| empresa | Nome da empresa |
| capital_social | Valor do capital social (R$) |
| data_capital | Data de referência do capital social |

### `anbima_indice_imab.csv`
| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| data | Data de referência |
| indice | Nome do índice (IMA-B, IMA-B5, etc.) |
| numero | Número do índice |
| variacao | Variação percentual |

### `b3_bvbg028.csv`, `b3_bvbg086.csv`, `b3_bvbg087.csv`
Boletins diários de operações da B3 (Ações, RF, Derivativos) — arquivos BVBG.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| data_pregão | Data do pregão |
| codigo | Código do ativo |
| quantidade | Quantidade negociada |
| preco | Preço de negociação |
| tipo | Tipo de operação |

<!-- ### `b3_cotahist_diario.csv` / `b3_cotahist_anual.csv` — DESATIVADOS -->
<!-- ### `b3_indicadores_economicos_fwf.csv` — DESATIVADO -->
<!-- ### `b3_negocios_balcao.csv` — DESATIVADO -->

### `cvm_cadastro_companhias_abertas.csv`
Cadastro de companhias abertas registradas na CVM.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| cnpj | CNPJ da companhia |
| denominação_social | Razão social |
| nome_de_pregao | Nome de pregão |
| codigo_cvm | Código CVM |
| situacao | Situação cadastral |

### `b3_indices_precos_historicos.csv`
Histórico de composição e preços de índices da B3.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| indice | Código do índice (IBOV, IBRA, IFIX, etc.) |
| ano | Ano de referência |
| ticker | Ticker do ativo |
| peso | Peso no índice (%) |
| quantidade_teorica | Quantidade teórica |

<!-- ### `b3_companhias_detalhes.csv` — DESATIVADO -->
<!-- ### `b3_companhias_info.csv` — DESATIVADO -->
<!-- ### `b3_dividendos_dinheiro.csv` — DESATIVADO -->

### `anbima_idka.csv`
Índice de Duração Constante ANBIMA (prefixado e inflação).

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| dt_referencia | Data de referência |
| no_indexador | Tipo de indexador (ex: PREFIXADO, IPCA) |
| no_indice | Nome do índice IDkA (ex: IDkA Pré 3M, IDkA IPCA 2A) |
| nu_indice | Número índice |
| ret_dia_perc | Retorno diário (%) |
| ret_mes_perc | Retorno mensal (%) |
| ret_ano_perc | Retorno anual (%) |
| ret_12_meses_perc | Retorno acumulado 12 meses (%) |
| vol_aa_perc | Volatilidade ao ano (%) |
| taxa_juros_aa_perc_compra_d1 | Taxa de juros de compra D+1 (% a.a.) |
| taxa_juros_aa_perc_venda_d0 | Taxa de juros de venda D+0 (% a.a.) |

### `anbima_matriz_probabilidade_resgate.csv`
Probabilidade histórica de resgates de fundos de investimento.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| dt_referencia | Data de referência do relatório |
| data | Data da observação |
| periodo | Mês/ano da observação |
| classe | Classe do fundo (Ações, RF, Multimercado, etc.) |
| segmento_investidor | Segmento do investidor (Varejo, Private, etc.) |
| tipo_metodologia | Tipo de metodologia estatística utilizada |
| metrica | Métrica calculada (ex: EWMA_97) |
| prazo | Prazo em dias |
| valor | Probabilidade calculada |

### `anbima_ranking_global.csv`
Ranking mensal de administradores e gestores de fundos ANBIMA.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| dt_referencia | Mês de referência do ranking |
| tipo_ativo | Descrição da tabela/aba analisada (ex: Ativos de RF, RV) |
| Unnamed: X | Nome da instituição e valores de custódia e lastro |

### `bacen_balancetes_bancos.csv`
Última data de publicação dos balancetes de bancos comerciais e múltiplos.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| data | Data do último balancete publicado pelo BACEN |

### `bacen_conglomerados.csv`
Dados cadastrais e financeiros de conglomerados financeiros no Brasil.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| dt_referencia | Mês de referência dos dados |

### `bacen_parcelas_capital_basileia.csv`
Parcelas de capital e patrimônio de referência sob as regras de Basileia III.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| TipoInstituicao | Código do tipo de instituição |
| CodInst | Código cadastral da instituição financeira |
| AnoMes | Mês/Ano de referência (ex: 202512) |
| NomeRelatorio | Nome do relatório (ex: Informações de Capital) |
| NumeroRelatorio | Número identificador do relatório |
| Grupo | Grupo de contas prudenciais |
| Conta | Código da conta do patrimônio |
| NomeColuna | Nome abreviado da coluna |
| DescricaoColuna | Descrição completa da conta prudencial |
| Saldo | Valor do saldo em conta (R$) |
| tipo_instituicao_label | Descrição legível da instituição |

### `yahoo_finance_series.csv`
Preços diários de ativos e índices de referência globais e nacionais.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| dt_ref | Data da cotação |
| ticker | Ticker de mercado (ex: ^BVSP, BRL=X, GC=F) |
| label | Descrição legível (IBOVESPA, Câmbio Dólar, Ouro, etc.) |
| vr_fechamento | Preço de fechamento da cotação |

### `investing_etf.csv`
Cotações diárias dos ETFs mais negociados no Brasil.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| nome | Nome completo do ETF |
| ticker | Código de negociação (ex: BOVA11) |
| link | Link do ativo no Investing.com |
| vr_ultimo | Último preço cotado |
| vr_variacao_pct | Variação percentual no dia |
| qt_volume | Volume de negociação |
| hr_atualizacao | Hora da última atualização |

### `s_p_entidades_brasil.csv`
Cadastro de entidades brasileiras avaliadas pela S&P Global.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| dt_captura | Data de captura dos dados |
| nome | Razão social do emissor |
| link | Link do emissor no portal da S&P |

### `s_p_ratings_brasil.csv`
Histórico de ratings vigentes atribuídos pela S&P na Escala Nacional Brasil.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| dt_captura | Data de captura dos dados |
| Tipo de Rating | Tipo de rating (ex: Escala Nacional Brasil de Longo Prazo) |
| Rating | Classificação de risco de crédito (ex: brAAA) |
| Data da Ação de Rating | Data em que o rating foi definido ou revisado |
| Data da ÚltimaRevisão | Data da última revisão periódica da agência |
| CreditWatch/ Perspectiva | Perspectiva atribuída (ex: Stable, Positive) |
| nome | Razão social do emissor |
| link | Link para detalhes no portal da S&P |

### `s_p_acoes_ratings.csv`
Histórico de ações de classificação de risco (Ratings Actions) nos últimos 7 dias da S&P Global.

| Campo | Descrição |
|---|---|
| data_captura | Data da execução (BRT) |
| dt_captura | Data de captura dos dados |
| descricao | Nome completo e descrição da emissão/ativo avaliado |
| classe | Série ou classe do papel |
| data_vencimento | Data de vencimento do papel |
| tipo_rating | Tipo de rating (ex: Escala Nacional Brasil de Longo Prazo) |
| data_acao | Data/hora em que a ação de rating foi divulgada |
| rating_novo | Nova classificação atribuída (ex: brAA-) |
| creditwatch_perspectiva_novo | Nova perspectiva atribuída |
| rating_anterior | Classificação anterior (ex: brAA) |
| creditwatch_perspectiva_anterior | Perspectiva anterior |
| acao | Tipo de ação executada (ex: Revised, Affirmed) |

---

## Estrutura do projeto

```
PulseFlat/
├── .github/
│   └── workflows/
│       └── captura_diaria.yml       # Agendamento GitHub Actions
├── data/                            # CSVs acumulativos e instantâneos (gerados automaticamente)
│   ├── .gitkeep
│   ├── anbima_indicadores.csv
│   ├── anbima_projecoes.csv
│   ├── anbima_titulos_publicos.csv
│   ├── anbima_debentures.csv
│   ├── anbima_ima_completo.csv
│   ├── anbima_550.csv
│   ├── anbima_indice_imab.csv
│   ├── bcb_ptax.csv
│   ├── bcb_sgs.csv
│   ├── bacen_negociacao_tpf_extragrupo_mes_corrente.csv
│   ├── bacen_negociacao_tpf_extragrupo_mes_anterior.csv
│   ├── ibge_sidra.csv
│   ├── cvm_cadastro_companhias_abertas.csv
│   ├── cvm_fundos_cadastro.csv
│   ├── cvm_fundos_informe_diario.csv
│   ├── cvm_fundos_extrato.csv
│   ├── cvm_fundos_classe.csv
│   ├── debentures_emissoes_caracteristicas.csv
│   ├── debentures_mercado_secundario_precos_negociacao.csv
│   ├── b3_fiis_listados.csv
│   ├── b3_etfs_listados.csv
│   ├── b3_carteiras_teoricas.csv
│   ├── b3_carteira_teorica_*.csv     # Carteiras teóricas individuais B3
│   ├── b3_indicadores_financeiros.csv
│   ├── b3_bdi_di_over.csv
│   ├── b3_taxa_cambio_referencia.csv
│   ├── b3_capital_social_empresas.csv
│   ├── b3_bvbg028.csv
│   ├── b3_bvbg086.csv
│   ├── b3_bvbg087.csv
│   ├── b3_indices_precos_historicos.csv
│   ├── b3_classificacao_setorial.csv
│   ├── b3_titulos_negociaveis.csv
├── scrapers/
│   ├── __init__.py
│   ├── anbima_indicadores.py
│   ├── anbima_projecoes.py
│   ├── anbima_titulos_publicos.py
│   ├── anbima_debentures.py
│   ├── anbima_ima_completo.py
│   ├── anbima_550.py
│   ├── anbima_indice_imab.py
│   ├── bcb_ptax.py
│   ├── bcb_sgs.py
│   ├── bacen_negociacao_tpf.py
│   ├── ibge_sidra.py
│   ├── cvm_cadastro_companhias_abertas.py
│   ├── cvm_fundos_cadastro.py
│   ├── cvm_fundos_informe_diario.py
│   ├── cvm_fundos_extrato.py
│   ├── cvm_fundos_classe.py
│   ├── debentures_emissoes_caracteristicas.py
│   ├── debentures_mercado_secundario_precos_negociacao.py
│   ├── b3_fiis.py
│   ├── b3_etfs.py
│   ├── b3_carteiras.py
│   ├── b3_carteira_teorica_ibov.py
│   ├── b3_carteira_teorica_*.py
│   ├── b3_indicadores_financeiros.py
│   ├── b3_bdi_di_over.py
│   ├── b3_taxa_cambio_referencia.py
│   ├── b3_capital_social_empresas.py
│   ├── b3_bvbg028.py
│   ├── b3_bvbg086.py
│   ├── b3_bvbg087.py
│   ├── b3_indices_precos_historicos.py
│   ├── b3_classificacao_setorial.py
│   ├── b3_titulos_negociaveis.py
├── utils/
│   ├── __init__.py
│   ├── base.py                      # Utilitários compartilhados
│   ├── parsers.py                   # Parsing de CSV, JSON, ZIP, XLS, FWF, XML
│   └── b3_helpers.py                # Helpers específicos B3 (company seeds)
├── tests/
│   ├── __init__.py
│   ├── test_scrapers.py
│   └── test_utils.py
├── scripts/
│   └── limpar_duplicatas.py         # Limpeza única de duplicatas históricas
├── run_all.py                       # Orquestrador
├── requirements.txt
├── .env.example                     # Template de credenciais
├── .gitignore
└── README.md
```

---

## Agendamento (GitHub Actions)

Múltiplas execuções automáticas ao longo do dia (horário BRT, seg–sex):

| Horário BRT | Cron (UTC) | Escopo |
|---|---|---|
| 06h00 | `0 9 * * 1-5` | Todos os scrapers |
| 08h00 | `0 11 * * 1-5` | Todos os scrapers |
| 09h00 | `0 12 * * 1-5` | Todos os scrapers |
| 09h30 | `30 12 * * 1-5` | Todos os scrapers |
| 18h00 | `0 21 * * 1-5` | Todos os scrapers |
| 21h00 | `0 0 * * 2-6` | Todos os scrapers |
| 23h00 | `0 2 * * 2-6` | Todos os scrapers |

**Execução manual:** Actions → Executar Automação de Dados Diária → Run workflow

---

## Instalação e uso local

```bash
git clone https://github.com/royopa/PulseFlat.git
cd PulseFlat
pip install -r requirements.txt

# Todos os scrapers
python run_all.py

# Por grupo
python run_all.py anbima
python run_all.py bcb
python run_all.py ibge
python run_all.py cvm
python run_all.py debentures
python run_all.py b3

# Scraper específico
python run_all.py anbima_indice_imab
python run_all.py bcb_ptax
python run_all.py bcb_sgs
python run_all.py bacen_negociacao_tpf
python run_all.py ibge_sidra
python run_all.py cvm_cadastro_companhias_abertas
python run_all.py cvm_fundos_cadastro
python run_all.py cvm_fundos_informe_diario
python run_all.py cvm_fundos_extrato
python run_all.py cvm_fundos_classe
python run_all.py debentures_emissoes_caracteristicas
python run_all.py debentures_mercado_secundario_precos_negociacao
python run_all.py b3_fiis
python run_all.py b3_etfs
python run_all.py b3_carteiras
python run_all.py b3_carteira_teorica_ibov
python run_all.py b3_indicadores_financeiros
python run_all.py b3_bdi_di_over
python run_all.py b3_taxa_cambio_referencia
python run_all.py b3_capital_social_empresas
python run_all.py b3_bvbg028
python run_all.py b3_bvbg086
python run_all.py b3_bvbg087
python run_all.py b3_indices_precos_historicos
python run_all.py b3_classificacao_setorial
python run_all.py b3_titulos_negociaveis
```

---

## Configuração do Boletim Diário B3 (opcional)

O download usa token retornado pela API. Caso o endpoint exija CAPTCHA, configure:

- `B3_RECAPTCHA_TOKEN` (token reCAPTCHA válido)
- `B3_BOLETIM_DATE` (YYYY-MM-DD, opcional para backfill)
- `B3_BOLETIM_FILES` (lista separada por vírgulas para sobrescrever os arquivos padrão)

---

## Configuração das credenciais ANBIMA (opcional)

O scraper de projeções usa **scraping como fallback automático** — funciona sem configuração.  
Para usar a API oficial com dados mais ricos (histórico, nº de instituições):

### 1. Obter as credenciais
- Cadastre-se em [developers.anbima.com.br](https://developers.anbima.com.br)
- Para acesso em produção: `anbimafeed@anbima.com.br`

### 2. Configurar no GitHub
**Settings → Secrets and variables → Actions → New repository secret**
- `ANBIMA_CLIENT_ID`
- `ANBIMA_CLIENT_SECRET`

### 3. Configurar localmente
```bash
cp .env.example .env
# Edite o .env com suas credenciais
```
O `.env` está no `.gitignore` — nunca será commitado.

---

## Adicionando um novo scraper

1. Crie `scrapers/novo_fonte.py` seguindo o padrão:
```python
from utils import get_logger, agora_brt, salvar_csv

ARQUIVO   = Path("data/novo_fonte.csv")
CABECALHO = ["data_captura", ...]

def capturar() -> list[dict]: ...

def main():
    salvar_csv(ARQUIVO, capturar(), CABECALHO)

if __name__ == "__main__":
    main()
```

2. Adicione em `SCRAPERS` no `run_all.py`
3. Adicione o CSV no `git add` do job correspondente em `captura_diaria.yml`

---

## Fontes oficiais

| Dados | URL |
|---|---|
| ANBIMA Indicadores | https://www.anbima.com.br/informacoes/indicadores/ |
| ANBIMA Projeções | https://www.anbima.com.br/pt_br/informar/projecoes-ipca-e-igp-m.htm |
| ANBIMA API Developers | https://developers.anbima.com.br |
| ANBIMA Títulos Públicos | https://www.anbima.com.br/informacoes/merc-sec/ |
| ANBIMA Debêntures | https://www.anbima.com.br/informacoes/merc-sec-debentures/ |
| ANBIMA IMA | https://www.anbima.com.br/informacoes/ima/ |
| BCB PTAX | https://www.bcb.gov.br/estatisticas/fechamento_cambio |
| BCB SGS | https://www.bcb.gov.br/estatisticas |
| IBGE SIDRA | https://sidra.ibge.gov.br/ |
| CVM Dados Abertos | https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/ |
| B3 FIIs | https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/fundos-de-investimento-imobiliario-fiis/ |
| B3 ETFs | https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/etfs/ |
| B3 Índices | https://www.b3.com.br/pt_br/market-data-e-indices/indices/ |
| B3 BVBG | https://www.b3.com.br/pesquisapregao/ |
