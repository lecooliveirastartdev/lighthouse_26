"""
Módulo responsável pela transformação dos dados.

Objetivo:
Receber um DataFrame, aplicar regras de limpeza e
retornar um novo DataFrame tratado.

Autor: Alexandro Oliveira
Projeto: Lighthouse 2026
"""

# ==========================================================
# IMPORTAÇÕES
# ==========================================================

import pandas as pd


# ==========================================================
# FUNÇÃO DE TRANSFORMAÇÃO
# ==========================================================

def transform_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica transformações básicas ao DataFrame.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dados extraídos do banco.

    Returns
    -------
    pd.DataFrame
        DataFrame tratado.
    """

    # Cria uma cópia para evitar alterar o DataFrame original.
    df = dataframe.copy()

    # Quantidade de linhas antes das transformações.
    total_before = len(df)

    # Remove linhas completamente vazias.
    df = df.dropna(how="all")

    # Remove registros duplicados.
    df = df.drop_duplicates()

    # Padroniza os nomes das colunas.
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # Quantidade de linhas após as transformações.
    total_after = len(df)

    print("=" * 60)
    print("TRANSFORMAÇÃO")
    print("=" * 60)
    print(f"Linhas antes : {total_before}")
    print(f"Linhas depois: {total_after}")
    print("Transformação concluída com sucesso! ✅")

    return df