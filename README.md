# 📊 PulseFlat

Pipeline automatizado de captura diária de dados financeiros brasileiros via **GitHub Actions**.  
Sem servidor. Sem custo. Histórico versionado em CSV no próprio repositório.

---

## Scrapers

| Scraper | Fonte | Método | CSV gerado | Frequência |
|---|---|---|---|---|
| `anbima_indicadores` | ANBIMA | Scraping HTML | `anbima_indicadores.csv` | Diário (2x/dia) |
| `anbima_projecoes` | ANBIMA | API OAuth 2.0 / Scraping | `anbima_projecoes.csv` | Sob divulgação |
| `b3_fiis` | B3 API | JSON + Base64 | `b3_fiis_listados.csv` | Diário |
| `b3_etfs` | B3 API | JSON + Base64 | `b3_etfs_listados.csv` | Diário |
| `b3_carteiras` | B3 API | JSON + Base64 | `b3_carteiras_teoricas.csv` | Diário |
| `b3_boletim_diario` | B3 Boletim Diário | API download + token | `data/b3_boletim_diario/` | Diário |
| `captura_downloads_migrados` | ANBIMA/BACEN/B3/CVM/Debêntures | Requests + parsing CSV/JSON/ZIP/TXT | `data/*.csv` (16 conjuntos migrados) | Diário |

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

### `b3_fiis_listados.csv`
Ticker, nome, CNPJ, administrador, segmento, tipo, mandato, prazo, gestão, cotistas, patrimônio líquido.

### `b3_etfs_listados.csv`
Categoria (RV/RF), ticker, nome, CNPJ, administrador, gestor, índice de referência, segmento, cotistas, patrimônio.

### `b3_carteiras_teoricas.csv`
22 índices B3 · ticker, nome, tipo, quantidade teórica, peso (%), segmento — por ativo/índice/data.

**Índices:** IBOV, IBRA, IBrX 100, IBrX 50, IGC, ITAG, MLCX, SMLL, IVBX, IDIV, IFIX, IFNC, ICON, IEEX, IMAT, IMOB, INDX, UTIL, IGCT, IGNM, ISE, ICO2

### `data/b3_boletim_diario/`
Arquivos diários do Boletim Diário B3 (CSV/ZIP) baixados via token.  
Os nomes seguem o retorno da API (ex: `LendingOpenPositionFile_YYYYMMDD_1.csv`).

### `captura_downloads_migrados` (novos CSVs)
Conjuntos migrados do repositório `captura_downloads` (sem Selenium), todos com `data_captura` e `hora_captura`:

- `anbima_mercado_secundario_debentures.csv`
- `anbima_mercado_secundario_titulos_publicos.csv`
- `anbima_ima_completo.csv`
- `bacen_negociacao_tpf_extragrupo_mes_corrente.csv`
- `bacen_negociacao_tpf_extragrupo_mes_anterior.csv`
- `b3_instrumentos_listados.csv`
- `b3_indicadores_financeiros.csv`
- `b3_taxa_cambio_referencia.csv`
- `b3_capital_social_empresas.csv`
- `debentures_emissoes_caracteristicas.csv`
- `debentures_mercado_secundario_precos_negociacao.csv`
- `debentures_mercado_pu_historico.csv`
- `cvm_cad_fi.csv`
- `cvm_extrato_fi.csv`
- `cvm_registro_fundo_classe.csv`
- `b3_classificacao_setorial.csv`
- `b3_titulos_negociaveis.csv`

---

## Estrutura do projeto

```
PulseFlat/
├── .github/
│   └── workflows/
│       └── captura_diaria.yml    # Agendamento GitHub Actions
├── data/                         # CSVs acumulativos (gerados automaticamente)
│   ├── .gitkeep
│   ├── anbima_indicadores.csv
│   ├── anbima_projecoes.csv
│   ├── b3_fiis_listados.csv
│   ├── b3_etfs_listados.csv
│   ├── b3_carteiras_teoricas.csv
│   └── b3_boletim_diario/       # Downloads diários (arquivos do boletim)
├── scrapers/
│   ├── __init__.py
│   ├── anbima_indicadores.py
│   ├── anbima_projecoes.py
│   ├── b3_fiis.py
│   ├── b3_etfs.py
│   ├── b3_carteiras.py
│   └── b3_boletim_diario.py
├── utils/
│   ├── __init__.py
│   └── base.py                   # Utilitários compartilhados
├── tests/
│   ├── __init__.py
│   └── test_utils.py
├── run_all.py                    # Orquestrador
├── requirements.txt
├── .env.example                  # Template de credenciais
├── .gitignore
└── README.md
```

---

## Agendamento (GitHub Actions)

| Job | Scrapers | Horário BRT | Cron (UTC) |
|---|---|---|---|
| `anbima` | indicadores + projeções | 09h30 seg-sex | `30 12 * * 1-5` |
| `b3` | fiis + etfs + carteiras | 10h00 seg-sex | `00 13 * * 1-5` |

**Execução manual:** Actions → Captura Diária → Run workflow

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
python run_all.py b3
python run_all.py migrados

# Scraper específico
python run_all.py anbima_indicadores
python run_all.py anbima_projecoes
python run_all.py b3_fiis
python run_all.py b3_etfs
python run_all.py b3_carteiras
python run_all.py b3_boletim_diario
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
| B3 FIIs | https://www.b3.com.br/.../fii/fiis-listados/ |
| B3 ETFs | https://www.b3.com.br/.../etf/renda-variavel/etfs-listados/ |
| B3 Índices | https://www.b3.com.br/pt_br/market-data-e-indices/indices/ |
| B3 Boletim Diário | https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/arquivos-para-download/ |
