"""
make_dataset.py

Pipeline de sanitização e processamento dos dados brutos de `orders.csv`
para a geração da camada `processed/`.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_ORDERS_PATH = Path('/mnt/c/Users/LecoOliveira/Downloads/1-lh_nautical_csv/orders.csv')
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'


def process_orders(raw_path: Path) -> pd.DataFrame:
    print('⏳ Carregando dados brutos de orders.csv...')
    df = pd.read_csv(raw_path)

    print('🛠️ Convertendo tipos de dados...')
    df['created_at'] = pd.to_datetime(df['created_at'])

    date_cols = [c for c in df.columns if c.endswith('_at') and c != 'created_at']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    print('🏷️ Tratando atribuição de vendedores (salesperson_id)...')
    df['has_salesperson'] = df['salesperson_id'].notnull()
    df['salesperson_id_clean'] = df['salesperson_id'].fillna(-1).astype(int)

    cutoff_date = pd.Timestamp.now()
    print(f'📅 Aplicando marcação de data limite (Cutoff: {cutoff_date.strftime("%Y-%m-%d")})...')
    df['is_future_order'] = df['created_at'] > cutoff_date

    future_count = df['is_future_order'].sum()
    print(f'  - Total de pedidos futuros identificados: {future_count:,}')
    print(f'  - Total de pedidos históricos válidos: {len(df) - future_count:,}')

    return df


def save_processed_data(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_output = output_dir / 'orders_processed.csv'
    parquet_output = output_dir / 'orders_processed.parquet'

    print(f'💾 Salvando arquivo CSV limpo em: {csv_output}')
    df.to_csv(csv_output, index=False)

    try:
        print(f'💾 Salvando cópia em Parquet em: {parquet_output}')
        df.to_parquet(parquet_output, index=False)
    except Exception as e:
        print(f'⚠️ Não foi possível salvar em Parquet (pyarrow/fastparquet ausente): {e}')

    print('✅ Processamento concluído com sucesso!')


if __name__ == '__main__':
    df_processed = process_orders(RAW_ORDERS_PATH)
    save_processed_data(df_processed, PROCESSED_DIR)
