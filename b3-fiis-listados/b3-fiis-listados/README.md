# 📊 B3 FIIs Listados — Captura Automatizada

Captura diária da lista completa de Fundos de Investimento Imobiliário (FIIs)
listados na B3, usando a mesma API interna que alimenta o botão
**"Exportar lista completa de fundos"** da página oficial:
https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/fundos-de-investimentos/fii/fiis-listados/

## Como funciona

A B3 expõe uma API REST em `sistemaswebb3-listados.b3.com.br` com parâmetros
codificados em Base64. O script decodifica a paginação automaticamente,
percorre todas as páginas e consolida o resultado em CSV.

**Endpoint utilizado:**
```
GET https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/GetListedFundsSupplement/<base64>
```
Parâmetros (antes da codificação):
```json
{"language":"pt-br","pageNumber":1,"pageSize":100,"fundsType":"FII"}
```

## Campos capturados

| Campo              | Descrição                          |
|--------------------|------------------------------------|
| data_captura       | Data da execução (YYYY-MM-DD)      |
| hora_captura       | Hora da execução (HH:MM:SS BRT)    |
| codigo_fundo       | Ticker do FII (ex: HGLG11)         |
| nome_fundo         | Nome completo do fundo             |
| cnpj               | CNPJ do fundo                      |
| administrador      | Instituição administradora         |
| segmento           | Segmento de atuação                |
| tipo               | Tipo do fundo                      |
| mandato            | Mandato do fundo                   |
| prazo_duracao      | Prazo de duração                   |
| gestao             | Tipo de gestão (ativa/passiva)     |
| data_encerramento  | Data de encerramento (se aplicável)|
| cotistas           | Número de cotistas                 |
| patrimonio_liquido | Patrimônio líquido                 |

## Agendamento

Roda automaticamente **de segunda a sexta às 09h30 (BRT)** via GitHub Actions.
Pode ser disparado manualmente em *Actions → Captura Diária B3 FIIs → Run workflow*.

## Estrutura

```
.
├── .github/
│   └── workflows/
│       └── captura_diaria.yml   # Agendamento e pipeline
├── data/
│   └── b3_fiis_listados.csv     # Histórico acumulativo (gerado automaticamente)
├── b3_fiis.py                   # Script de captura
├── requirements.txt
└── README.md
```

## Rodando localmente

```bash
pip install -r requirements.txt
python b3_fiis.py
```

## Relação com outros projetos

Este projeto segue o mesmo padrão do repositório `anbima-indicadores`,
formando uma coleção de pipelines de dados financeiros brasileiros com
GitHub Actions. Para criar um novo coletor, basta duplicar a estrutura
e trocar apenas o script de captura.
