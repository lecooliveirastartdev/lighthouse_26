"""
Questão 3 — Carregamento dos CSVs no PostgreSQL.

Objetivo:
Ler todos os arquivos CSV de um diretório e carregar seus dados
nas tabelas correspondentes do PostgreSQL.

Premissas do desafio:
- utilizar Python 3;
- carregar todos os CSVs;
- não remover valores nulos;
- não corrigir caracteres especiais;
- preservar os dados brutos;
- utilizar o schema criado anteriormente.

Bibliotecas:
- csv, sys e pathlib: bibliotecas padrão do Python;
- psycopg: biblioteca utilizada para conexão com PostgreSQL.

Uso:
    python load_csvs.py \
        <diretorio_dos_csvs> \
        <host> \
        <porta> \
        <banco> \
        <usuario> \
        <senha>

Exemplo:
    python load_csvs.py \
        ./csvs \
        localhost \
        5432 \
        lh_nautical \
        lighthouse \
        lighthouse123
"""

import csv
import sys
from pathlib import Path

import psycopg
from psycopg import sql


# ============================================================
# LOCALIZAÇÃO DOS CSVs
# ============================================================

def find_csv_files(directory: Path) -> list[Path]:
    """
    Localiza todos os arquivos CSV existentes no diretório.
    """

    if not directory.exists():
        raise FileNotFoundError(
            f"Diretório não encontrado: {directory}"
        )

    if not directory.is_dir():
        raise NotADirectoryError(
            f"O caminho informado não é um diretório: {directory}"
        )

    csv_files = sorted(directory.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"Nenhum arquivo CSV encontrado em: {directory}"
        )

    return csv_files


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

    Os dados da conexão são recebidos em tempo de execução,
    evitando dependência de configurações específicas da
    máquina onde o script foi desenvolvido.
    """

    return psycopg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )


# ============================================================
# PREPARAÇÃO DOS VALORES
# ============================================================

def prepare_value(value: str):
    """
    Prepara o valor do CSV para inserção no PostgreSQL.

    Não é realizada limpeza ou correção do conteúdo.

    String vazia é representada como None para que o PostgreSQL
    registre a ausência de valor como NULL.
    """

    if value == "":
        return None

    return value


# ============================================================
# CARREGAMENTO DE UM CSV
# ============================================================

def load_csv(
    connection,
    file_path: Path,
) -> int:
    """
    Carrega um arquivo CSV na tabela de mesmo nome.

    Exemplo:
        orders.csv -> tabela orders

    Retorna a quantidade de registros inseridos.
    """

    table_name = file_path.stem

    with file_path.open(
        mode="r",
        encoding="utf-8",
        newline="",
    ) as csv_file:

        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise ValueError(
                f"CSV sem cabeçalho: {file_path}"
            )

        columns = reader.fieldnames

        insert_query = sql.SQL(
            "INSERT INTO {} ({}) VALUES ({})"
        ).format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(
                sql.Identifier(column)
                for column in columns
            ),
            sql.SQL(", ").join(
                sql.Placeholder()
                for _ in columns
            ),
        )

        inserted_rows = 0

        with connection.cursor() as cursor:

            for row in reader:

                values = [
                    prepare_value(row[column])
                    for column in columns
                ]

                cursor.execute(
                    insert_query,
                    values,
                )

                inserted_rows += 1

    return inserted_rows


# ============================================================
# CARREGAMENTO DE TODOS OS CSVs
# ============================================================

def load_all_csvs(
    csv_directory: Path,
    host: str,
    port: int,
    dbname: str,
    user: str,
    password: str,
) -> dict[str, int]:
    """
    Carrega todos os CSVs encontrados no diretório.

    Retorna:
        nome da tabela -> quantidade de registros inseridos
    """

    csv_files = find_csv_files(csv_directory)

    results = {}

    with connect_database(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    ) as connection:

        for csv_file in csv_files:

            table_name = csv_file.stem

            print(
                f"Carregando tabela: {table_name}..."
            )

            inserted_rows = load_csv(
                connection,
                csv_file,
            )

            results[table_name] = inserted_rows

            print(
                f"  Registros inseridos: {inserted_rows}"
            )

        connection.commit()

    return results


# ============================================================
# ARGUMENTOS DA LINHA DE COMANDO
# ============================================================

def parse_arguments():
    """
    Obtém os parâmetros necessários para executar a carga.

    Argumentos:
    1. diretório dos CSVs;
    2. host PostgreSQL;
    3. porta PostgreSQL;
    4. banco de dados;
    5. usuário;
    6. senha.
    """

    if len(sys.argv) != 7:
        print(
            "Uso: python load_csvs.py "
            "<diretorio_dos_csvs> "
            "<host> "
            "<porta> "
            "<banco> "
            "<usuario> "
            "<senha>"
        )
        sys.exit(1)

    csv_directory = Path(sys.argv[1])
    host = sys.argv[2]

    try:
        port = int(sys.argv[3])
    except ValueError:
        print(
            "Erro: a porta deve ser um número inteiro."
        )
        sys.exit(1)

    dbname = sys.argv[4]
    user = sys.argv[5]
    password = sys.argv[6]

    return (
        csv_directory,
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
    Executa o processo completo de carregamento.
    """

    (
        csv_directory,
        host,
        port,
        dbname,
        user,
        password,
    ) = parse_arguments()

    print("=" * 70)
    print("QUESTÃO 3 — CARREGAMENTO DOS CSVs NO POSTGRESQL")
    print("=" * 70)

    print(f"Banco de destino: {dbname}")
    print(f"Host: {host}:{port}")
    print()

    try:
        results = load_all_csvs(
            csv_directory=csv_directory,
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
        )

    except (
        FileNotFoundError,
        NotADirectoryError,
        ValueError,
        psycopg.Error,
    ) as error:

        print(f"\nErro: {error}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("CARREGAMENTO CONCLUÍDO")
    print("=" * 70)

    total_rows = 0

    for table_name, row_count in results.items():

        print(
            f"{table_name:<30} "
            f"{row_count:>10} registros"
        )

        total_rows += row_count

    print("-" * 70)
    print(
        f"Total de tabelas: {len(results)}"
    )
    print(
        f"Total de registros carregados: {total_rows}"
    )


# ============================================================
# PONTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    main()