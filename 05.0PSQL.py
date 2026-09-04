"""
PostgreSQL Connection Test

This module tests basic PostgreSQL connectivity using psycopg2 and SQLAlchemy.
It demonstrates connection, version query, and table operations.

Purpose:
    - Verify database connectivity and credentials
    - Demonstrate psycopg2 connection pattern
    - Show table creation and deletion (commented out)

Environment Variables Required (in .env):
    - PSQL_USER: Database username
    - PSQL_PASS: Database password
    - PSQL_HOST: Database host
    - PSQL_PORT: Database port
    - PSQL_DB: Database name
    - PSQL_MODE: SSL mode (e.g., require)

Dependencies:
    - psycopg2: PostgreSQL adapter
    - python-dotenv: Environment variable loading
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def create_table(cur: psycopg2.extensions.cursor) -> None:
    """
    Create the prices table if it doesn't exist.

    Args:
        cur: Active database cursor.
    """
    query = """
        CREATE TABLE prices(
            id SERIAL PRIMARY KEY,
            symbol TEXT,
            price FLOAT,
            extracted_time TIMESTAMP
        )
    """
    cur.execute(query)
    print("Table created successfully")


def delete_table(cur: psycopg2.extensions.cursor) -> None:
    """
    Delete all rows from the prices table (truncate).

    Args:
        cur: Active database cursor.
    """
    query = "DELETE FROM prices;"
    cur.execute(query)
    print("Table cleared")


def main() -> None:
    """
    Test PostgreSQL connection and perform basic operations.

    Connects to Aiven PostgreSQL, prints server version,
    and optionally creates/clears the prices table.
    """
    # Connection string for Aiven PostgreSQL with SSL
    conn = psycopg2.connect(
        f'postgres://{os.getenv("PSQL_USER")}:{os.getenv("PSQL_PASS")}'
        f'@pg-2cfd852e-testingp348-273c.c.aivencloud.com:14375/defaultdb?sslmode=require'
    )

    query_sql = 'SELECT VERSION()'
    cur = conn.cursor()
    cur.execute(query_sql)

    version = cur.fetchone()[0]
    print(f"PostgreSQL Version: {version}")

    # Uncomment to create table
    # create_table(cur)
    delete_table(cur)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()