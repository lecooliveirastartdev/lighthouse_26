WITH periodo AS (
    SELECT
        MIN(created_at::date) AS data_inicial,
        CURRENT_DATE AS data_final
    FROM orders
),

dim_calendario AS (
    SELECT
        data::date AS data
    FROM periodo
    CROSS JOIN LATERAL generate_series(
        periodo.data_inicial,
        periodo.data_final,
        INTERVAL '1 day'
    ) AS data
),

vendas_diarias AS (
    SELECT
        created_at::date AS data,
        SUM(total) AS total_vendas_dia
    FROM orders
    WHERE channel = 'pos'
    GROUP BY created_at::date
),

calendario_com_vendas AS (
    SELECT
        c.data,
        EXTRACT(DOW FROM c.data) AS numero_dia_semana,

        CASE EXTRACT(DOW FROM c.data)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
        END AS dia_semana,

        COALESCE(v.total_vendas_dia, 0) AS total_vendas_dia

    FROM dim_calendario AS c

    LEFT JOIN vendas_diarias AS v
        ON v.data = c.data
)

SELECT
    dia_semana,
    COUNT(*) AS dias_calendario,
    COUNT(*) FILTER (
        WHERE total_vendas_dia = 0
    ) AS dias_sem_venda,
    ROUND(
        AVG(total_vendas_dia),
        2
    ) AS media_vendas

FROM calendario_com_vendas

GROUP BY
    numero_dia_semana,
    dia_semana

ORDER BY
    media_vendas ASC,
    numero_dia_semana ASC;