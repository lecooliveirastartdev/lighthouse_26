"""
Módulo responsável pelo primeiro profiling dos dados da LH Nautical.

Objetivo:
    Ler os arquivos CSV da fonte original e apresentar informações
    básicas sobre cada tabela.

Neste primeiro momento NÃO vamos:
    - alterar os dados;
    - limpar os dados;
    - transformar os dados;
    - salvar arquivos tratados.

A finalidade é conhecer a estrutura dos dados antes de tomar
decisões sobre o pipeline.
"""

from pathlib import Path

import pandas as pd


# Caminho da pasta que contém os 24 arquivos CSV originais.
# Estamos acessando os arquivos diretamente pelo WSL, sem copiá-los.
DATA_PATH = Path(
    "/mnt/c/Users/LecoOliveira/Downloads/1-lh_nautical_csv"
)


def profile_csv(file_path: Path) -> None:
    """
    Exibe informações básicas de um arquivo CSV.

    Parâmetros:
        file_path: caminho completo do arquivo CSV.
    """

    # Lê o arquivo CSV para um DataFrame.
    dataframe = pd.read_csv(file_path)

    # Exibe o nome da tabela que estamos analisando.
    print("=" * 70)
    print(f"TABELA: {file_path.stem}")
    print("=" * 70)

    # Mostra a quantidade de linhas e colunas.
    print(f"Linhas: {dataframe.shape[0]}")
    print(f"Colunas: {dataframe.shape[1]}")

    # Mostra os nomes das colunas.
    print("\nColunas:")
    print(list(dataframe.columns))

    # Mostra os tipos de dados identificados pelo Pandas.
    print("\nTipos:")
    print(dataframe.dtypes)

    # Mostra a quantidade de valores nulos por coluna.
    print("\nValores nulos:")
    print(dataframe.isna().sum())

    print()


def main() -> None:
    """
    Executa o profiling de todos os arquivos CSV encontrados.
    """

    # Procura todos os arquivos .csv na pasta de origem.
    csv_files = sorted(DATA_PATH.glob("*.csv"))

    print(f"Arquivos encontrados: {len(csv_files)}")
    print()

    # Percorre cada arquivo e executa o profiling.
    for csv_file in csv_files:
        profile_csv(csv_file)


# Garante que o código abaixo seja executado somente quando
# este arquivo for executado diretamente.
if __name__ == "__main__":
    main()
