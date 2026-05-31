# 📊 B3 Carteiras Teóricas — Captura Automatizada

Captura diária da composição das carteiras teóricas dos principais índices da B3,
usando a mesma API interna que alimenta as páginas de composição de cada índice:
https://www.b3.com.br/pt_br/market-data-e-indices/indices/

## Índices capturados

### Índices Amplos
| Código | Nome |
|--------|------|
| IBOV   | Ibovespa |
| IBRA   | IBrA - Índice Brasil Amplo |
| IBRX   | IBrX 100 - Índice Brasil 100 |
| IBXL   | IBrX 50 - Índice Brasil 50 |
| IGCX   | IGC - Governança Corporativa |
| ITAG   | ITAG - Tag Along |
| MLCX   | Mid-Large Cap |
| SMLL   | Small Cap |
| IVBX   | IVBX-2 - Valor BM&F Bovespa |

### Índices de Segmentos e Setoriais
| Código | Nome |
|--------|------|
| IDIV   | Índice Dividendos |
| IFIX   | Índice de Fundos Imobiliários |
| IFNC   | Índice Financeiro |
| ICON   | Índice de Consumo |
| IEEX   | Índice de Energia Elétrica |
| IMAT   | Índice de Materiais Básicos |
| IMOB   | Índice Imobiliário |
| INDX   | Índice do Setor Industrial |
| UTIL   | Índice Utilidade Pública |

### Índices de Sustentabilidade e Governança
| Código | Nome |
|--------|------|
| IGCT   | Governança Corporativa Trade |
| IGNM   | Novo Mercado |
| ISEE   | ISE - Sustentabilidade Empresarial |
| ICO2   | ICO2 - Carbono Eficiente |

## Como funciona

**Endpoint da API B3:**
```
GET https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/<base64>
```
Parâmetros (antes da codificação Base64):
```json
{"language":"pt-br","pageNumber":1,"pageSize":120,"index":"IBOV","segment":"1"}
```

## Campos capturados

| Campo              | Descrição                                   |
|--------------------|---------------------------------------------|
| data_captura       | Data da execução (YYYY-MM-DD)               |
| hora_captura       | Hora da execução (HH:MM:SS BRT)             |
| indice             | Código do índice (ex: IBOV, SMLL)           |
| indice_nome        | Nome completo do índice                     |
| codigo_ativo       | Ticker do ativo (ex: PETR4, HGLG11)         |
| nome_ativo         | Nome da empresa ou fundo                    |
| tipo_ativo         | Tipo do ativo (ON, PN, UNT, CI...)          |
| quantidade_teorica | Quantidade teórica na carteira              |
| participacao_pct   | Peso do ativo no índice (%)                 |
| reducao_capital    | Indicador de redução de capital             |
| segmento           | Segmento de listagem                        |

## Exemplo do CSV

```
data_captura,hora_captura,indice,indice_nome,codigo_ativo,nome_ativo,tipo_ativo,quantidade_teorica,participacao_pct,...
2026-05-30,09:30:01,IBOV,Ibovespa,PETR4,PETROBRAS,PN,529.660.608,6,854,...
2026-05-30,09:30:01,IBOV,Ibovespa,VALE3,VALE,ON,404.184.288,6,354,...
2026-05-30,09:30:01,SMLL,Small Cap,PETZ3,PET CENTER,ON,74.123.456,1,234,...
2026-05-30,09:30:01,IFIX,Índice de Fundos Imobiliários,HGLG11,CSHG LOG,CI,8.234.567,3,12,...
```

## Agendamento

Roda automaticamente **de segunda a sexta às 09h30 (BRT)** via GitHub Actions.
Pode ser disparado manualmente em *Actions → Captura Diária B3 Carteiras Teóricas → Run workflow*.

## Estrutura

```
.
├── .github/
│   └── workflows/
│       └── captura_diaria.yml      # Agendamento e pipeline
├── data/
│   └── b3_carteiras_teoricas.csv  # Histórico acumulativo (gerado automaticamente)
├── b3_carteiras.py                 # Script de captura
├── requirements.txt
└── README.md
```

## Adicionando novos índices

Para incluir outros índices, basta adicionar uma linha na lista `INDICES` em `b3_carteiras.py`:

```python
INDICES = [
    ("IBOV", "1", "Ibovespa"),
    ("MEUINDICE", "1", "Nome do Índice"),   # nova linha
    ...
]
```

## Rodando localmente

```bash
pip install -r requirements.txt
python b3_carteiras.py
```

## Coleção de pipelines B3/ANBIMA

| Repositório               | Fonte   | Dados                          |
|---------------------------|---------|--------------------------------|
| `anbima-indicadores`      | ANBIMA  | SELIC, IGP-M, IPCA, Câmbio     |
| `b3-fiis-listados`        | B3 API  | FIIs listados na bolsa         |
| `b3-etfs-listados`        | B3 API  | ETFs de RV e RF listados       |
| `b3-carteiras-teoricas`   | B3 API  | Composição dos índices B3      |
