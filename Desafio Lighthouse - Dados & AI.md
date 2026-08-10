# 🚢 Desafio Lighthouse — Dados & AI

**Candidato / Responsável:** Leco Oliveira  
**Projeto:** Lighthouse '26 (`lighthouse_26`)  
**Escopo da Análise:** Análise Exploratória, Diagnóstico e Distribuição da Tabela `orders`  
**Data da Análise:** Agosto de 2026  

---

## 📌 1. Visão Geral & Diretrizes do Desafio

Este documento reúne os resultados, métricas e análises técnicas extraídas do banco de dados relacional do ERP da **LH Nautical**. O objetivo desta fase é fornecer ao **Sr. Almir** uma visão clara sobre a integridade, distribuição e confiabilidade dos dados de vendas.

### Premissas Obrigatórias (Escopo Fechado)
1. **Tabela Exclusiva:** Utilizar **apenas** a tabela `orders`.
2. **Sem Tratamento Precoce:** Não realizar limpeza, remoção de nulos, imputação ou transformações de tipos nos dados brutos nesta fase.
3. **Abordagem Observacional:** Limitar a fase inicial à carga, agregação direta (`min`, `max`, `mean`, `median`, `IQR`) e diagnóstico do estado original dos dados.

---

## 📊 2. Visão Geral & Estatística Descritiva da Tabela `orders`

### 2.1 Metadados e Volume
| Métrica / Atributo | Valor Observado | Observação Técnica |
| :--- | :---: | :--- |
| **Total de Linhas (Registros)** | `48.998` | Volume expressivo de pedidos cadastrados no sistema. |
| **Total de Colunas** | `13` | Inclui IDs, status, canal, valores financeiros e timestamps. |
| **Data Mínima (`created_at`)** | `2020-01-01 01:19:28` | Início do histórico registrado. |
| **Data Máxima (`created_at`)** | `2026-12-31 23:43:09` | Contém lançamentos cobrindo todo o ano corrente. |

### 2.2 Análise Financeira e Dispersão (`total`)
* **Valor Mínimo por Pedido:** `R$ 32,62`
* **Primeiro Quartil (Q1 - 25%):** `R$ 13.171,24`
* **Mediana (Q2 - Pedido Central):** `R$ 25.917,84`
* **Valor Médio por Pedido:** `R$ 28.704,99`
* **Terceiro Quartil (Q3 - 75%):** `R$ 40.941,88`
* **Intervalo Interquartil (IQR):** `R$ 27.770,65`
* **Desvio Padrão:** `R$ 19.425,64`
* **Valor Máximo por Pedido:** `R$ 127.262,02`
* **Outliers Identificados (IQR > 1.5):** `452 pedidos` (`0,92%` do total de vendas, acima de `R$ 82.597,85`).

---

## 🛍️ 3. Análise de Canais e Atribuição de Vendedores

A investigação sobre os canais de venda (`channel`) e a presença de valores nulos em `salesperson_id` revelou a dinâmica operacional do negócio:

| Canal (`channel`) | Volume de Pedidos | % do Total | Com Vendedor (%) | Sem Vendedor / Nulo (%) |
| :--- | :---: | :---: | :---: | :---: |
| **`ecommerce`** | 34.342 | 70,09% | 29,73% | 70,27% |
| **`pos` (Ponto de Venda)** | 14.656 | 29,91% | 100,00% | 0,00% |

> **Achado de Negócio:** Os registros nulos de `salesperson_id` não representam falha de sistema, mas sim a natureza das compras autoatendidas no canal digital (`ecommerce`). No canal presencial (`pos`), $100\%$ das vendas possuem identificação do vendedor.

---

## 🩺 4. Diagnóstico de Confiabilidade (Parecer Executivo)

### ❓ Pergunta do Sr. Almir:
> *"Com base nestes dados, os números refletem com 100% de confiabilidade a realidade financeira da operação para tomada de decisão?"*

### ❌ Resposta do Diagnóstico:
**Não. Os dados brutos NÃO devem ser utilizados de forma isolada sem as devidas contextualizações de canal e filtros de integridade temporal.**

### 🔎 Síntese das Vulnerabilidades e Oportunidades Identificadas:

1. **Assimetria e Distorção da Média:**
   * A média de **R$ 28.704,99** é inflacionada por 452 pedidos de alto valor (*outliers*). A **Mediana de R$ 25.917,84** deve ser utilizada como referência oficial de ticket médio operacional.
2. **Atribuição de Vendas por Canal:**
   * Análises de comissionamento e performance de equipe devem obrigatoriamente filtrar o canal `pos` ou apenas as vendas assistidas do `ecommerce` ($29,73\%$).
3. **Anomalia Temporal (`created_at`):**
   * A presença de registros cobrindo todo o período até **31/12/2026** exige segregação entre pedidos passados e vendas agendadas/futuras antes do treinamento de modelos preditivos.

---

## 🚀 5. Histórico e Próximos Passos

- [x] **Fase 1:** Carga e profiling inicial da tabela `orders`.
- [x] **Fase 2:** Análise de distribuição (Mediana, Quartis, Outliers e estudo por `channel`).
- [ ] **Fase 3:** Construção das pipelines de transformação (`processed`) e modelagem preditiva.

---
