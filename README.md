<p align="center">
  <img src="logo.png" alt="PulseFlat Logo" width="280">
</p>

# PulseFlat

> 🚀 **Página do Projeto:** [https://royopa.github.io/PulseFlat/](https://royopa.github.io/PulseFlat/)

Pipeline automatizado de captura diária de dados financeiros brasileiros via **GitHub Actions**.  
Sem servidor. Sem custo. Histórico versionado em CSV no próprio repositório.

---

## Recursos e Diferenciais do Projeto

*   **Arquitetura Baseada em Classes**: Implementação de uma classe base sólida (`BaseScraper`) para gerenciar automaticamente a execução, o ciclo de vida dos scrapers, e a sanitização padrão de dados.
*   **Limpeza Inteligente de Tipagem**: Conversão automática de datas brasileiras (`DD/MM/YYYY` ou `DD/MM/YY` para o padrão ISO `YYYY-MM-DD`) e normalização de floats com vírgula para ponto (ex: `"5,3656"` para `5.3656`).
*   **Execução Paralela**: Orquestrador (`run_all.py`) integrado com `ThreadPoolExecutor`, permitindo processamento concorrente seguro de scrapers independentes e organizando a execução em fases (fase 1: independentes; fase 2: dependentes).
*   **Monitoramento de Schema Drift**: Validação dinâmica de colunas na persistência do arquivo contra schemas conhecidos, logando discrepâncias de colunas novas ou removidas.
*   **Dashboard Dinâmico e Otimizado**: Interface HTML enriquecida que carrega e renderiza dados sob demanda a partir de JSONs estáticos (`datasets.json`, `schemas.json`, `pipeline_status.json`), apresentando busca instantânea debouncada (delay de 100ms), filtragem por fontes de dados, visualização de tabelas e snippets copy-paste prontos para Pandas.
*   **Carregamento Ultra Rápido**: Otimizações de front-end com tags `<link rel="preload">` e CSS Containment (`content-visibility: auto` e `contain-intrinsic-size: 500px`) para garantir rolagem de página suave e tempo mínimo até a interatividade (LCP/FCP baixos).

---

## Estrutura do Projeto

```
PulseFlat/
├── .github/
│   └── workflows/
│       └── captura_diaria.yml       # Agendamento do pipeline no GitHub Actions
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
│   ├── *.py                         # Scripts específicos de coleta por dataset
├── utils/                           # Utilitários compartilhados auxiliares
│   ├── __init__.py
│   ├── base.py                      # Funções genéricas e salvamento de CSVs
│   ├── parsers.py                   # Parsers robustos para ZIP, Excel, XLS, CSV, FWF, XML
│   └── b3_helpers.py                # Helpers específicos para seeds da B3
├── tests/                           # Suíte de testes automatizados
│   ├── test_scrapers.py
│   └── test_utils.py
├── run_all.py                       # Orquestrador CLI central do projeto
├── requirements.txt                 # Dependências do Python
├── .env.example                     # Template de variáveis de ambiente
├── .gitignore
└── README.md
```

---

## Funcionamento e Execução do Orquestrador (`run_all.py`)

O script `run_all.py` atua como o cérebro do pipeline. Ele importa e executa os scrapers em paralelo ou de forma sequencial, monitorando tempos de execução e erros.

### Fases de Execução
Para evitar falhas de dependência (como scrapers que requerem o cadastro de emissores atualizado de outros scripts), a execução é segmentada em duas fases:
1.  **Fase 1 (Independentes)**: Executa a maioria dos scrapers de forma concorrente.
2.  **Fase 2 (Dependentes)**: Executa scrapers como `s_p_ratings_brasil` após a conclusão bem-sucedida de seus pré-requisitos (`s_p_entidades_brasil`).

### CLI Options e Exemplos

```bash
# Executa todos os scrapers registrados (padrão paralelo com 4 workers)
python run_all.py

# Executa os scrapers sequencialmente (bom para depuração de rede)
python run_all.py --sequential

# Executa os scrapers em paralelo definindo o número máximo de threads
python run_all.py --parallel --max-workers 8

# Filtra execução para um grupo específico
python run_all.py --group anbima
python run_all.py --group b3
python run_all.py --group bcb
python run_all.py --group cvm
python run_all.py --group ibge
python run_all.py --group ratings
python run_all.py --group misc

# Executa apenas um único scraper específico pelo nome do módulo
python run_all.py --scraper anbima_indicadores
```

---

## Infraestrutura do `BaseScraper`

Todos os novos scrapers herdam de `BaseScraper` localizado em [scrapers/utils/base.py](file:///Users/rodrigo/projects/PulseFlat/scrapers/utils/base.py). Esta classe abstrai a complexidade do pipeline:

```python
from scrapers.utils.base import BaseScraper
import pandas as pd

class MeuScraperScraper(BaseScraper):
    # O nome do scraper determina o arquivo CSV final (data/meu_scraper.csv)
    name = "meu_scraper"
    
    # Define se os dados capturados acumulam ao longo dos dias ou substituem o CSV por completo
    accumulate = True
    
    # Chaves para evitar duplicados em re-execuções no mesmo dia
    chaves_dedup = ["data_captura", "ticker"]

    def fetch(self) -> pd.DataFrame:
        # 1. Faz chamadas de API ou extração
        # 2. Retorna um Pandas DataFrame
        dados = [{"ticker": "PETR4", "preco": "42,50", "data": "04/06/2026"}]
        return pd.DataFrame(dados)
```

### Sanitizações e Fluxos Automáticos na Execução (`run()`)
*   **Tratamento de Dados**: Se a coluna `data_captura` estiver ausente, ela é gerada dinamicamente.
*   **Limpeza de Formatos**: Converte strings de data de `DD/MM/YYYY` ou `DD/MM/YY` para `YYYY-MM-DD` automaticamente. Substitui separadores decimais de vírgula por ponto (ex: `"12,34"` vira `"12.34"`).
*   **Preenchimento de NaNs**: Valores nulos do Pandas (`NaN`, `None`, `NaT`) são limpos para string vazia `""` para manter a integridade dos CSVs.
*   **Monitoramento de Schema**: Verifica se houve adição ou remoção de campos em relação ao schema registrado em `data/schemas.json`, emitindo alertas de *Schema Drift*.

---

## Instalação e Uso Local

### 1. Clonar o Repositório e Instalar Dependências
```bash
git clone https://github.com/royopa/PulseFlat.git
cd PulseFlat
pip install -r requirements.txt
```

### 2. Variáveis de Ambiente (Opcional)
Crie um arquivo `.env` a partir do template `.env.example`:
```bash
cp .env.example .env
```
Edite as credenciais caso queira usar as APIs oficiais da ANBIMA e B3:
*   `ANBIMA_CLIENT_ID` / `ANBIMA_CLIENT_SECRET`: Acesso à API REST oficial da ANBIMA (há fallback de scraping web caso não configurado).
*   `B3_RECAPTCHA_TOKEN`: Token para contornar desafios de download em relatórios diários da B3.

---

## Suíte de Testes

O projeto utiliza `pytest` para testes automatizados rápidos de integridade e regressão:

```bash
# Executa todos os testes unitários
python -m pytest tests/ -v
```

Os testes estão distribuídos em:
*   [tests/test_scrapers.py](file:///Users/rodrigo/projects/PulseFlat/tests/test_scrapers.py): Valida a resposta mockada das APIs do Banco Central (PTAX, SGS), scrapers baseados em JSON e arquivos ZIP da B3.
*   [tests/test_utils.py](file:///Users/rodrigo/projects/PulseFlat/tests/test_utils.py): Valida a lógica do salvamento deduplicado de arquivos CSV, tratamento de fuso horário, e codificadores JSON Base64 da B3.

---

## Fontes Oficiais de Dados

| Grupo | Fonte Primária | Dados Disponibilizados |
|---|---|---|
| **ANBIMA** | [Portal ANBIMA](https://www.anbima.com.br) | Taxas indicativas, Projeções de Inflação (IPCA/IGPM), Títulos Públicos, Debêntures, Índices IMA/IDkA. |
| **BCB** | [Banco Central do Brasil](https://www.bcb.gov.br) | Cotações diárias do Dólar (PTAX), séries do Sistema de Gerenciamento de Séries (SGS), negociação de títulos públicos (DEMAB), balancetes cadastrais de bancos e dados de Basileia III. |
| **CVM** | [Portal Brasileiro de Dados Abertos](https://dados.cvm.gov.br) | Cadastro geral de companhias abertas, informes diários e dados de cotas e classes de fundos de investimento. |
| **B3** | [B3 Market Data](https://www.b3.com.br) | FIIs e ETFs listados, composição histórica das carteiras teóricas dos índices (IBOV, SMLL, ISEE, BDRX, IFNC, etc.), taxas DI Over e taxas de câmbio de referência. |
| **IBGE** | [IBGE SIDRA API](https://sidra.ibge.gov.br) | Índices oficiais de inflação do Brasil (IPCA, IPCA-15, INPC). |
| **Ratings** | [S&P Global](https://www.spglobal.com) / [Moody's Local](https://www.moodyslocal.com) | Classificação de ratings corporativos e histórico de Ratings Actions na Escala Nacional Brasil. |
| **Misc** | [Yahoo Finance](https://finance.yahoo.com) / [ONU](https://unglobalcompact.org) | Cotações históricas globais e lista de empresas brasileiras participantes do Pacto Global da ONU. |
