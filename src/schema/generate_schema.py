"""
Módulo responsável pela geração automática do schema PostgreSQL
a partir dos arquivos CSV da LH Nautical.

Questão 2 — Schema

Responsabilidades deste módulo:
- localizar todos os arquivos CSV;
- identificar tabelas e colunas;
- analisar os valores de cada coluna;
- inferir tipos compatíveis com PostgreSQL;
- aplicar regras semânticas para identificadores;
- gerar um único arquivo schema.sql com um CREATE TABLE
  para cada arquivo CSV encontrado.

Importante:
Este módulo utiliza somente bibliotecas padrão do Python 3,
conforme exigido pelo desafio.
"""

import csv
from datetime import datetime
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO
# ============================================================

CSV_DIRECTORY = Path(
    "/mnt/c/Users/LecoOliveira/Downloads/1-lh_nautical_csv"
)

OUTPUT_SQL = Path("sql/schema.sql")


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

    Parameters
    ----------
    directory : Path
        Diretório onde estão os arquivos CSV.

    Returns
    -------
    list[Path]
        Lista ordenada com os arquivos CSV encontrados.
    """

    if not directory.exists():
        raise FileNotFoundError(
            f"Diretório não encontrado: {directory}"
        )

    return sorted(directory.glob("*.csv"))


# ============================================================
# FUNÇÕES AUXILIARES DE DETECÇÃO DE TIPO
# ============================================================

def is_boolean(value: str) -> bool:
    """
    Verifica se o valor pode ser interpretado como booleano.
    """

    return value.lower() in {
        "true",
        "false",
    }


def is_integer(value: str) -> bool:
    """
    Verifica se o valor pode ser interpretado como inteiro.
    """

    try:
        int(value)
        return True
    except ValueError:
        return False


def is_numeric(value: str) -> bool:
    """
    Verifica se o valor pode ser interpretado como número decimal.
    """

    try:
        float(value)
        return True
    except ValueError:
        return False


def is_date(value: str) -> bool:
    """
    Verifica se o valor possui formato de data YYYY-MM-DD.
    """

    try:
        datetime.strptime(
            value,
            "%Y-%m-%d"
        )
        return True
    except ValueError:
        return False


def is_timestamp(value: str) -> bool:
    """
    Verifica se o valor possui formato de data e hora.
    """

    timestamp_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
    ]

    for timestamp_format in timestamp_formats:
        try:
            datetime.strptime(
                value,
                timestamp_format
            )
            return True
        except ValueError:
            continue

    return False


# ============================================================
# CLASSIFICAÇÃO DE UM VALOR
# ============================================================

def detect_value_type(value: str) -> str | None:
    """
    Detecta o tipo PostgreSQL mais provável para um valor.

    Valores vazios são ignorados porque não devem definir
    o tipo da coluna.
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
    new_type: str | None
) -> str | None:
    """
    Combina os tipos encontrados em diferentes linhas
    da mesma coluna.
    """

    if new_type is None:
        return current_type

    if current_type is None:
        return new_type

    if current_type == new_type:
        return current_type

    numeric_types = {
        "BIGINT",
        "NUMERIC",
    }

    if (
        current_type in numeric_types
        and new_type in numeric_types
    ):
        return "NUMERIC"

    return "TEXT"


# ============================================================
# REGRA SEMÂNTICA PARA IDENTIFICADORES
# ============================================================

def is_text_identifier(column_name: str) -> bool:
    """
    Verifica se a coluna representa um identificador textual.
    """

    return column_name.lower() in TEXT_IDENTIFIER_COLUMNS


# ============================================================
# INFERÊNCIA DOS TIPOS DE UMA TABELA
# ============================================================

def infer_csv_types(
    file_path: Path
) -> dict[str, str]:
    """
    Analisa as linhas do CSV e infere o tipo de cada coluna.
    """

    with file_path.open(
        mode="r",
        encoding="utf-8",
        newline=""
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

                if is_text_identifier(column):
                    inferred_types[column] = "TEXT"
                    continue

                detected_type = detect_value_type(
                    value
                )

                inferred_types[column] = merge_types(
                    inferred_types[column],
                    detected_type
                )

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
    columns: dict[str, str]
) -> str:
    """
    Monta a instrução CREATE TABLE de uma tabela.

    Parameters
    ----------
    table_name : str
        Nome da tabela.

    columns : dict[str, str]
        Dicionário contendo nome da coluna e tipo PostgreSQL.

    Returns
    -------
    str
        Instrução SQL completa da tabela.
    """

    lines = []

    lines.append(
        f"CREATE TABLE {table_name} ("
    )

    column_definitions = []

    for column_name, column_type in columns.items():
        column_definitions.append(
            f"    {column_name} {column_type}"
        )

    lines.append(
        ",\n".join(column_definitions)
    )

    lines.append(");")

    return "\n".join(lines)


# ============================================================
# GERAÇÃO DO ARQUIVO schema.sql
# ============================================================

def generate_schema(
    csv_files: list[Path],
    output_path: Path
) -> None:
    """
    Gera um único arquivo schema.sql com todos os CREATE TABLE.

    Parameters
    ----------
    csv_files : list[Path]
        Lista dos CSVs que serão processados.

    output_path : Path
        Caminho do arquivo SQL de saída.
    """

    # Garante que a pasta sql exista.
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    create_statements = []

    for csv_file in csv_files:

        # O nome do CSV sem extensão vira o nome da tabela.
        table_name = csv_file.stem

        # Infere os tipos das colunas.
        inferred_types = infer_csv_types(
            csv_file
        )

        # Monta o CREATE TABLE.
        create_table_sql = build_create_table(
            table_name,
            inferred_types
        )

        create_statements.append(
            create_table_sql
        )

    # Cabeçalho informativo do arquivo.
    header = """\
-- ============================================================
-- Desafio Lighthouse — Dados & IA
-- Questão 2 — Schema PostgreSQL
--
-- Arquivo gerado automaticamente por:
-- src/schema/generate_schema.py
--
-- Cada arquivo CSV de origem gera uma tabela PostgreSQL.
-- ============================================================

"""

    # Separa cada CREATE TABLE por duas quebras de linha.
    schema_content = (
        header
        + "\n\n".join(create_statements)
        + "\n"
    )

    # Salva o arquivo final.
    output_path.write_text(
        schema_content,
        encoding="utf-8"
    )


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main() -> None:
    """
    Executa todo o processo de geração do schema PostgreSQL.
    """

    csv_files = find_csv_files(
        CSV_DIRECTORY
    )

    print("=" * 70)
    print("QUESTÃO 2 — GERAÇÃO DO SCHEMA POSTGRESQL")
    print("=" * 70)

    print(
        f"\nArquivos CSV encontrados: "
        f"{len(csv_files)}"
    )

    generate_schema(
        csv_files,
        OUTPUT_SQL
    )

    print(
        f"\nSchema gerado com sucesso: "
        f"{OUTPUT_SQL}"
    )

    print(
        f"Tabelas geradas: "
        f"{len(csv_files)}"
    )


# ============================================================
# PONTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    main()