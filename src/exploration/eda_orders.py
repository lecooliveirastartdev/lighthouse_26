"""
eda_orders.py

Análise exploratória da tabela `orders` para o desafio LH Nautical.
Fase 2: Distribuição por Canais, Atribuição de Vendedores e Estatística Descritiva.
"""

from pathlib import Path
import numpy as np
import pandas as pd

ORDERS_PATH = Path(
    "/mnt/c/Users/LecoOliveira/Downloads/1-lh_nautical_csv/orders.csv"
)


def load_orders() -> pd.DataFrame:
    """Carrega a tabela `orders` em seu estado bruto."""
    if not ORDERS_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {ORDERS_PATH}")
    return pd.read_csv(ORDERS_PATH)


def run_fase_2_analysis(df: pd.DataFrame) -> None:
    """Executa a análise de canais, vendedores e estatísticas de dispersão."""
    print("=" * 65)
    print("FASE 2 — ANÁLISE DE CANAIS E ATRIBUIÇÃO DE VENDEDORES")
    print("=" * 65)

    # 1. Distribuição por Canal
    total_pedidos = len(df)
    canais = df["channel"].value_counts(dropna=False)
    canais_pct = df["channel"].value_counts(normalize=True, dropna=False) * 100

    print("• Distribuição de Pedidos por Canal (channel):")
    for canal, qtd in canais.items():
        pct = canais_pct[canal]
        print(f"  - {canal}: {qtd:,} pedidos ({pct:.2f}%)")

    # 2. Cruzamento: Canal vs Salesperson Nulo
    print("\n• Análise de Vendedores Nulos (salesperson_id) por Canal:")
    df["salesperson_is_null"] = df["salesperson_id"].isnull()
    cruzamento = pd.crosstab(
        df["channel"],
        df["salesperson_is_null"],
        normalize="index",
    ) * 100
    cruzamento.columns = ["Com Vendedor (%)", "Sem Vendedor (Nulo %)"]
    print(cruzamento.round(2).to_string())

    print("\n" + "=" * 65)
    print("FASE 2 — ESTATÍSTICA DE DISPERSÃO DA COLUNA TOTAL")
    print("=" * 65)

    # 3. Mediana, Quartis e IQR
    q1 = df["total"].quantile(0.25)
    mediana = df["total"].median()
    q3 = df["total"].quantile(0.75)
    iqr = q3 - q1
    std_dev = df["total"].std()

    # Outliers pelo critério do IQR (1.5 * IQR)
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    outliers = df[(df["total"] < limite_inferior) | (df["total"] > limite_superior)]
    qtd_outliers = len(outliers)
    pct_outliers = (qtd_outliers / total_pedidos) * 100

    print(f"• Mediana (Q2 - Pedido Central): R$ {mediana:,.2f}")
    print(f"• Primeiro Quartil (Q1 - 25%):   R$ {q1:,.2f}")
    print(f"• Terceiro Quartil (Q3 - 75%):   R$ {q3:,.2f}")
    print(f"• Intervalo Interquartil (IQR):  R$ {iqr:,.2f}")
    print(f"• Desvio Padrão:                 R$ {std_dev:,.2f}")
    print(f"• Limite Superior para Outliers: R$ {limite_superior:,.2f}")
    print(f"• Total de Outliers Identificados: {qtd_outliers:,} ({pct_outliers:.2f}% dos pedidos)")
    print("=" * 65)


if __name__ == "__main__":
    orders_df = load_orders()
    run_fase_2_analysis(orders_df)