import argparse
from pathlib import Path

import psycopg
from psycopg import sql

from config import DATABASE_CONFIG


ROOT = Path(__file__).resolve().parent
SCHEMA_FILE = ROOT / "sql" / "create_schema.sql"
SEED_FILE = ROOT / "sql" / "seed_ecommerce.sql"


def load_sql_file(connection: psycopg.Connection, path: Path) -> None:
    connection.execute(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Crée la base PostgreSQL et charge le schéma et les données."
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="supprime puis recrée la base existante (destructif)",
    )
    args = parser.parse_args()

    database_name = DATABASE_CONFIG["dbname"]
    if database_name == "postgres":
        parser.error("DB_NAME ne peut pas être la base système 'postgres'.")

    if args.reset and input(
        f"Tapez {database_name} pour confirmer sa suppression : "
    ) != database_name:
        parser.error("Confirmation incorrecte ; aucune modification effectuée.")

    maintenance_config = {**DATABASE_CONFIG, "dbname": "postgres"}
    with psycopg.connect(**maintenance_config, autocommit=True) as connection:
        database_exists = connection.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", (database_name,)
        ).fetchone()

        if database_exists and not args.reset:
            parser.error(
                f"La base {database_name!r} existe déjà. "
                "Relancez avec --reset pour la remplacer."
            )

        if database_exists:
            connection.execute(
                sql.SQL("DROP DATABASE {}").format(sql.Identifier(database_name))
            )
        connection.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name))
        )

    with psycopg.connect(**DATABASE_CONFIG, autocommit=True) as connection:
        load_sql_file(connection, SCHEMA_FILE)
        print("Schéma créé.")
        load_sql_file(connection, SEED_FILE)
        print("Jeu de données chargé.")

    print(f"Base {database_name!r} prête.")


if __name__ == "__main__":
    main()
