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

## Status atual

- [x] **Questão 1 — EDA**
- [x] **Questão 2 — Schema PostgreSQL**
- [x] **Questão 3 — Carregamento**
- [ ] **Próximas questões — Pendentes**