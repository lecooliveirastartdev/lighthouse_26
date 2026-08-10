# Desafio Lighthouse — Dados & IA

## Questão 1 — EDA

### Parte 1 — Visão geral da tabela `orders`

A análise foi realizada diretamente sobre a tabela `orders`, sem aplicação
de limpeza ou tratamento dos dados, conforme as premissas da questão.

- Quantidade total de linhas: **48.998**
- Quantidade total de colunas: **13**
- Data mínima de `created_at`: **01/01/2020 01:19:28**
- Data máxima de `created_at`: **31/12/2026 23:43:09**

---

### Parte 2 — Análise da coluna `total`

Foram obtidos os seguintes valores:

- Valor mínimo: **R$ 32,62**
- Valor máximo: **R$ 127.262,02**
- Valor médio: **R$ 28.704,99**

A amplitude entre os valores observados indica a existência de valores
extremos que merecem investigação. Entretanto, valores elevados não devem
ser considerados erros automaticamente, pois podem representar pedidos
legítimos de maior valor.

---

### Parte 3 — Diagnóstico de qualidade

A tabela `orders` possui 48.998 registros e 13 colunas, abrangendo dados
entre 01/01/2020 e 31/12/2026.

Em relação à completude dos dados, a única coluna com valores nulos
identificada foi `salesperson_id`, com **24.131 ocorrências**. As demais
colunas não apresentaram valores ausentes nesta análise inicial.

A coluna `total` apresenta grande amplitude, variando de R$ 32,62 a
R$ 127.262,02, o que indica a necessidade de investigar possíveis valores
extremos antes de análises sensíveis a outliers. Esses valores, porém, não
podem ser classificados como erros apenas por sua magnitude.

Dessa forma, considero a tabela adequada para exploração inicial, mas não
completamente pronta para análises posteriores sem uma etapa prévia de
tratamento. Recomenda-se investigar os valores extremos de `total`,
compreender o significado dos valores nulos em `salesperson_id` e avaliar
o intervalo temporal antes da utilização dos dados em análises mais
avançadas ou modelos.