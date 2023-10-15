import os
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from dotenv import load_dotenv

DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file: "

db_params = {
    'dbname': 'trainingscraper',
    'user': 'postgres',
    'password': os.environ["DATABASE_PASSWORD"],
    'host': 'localhost',
    'port': '5432'
}

database_uri = input(DATABASE_PROMPT)
if not database_uri:
    load_dotenv()
    database_uri = os.environ["DATABASE_URI"]

# pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_uri)
pool = SimpleConnectionPool(minconn=1, maxconn=10, **db_params)


# context manager
@contextmanager
def get_connection():
    connection = pool.getconn()
    try:
        yield connection
    finally:
        pool.putconn()
