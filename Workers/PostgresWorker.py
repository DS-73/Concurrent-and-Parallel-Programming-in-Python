"""
PostgreSQL Worker Classes

This module provides thread-based workers for PostgreSQL database operations.
Used in the stock price pipeline for concurrent database writes.

Classes:
    - PostgresMasterScheduler: Thread that consumes queue and delegates to PostgresWorker
    - PostgresWorker: Handles individual insert/select operations

Design:
    - Scheduler runs as daemon thread, continuously processing queue
    - Worker encapsulates single-record database operations
    - SQLAlchemy engine shared for connection pooling
    - Sentinel (None) pattern for graceful shutdown
"""

import os
import threading
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text

load_dotenv()


def create_psql_engine() -> Engine:
    """
    Build a SQLAlchemy engine from environment variables.

    Required environment variables:
        PSQL_USER: Database username
        PSQL_PASS: Database password
        PSQL_HOST: Database host
        PSQL_PORT: Database port
        PSQL_DB: Database name
        PSQL_MODE: SSL mode (e.g., require)

    Returns:
        Configured SQLAlchemy Engine instance.
    """
    user = os.environ.get("PSQL_USER")
    password = os.environ.get("PSQL_PASS")
    host = os.environ.get("PSQL_HOST")
    port = os.environ.get("PSQL_PORT")
    db = os.environ.get("PSQL_DB")
    mode = os.environ.get("PSQL_MODE")

    return create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}?{mode}"
    )


class PostgresMasterScheduler(threading.Thread):
    """
    Thread that consumes price data from a queue and inserts into PostgreSQL.

    Runs continuously until receiving None sentinel. Each queue item
    is delegated to a PostgresWorker for the actual database operation.

    Attributes:
        _input_queue: Queue containing (symbol, price, extracted_time) tuples.
        _engine: Shared SQLAlchemy engine for database connections.
    """

    def __init__(self, input_queue, **kwargs) -> None:
        """
        Initialize scheduler with input queue.

        Args:
            input_queue: multiprocessing.Queue with price data.
            **kwargs: Additional Thread arguments (e.g., daemon=True).
        """
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self._engine = create_psql_engine()
        self.start()  # Auto-start thread on creation

    def run(self) -> None:
        """
        Main thread loop: process queue items until sentinel received.

        For each item:
        1. Get (symbol, price, extracted_time) from queue
        2. If None: break (shutdown signal)
        3. Create PostgresWorker and insert
        4. Catch exceptions to keep scheduler alive
        """
        while True:
            val = self._input_queue.get()
            print(f"Scheduler received: {val}")

            if val is None:
                print("Scheduler received shutdown signal")
                break

            symbol, price, extracted_time = val
            try:
                postgres_worker = PostgresWorker(
                    symbol, price, extracted_time, self._engine
                )
                postgres_worker._insert_into_db()
            except Exception as e:
                # Log error but continue processing remaining items
                print(f"Error inserting {symbol}: {e}")


class PostgresWorker:
    """
    Handles individual stock price database operations.

    Encapsulates insert and select queries for the prices table.
    Can use shared engine or create its own.

    Attributes:
        _symbol: Stock symbol.
        _price: Current price.
        _extracted_time: Timestamp of price extraction.
        _engine: SQLAlchemy engine for database connection.
    """

    def __init__(
        self,
        symbol: str,
        price: float,
        extracted_time: str,
        engine: Optional[Engine] = None
    ) -> None:
        """
        Initialize worker with stock data.

        Args:
            symbol: Stock ticker symbol.
            price: Current price.
            extracted_time: Extraction timestamp (ISO format string).
            engine: Optional shared SQLAlchemy engine.
        """
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time
        self._engine = engine if engine is not None else create_psql_engine()

    def _create_insert_query(self) -> str:
        """
        Generate parameterized INSERT query.

        Returns:
            SQL query string with named parameters.
        """
        return (
            "INSERT INTO prices(symbol, price, extracted_time) "
            "VALUES(:symbol, :price, :extracted_time)"
        )

    def _insert_into_db(self) -> None:
        """Execute insert query with current stock data."""
        query = self._create_insert_query()

        with self._engine.connect() as conn:
            response = conn.execute(
                text(query),
                {
                    "symbol": self._symbol,
                    "price": self._price,
                    "extracted_time": self._extracted_time
                }
            )
            conn.commit()
            print(f"Inserted {response.rowcount} row(s) for {self._symbol}")

    def _create_select_query(self) -> str:
        """
        Generate SELECT all query.

        Returns:
            SQL query string.
        """
        return "SELECT * FROM prices"

    def _select_from_db(self) -> None:
        """Execute select query and print all rows."""
        query = self._create_select_query()

        with self._engine.connect() as conn:
            response = conn.execute(text(query))
            rows = response.fetchall()

            print("Table Data")
            print("-" * 30)
            for row in rows:
                print(row)
            print("-" * 30)