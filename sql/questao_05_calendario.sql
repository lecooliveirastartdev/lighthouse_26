-- ============================================================
-- Desafio Lighthouse — Dados & IA
-- Questão 5 — Dimensão de calendário
-- ============================================================
--
-- Objetivo:
-- Criar uma dimensão de datas para garantir que dias sem vendas
-- também sejam considerados no cálculo da média por dia da semana.
--
-- Premissas:
-- - considerar somente vendas em lojas físicas (channel = 'pos');
-- - considerar todas as datas desde a menor data de venda até hoje;
-- - considerar dias sem venda com valor igual a zero;
-- - calcular vendas diárias antes da média por dia da semana.
-- ============================================================


-- ============================================================
-- 1. IDENTIFICAÇÃO DA DATA INICIAL
-- ============================================================

WITH periodo AS (

    SELECT
        MIN(created_at::date) AS data_inicial,
        CURRENT_DATE AS data_final

    FROM orders
),


-- ============================================================
-- 2. DIMENSÃO DE CALENDÁRIO
-- ============================================================

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


-- ============================================================
-- 3. VENDAS DIÁRIAS DAS LOJAS FÍSICAS
-- ============================================================

vendas_diarias AS (

    SELECT
        created_at::date AS data,
        SUM(total) AS total_vendas_dia

    FROM orders

    WHERE channel = 'pos'

    GROUP BY
        created_at::date
),


-- ============================================================
-- 4. CALENDÁRIO + VENDAS
-- ============================================================

calendario_com_vendas AS (

    SELECT
        c.data,

        -- Dia da semana:
        -- 0 = Domingo
        -- 1 = Segunda
        -- ...
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

        -- Dias sem venda passam a valer zero.
        COALESCE(
            v.total_vendas_dia,
            0
        ) AS total_vendas_dia

    FROM dim_calendario AS c

    LEFT JOIN vendas_diarias AS v
        ON v.data = c.data
),


-- ============================================================
-- 5. MÉDIA DE VENDAS POR DIA DA SEMANA
-- ============================================================

media_por_dia_semana AS (

    SELECT
        numero_dia_semana,
        dia_semana,

        AVG(total_vendas_dia) AS media_vendas

    FROM calendario_com_vendas

    GROUP BY
        numero_dia_semana,
        dia_semana
)


-- ============================================================
-- RESULTADO FINAL
-- ============================================================

SELECT
    dia_semana,
    ROUND(media_vendas, 2) AS media_vendas

FROM media_por_dia_semana

ORDER BY
    media_vendas ASC,
    numero_dia_semana ASC;