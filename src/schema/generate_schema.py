"""
Módulo responsável pela geração automática do schema PostgreSQL
a partir dos arquivos CSV da LH Nautical.

Questão 2 — Schema

Uso:
    python generate_schema.py <diretorio_dos_csvs> [arquivo_saida]

Exemplo:
    python generate_schema.py data/raw sql/schema.sql

Responsabilidades:
- localizar todos os arquivos CSV;
- identificar tabelas e colunas;
- inferir tipos compatíveis com PostgreSQL;
- aplicar regras semânticas para identificadores;
- gerar um único arquivo schema.sql.

Importante:
Este módulo utiliza somente bibliotecas padrão do Python 3,
conforme exigido pelo desafio.
"""

import csv
import sys
from datetime import datetime
from pathlib import Path


# ============================================================
# COLUNAS QUE DEVEM SER TRATADAS COMO TEXTO
# ============================================================

TEXT_IDENTIFIER_COLUMNS = {
    "cpf",
    "tax_id",
    "phone",
    "postal_code",
    "barcode_ean",
    "nfe_access_key",
    "ncm_code",
    "state_registration",
}


# ============================================================
# LOCALIZAÇÃO DOS ARQUIVOS CSV
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
# DETECÇÃO DE TIPOS
# ============================================================

def is_boolean(value: str) -> bool:
    """Verifica se o valor representa um booleano."""
    return value.lower() in {"true", "false"}


def is_integer(value: str) -> bool:
    """Verifica se o valor representa um número inteiro."""
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_numeric(value: str) -> bool:
    """Verifica se o valor representa um número decimal."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_date(value: str) -> bool:
    """Verifica se o valor possui formato YYYY-MM-DD."""
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_timestamp(value: str) -> bool:
    """Verifica se o valor possui formato de data e hora."""

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
    ]

    for timestamp_format in formats:
        try:
            datetime.strptime(value, timestamp_format)
            return True
        except ValueError:
            continue

    return False


def detect_value_type(value: str) -> str | None:
    """
    Detecta o tipo PostgreSQL mais provável para um valor.
    """

    value = value.strip()

    if value == "":
        return None

    if is_boolean(value):
        return "BOOLEAN"

    if is_integer(value):
        return "BIGINT"

    if is_numeric(value):
        return "NUMERIC"

    if is_timestamp(value):
        return "TIMESTAMP"

    if is_date(value):
        return "DATE"

    return "TEXT"


# ============================================================
# CONSOLIDAÇÃO DOS TIPOS
# ============================================================

def merge_types(
    current_type: str | None,
    new_type: str | None,
) -> str | None:
    """
    Consolida os tipos encontrados nas linhas de uma coluna.
    """

    if new_type is None:
        return current_type

    if current_type is None:
        return new_type

    if current_type == new_type:
        return current_type

    numeric_types = {"BIGINT", "NUMERIC"}

    if (
        current_type in numeric_types
        and new_type in numeric_types
    ):
        return "NUMERIC"

    return "TEXT"


# ============================================================
# REGRA SEMÂNTICA
# ============================================================

def is_text_identifier(column_name: str) -> bool:
    """
    Identifica campos que, mesmo contendo apenas números,
    devem ser armazenados como texto.
    """

    return column_name.lower() in TEXT_IDENTIFIER_COLUMNS


# ============================================================
# INFERÊNCIA DOS TIPOS DE UMA TABELA
# ============================================================

def infer_csv_types(file_path: Path) -> dict[str, str]:
    """
    Analisa o CSV e infere o tipo PostgreSQL de cada coluna.
    """

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

        inferred_types = {
            column: None
            for column in reader.fieldnames
        }

        for row in reader:

            for column, value in row.items():

                if value is None:
                    continue

                if is_text_identifier(column):
                    inferred_types[column] = "TEXT"
                    continue

                detected_type = detect_value_type(value)

                inferred_types[column] = merge_types(
                    inferred_types[column],
                    detected_type,
                )

    # Colunas totalmente vazias utilizam TEXT como fallback.
    return {
        column: (
            inferred_type
            if inferred_type is not None
            else "TEXT"
        )
        for column, inferred_type in inferred_types.items()
    }


# ============================================================
# GERAÇÃO DO CREATE TABLE
# ============================================================

def build_create_table(
    table_name: str,
    columns: dict[str, str],
) -> str:
    """
    Monta a instrução CREATE TABLE de uma tabela.
    """

    column_definitions = [
        f"    {column_name} {column_type}"
        for column_name, column_type in columns.items()
    ]

    return (
        f"CREATE TABLE {table_name} (\n"
        + ",\n".join(column_definitions)
        + "\n);"
    )


# ============================================================
# GERAÇÃO DO schema.sql
# ============================================================

def generate_schema(
    csv_directory: Path,
    output_path: Path,
) -> int:
    """
    Gera o schema SQL para todos os CSVs encontrados.

    Returns
    -------
    int
        Quantidade de tabelas geradas.
    """

    csv_files = find_csv_files(csv_directory)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    create_statements = []

    for csv_file in csv_files:

        table_name = csv_file.stem

        inferred_types = infer_csv_types(csv_file)

        create_statements.append(
            build_create_table(
                table_name,
                inferred_types,
            )
        )

    header = """\
-- ============================================================
-- Desafio Lighthouse — Dados & IA
-- Questão 2 — Schema PostgreSQL
--
-- Arquivo gerado automaticamente por generate_schema.py
-- ============================================================

"""

    schema_content = (
        header
        + "\n\n".join(create_statements)
        + "\n"
    )

    output_path.write_text(
        schema_content,
        encoding="utf-8",
    )

    return len(csv_files)


# ============================================================
# ARGUMENTOS DA LINHA DE COMANDO
# ============================================================

def parse_arguments() -> tuple[Path, Path]:
    """
    Obtém os caminhos informados na linha de comando.

    Argumento 1:
        diretório contendo os CSVs.

    Argumento 2 (opcional):
        arquivo SQL de saída.

    Se o segundo argumento não for informado,
    utiliza schema.sql no diretório atual.
    """

    if len(sys.argv) < 2:
        print(
            "Uso: python generate_schema.py "
            "<diretorio_dos_csvs> [arquivo_saida]"
        )
        sys.exit(1)

    csv_directory = Path(sys.argv[1])

    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = Path("schema.sql")

    return csv_directory, output_path


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main() -> None:
    """
    Executa o processo completo de geração do schema.
    """

    csv_directory, output_path = parse_arguments()

    print("=" * 70)
    print("QUESTÃO 2 — GERAÇÃO DO SCHEMA POSTGRESQL")
    print("=" * 70)

    try:
        table_count = generate_schema(
            csv_directory,
            output_path,
        )

    except (
        FileNotFoundError,
        NotADirectoryError,
        ValueError,
    ) as error:
        print(f"\nErro: {error}")
        sys.exit(1)

    print(
        f"\nDiretório de origem: {csv_directory}"
    )
    print(
        f"Schema gerado com sucesso: {output_path}"
    )
    print(
        f"Tabelas geradas: {table_count}"
    )


# ============================================================
# PONTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    main()