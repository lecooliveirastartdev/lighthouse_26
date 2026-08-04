"""
Teste da camada de transformação.

Objetivo:
- Ler dados do banco.
- Aplicar as transformações.
- Verificar o resultado.

Autor: Alexandro Oliveira
Projeto: Lighthouse 2026
"""

# ==========================================================
# IMPORTAÇÕES
# ==========================================================

from src.ingestion.extract import extract_table
from src.transformation.transform import transform_data


def main() -> None:
    """
    Executa o teste da transformação.
    """

    print("=" * 60)
    print("TESTE DA CAMADA DE TRANSFORMAÇÃO")
    print("=" * 60)

    # Extrai os dados da tabela Product.
    dataframe = extract_table("Product")

    # Aplica as transformações.
    dataframe_transformado = transform_data(dataframe)

    print("\nPrimeiras linhas após a transformação:\n")
    print(dataframe_transformado.head())

    print("\nTipos das colunas:\n")
    print(dataframe_transformado.dtypes)


# Executa o teste apenas quando este arquivo for chamado diretamente.
if __name__ == "__main__":
    main()