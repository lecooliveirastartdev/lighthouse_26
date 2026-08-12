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

---

## Questão 2 — Schema PostgreSQL

### Objetivo

Como os dados do ERP são disponibilizados exclusivamente por meio de
arquivos CSV, foi necessário construir automaticamente o schema do banco
PostgreSQL que será utilizado nas etapas posteriores.

Foi desenvolvido um script em Python 3 capaz de percorrer todos os arquivos
CSV de um diretório, identificar suas colunas, analisar os valores existentes
e gerar um único arquivo `schema.sql` contendo as instruções `CREATE TABLE`.

A solução utiliza somente bibliotecas padrão do Python 3, conforme exigido
pela questão.

---

### Geração do schema

Foram processados:

- Arquivos CSV encontrados: **24**
- Tabelas identificadas: **24**
- Instruções `CREATE TABLE` geradas: **24**

O script realiza inferência dos tipos necessários para o PostgreSQL,
utilizando tipos como:

- `BIGINT`
- `NUMERIC`
- `BOOLEAN`
- `DATE`
- `TIMESTAMP`
- `TEXT`

Campos que representam identificadores, mesmo quando compostos apenas por
dígitos, são preservados como `TEXT` quando necessário para evitar perda de
informações, como zeros à esquerda.

Quando não existem valores suficientes para determinar o tipo de uma coluna,
é utilizado `TEXT` como fallback seguro.

---

### Portabilidade

A versão final do script não depende de caminhos específicos da máquina onde
foi desenvolvida.

O diretório contendo os CSVs e o nome do arquivo de saída podem ser
informados durante a execução.

Exemplo:

```bash
python3 generate_schema.py ./csvs schema.sql
```

---

### Arquivos da entrega

- `generate_schema.py` — código Python responsável pela geração do schema.
- `schema.sql` — arquivo produzido pelo código contendo as instruções de
  criação das 24 tabelas.

A solução foi testada de forma independente e o arquivo `schema.sql` final
foi validado contendo **24 instruções `CREATE TABLE`**.

---

## Questão 3 — Carregamento dos CSVs no PostgreSQL

### Objetivo

Após a geração do schema, foi desenvolvido um script em Python 3 para
realizar o carregamento dos arquivos CSV brutos nas respectivas tabelas do
PostgreSQL.

O carregamento foi realizado respeitando as premissas da questão, sem
remoção de valores nulos ou correção de caracteres especiais.

---

### Implementação

Foi desenvolvido o arquivo:

`load_csvs.py`

O script:

- identifica automaticamente todos os arquivos CSV do diretório informado;
- utiliza o nome de cada arquivo para identificar a tabela correspondente;
- utiliza o cabeçalho dos CSVs para determinar as colunas;
- conecta ao PostgreSQL utilizando a biblioteca `psycopg`;
- insere os registros nas tabelas criadas na Questão 2;
- representa campos vazios como `NULL` no PostgreSQL;
- preserva os demais valores provenientes dos arquivos CSV;
- informa a quantidade de registros inseridos em cada tabela.

---

### Portabilidade

A versão final não possui caminho dos CSVs, banco de dados, usuário ou senha
fixos no código.

As informações necessárias são fornecidas durante a execução:

```bash
python load_csvs.py \
    <diretorio_dos_csvs> \
    <host> \
    <porta> \
    <banco> \
    <usuario> \
    <senha>
```

Isso permite que o avaliador utilize suas próprias configurações de
PostgreSQL sem depender do ambiente utilizado no desenvolvimento.

---

### Resultado do carregamento

A versão final foi testada em um banco PostgreSQL separado:

`lh_nautical_teste`

Foram obtidos os seguintes resultados:

- Arquivos CSV processados: **24**
- Tabelas carregadas: **24**
- Total de registros carregados: **433.424**
- Registros em `orders`: **48.998**
- Registros em `order_items`: **147.320**
- Registros em `stock_movements`: **115.312**

---

### Validação

Foi realizada uma comparação entre a quantidade de registros existente nos
arquivos CSV e a quantidade armazenada nas respectivas tabelas PostgreSQL.

Resultado:

- Tabelas validadas: **24/24**
- Total de registros nos CSVs: **433.424**
- Total de registros no PostgreSQL: **433.424**
- Resultado da validação: **OK**

Como validação adicional, a versão final e portátil foi executada em um banco
separado e limpo, denominado `lh_nautical_teste`.

A consulta direta ao PostgreSQL confirmou:

- `orders`: **48.998 registros**
- `order_items`: **147.320 registros**
- `stock_movements`: **115.312 registros**
- Total de tabelas: **24**
- Total de registros: **433.424**

Dessa forma, o carregamento foi considerado consistente com os arquivos de
origem e reproduzível em um ambiente PostgreSQL independente.

---

### Arquivo da entrega

- `load_csvs.py` — código Python responsável pelo carregamento dos CSVs no
  PostgreSQL.

### Evidência complementar

- `questao_03_validacao_carga.png` — validação final realizada diretamente
  no banco PostgreSQL de teste.

---

## Questão 4 — Análise de clientes

### Objetivo

A análise teve como objetivo identificar os clientes considerados fiéis ou
de elite, considerando não apenas o volume total de compras, mas também o
Ticket Médio e a diversidade de categorias consumidas.

Conforme as premissas da questão, foram considerados no ranking apenas
clientes que compraram produtos de **13 ou mais categorias distintas**.

---

### Métricas utilizadas

Para cada `customer_id`, foram calculadas as seguintes métricas:

- **Faturamento Total:** soma de `orders.total`;
- **Frequência:** quantidade total de transações do cliente;
- **Ticket Médio:** Faturamento Total / Frequência;
- **Diversidade de Categorias:** quantidade de `category_id` distintos
  presentes nas compras do cliente.

Para evitar duplicação do faturamento provocada pelo relacionamento entre
`orders` e `order_items`, as métricas financeiras e a diversidade de
categorias foram calculadas separadamente e posteriormente relacionadas.

---

### Relacionamentos utilizados

A análise utilizou o seguinte caminho entre as tabelas:

```text
customers.id
    ↓
orders.customer_id

orders.id
    ↓
order_items.order_id

order_items.product_variant_id
    ↓
product_variants.id

product_variants.product_id
    ↓
products.id

products.category_id
    ↓
categories.id
```

---

### Filtro de clientes de elite

Após o cálculo das métricas, foram mantidos apenas os clientes com:

**Diversidade de Categorias >= 13**

Em seguida, os clientes foram ordenados pelo Ticket Médio em ordem
decrescente.

Conforme exigido pela questão, em caso de empate no Ticket Médio,
`customer_id` é utilizado em ordem crescente como critério de desempate.

---

### Top 10 clientes por Ticket Médio

O ranking obtido foi:

| Posição | customer_id | Faturamento Total | Frequência | Ticket Médio | Diversidade |
|---:|---:|---:|---:|---:|---:|
| 1 | 22 | R$ 1.087.838,44 | 26 | R$ 41.839,94 | 14 |
| 2 | 1477 | R$ 916.262,58 | 22 | R$ 41.648,30 | 14 |
| 3 | 929 | R$ 1.082.775,89 | 26 | R$ 41.645,23 | 14 |
| 4 | 1116 | R$ 655.737,20 | 16 | R$ 40.983,58 | 14 |
| 5 | 1691 | R$ 815.471,30 | 20 | R$ 40.773,57 | 14 |
| 6 | 774 | R$ 726.127,99 | 18 | R$ 40.340,44 | 14 |
| 7 | 1470 | R$ 1.040.553,09 | 26 | R$ 40.021,27 | 14 |
| 8 | 1599 | R$ 997.616,46 | 25 | R$ 39.904,66 | 14 |
| 9 | 965 | R$ 677.297,78 | 17 | R$ 39.841,05 | 14 |
| 10 | 1722 | R$ 1.146.455,22 | 29 | R$ 39.532,94 | 14 |

O cliente com maior Ticket Médio foi o `customer_id = 22`, com
**R$ 41.839,94** por transação.

---

### Categoria mais consumida pelo Top 10

Após identificar os 10 clientes com maior Ticket Médio, suas compras foram
relacionadas aos itens, produtos e categorias.

Foi calculada a soma de `order_items.quantity` para cada categoria,
considerando somente as compras realizadas pelos 10 clientes selecionados.

O resultado foi:

- `category_id`: **8**
- Categoria: **Hélices**
- Quantidade total de itens: **492**

Portanto, **Hélices** foi a categoria que concentrou a maior quantidade
total de itens comprados pelo grupo dos 10 clientes de elite.

---

### Implementação

Foram utilizados dois arquivos SQL:

- `questao_04_clientes.sql` — consulta principal responsável pelo cálculo
  das métricas, aplicação do filtro de elite, seleção do Top 10 e
  identificação da categoria com maior quantidade de itens;
- `questao_04_top10_validacao.sql` — consulta auxiliar utilizada para
  visualizar e validar os 10 clientes selecionados.

---

### Validação

A consulta auxiliar confirmou os **10 clientes** selecionados, seus
respectivos valores de faturamento, frequência, Ticket Médio e diversidade.

Todos os clientes do Top 10 apresentaram **14 categorias distintas**,
atendendo ao requisito mínimo de 13 categorias.

A consulta principal retornou:

```text
 category_id | categoria | quantidade_total_itens
-------------+-----------+------------------------
           8 | Hélices   |                    492
```

O resultado confirma que a categoria **Hélices** foi a mais consumida em
quantidade total de itens pelo grupo selecionado.

---

### Teste de portabilidade

Também foi realizado um teste para verificar se o arquivo SQL dependia de
sua localização dentro do projeto.

Uma cópia de `questao_04_clientes.sql` foi executada a partir de um
diretório temporário externo à estrutura original do projeto.

A execução retornou novamente:

```text
 category_id | categoria | quantidade_total_itens
-------------+-----------+------------------------
           8 | Hélices   |                    492
```

O teste confirmou que a consulta não depende de caminhos específicos da
máquina onde foi desenvolvida.

Para sua execução em outro ambiente, é necessário apenas que o PostgreSQL
de destino contenha o schema e os dados correspondentes às etapas
anteriores do desafio.

---

### Evidências complementares

- `questao_04_top10_clientes.png` — resultado do ranking dos 10 clientes de
  elite;
- `questao_04_resultado_categoria.png` — resultado final da categoria com
  maior quantidade total de itens.

---

## Status atual

- [x] **Questão 1 — EDA**
- [x] **Questão 2 — Schema PostgreSQL**
- [x] **Questão 3 — Carregamento**
- [x] **Questão 4 — Análise de clientes**
- [ ] **Próximas questões — Pendentes**