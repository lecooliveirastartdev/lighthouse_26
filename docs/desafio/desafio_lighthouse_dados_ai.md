# 🚢 Desafio Lighthouse — Dados & AI

**Candidato / Responsável:** Leco Oliveira  
**Projeto:** Lighthouse '26 (`lighthouse_26`)  
**Escopo:** Análise Exploratória, Diagnóstico e Pipeline de Dados  
**Data da Análise:** Agosto de 2026  

---

## 📌 1. Visão Geral

Este documento registra as análises, resultados, decisões técnicas e respostas
desenvolvidas durante o desafio de Dados & IA da LH Nautical.

O objetivo é manter a rastreabilidade do raciocínio utilizado ao longo do
desafio, desde a análise dos dados brutos até as etapas posteriores de
tratamento, análise e modelagem.

### Diretrizes adotadas no projeto

1. **Preservação dos dados brutos:** os arquivos originais não são alterados.
2. **Rastreabilidade:** transformações são realizadas por scripts versionados.
3. **Separação de responsabilidades:** exploração, transformação e demais
   etapas possuem módulos próprios.
4. **Decisões baseadas em evidências:** hipóteses de negócio são diferenciadas
   de conclusões efetivamente sustentadas pelos dados.

---

# 📊 Questão 1 — EDA

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

# 🗺️ Status do Desafio

- [x] **Questão 1:** EDA da tabela `orders`
- [x] **Profiling inicial**
- [x] **Diagnóstico estatístico complementar**
- [x] **Construção inicial da camada `processed`**
- [ ] **Questão 2:** Aguardando análise
- [ ] **Demais questões:** Pendentes

---

# 📝 Observações Técnicas

As análises complementares realizadas durante o desenvolvimento podem
ultrapassar o mínimo solicitado por determinadas questões.

Quando isso ocorrer, os resultados adicionais serão utilizados como apoio ao
raciocínio, mantendo separadas:

- as informações explicitamente solicitadas pelo desafio;
- as análises exploratórias complementares;
- as hipóteses de negócio;
- e as conclusões efetivamente sustentadas pelos dados.