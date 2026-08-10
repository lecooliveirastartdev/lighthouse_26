-- ============================================================
-- Desafio Lighthouse — Dados & IA
-- Questão 1.1 — EDA com SQL
-- Tabela analisada: orders
-- ============================================================
--
-- Objetivo:
-- Calcular as métricas solicitadas na Questão 1 utilizando SQL,
-- sem realizar limpeza ou transformação dos dados.
--
-- O DuckDB consulta diretamente o arquivo CSV original.
-- Nenhuma alteração é realizada nos dados de origem.
-- ============================================================

SELECT
    -- Quantidade total de registros da tabela.
    COUNT(*) AS total_linhas,

    -- Primeiro registro temporal encontrado em created_at.
    MIN(created_at) AS data_minima,

    -- Último registro temporal encontrado em created_at.
    MAX(created_at) AS data_maxima,

    -- Menor valor registrado na coluna total.
    MIN(total) AS valor_minimo,

    -- Maior valor registrado na coluna total.
    MAX(total) AS valor_maximo,

    -- Média dos valores registrados na coluna total.
    AVG(total) AS valor_medio

FROM read_csv_auto(
    '/mnt/c/Users/LecoOliveira/Downloads/1-lh_nautical_csv/orders.csv'
);
