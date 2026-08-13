-- ============================================================
-- Desafio Lighthouse — Dados & IA
-- Questão 6 — Dataset mensal para previsão de demanda
-- Produto: Bússola de Bordo 702
-- ============================================================

WITH meses AS (

    SELECT
        generate_series(
            DATE '2020-01-01',
            DATE '2026-03-01',
            INTERVAL '1 month'
        )::date AS mes
),

vendas_mensais AS (

    SELECT
        DATE_TRUNC(
            'month',
            o.created_at
        )::date AS mes,

        SUM(oi.quantity) AS unidades_vendidas

    FROM orders AS o

    INNER JOIN order_items AS oi
        ON oi.order_id = o.id

    INNER JOIN product_variants AS pv
        ON pv.id = oi.product_variant_id

    INNER JOIN products AS p
        ON p.id = pv.product_id

    WHERE
        p.name = 'Bússola de Bordo 702'

    GROUP BY
        DATE_TRUNC('month', o.created_at)
)

SELECT
    m.mes,

    COALESCE(
        v.unidades_vendidas,
        0
    ) AS unidades_vendidas

FROM meses AS m

LEFT JOIN vendas_mensais AS v
    ON v.mes = m.mes

ORDER BY
    m.mes;