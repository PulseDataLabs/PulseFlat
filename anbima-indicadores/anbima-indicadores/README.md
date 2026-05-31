# 📊 ANBIMA Indicadores — Captura Automatizada

Captura diária dos indicadores financeiros da ANBIMA via GitHub Actions,
salvando o histórico em CSV versionado no próprio repositório.

## Indicadores capturados

| Categoria         | Indicadores                                      |
|-------------------|--------------------------------------------------|
| Taxa de Juros     | Estimativa SELIC, Taxa SELIC (BC), DI-B3         |
| Índices de Preços | IGP-M (número índice, var. mês, projeção), IPCA  |
| Câmbio            | Dólar Comercial (compra/venda), Euro (compra/venda) |
| Taxa de Referência| TR, TBF                                          |
| FDS               | Valor da cota (2 últimos dias)                   |

## Agendamento

Roda automaticamente **de segunda a sexta às 09h30 (BRT)** via GitHub Actions.
Pode ser disparado manualmente em *Actions → Captura Diária ANBIMA → Run workflow*.

## Estrutura

```
.
├── .github/
│   └── workflows/
│       └── captura_diaria.yml   # Agendamento e pipeline
├── data/
│   └── indicadores_anbima.csv   # Histórico acumulativo (gerado automaticamente)
├── anbima_indicadores.py        # Script de captura
├── requirements.txt
└── README.md
```

## Formato do CSV

```
data_captura,hora_captura,data_referencia_pagina,indicador,categoria,valor,unidade
2026-05-30,09:30:01,02/03/2026 16:12,Taxa SELIC (BC),Taxa de Juros,14.90,% a.a.
2026-05-30,09:30:01,02/03/2026 16:12,Dólar Comercial Compra,Câmbio,5.1995,R$
```

## Como usar em outros projetos

Este repositório serve como **template**. Para adaptar:

1. Substitua `anbima_indicadores.py` pelo script de captura do novo fonte
2. Ajuste o horário no `captura_diaria.yml` se necessário
3. O restante (commit automático, versionamento do CSV) funciona sem alteração

## Rodando localmente

```bash
pip install -r requirements.txt
python anbima_indicadores.py
```
