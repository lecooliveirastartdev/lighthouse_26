"""
eda_orders.py

Análise exploratória da tabela `orders`, para o desafio LH Nautical.

Regra do desafio (importante):
    - Usar SOMENTE a tabela `orders`.
    - NÃO limpar, NÃO tratar, NÃO transformar os dados.
    - Apenas observar, agregar e descrever.
"""

from pathlib import Path
import pandas as pd

# Caminho do arquivo orders.csv no WSL
ORDERS_PATH = Path(
    "/mnt/c/Users/LecoOliveira/Downloads/1-lh_nautical_csv/orders.csv"
)

def load_orders() -> pd.DataFrame:
    """Carrega a tabela `orders` em seu estado bruto."""
    if not ORDERS_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {ORDERS_PATH}")

    return pd.read_csv(ORDERS_PATH)

def run_desafio_parte_1_e_2(df: pd.DataFrame) -> None:
    """
    Executa a extração das métricas da Parte 1 e Parte 2 do Desafio.
    """
    # --- PARTE 1: Visão Geral ---
    qtd_linhas, qtd_colunas = df.shape
    
    # Para encontrar a data mínima e máxima, convertemos a Series temporariamente em datetime.
    # Isso não altera o dataframe original df.
    created_at_dt = pd.to_datetime(df['created_at'])
    data_min = created_at_dt.min()
    data_max = created_at_dt.max()

    # --- PARTE 2: Análise da Coluna 'total' ---
    total_min = df['total'].min()
    total_max = df['total'].max()
    total_medio = df['total'].mean()

    # --- SUPORTE PARTE 3: Checagens de Qualidade/Inconsistência ---
    nulos_total = df['total'].isnull().sum()
    nulos_created_at = df['created_at'].isnull().sum()
    totais_negativos = (df['total'] < 0).sum()
    totais_zero = (df['total'] == 0).sum()

    # IMPRESSÃO ORGANIZADA
    print("=" * 60)
    print("PARTE 1 — VISÃO GERAL DA TABELA ORDERS")
    print("=" * 60)
    print(f"• Quantidade total de linhas:  {qtd_linhas}")
    print(f"• Quantidade total de colunas: {qtd_colunas}")
    print(f"• Data mínima (created_at):    {data_min}")
    print(f"• Data máxima (created_at):    {data_max}")

    print("\n" + "=" * 60)
    print("PARTE 2 — ANÁLISE DE VALORES NUMÉRICOS (COLUNA TOTAL)")
    print("=" * 60)
    print(f"• Valor mínimo: R$ {total_min:,.2f}")
    print(f"• Valor máximo: R$ {total_max:,.2f}")
    print(f"• Valor médio:  R$ {total_medio:,.2f}")

    print("\n" + "=" * 60)
    print("DADOS AUXILIARES PARA O DIAGNÓSTICO (PARTE 3)")
    print("=" * 60)
    print(f"• Val. nulos em 'total':      {nulos_total}")
    print(f"• Val. nulos em 'created_at': {nulos_created_at}")
    print(f"• Pedidos com total < 0:      {totais_negativos}")
    print(f"• Pedidos com total == 0:     {totais_zero}")
    print("=" * 60)

if __name__ == "__main__":
    orders_df = load_orders()
    run_desafio_parte_1_e_2(orders_df)