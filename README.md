# SalesInsight PY

Projeto avaliativo de **Análise de Dados de Vendas com Python**, desenvolvido de acordo com o escopo reduzido do Módulo 01 — Semanas 01 a 05.

## Objetivo

Carregar, inspecionar, limpar, transformar e agregar um dataset de vendas, produzindo métricas por período, produto, categoria e região, além de segmentar clientes por nível de gasto.

## Funcionalidades

- Geração automática de `vendas.csv` com 200 registros;
- Inspeção de registros, colunas e valores ausentes;
- Limpeza de espaços, datas inválidas, valores ausentes e ruído textual;
- Uso de `datetime` e expressões regulares (`re`);
- Criação de `receita_total`, `mes`, `mes_nome`, `trimestre`, `ano` e `faixa_receita_item`;
- Métricas por mês, produto, categoria e região;
- Top 5 produtos por receita;
- Ticket médio por região;
- Segmentação de clientes em Bronze, Prata e Ouro;
- Contagem de vendas com receita acima da média;
- Função de ordem superior que recebe outra função como argumento;
- Dois usos de `lambda`;
- Exportação para CSV e JSON;
- Leitura do JSON de volta para conferência.

## Como executar

### Google Colab

1. Faça upload de `salesinsight.py`.
2. Execute:

```bash
!python salesinsight.py
```

O programa gera `vendas.csv` automaticamente caso o arquivo não exista.

### VS Code / terminal

Requer Python 3.10+.

```bash
python salesinsight.py
```

Não são necessárias bibliotecas externas. O projeto usa apenas a biblioteca padrão do Python.

## Estrutura

```text
salesinsight-py/
├── salesinsight.py
├── vendas.csv
├── README.md
├── planejamento/
│   └── tarefas-kanban.md
└── outputs/
    ├── metricas_por_mes.csv
    ├── segmentacao_clientes.csv
    └── estatisticas_gerais.json
```

## Conceitos aplicados

- Variáveis e tipos de dados;
- Operadores aritméticos, relacionais e lógicos;
- `if`, `elif`, `else`;
- `for`;
- listas e dicionários;
- funções com parâmetros, retorno e docstrings;
- `lambda`;
- função de ordem superior;
- CSV e JSON;
- `datetime`;
- expressões regulares;
- Git e GitHub.

## Decisão técnica

Registros com data inválida ou com valores ausentes nos campos críticos são removidos porque não permitem calcular a receita da venda com segurança. O projeto não utiliza imputação estatística nem tratamento de outliers, pois esses conteúdos não fazem parte do escopo obrigatório desta versão.

## Versionamento sugerido

Branches:

- `main`
- `develop`
- `feat/pipeline-dados`
- `docs/readme`

Commits sugeridos:

1. `feat: cria estrutura inicial do projeto e salesinsight.py`
2. `feat: adiciona geracao e leitura do dataset de vendas`
3. `feat: implementa limpeza de dados com datetime e regex`
4. `feat: adiciona colunas derivadas e transformacoes condicionais`
5. `feat: implementa metricas e segmentacao de clientes`
6. `feat: implementa exportacao de resultados em csv e json`
7. `docs: atualiza readme com instrucoes e conceitos`

## Status do projeto

Projeto acadêmico desenvolvido para análise de dados de vendas utilizando Python e recursos da biblioteca padrão.

