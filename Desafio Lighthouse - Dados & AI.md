# 🚢 Desafio Lighthouse — Dados & AI

**Candidato / Responsável:** Leco Oliveira  
**Projeto:** Lighthouse '26 (`lighthouse_26`)  
**Escopo da Análise:** Análise Exploratória, Diagnóstico e Pipeline de Processamento (`processed`)  
**Data da Análise:** Agosto de 2026  

---

## 📌 1. Visão Geral & Diretrizes do Desafio

Este documento reúne os resultados, métricas e análises técnicas extraídas do banco de dados relacional do ERP da **LH Nautical**.

### Premissas Obrigatórias
1. **Rastreabilidade:** Manter os dados brutos intactos em `raw/` e gravar apenas dados tratados na camada `processed/`.
2. **Integridade de Negócio:** Tratamento de nulos em vendedores e segregação de lançamentos futuros.

---

## 📊 2. Estatística Descritiva dos Dados Brutos (`orders`)

### 2.1 Metadados e Volume Original
* **Total de Linhas:** `48.998`
* **Total de Colunas:** `13`
* **Período Registrado:** `01/01/2020` a `31/12/2026`

### 2.2 Análise Financeira (`total`)
* **Mediana (Q2 - Ticket Central):** `R$ 25.917,84`
* **Valor Médio:** `R$ 28.704,99`
* **Outliers Identificados (IQR > 1.5):** `452 pedidos` (`0,92%` das vendas, acima de `R$ 82.597,85`).

---

## ⚙️ 3. Camada de Processamento (`data/processed/`)

O pipeline executado via `src/data/make_dataset.py` aplicou as seguintes transformações:

1. **Tratamento Temporal (Cutoff em 10/08/2026):**
   * **Pedidos Históricos Válidos:** `44.668` registros (`87,1%`).
   * **Lançamentos Futuros (`is_future_order`):** `4.330` registros (`12,9%`).
2. **Tratamento de Vendedores (`salesperson_id`):**
   * Preenchimento de nulos com `-1` (`salesperson_id_clean`) representando compras diretas via e-commerce (autoatendimento).
   * Criação da flag booleana `has_salesperson`.
3. **Formatos de Exportação:** Salvos em `CSV` e `Parquet` otimizado.

---

## 🚀 4. Histórico e Próximos Passos

- [x] **Fase 1:** Profiling inicial da tabela `orders`.
- [x] **Fase 2:** Análise de distribuição (Mediana, Quartis, Outliers e Canais).
- [x] **Fase 3:** Construção e validação da camada de transformação (`data/processed/`).
- [ ] **Fase 4:** Feature Engineering e Modelagem Preditiva de IA/ML.

---
