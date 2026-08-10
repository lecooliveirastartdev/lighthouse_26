from pathlib import Path

content = """# 🚢 Desafio Lighthouse — Dados & AI

**Candidato / Responsável:** Leco Oliveira  
**Projeto:** Lighthouse '26 (`lighthouse_26`)  
**Escopo da Análise:** Análise Exploratória e Diagnóstico de Confiabilidade da Tabela `orders`  
**Data da Análise:** Agosto de 2026  

---

## 📌 1. Visão Geral & Diretrizes do Desafio

Este documento reúne os resultados, métricas e análises técnicas extraídas do banco de dados relacional do ERP da **LH Nautical**. O objetivo desta primeira fase é fornecer ao **Sr. Almir** uma visão clara sobre a integridade e confiabilidade dos dados de vendas.

### Premissas Obrigatórias (Escopo Fechado)
1. **Tabela Exclusiva:** Utilizar **apenas** a tabela `orders`.
2. **Sem Tratamento Precoce:** Não realizar limpeza, remoção de nulos, imputação ou transformações de tipos nos dados brutos nesta fase.
3. **Abordagem Observacional:** Limitar a fase inicial à carga, agregação direta (`min`, `max`, `mean`, `count`) e diagnóstico visual/estatístico do estado original dos dados.

---

## 📊 2. Parte 1 — Visão Geral da Tabela `orders`

A extração dos metadados e limites temporais da tabela `orders` revelou o seguinte panorama operacional:

| Métrica / Atributo | Valor Observado | Observação Técnica |
| :--- | :---: | :--- |
| **Total de Linhas (Registros)** | `48.998` | Volume expressivo de pedidos cadastrados no sistema. |
| **Total de Colunas** | `13` | Inclui IDs, status, canal, valores financeiros e timestamps. |
| **Data Mínima (`created_at`)** | `2020-01-01 01:19:28` | Início do histórico registrado. |
| **Data Máxima (`created_at`)** | `2026-12-31 23:43:09` | Contém lançamentos cobrindo todo o ano corrente. |

---

## 💰 3. Parte 2 — Análise de Valores Numéricos (`total`)

A agregação dos valores financeiros da coluna `total` (sem filtros ou tratamentos de *outliers*) apresentou os seguintes resultados:

* **Valor Mínimo por Pedido:** `R$ 32,62`
* **Valor Máximo por Pedido:** `R$ 127.262,02`
* **Valor Médio por Pedido:** `R$ 28.704,99`

---

## 🩺 4. Parte 3 — Diagnóstico de Confiabilidade (Parecer Executivo)

### ❓ Pergunta do Sr. Almir:
> *"Com base apenas nestes dados agregados, os números refletem com 100% de confiabilidade a realidade financeira da operação para tomada de decisão?"*

### ❌ Resposta do Diagnóstico:
**Não. Os dados no estado em que se encontram NÃO devem ser utilizados de forma isolada para tomadas de decisão estratégicas ou projeções financeiras definitivas.**

### 🔎 Análise de Vulnerabilidades Identificadas nos Dados Brutos:

1. **Assimetria Severa e Efeito de Outliers no Ticket Médio:**
   * A média de **R$ 28.704,99** está muito distante do valor mínimo (**R$ 32,62**) e é fortemente inflacionada por pedidos atípicos de alto valor (como o máximo de **R$ 127.262,02**).
   * **Risco de Negócio:** Usar a média aritmética simples como "ticket médio padrão" mascarará a real distribuição de vendas (provavelmente composta por muitos pedidos pequenos e poucos contratos B2B gigantescos). É fundamental analisar a **Mediana** e o **Desvio Padrão** nas próximas fases.

2. **Integridade Temporal do Sistema:**
   * A presença de registros cobrindo todo o período até **31/12/2026** exige validação sobre se esses dados representam pedidos reais, transações agendadas/recorrentes ou lançamentos sintéticos/testes de sistema mantidos no ambiente de produção.

3. **Lacuna na Atribuição de Vendas (`salesperson_id`):**
   * O profiling indicou **24.131 registros nulos** (~49,2%) na coluna de vendedores.
   * **Impacto:** Embora não altere a soma da receita total, essa ausência impede análises de performance de equipe e comissionamento sem o cruzamento adequado com a coluna `channel` (vendas e-commerce vs. vendas diretas).

4. **Necessidade de Auditoria de Consistência Interna:**
   * Embora o campo `total` não contenha valores nulos ou negativos, é necessário validar em fases futuras se a regra de negócio se mantém:  
     $$\text{total} = \text{subtotal} - \text{discount\_amount}$$

---

## 🚀 5. Próximos Passos Recomendados

- [x] **Fase 1:** Carga e profiling inicial da tabela `orders` (`src/exploration/eda_orders.py`).
- [ ] **Fase 2:** Análise de distribuição (Mediana, Quartis e Desvio Padrão da coluna `total`).
- [ ] **Fase 3:** Análise por canais de venda (`channel`) e cruzamento com atribuição de vendedores (`salesperson_id`).
- [ ] **Fase 4:** Desenvolvimento de pipelines de preparação de dados (`processed`) mantendo a rastreabilidade do dado bruto.

---
"""

doc_path = Path("Desafio Lighthouse - Dados & AI.md")
doc_path.write_text(content, encoding="utf-8")
print("✅ Arquivo 'Desafio Lighthouse - Dados & AI.md' gerado com sucesso!")
