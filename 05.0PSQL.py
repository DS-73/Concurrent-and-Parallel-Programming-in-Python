import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

def create_table(cur):
    query = """create table prices(
                id serial primary key,
                symbol text,
                price float,
                extracted_time timestamp
    )"""

    response = cur.execute(query)
    print(response)


def main():
    conn = psycopg2.connect(f'postgres://{os.getenv("PSQL_USER")}:{os.getenv("PSQL_PASS")}@pg-2cfd852e-testingp348-273c.c.aivencloud.com:14375/defaultdb?sslmode=require')

    query_sql = 'SELECT VERSION()'

    cur = conn.cursor()
    cur.execute(query_sql)

    version = cur.fetchone()[0]
    print(version)

    
    # create_table(cur)


if __name__ == "__main__":
    main()