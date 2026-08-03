"""
Módulo responsável pela extração de dados.

Este módulo contém funções para conectar ao banco SQLite
e extrair tabelas para DataFrames do Pandas.

Autor: Alexandro Oliveira
Projeto: Lighthouse 2026
"""

# ==========================================================
# IMPORTAÇÕES
# ==========================================================

# Biblioteca para manipulação de caminhos de arquivos.
# Ela funciona tanto no Windows quanto no Linux e macOS.
from pathlib import Path

# Biblioteca padrão do Python para trabalhar com SQLite.
import sqlite3

# Biblioteca utilizada para manipulação de dados.
import pandas as pd


# ==========================================================
# CONEXÃO COM O BANCO
# ==========================================================

def get_connection() -> sqlite3.Connection:
    """
    Cria e retorna uma conexão com o banco SQLite.

    A função localiza automaticamente a pasta raiz do projeto,
    encontra o banco de dados e cria uma conexão.

    Returns:
        sqlite3.Connection:
            Objeto de conexão com o banco SQLite.
    """

    # Caminho da raiz do projeto.
    #
    # Exemplo:
    #
    # lighthouse_26/
    # ├── src/
    # │   └── ingestion/
    # │       └── extract.py
    #
    # O "parents[2]" sobe dois níveis:
    #
    # extract.py
    #      ↑
    # ingestion
    #      ↑
    # src
    #      ↑
    # lighthouse_26
    #
    project_root = Path(__file__).resolve().parents[2]

    # Caminho completo do banco.
    database_path = (
        project_root
        / "data"
        / "raw"
        / "Northwind_small.sqlite"
    )

    # Cria e retorna a conexão.
    return sqlite3.connect(database_path)


# ==========================================================
# EXTRAÇÃO DOS DADOS
# ==========================================================

def extract_table(table_name: str) -> pd.DataFrame:
    """
    Extrai qualquer tabela do banco SQLite.

    Parameters
    ----------
    table_name : str
        Nome da tabela que será lida.

    Returns
    -------
    pd.DataFrame
        DataFrame contendo todos os registros da tabela.
    """

    # Monta a consulta SQL.
    #
    # Exemplo:
    #
    # SELECT * FROM Product
    #
    query = f"SELECT * FROM {table_name}"

    # Abre a conexão.
    #
    # O "with" garante que a conexão será fechada
    # automaticamente mesmo que aconteça algum erro.
    with get_connection() as connection:

        # Executa a consulta SQL.
        #
        # O resultado será armazenado em um DataFrame.
        dataframe = pd.read_sql_query(
            sql=query,
            con=connection
        )

    # Retorna o DataFrame para quem chamou a função.
    return dataframe