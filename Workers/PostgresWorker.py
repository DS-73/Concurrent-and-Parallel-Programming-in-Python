import os
import threading

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.sql import text

load_dotenv()


def create_psql_engine():
    """Build a SQLAlchemy engine from environment variables."""
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
    def __init__(self, input_queue, **kwargs):
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self._engine = create_psql_engine()
        self.start()

    def run(self):
        while True:
            val = self._input_queue.get()
            print(val)
            if val is None:
                break

            symbol, price, extracted_time = val
            try:
                postgresWorker = PostgresWorker(symbol, price, extracted_time, self._engine)
                postgresWorker._insert_into_db()
            except Exception as e:
                # Keep the worker alive so remaining queue items are processed
                print(f"Error inserting {symbol}: {e}")

class PostgresWorker:
    def __init__(self, symbol, price, extracted_time, engine=None):
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time
        self._engine = engine if engine is not None else create_psql_engine()

    def _create_insert_query(self):
        query = "Insert into prices(symbol, price, extracted_time) VALUES(:symbol, :price, :extracted_time)"
        return query

    def _insert_into_db(self):
        query = self._create_insert_query()

        with self._engine.connect() as conn:
            response = conn.execute(text(query), {"symbol": self._symbol, "price": self._price, "extracted_time": self._extracted_time})

            conn.commit()
            print(f"Inserted {response.rowcount} row(s)")
        
    
    def _create_select_query(self):
        query = "SELECT * FROM PRICES"
        return query

    def _select_from_db(self):
        query = self._create_select_query()

        with self._engine.connect() as conn:
            response = conn.execute(text(query))
            rows = response.fetchall()

            print("Table Data")
            print("-" * 30)
            for row in rows:
                print(row)
            print("-" * 30)
