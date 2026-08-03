"""
Arquivo temporário para testar o módulo de extração.

Objetivo:
- Verificar se a conexão com o banco SQLite está funcionando.
- Ler uma tabela do banco.
- Exibir algumas informações no terminal.

Este arquivo será removido quando o pipeline principal estiver pronto.
"""

# Importa a função responsável por extrair dados do banco.
from src.ingestion.extract import extract_table


def main():
    """
    Função principal do teste.
    """

    print("=" * 60)
    print("TESTE DO MÓDULO DE EXTRAÇÃO")
    print("=" * 60)

    # Lê a tabela Product do banco.
    dataframe = extract_table("Product")

    print("\nPrimeiras linhas:\n")
    print(dataframe.head())

    print("\nInformações do DataFrame\n")
    print(f"Linhas: {dataframe.shape[0]}")
    print(f"Colunas: {dataframe.shape[1]}")

    print("\nNome das colunas:\n")
    print(dataframe.columns.tolist())

    print("\nTeste concluído com sucesso! ✅")


# Executa o teste somente quando este arquivo for executado diretamente.
if __name__ == "__main__":
    main()