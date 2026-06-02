# PulseFlat

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
| `anbima_ima` | ANBIMA | TXT delimitado | `anbima_ima.csv` |
| `anbima_550` | ANBIMA | TXT (Resolução 550) | `anbima_550.csv` |

### Grupo BCB

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `bcb_ptax` | BCB | API REST (Olinda) | `bcb_ptax.csv` |
| `bcb_sgs` | BCB | API REST (SGS) | `bcb_sgs.csv` |

### Grupo IBGE

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `ibge_sidra` | IBGE | API REST (SIDRA) | `ibge_sidra.csv` |

### Grupo B3

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `b3_fiis` | B3 | API JSON + Base64 | `b3_fiis_listados.csv` |
| `b3_etfs` | B3 | API JSON + Base64 | `b3_etfs_listados.csv` |
| `b3_carteiras` | B3 | API JSON + Base64 | `b3_carteiras_teoricas.csv` |
| `b3_futuros_ajustes` | B3 | Scraping HTML | `b3_futuros_ajustes.csv` |
| `b3_bmf_taxas_juros` | B3 | API (BDI / Hub de Dados) | `b3_bmf_taxas_juros.csv` |
| `b3_indicadores_financeiros` | B3 | API JSON + Base64 | `b3_indicadores_financeiros.csv` |
| `b3_bdi_di_over` | B3 | API POST (BDI) | `b3_bdi_di_over.csv` |

### Grupo Migrados

| Scraper | Fonte | Método | CSV(s) gerado(s) |
|---|---|---|---|
| `captura_downloads_migrados` | ANBIMA / BCB / B3 | Requests + parsing CSV/ZIP/JSON/TXT | `anbima_ima_completo.csv`, `bacen_negociacao_tpf_extragrupo_mes_anterior.csv`, `b3_capital_social_empresas.csv`, `b3_taxa_cambio_referencia.csv` e outros |

---

## Dados capturados

### `anbima_indicadores.csv`
| Campo | Descrição |
|---|---|
| data_captura / hora_captura | Data e hora da execução (BRT) |
| data_referencia_pagina | Data/hora da última atualização na página |
| indicador | Nome do indicador (ex: Taxa SELIC (BC)) |
| categoria | Grupo: Taxa de Juros, Câmbio, Índice de Preços, etc. |
| valor | Valor numérico (ponto como separador decimal) |
| unidade | % a.a., R$, % mês, índice, R$ cota |

**Indicadores:** SELIC (Estimativa e BC), DI-B3, IGP-M (índice, var.%, projeção), IPCA (índice, var.%, projeção), Dólar Comercial (compra/venda), Euro (compra/venda), TR, TBF, FDS.

### `anbima_projecoes.csv`
| Campo | Descrição |
|---|---|
| estrategia_coleta | `api_oficial` ou `scraping_indicadores` |
| indice | IPCA ou IGP-M |
| mes_referencia | Mês/ano da projeção (ex: mai/26) |
| tipo_projecao | corrente / seguinte / posterior / fechado |
| valor_pct | Valor em % (separador decimal: ponto) |
| data_divulgacao | Data de divulgação da projeção |
| num_instituicoes | Nº de instituições (disponível via API) |

**IGP-M:** divulgado ~3x/mês nos dias de prévia e fechado pela FGV  
**IPCA:** divulgado ~2x/mês no dia do IPCA fechado e do IPCA-15 pelo IBGE

### `anbima_titulos_publicos.csv`
| Campo | Descrição |
|---|---|
| data_captura / hora_captura | Data e hora da execução (BRT) |
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
| data_captura / hora_captura | Data e hora da execução (BRT) |
| codigo | Código da debênture |
| nome_emissor | Nome do emissor |
| dt_repactuacao_vencimento | Data de repactuação/vencimento |
| indice_correcao | Índice de correção (CDI, IPCA, etc.) |
| tx_compra / tx_venda / tx_indicativa | Taxas de compra, venda e indicativa |
| pu | Preço unitário (R$) |
| duration | Duration do ativo (dias úteis) |

### `anbima_ima.csv`
| Campo | Descrição |
|---|---|
| data_captura / hora_captura | Data e hora da execução (BRT) |
| data_referencia | Data de referência |
| indice | Nome do índice (IMA-Geral, IRF-M, IDA, etc.) |
| numero_indice | Número do índice |
| variacao_diaria / _mensal / _anual | Variações percentuais |
| duration_du | Duration em dias úteis |
| peso_geral | Peso do subíndice no índice geral (%) |

### `anbima_550.csv`
| Campo | Descrição |
|---|---|
| data_captura / hora_captura | Data e hora da execução (BRT) |
| titulo | Nome do ativo |
| vencimento | Data de vencimento |
| preco_unitario | Preço unitário (R$) |
| preco_retorno | Preço de retorno |
| posicao_custodia | Posição em custódia |

### `bcb_ptax.csv`
| Campo | Descrição |
|---|---|
| data_captura / hora_captura | Data e hora da execução (BRT) |
| data_hora_cotacao | Data/hora da cotação PTAX |
| cotacao_compra | Cotação de compra (R$/US$) |
| cotacao_venda | Cotação de venda (R$/US$) |

### `bcb_sgs.csv`
| Campo | Descrição |
|---|---|
| data_captura / hora_captura | Data e hora da execução (BRT) |
| codigo_serie | Código da série SGS (ex: 11, 432, 433) |
| nome_serie | Nome descritivo da série |
| data | Data do valor |
| valor | Valor da série |

**Séries:** SELIC diária, SELIC acumulada mês, CDI diário, CDI acumulado mês, IPCA mensal, IPCA acumulado 12m, IGP-M mensal, IGP-M acumulado 12m, Dólar venda.

### `ibge_sidra.csv`
| Campo | Descrição |
|---|---|
| data_captura / hora_captura | Data e hora da execução (BRT) |
| serie_id | Código da tabela SIDRA |
| nome_serie | Nome da série |
| fonte | Fonte dos dados |
| periodo_referencia | Período de referência |
| data_modificacao | Data da última modificação |

**Tabelas:** 1737 (IPCA), 3065 (IPCA-15), 1621 (INPC), 3066 (IPC-Br).

### `b3_fiis_listados.csv`
Ticker, nome, CNPJ, administrador, segmento, tipo, mandato, prazo, gestão, cotistas, patrimônio líquido.

### `b3_etfs_listados.csv`
Categoria (RV/RF), ticker, nome, CNPJ, administrador, gestor, índice de referência, segmento, cotistas, patrimônio.

### `b3_carteiras_teoricas.csv`
22 índices B3 · ticker, nome, tipo, quantidade teórica, peso (%), segmento — por ativo/índice/data.

**Índices:** IBOV, IBRA, IBrX 100, IBrX 50, IGC, ITAG, MLCX, SMLL, IVBX, IDIV, IFIX, IFNC, ICON, IEEX, IMAT, IMOB, INDX, UTIL, IGCT, IGNM, ISE, ICO2

### `b3_futuros_ajustes.csv`
| Campo | Descrição |
|---|---|
| data_captura / hora_captura | Data e hora da execução (BRT) |
| data_referencia | Data de referência dos ajustes |
| mercadoria | Código da mercadoria/contrato futuro |
| vencimento | Mês/ano de vencimento |
| preco_ajuste_anterior / preco_ajuste_atual | Preços de ajuste |
| variacao | Variação percentual |
| valor_ajuste_por_contrato_brl | Ajuste por contrato (R$) |

### `b3_bmf_taxas_juros.csv`
| Campo | Descrição |
|---|---|
| data_captura / hora_captura | Data e hora da execução (BRT) |
| tabela_origem | Tabela de origem no BDI |
| data_referencia | Data de referência |
| curva | Nome da curva (DI x Pré, Cupom Cambial, etc.) |
| prazo_dias | Prazo em dias úteis |
| taxa | Taxa (% a.a.) |

### `b3_indicadores_financeiros.csv`
| Campo | Descrição |
|---|---|
| data_captura / hora_captura | Data e hora da execução (BRT) |
| security_identification_code | Código do indicador |
| description | Descrição do indicador |
| group_description | Grupo (Interest Rates, Exchange Rates, etc.) |
| value | Valor numérico |
| rate | Taxa associada |

### `b3_bdi_di_over.csv`
| Campo | Descrição |
|---|---|
| data_captura / hora_captura | Data e hora da execução (BRT) |
| rpt_dt | Data de referência |
| number_of_operations | Número de operações |
| financial_volume | Volume financeiro (R$) |
| average | Taxa média (% a.d.) |
| daily_factor | Fator diário |
| selic_rate | Taxa SELIC no período |

### `captura_downloads_migrados` (novos CSVs)
Conjuntos migrados do repositório `captura_downloads` (sem Selenium), todos com `data_captura` e `hora_captura`:

- `anbima_ima_completo.csv`
- `bacen_negociacao_tpf_extragrupo_mes_anterior.csv`
- `b3_indicadores_financeiros.csv`
- `b3_taxa_cambio_referencia.csv`
- `b3_capital_social_empresas.csv`

---

## Estrutura do projeto

```
PulseFlat/
├── .github/
│   └── workflows/
│       └── captura_diaria.yml       # Agendamento GitHub Actions
├── data/                            # CSVs acumulativos (gerados automaticamente)
│   ├── .gitkeep
│   ├── anbima_indicadores.csv
│   ├── anbima_projecoes.csv
│   ├── anbima_titulos_publicos.csv
│   ├── anbima_debentures.csv
│   ├── anbima_ima.csv
│   ├── anbima_550.csv
│   ├── bcb_ptax.csv
│   ├── bcb_sgs.csv
│   ├── ibge_sidra.csv
│   ├── b3_fiis_listados.csv
│   ├── b3_etfs_listados.csv
│   ├── b3_carteiras_teoricas.csv
│   ├── b3_indicadores_financeiros.csv
│   ├── b3_bdi_di_over.csv
│   └── anbima_ima_completo.csv
├── scrapers/
│   ├── __init__.py
│   ├── anbima_indicadores.py
│   ├── anbima_projecoes.py
│   ├── anbima_titulos_publicos.py
│   ├── anbima_debentures.py
│   ├── anbima_ima.py
│   ├── anbima_550.py
│   ├── bcb_ptax.py
│   ├── bcb_sgs.py
│   ├── ibge_sidra.py
│   ├── b3_fiis.py
│   ├── b3_etfs.py
│   ├── b3_carteiras.py
│   ├── b3_futuros_ajustes.py
│   ├── b3_bmf_taxas_juros.py
│   ├── b3_indicadores_financeiros.py
│   ├── b3_bdi_di_over.py
│   └── captura_downloads_migrados.py
├── utils/
│   ├── __init__.py
│   └── base.py                      # Utilitários compartilhados
├── tests/
│   ├── __init__.py
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
| 21h00 | `0 0 * * 2-6` | Fechamento |
| 23h00 | `0 2 * * 2-6` | Fechamento |

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
python run_all.py b3
python run_all.py migrados

# Scraper específico
python run_all.py anbima_indicadores
python run_all.py anbima_projecoes
python run_all.py anbima_titulos_publicos
python run_all.py anbima_debentures
python run_all.py anbima_ima
python run_all.py anbima_550
python run_all.py bcb_ptax
python run_all.py bcb_sgs
python run_all.py ibge_sidra
python run_all.py b3_fiis
python run_all.py b3_etfs
python run_all.py b3_carteiras
python run_all.py b3_futuros_ajustes
python run_all.py b3_bmf_taxas_juros
python run_all.py b3_indicadores_financeiros
python run_all.py b3_bdi_di_over
python run_all.py captura_downloads_migrados
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
CABECALHO = ["data_captura", "hora_captura", ...]

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
| B3 FIIs | https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/fundos-de-investimento-imobiliario-fiis/ |
| B3 ETFs | https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/etfs/ |
| B3 Índices | https://www.b3.com.br/pt_br/market-data-e-indices/indices/ |
