"""
Questão 6 — Previsão de demanda
Baseline com média móvel de 3 meses.

Produto:
Bússola de Bordo 702

Período de treino:
até 31/12/2025

Período de teste:
primeiro trimestre de 2026

Regra do baseline:
a previsão de cada mês utiliza a média das vendas
dos 3 meses imediatamente anteriores.
"""

import sys
from statistics import mean

import psycopg


# ============================================================
# CONEXÃO COM O POSTGRESQL
# ============================================================

def connect_database(
    host: str,
    port: int,
    dbname: str,
    user: str,
    password: str,
):
    """
    Cria e retorna uma conexão com o PostgreSQL.
    """

    return psycopg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )


# ============================================================
# CONSULTA DAS VENDAS MENSAIS
# ============================================================

def load_monthly_sales(connection) -> dict[str, int]:
    """
    Consulta as vendas mensais do produto Bússola de Bordo 702.

    Todos os registros com esse nome de produto são considerados,
    incluindo suas respectivas variantes.
    """

    query = """
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
            TO_CHAR(m.mes, 'YYYY-MM') AS mes,

            COALESCE(
                v.unidades_vendidas,
                0
            ) AS unidades_vendidas

        FROM meses AS m

        LEFT JOIN vendas_mensais AS v
            ON v.mes = m.mes

        ORDER BY
            m.mes;
    """

    vendas_mensais = {}

    with connection.cursor() as cursor:

        cursor.execute(query)

        for mes, unidades in cursor.fetchall():
            vendas_mensais[mes] = int(unidades)

    return vendas_mensais


# ============================================================
# MÉDIA MÓVEL DE 3 MESES
# ============================================================

def media_movel_3_meses(valores: list[int]) -> float:
    """
    Calcula a média de três valores mensais.
    """

    return mean(valores)


# ============================================================
# PREVISÕES DO PERÍODO DE TESTE
# ============================================================

def generate_forecasts(
    vendas_mensais: dict[str, int]
) -> dict[str, float]:
    """
    Gera as previsões para janeiro, fevereiro e março de 2026.

    Para cada mês previsto são utilizados apenas os
    três meses anteriores.
    """

    previsoes = {
        "2026-01": media_movel_3_meses(
            [
                vendas_mensais["2025-10"],
                vendas_mensais["2025-11"],
                vendas_mensais["2025-12"],
            ]
        ),

        "2026-02": media_movel_3_meses(
            [
                vendas_mensais["2025-11"],
                vendas_mensais["2025-12"],
                vendas_mensais["2026-01"],
            ]
        ),

        "2026-03": media_movel_3_meses(
            [
                vendas_mensais["2025-12"],
                vendas_mensais["2026-01"],
                vendas_mensais["2026-02"],
            ]
        ),
    }

    return previsoes


# ============================================================
# CÁLCULO DO MAE
# ============================================================

def calculate_mae(
    previsoes: dict[str, float],
    valores_reais: dict[str, int],
):
    """
    Calcula o erro absoluto de cada mês e o MAE.
    """

    erros_absolutos = {}

    for mes in previsoes:

        erro = abs(
            valores_reais[mes]
            - previsoes[mes]
        )

        erros_absolutos[mes] = erro

    mae = mean(
        erros_absolutos.values()
    )

    return erros_absolutos, mae


# ============================================================
# ARGUMENTOS
# ============================================================

def parse_arguments():
    """
    Obtém os parâmetros de conexão com PostgreSQL.

    Uso:
        python questao_06_baseline.py
        <host> <porta> <banco> <usuario> <senha>
    """

    if len(sys.argv) != 6:

        print(
            "Uso: python questao_06_baseline.py "
            "<host> "
            "<porta> "
            "<banco> "
            "<usuario> "
            "<senha>"
        )

        sys.exit(1)

    host = sys.argv[1]

    try:
        port = int(
            sys.argv[2]
        )

    except ValueError:

        print(
            "Erro: a porta deve ser um número inteiro."
        )

        sys.exit(1)

    dbname = sys.argv[3]
    user = sys.argv[4]
    password = sys.argv[5]

    return (
        host,
        port,
        dbname,
        user,
        password,
    )


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main() -> None:
    """
    Executa o baseline completo.
    """

    (
        host,
        port,
        dbname,
        user,
        password,
    ) = parse_arguments()

    try:

        with connect_database(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
        ) as connection:

            vendas_mensais = load_monthly_sales(
                connection
            )

    except psycopg.Error as error:

        print(
            f"Erro de conexão ou consulta: {error}"
        )

        sys.exit(1)

    previsoes = generate_forecasts(
        vendas_mensais
    )

    valores_reais = {
        "2026-01": vendas_mensais["2026-01"],
        "2026-02": vendas_mensais["2026-02"],
        "2026-03": vendas_mensais["2026-03"],
    }

    erros_absolutos, mae = calculate_mae(
        previsoes,
        valores_reais,
    )

    print("=" * 72)
    print("QUESTÃO 6 — BASELINE DE PREVISÃO DE DEMANDA")
    print("=" * 72)

    print(
        f"{'Mês':<12}"
        f"{'Real':>10}"
        f"{'Previsão':>14}"
        f"{'Erro absoluto':>18}"
    )

    print("-" * 72)

    for mes in previsoes:

        print(
            f"{mes:<12}"
            f"{valores_reais[mes]:>10}"
            f"{previsoes[mes]:>14.2f}"
            f"{erros_absolutos[mes]:>18.2f}"
        )

    print("-" * 72)

    print(
        f"MAE: {mae:.2f} unidades"
    )

    print("=" * 72)


# ============================================================
# PONTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    main()