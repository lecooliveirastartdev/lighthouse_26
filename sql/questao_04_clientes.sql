-- ============================================================
-- Desafio Lighthouse — Dados & IA
-- Questão 4 — Análise de clientes
-- ============================================================
--
-- Objetivos:
-- 1. Calcular faturamento, frequência e ticket médio por cliente.
-- 2. Calcular a diversidade de categorias compradas.
-- 3. Selecionar clientes com 13 ou mais categorias.
-- 4. Identificar os 10 maiores tickets médios.
-- 5. Encontrar a categoria com maior quantidade de itens
--    comprados por esse grupo de clientes.
-- ============================================================


-- ============================================================
-- 1. MÉTRICAS FINANCEIRAS POR CLIENTE
-- ============================================================

WITH metricas_clientes AS (

    SELECT
        o.customer_id,

        -- Soma do valor total dos pedidos do cliente.
        SUM(o.total) AS faturamento_total,

        -- Quantidade de transações realizadas pelo cliente.
        COUNT(DISTINCT o.id) AS frequencia,

        -- Ticket médio:
        -- faturamento total dividido pela quantidade de pedidos.
        SUM(o.total) / COUNT(DISTINCT o.id) AS ticket_medio

    FROM orders AS o

    GROUP BY
        o.customer_id
),


-- ============================================================
-- 2. DIVERSIDADE DE CATEGORIAS
-- ============================================================

diversidade_clientes AS (

    SELECT
        o.customer_id,

        -- Quantidade de categorias diferentes compradas
        -- por cada cliente.
        COUNT(DISTINCT p.category_id) AS diversidade_categorias

    FROM orders AS o

    INNER JOIN order_items AS oi
        ON oi.order_id = o.id

    INNER JOIN product_variants AS pv
        ON pv.id = oi.product_variant_id

    INNER JOIN products AS p
        ON p.id = pv.product_id

    GROUP BY
        o.customer_id
),


-- ============================================================
-- 3. CLIENTES QUE ATENDEM AO CRITÉRIO DE ELITE
-- ============================================================

clientes_elite AS (

    SELECT
        m.customer_id,
        m.faturamento_total,
        m.frequencia,
        m.ticket_medio,
        d.diversidade_categorias

    FROM metricas_clientes AS m

    INNER JOIN diversidade_clientes AS d
        ON d.customer_id = m.customer_id

    -- Premissa obrigatória:
    -- somente clientes com 13 ou mais categorias.
    WHERE d.diversidade_categorias >= 13
),


-- ============================================================
-- 4. TOP 10 CLIENTES POR TICKET MÉDIO
-- ============================================================

top_10_clientes AS (

    SELECT
        customer_id,
        faturamento_total,
        frequencia,
        ticket_medio,
        diversidade_categorias

    FROM clientes_elite

    ORDER BY
        ticket_medio DESC,
        customer_id ASC

    LIMIT 10
),


-- ============================================================
-- 5. CONSUMO POR CATEGORIA DOS 10 CLIENTES
-- ============================================================

consumo_categorias AS (

    SELECT
        p.category_id,
        c.name AS categoria,

        -- Quantidade total de itens comprados
        -- pelos 10 clientes selecionados.
        SUM(oi.quantity) AS quantidade_total_itens

    FROM top_10_clientes AS t

    INNER JOIN orders AS o
        ON o.customer_id = t.customer_id

    INNER JOIN order_items AS oi
        ON oi.order_id = o.id

    INNER JOIN product_variants AS pv
        ON pv.id = oi.product_variant_id

    INNER JOIN products AS p
        ON p.id = pv.product_id

    INNER JOIN categories AS c
        ON c.id = p.category_id

    GROUP BY
        p.category_id,
        c.name
)


-- ============================================================
-- RESULTADO FINAL
-- ============================================================

SELECT
    category_id,
    categoria,
    quantidade_total_itens

FROM consumo_categorias

ORDER BY
    quantidade_total_itens DESC,
    category_id ASC

LIMIT 1;