"""
Arquivo temporário para testar o módulo de extração.

Este arquivo será removido depois que o pipeline estiver funcionando.
"""

from src.ingestion.extract import extract_table

# Lê a tabela Product do banco
df = extract_table("Product")

# Exibe informações básicas
print("=" * 50)
print("Primeiras linhas da tabela Product")
print("=" * 50)

print(df.head())

print("\nQuantidade de linhas e colunas:")
print(df.shape)

print("\nColunas:")
print(df.columns.tolist())