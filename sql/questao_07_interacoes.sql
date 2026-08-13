"""
Questão 7 — Sistema de recomendação.

Objetivo:
Construir uma matriz binária Cliente x Produto e calcular
a similaridade de cosseno entre produtos.

Produto de referência:
Motor de Popa 1949
"""

import sys

import pandas as pd
import psycopg
from sklearn.metrics.pairwise import cosine_similarity


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
# CARREGAMENTO DAS INTERAÇÕES
# ============================================================

def load_interactions(connection) -> pd.DataFrame:
    """
    Carrega as interações Cliente x Produto.

    Cada par customer_id + product_id aparece apenas uma vez.
    A quantidade comprada não é considerada.
    """

    query = """
        SELECT DISTINCT
            o.customer_id,
            pv.product_id

        FROM orders AS o

        INNER JOIN order_items AS oi
            ON oi.order_id = o.id

        INNER JOIN product_variants AS pv
            ON pv.id = oi.product_variant_id

        WHERE o.customer_id IS NOT NULL;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "customer_id",
            "product_id",
        ],
    )


# ============================================================
# NOMES DOS PRODUTOS
# ============================================================

def load_products(connection) -> pd.DataFrame:
    """
    Carrega id e nome dos produtos.
    """

    query = """
        SELECT
            id AS product_id,
            name

        FROM products;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "product_id",
            "name",
        ],
    )


# ============================================================
# MATRIZ CLIENTE x PRODUTO
# ============================================================

def build_interaction_matrix(
    interactions: pd.DataFrame,
) -> pd.DataFrame:
    """
    Constrói a matriz binária Cliente x Produto.

    Valor:
    1 -> cliente comprou o produto
    0 -> cliente não comprou o produto
    """

    interactions = interactions.copy()

    interactions["interaction"] = 1

    matrix = interactions.pivot_table(
        index="customer_id",
        columns="product_id",
        values="interaction",
        aggfunc="max",
        fill_value=0,
    )

    return matrix


# ============================================================
# SIMILARIDADE ENTRE PRODUTOS
# ============================================================

def calculate_product_similarity(
    interaction_matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula a similaridade de cosseno produto x produto.
    """

    # A matriz original é Cliente x Produto.
    # Para comparar produtos, fazemos a transposição:
    #
    # Produto x Cliente.
    product_matrix = interaction_matrix.T

    similarities = cosine_similarity(
        product_matrix
    )

    similarity_df = pd.DataFrame(
        similarities,
        index=product_matrix.index,
        columns=product_matrix.index,
    )

    return similarity_df


# ============================================================
# RANKING DOS PRODUTOS
# ============================================================

def get_top_similar_products(
    similarity_df: pd.DataFrame,
    products: pd.DataFrame,
    reference_product_id: int,
    top_n: int = 5,
) -> pd.DataFrame:
    """
    Retorna os produtos mais similares ao produto de referência.
    """

    if reference_product_id not in similarity_df.index:
        raise ValueError(
            f"Produto {reference_product_id} não encontrado "
            "na matriz de interações."
        )

    scores = (
        similarity_df.loc[reference_product_id]
        .drop(reference_product_id)
        .sort_values(ascending=False)
        .head(top_n)
    )

    ranking = scores.reset_index()

    ranking.columns = [
        "product_id",
        "similaridade",
    ]

    ranking = ranking.merge(
        products,
        on="product_id",
        how="left",
    )

    return ranking[
        [
            "product_id",
            "name",
            "similaridade",
        ]
    ]


# ============================================================
# ARGUMENTOS
# ============================================================

def parse_arguments():
    """
    Obtém os parâmetros de conexão.

    Uso:
        python questao_07_recomendacao.py
        <host> <porta> <banco> <usuario> <senha>
    """

    if len(sys.argv) != 6:

        print(
            "Uso: python questao_07_recomendacao.py "
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
    Executa o sistema de recomendação.
    """

    REFERENCE_PRODUCT_ID = 180
    REFERENCE_PRODUCT_NAME = "Motor de Popa 1949"

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

            interactions = load_interactions(
                connection
            )

            products = load_products(
                connection
            )

    except psycopg.Error as error:

        print(
            f"Erro de conexão ou consulta: {error}"
        )

        sys.exit(1)

    interaction_matrix = build_interaction_matrix(
        interactions
    )

    similarity_df = calculate_product_similarity(
        interaction_matrix
    )

    ranking = get_top_similar_products(
        similarity_df=similarity_df,
        products=products,
        reference_product_id=REFERENCE_PRODUCT_ID,
        top_n=5,
    )

    print("=" * 72)
    print("QUESTÃO 7 — SISTEMA DE RECOMENDAÇÃO")
    print("=" * 72)

    print(
        f"Produto de referência: "
        f"{REFERENCE_PRODUCT_NAME} "
        f"(product_id={REFERENCE_PRODUCT_ID})"
    )

    print(
        f"Clientes na matriz: "
        f"{interaction_matrix.shape[0]}"
    )

    print(
        f"Produtos na matriz: "
        f"{interaction_matrix.shape[1]}"
    )

    print("-" * 72)

    print(
        f"{'Posição':<10}"
        f"{'ID':>8}  "
        f"{'Produto':<35}"
        f"{'Similaridade':>15}"
    )

    print("-" * 72)

    for position, row in enumerate(
        ranking.itertuples(index=False),
        start=1,
    ):

        print(
            f"{position:<10}"
            f"{row.product_id:>8}  "
            f"{row.name:<35}"
            f"{row.similaridade:>15.4f}"
        )

    print("=" * 72)


# ============================================================
# PONTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    main()