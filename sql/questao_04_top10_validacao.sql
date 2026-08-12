WITH metricas_clientes AS (

    SELECT
        o.customer_id,
        SUM(o.total) AS faturamento_total,
        COUNT(DISTINCT o.id) AS frequencia,
        SUM(o.total) / COUNT(DISTINCT o.id) AS ticket_medio

    FROM orders AS o

    GROUP BY
        o.customer_id
),

diversidade_clientes AS (

    SELECT
        o.customer_id,
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

    WHERE d.diversidade_categorias >= 13
)

SELECT
    customer_id,
    ROUND(faturamento_total, 2) AS faturamento_total,
    frequencia,
    ROUND(ticket_medio, 2) AS ticket_medio,
    diversidade_categorias

FROM clientes_elite

ORDER BY
    ticket_medio DESC,
    customer_id ASC

LIMIT 10;