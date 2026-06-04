<p align="center">
  <img src="logo.png" alt="PulseFlat Logo" width="280">
</p>

<h1 align="center">PulseFlat</h1>

<p align="center">
  <strong>Pipeline Serverless e Automatizado de Captura de Dados Financeiros Brasileiros</strong>
</p>

<p align="center">
  <a href="https://github.com/PulseDataLabs/PulseFlat/actions/workflows/main.yml"><img src="https://github.com/PulseDataLabs/PulseFlat/actions/workflows/main.yml/badge.svg" alt="Build Status"></a>
  <img src="https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg" alt="Python Versions">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/data-63%20datasets-orange.svg" alt="Data Count">
  <a href="https://pulsedatalabs.github.io/PulseFlat/"><img src="https://img.shields.io/badge/dashboard-live-brightgreen.svg" alt="Live Dashboard"></a>
</p>

<p align="center">
  <a href="#-recursos-e-diferenciais">Recursos</a> •
  <a href="#-arquitetura-do-pipeline">Arquitetura</a> •
  <a href="#-funcionamento-do-orquestrador">Funcionamento</a> •
  <a href="#-estrutura-do-projeto">Estrutura</a> •
  <a href="#-guia-do-desenvolvedor">Desenvolvedor</a> •
  <a href="#-fontes-e-datasets">Datasets</a>
</p>

---

**PulseFlat** é um pipeline de ETL (Extração, Transformação e Carga) serverless projetado para coletar, tratar e disponibilizar dados financeiros brasileiros históricos de fontes oficiais diariamente. Ele funciona 100% de forma automatizada via **GitHub Actions**, versionando o histórico diretamente no repositório em formato CSV plano, sem custos com banco de dados ou servidores.

---

## 🚀 Recursos e Diferenciais

*   **OOP & Abstração Sólida**: Scrapers estruturados sob uma classe base robusta (`BaseScraper`) que gerencia nativamente o ciclo de vida da execução, tratamento de exceções *thread-safe* e logs padronizados.
*   **Descoberta Dinâmica (Reflection)**: O orquestrador detecta scrapers dinamicamente inspecionando a pasta `scrapers/` no momento da execução, eliminando a necessidade de registros estáticos ou configurações hardcoded.
*   **Sanitização Automática de Dados**: Limpeza inteligente embutida que padroniza formatos de data brasileiros (`DD/MM/YYYY` ou `DD/MM/YY` para ISO `YYYY-MM-DD`) e normaliza representações decimais com vírgula para floats com ponto.
*   **Execução Concorrente Multicondicional**: Orquestrador inteligente capaz de paralelizar a execução de scripts independentes e enfileirar sequencialmente os scripts dependentes.
*   **Monitoramento de Schema Drift**: Proteção na persistência de arquivos contra mudanças repentinas nas estruturas originais de dados (emite logs detalhados sobre colunas adicionadas ou removidas).
*   **Frontend Otimizado (Zero CLS/LCP Baixo)**: Dashboard interativo desenvolvido em vanilla HTML/CSS que consome os JSONs estáticos diretamente do repositório, com recursos avançados de preloading, busca instantânea debouncada e renderização adiada via CSS Containment (`content-visibility`).

---

## 📐 Arquitetura do Pipeline

A fluxo de processamento e disponibilização de dados funciona conforme a estrutura abaixo:

```mermaid
graph TD
    A[GitHub Actions Cron / Trigger] --> B[run_all.py Orchestrator]
    B -->|Dynamic Discovery| C[scrapers/ folder]
    B -->|Executes Phase 1| D[Independent Scrapers]
    B -->|Executes Phase 2| E[Dependent Scrapers]
    D --> F[data/*.csv files]
    E --> F
    B -->|Calls generate_catalog.py| G[data/datasets.json]
    F & G --> H[git push origin main]
    H --> I[GitHub Pages / index.html]
```

---

## ⚙️ Funcionamento do Orquestrador (`run_all.py`)

O orquestrador `run_all.py` varre a pasta `scrapers/`, importa as classes e lê os metadados diretamente de seus atributos de classe:
*   `group` (grupo a que pertence: `anbima`, `bcb`, `b3`, `cvm`, `ibge`, `ratings`, `misc`).
*   `enabled` (indica se deve rodar no pipeline diário principal).
*   `phase` (ordem de dependência: Phase 1 para independentes; Phase 2 para dependentes que dependem do resultado da Phase 1).

### CLI Options e Exemplos de Uso

```bash
# Executa todos os scrapers ativos em paralelo (padrão: 4 workers)
python run_all.py

# Executa os scrapers sequencialmente (ideal para depuração de rede)
python run_all.py --sequential

# Executa em paralelo especificando um limite de threads
python run_all.py --parallel --max-workers 8

# Executa apenas scrapers pertencentes a um grupo específico
python run_all.py --group bcb
python run_all.py --group ratings

# Executa manualmente um scraper específico (mesmo se desabilitado por padrão)
python run_all.py --scraper anbima_indicadores

# Apenas regenera o catálogo data/datasets.json a partir dos metadados das classes
python run_all.py --generate-catalog
```

---

## 📂 Estrutura do Projeto

```
PulseFlat/
├── .github/
│   └── workflows/
│       └── main.yml                 # Agendamento do pipeline no GitHub Actions
├── data/                            # Datasets, schemas e metadados de controle
│   ├── datasets.json                # Catálogo estruturado de metadados dos datasets
│   ├── schemas.json                 # Definição e mapeamento de campos e tipos
│   ├── pipeline_status.json / .js   # Logs de saúde e duração da última execução
│   ├── last_updates.json / .js      # Período de cobertura temporal mínima/máxima de cada CSV
│   └── *.csv                        # Séries temporais de dados financeiros
├── scrapers/                        # Módulos de captura
│   ├── utils/
│   │   ├── __init__.py
│   │   └── base.py                  # Classe infraestrutural BaseScraper
│   ├── generic_scraper.py           # Scraper base genérico parametrizado por YAML
│   └── *.py                         # Scripts específicos de coleta por dataset
├── utils/                           # Utilitários compartilhados auxiliares
│   ├── __init__.py
│   ├── base.py                      # Funções genéricas e salvamento de CSVs
│   ├── parsers.py                   # Parsers robustos para ZIP, Excel, XLS, CSV, FWF, XML
│   └── b3_helpers.py                # Helpers específicos para seeds da B3
├── tests/                           # Suíte de testes automatizados
│   ├── test_base_scraper.py         # Testes de sanitização e ciclo da classe base
│   ├── test_parsers.py              # Testes para os parsers auxiliares (ZIP, FWF, etc.)
│   ├── test_run_all.py              # Testes da CLI e do mecanismo de descoberta dinâmica
│   ├── test_scrapers.py             # Testes mockados de scrapers individuais
│   └── test_utils.py                # Testes de persistência de arquivos e helpers
├── run_all.py                       # Orquestrador CLI central do projeto
├── requirements.txt                 # Dependências do Python
├── .env.example                     # Template de variáveis de ambiente
├── .gitignore
└── README.md
```

---

## 💻 Guia do Desenvolvedor

### Instalação Local

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/PulseDataLabs/PulseFlat.git
    cd PulseFlat
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure o arquivo de variáveis de ambiente:**
    ```bash
    cp .env.example .env
    ```
    *(Edite o `.env` com suas chaves caso precise utilizar APIs oficiais da ANBIMA ou B3).*

### Criando um Novo Scraper

Basta criar um novo arquivo Python dentro de `scrapers/` herdando de `BaseScraper`. O orquestrador o detectará automaticamente:

```python
from scrapers.utils.base import BaseScraper
import pandas as pd

class MeuNovoScraper(BaseScraper):
    # Propriedades de Orquestração
    name = "meu_novo_scraper"
    group = "misc"
    enabled = True
    phase = 1
    
    # Propriedades de Persistência
    accumulate = True
    chaves_dedup = ["data_captura", "ticker"]
    
    # Propriedades do Catálogo (Metadados do Dashboard)
    title = "Meu Novo Dataset"
    description = "Coleta dados de teste diariamente."
    icon = "📊"
    icon_class = "icon-misc"
    badge = "Diário"
    badge_class = "badge-daily"
    tags = ["teste", "novo"]
    source = "Minha Fonte"

    def fetch(self) -> pd.DataFrame:
        # A lógica do scraper deve ir aqui, retornando um Pandas DataFrame
        dados = [{"ticker": "ABCD3", "preco": "10,50", "data": "04/06/2026"}]
        return pd.DataFrame(dados)
```

### Executando Testes

A suíte de testes utiliza `pytest` com `requests-mock` para testar os parsers e APIs mockadas de forma rápida e offline:

```bash
python -m pytest tests/ -v
```

---

## 📊 Fontes e Datasets

Os scrapers estão classificados nos seguintes grupos de dados principais:

| Grupo | Fonte Primária | Exemplos de Dados Disponibilizados | Frequência |
|---|---|---|---|
| **ANBIMA** | [Portal ANBIMA](https://www.anbima.com.br) / [SND Debêntures](https://www.debentures.com.br) | Taxas indicativas, Projeções de Inflação (IPCA/IGPM), Títulos Públicos, Emissões e Mercado Secundário de Debêntures, Índices IMA/IDkA. | Diária |
| **BCB** | [Banco Central do Brasil](https://www.bcb.gov.br) | Cotações diárias do Dólar (PTAX), Séries SGS (SELIC, CDI, Inflação), Negociação de títulos públicos (DEMAB), Balancetes cadastrais de bancos. | Diária |
| **CVM** | [Portal Brasileiro de Dados Abertos](https://dados.cvm.gov.br) | Cadastro geral de companhias abertas, informes diários e dados de cotas/classes de fundos. | Diária |
| **B3** | [B3 Market Data](https://www.b3.com.br) | FIIs/ETFs listados, composição das carteiras teóricas de índices (IBOV, SMLL, ISEE, BDRX, IFNC), taxas DI Over. | Diária |
| **IBGE** | [IBGE SIDRA API](https://sidra.ibge.gov.br) | Índices oficiais de inflação do Brasil (IPCA, IPCA-15, INPC). | Mensal |
| **Misc** | [Yahoo Finance](https://finance.yahoo.com) / [ONU](https://unglobalcompact.org) | Cotações históricas de índices globais e lista de empresas brasileiras participantes do Pacto Global da ONU. | Diária |

---

## 📄 Licença

Este projeto é de código aberto e está licenciado sob os termos da licença **MIT**.
