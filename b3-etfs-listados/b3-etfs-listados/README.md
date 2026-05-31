# 📊 B3 ETFs Listados — Captura Automatizada

Captura diária da lista completa de ETFs listados na B3, usando a mesma API
interna que alimenta o botão **"Exportar lista completa de fundos"** das páginas oficiais:

- **Renda Variável:** https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/etf/renda-variavel/etfs-listados/
- **Renda Fixa:** https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-fixa/etf-de-renda-fixa.htm

## Categorias capturadas

A B3 divide os ETFs em dois grupos, ambos capturados e consolidados em um único CSV:

| `categoria_etf`      | `fundsType` | Descrição                              |
|----------------------|-------------|----------------------------------------|
| ETF Renda Variável   | `ETF`       | Réplica de índices de ações            |
| ETF Renda Fixa       | `ETF-RF`    | Réplica de índices de títulos públicos |

## Como funciona

Mesmo padrão da API usada no projeto `b3-fiis-listados`:

**Endpoint:**
```
GET https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/GetListedFundsSupplement/<base64>
```
Parâmetros (antes da codificação Base64):
```json
{"language":"pt-br","pageNumber":1,"pageSize":100,"fundsType":"ETF"}
{"language":"pt-br","pageNumber":1,"pageSize":100,"fundsType":"ETF-RF"}
```

## Campos capturados

| Campo               | Descrição                              |
|---------------------|----------------------------------------|
| data_captura        | Data da execução (YYYY-MM-DD)          |
| hora_captura        | Hora da execução (HH:MM:SS BRT)        |
| categoria_etf       | ETF Renda Variável ou ETF Renda Fixa   |
| codigo_fundo        | Ticker do ETF (ex: BOVA11, IMAB11)     |
| nome_fundo          | Nome completo do fundo                 |
| cnpj                | CNPJ do fundo                          |
| administrador       | Instituição administradora             |
| gestor              | Gestora do fundo                       |
| indice_referencia   | Índice replicado pelo ETF              |
| segmento            | Segmento de atuação                    |
| tipo                | Tipo do fundo                          |
| prazo_duracao       | Prazo de duração                       |
| data_encerramento   | Data de encerramento (se aplicável)    |
| cotistas            | Número de cotistas                     |
| patrimonio_liquido  | Patrimônio líquido                     |

## Agendamento

Roda automaticamente **de segunda a sexta às 09h30 (BRT)** via GitHub Actions.
Pode ser disparado manualmente em *Actions → Captura Diária B3 ETFs → Run workflow*.

## Estrutura

```
.
├── .github/
│   └── workflows/
│       └── captura_diaria.yml   # Agendamento e pipeline
├── data/
│   └── b3_etfs_listados.csv     # Histórico acumulativo (gerado automaticamente)
├── b3_etfs.py                   # Script de captura
├── requirements.txt
└── README.md
```

## Rodando localmente

```bash
pip install -r requirements.txt
python b3_etfs.py
```

## Relação com outros projetos

Faz parte de uma coleção de pipelines de dados financeiros brasileiros com GitHub Actions:

| Repositório           | Fonte   | Dados                        |
|-----------------------|---------|------------------------------|
| `anbima-indicadores`  | ANBIMA  | SELIC, IGP-M, IPCA, Câmbio   |
| `b3-fiis-listados`    | B3 API  | FIIs listados na bolsa       |
| `b3-etfs-listados`    | B3 API  | ETFs de RV e RF listados     |
