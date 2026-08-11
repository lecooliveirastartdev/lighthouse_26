# 🚢 Desafio Lighthouse — Dados & AI

**Candidato / Responsável:** Leco Oliveira  
**Projeto:** Lighthouse '26 (`lighthouse_26`)  
**Escopo:** Análise Exploratória, Engenharia e Pipeline de Dados  
**Data da Análise:** Agosto de 2026

---

## 📌 1. Visão Geral

Este documento registra as análises, resultados, decisões técnicas e respostas
desenvolvidas durante o desafio de Dados & IA da LH Nautical.

O objetivo é manter a rastreabilidade do raciocínio utilizado ao longo do
desafio, desde a análise dos dados brutos até as etapas posteriores de
tratamento, estruturação, análise e modelagem.

### Diretrizes adotadas no projeto

1. **Preservação dos dados brutos:** os arquivos originais não são alterados.
2. **Rastreabilidade:** transformações são realizadas por scripts versionados.
3. **Separação de responsabilidades:** exploração, transformação, geração de
   schema e demais etapas possuem módulos próprios.
4. **Decisões baseadas em evidências:** hipóteses de negócio são diferenciadas
   de conclusões efetivamente sustentadas pelos dados.
5. **Reprodutibilidade:** as soluções devem poder ser executadas novamente
   sem depender de configurações específicas da máquina de desenvolvimento.

---

# 📊 Questão 1 — EDA

**Status: Concluída ✅**

## Cenário

A primeira etapa consiste em avaliar a tabela `orders` em seu estado bruto,
sem realizar limpeza ou tratamento.

O objetivo é compreender seu volume, distribuição e qualidade inicial para
avaliar se os dados podem ser utilizados com segurança em análises futuras.

---

## 1.1 Visão geral da tabela `orders`

A análise foi realizada diretamente sobre o arquivo bruto `orders.csv`.

- **Quantidade total de linhas:** `48.998`
- **Quantidade total de colunas:** `13`
- **Data mínima de `created_at`:** `01/01/2020 01:19:28`
- **Data máxima de `created_at`:** `31/12/2026 23:43:09`

Portanto, os registros disponíveis abrangem o período de 2020 a 2026.

---

## 1.2 Análise da coluna `total`

Os valores encontrados foram:

- **Valor mínimo:** `R$ 32,62`
- **Valor máximo:** `R$ 127.262,02`
- **Valor médio:** `R$ 28.704,99`

Como análise exploratória complementar, também foram calculados:

- **Mediana (Q2):** `R$ 25.917,84`
- **Potenciais outliers pelo critério do IQR:** `452 pedidos`
- **Percentual aproximado de potenciais outliers:** `0,92%`
- **Limite superior pelo critério de 1,5 × IQR:** `R$ 82.597,85`

A diferença entre média, mediana e valor máximo indica uma distribuição com
valores elevados que merecem investigação.

Entretanto, esses registros devem ser tratados como **potenciais outliers**,
e não automaticamente como erros, pois podem representar pedidos legítimos
de maior valor.

---

## 1.3 Qualidade dos dados

A verificação inicial de valores ausentes identificou:

- `salesperson_id`: **24.131 valores nulos**
- Demais colunas: **nenhum valor nulo identificado**

A presença de valores nulos em `salesperson_id` merece investigação do ponto
de vista de negócio.

Nesta etapa, não se assume que esses valores representem erro ou um canal
específico de venda, pois essa conclusão exige evidências adicionais.

---

## 1.4 Diagnóstico

A tabela `orders` apresenta boa completude geral, uma vez que 12 das 13
colunas não possuem valores ausentes na verificação inicial.

A coluna `salesperson_id`, entretanto, possui 24.131 valores nulos e deve ser
investigada antes de qualquer decisão de preenchimento, remoção ou
interpretação desses registros.

A coluna `total` apresenta grande amplitude, variando entre R$ 32,62 e
R$ 127.262,02. A análise complementar pelo método do IQR identificou 452
registros como potenciais outliers. Esses valores devem ser investigados,
mas não considerados erros somente por apresentarem magnitude elevada.

Dessa forma, considero a tabela adequada para exploração inicial, porém não
completamente pronta para análises posteriores sem uma etapa prévia de
avaliação e tratamento dos pontos identificados.

### Arquivo da solução

- `sql/questao_01_eda.sql`

---

# ⚙️ Camada de Processamento — `data/processed/`

Após a exploração dos dados brutos, foi construída uma camada separada para
os dados processados.

O objetivo dessa camada é preservar os arquivos originais e permitir que as
transformações realizadas sejam reproduzidas por código.

## Segregação temporal

Foi utilizada uma referência temporal de **10/08/2026** para distinguir
registros históricos de registros posteriores à data de referência.

Resultado:

- **Pedidos históricos:** `44.668` registros (`91,16%`)
- **Pedidos posteriores à referência:** `4.330` registros (`8,84%`)
- **Total:** `48.998` registros

Foi criada a flag:

`is_future_order`

para preservar essa informação no conjunto processado.

> A data de referência utilizada no processamento é uma decisão técnica do
> projeto e não uma característica original da tabela `orders`.

---

## Tratamento técnico de `salesperson_id`

Para preservar a informação original e, ao mesmo tempo, permitir o uso
posterior da variável, foram criados novos atributos:

- `salesperson_id_clean`
- `has_salesperson`

Na coluna `salesperson_id_clean`, valores ausentes são representados
tecnicamente por `-1`.

A coluna original `salesperson_id` permanece disponível, permitindo manter a
rastreabilidade dos dados.

A flag `has_salesperson` registra se o pedido possui ou não um vendedor
associado.

Essa transformação não pressupõe, por si só, que a ausência de vendedor
represente e-commerce ou autoatendimento. Essa interpretação depende de
validação com outras informações do negócio.

---

## Formatos de saída

Os dados processados foram disponibilizados em:

- CSV
- Parquet

A separação entre dados brutos e processados permite preservar a fonte
original e reproduzir as transformações realizadas pelo pipeline.

---

# 🗄️ Questão 2 — Schema PostgreSQL

**Status: Concluída ✅**

## Cenário

Como o ERP não permite conexão direta com seu banco de dados, os arquivos
CSV fornecidos são considerados as fontes disponíveis para construção da
estrutura do banco de destino.

O objetivo da questão foi desenvolver um script em Python 3 capaz de
identificar automaticamente as colunas presentes nos CSVs e gerar um único
arquivo `schema.sql` contendo as instruções de criação das tabelas para
PostgreSQL.

A solução foi desenvolvida utilizando somente bibliotecas padrão do Python 3,
conforme exigido pelo desafio.

---

## 2.1 Detecção dos arquivos e colunas

O script identifica automaticamente todos os arquivos `.csv` existentes no
diretório informado.

Resultado:

- **Arquivos CSV encontrados:** `24`
- **Tabelas identificadas:** `24`

O cabeçalho de cada CSV é utilizado para determinar o nome das colunas de
cada tabela.

---

## 2.2 Inferência dos tipos PostgreSQL

Os valores presentes nas colunas são analisados para determinar tipos
compatíveis com PostgreSQL.

Entre os tipos utilizados estão:

- `BIGINT`
- `NUMERIC`
- `BOOLEAN`
- `DATE`
- `TIMESTAMP`
- `TEXT`

Valores vazios são ignorados durante a análise para que não determinem
incorretamente o tipo da coluna.

Quando uma coluna não possui valores suficientes para inferência, `TEXT` é
utilizado como fallback seguro.

---

## 2.3 Tratamento de identificadores

Durante a validação foi identificado que alguns campos podem possuir somente
dígitos sem representarem valores destinados a operações matemáticas.

Entre os exemplos estão:

- CPF
- `tax_id`
- telefone
- CEP
- código de barras (`barcode_ean`)
- chave de NF-e (`nfe_access_key`)
- código NCM (`ncm_code`)
- inscrição estadual

Esses campos são tratados como `TEXT`, evitando perda de zeros à esquerda ou
interpretação inadequada como valores numéricos.

---

## 2.4 Coluna `reorder_point`

Durante a validação da tabela `stock_levels`, foi identificado que a coluna
`reorder_point` não possui valores preenchidos.

Resultado da verificação:

- **Total de registros:** `6.054`
- **Valores vazios:** `6.054`
- **Valores preenchidos:** `0`

Como não existem valores disponíveis para determinar seu tipo, a solução
utiliza `TEXT` como fallback.

Essa decisão evita assumir um tipo sem evidência disponível nos dados.

---

## 2.5 Geração do `schema.sql`

Após a inferência das colunas e seus respectivos tipos, o script gera
automaticamente uma instrução `CREATE TABLE` para cada arquivo CSV.

Todas as instruções são reunidas em um único arquivo:

`sql/schema.sql`

Resultado:

- **Arquivos CSV processados:** `24`
- **Instruções `CREATE TABLE` geradas:** `24`

---

## 2.6 Portabilidade e validação

Inicialmente, o script utilizava um caminho específico da máquina de
desenvolvimento para localizar os CSVs.

Antes da entrega, essa dependência foi removida.

A versão final recebe o diretório contendo os arquivos CSV como argumento,
permitindo sua execução em diferentes ambientes.

Exemplo:

```bash
python3 generate_schema.py ./csvs schema.sql
```

---

# 🗄️ Questão 3 — Carregamento

**Status: Concluída ✅**

## Objetivo

Após a criação do schema PostgreSQL, foi desenvolvido um processo para
carregar todos os arquivos CSV brutos nas respectivas tabelas do banco de
dados.

A implementação respeita as premissas da questão, mantendo os dados brutos
sem remoção de nulos ou correção de caracteres especiais.

---

## Implementação

Foi desenvolvido o script:

`src/load/load_csvs.py`

O script:

- identifica automaticamente todos os arquivos CSV de um diretório;
- utiliza o nome de cada arquivo para identificar a tabela correspondente;
- utiliza o cabeçalho do CSV para identificar as colunas;
- conecta ao PostgreSQL utilizando a biblioteca `psycopg`;
- insere os registros nas tabelas criadas anteriormente;
- representa campos vazios como `NULL` no PostgreSQL;
- recebe as configurações de conexão em tempo de execução.

O diretório dos CSVs, host, porta, banco de dados, usuário e senha são
informados por argumentos, evitando dependência dos caminhos e configurações
da máquina utilizada no desenvolvimento.

---

## Resultado do carregamento

A versão final foi executada em um banco PostgreSQL separado para validação:

`lh_nautical_teste`

Resultados:

- **Arquivos CSV processados:** `24`
- **Tabelas carregadas:** `24`
- **Total de registros carregados:** `433.424`
- **Registros em `orders`:** `48.998`
- **Registros em `order_items`:** `147.320`
- **Registros em `stock_movements`:** `115.312`

---

## Validação

A carga foi validada diretamente no PostgreSQL.

A conferência final apresentou:

- **Total de tabelas:** `24`
- **Total de registros:** `433.424`
- **`orders`:** `48.998`
- **`order_items`:** `147.320`
- **`stock_movements`:** `115.312`

Também foi realizada uma comparação entre as quantidades existentes nos
arquivos CSV e as quantidades carregadas no PostgreSQL, com resultado de
`24/24` tabelas correspondentes.

Dessa forma, a carga foi considerada reproduzível e consistente com os
arquivos de origem.