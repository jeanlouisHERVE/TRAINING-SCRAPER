import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from dotenv import load_dotenv

db_params = {
    'dbname': 'trainingscraper',
    'user': os.environ["DATABASE_USER"],
    'password': os.environ["DATABASE_PASSWORD"],
    'host': os.environ["DATABASE_HOST"],
    'port': os.environ["DATABASE_PORT"]
}

load_dotenv()
database_uri = os.environ["DATABASE_URI"]

# pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_uri)
try:
    pool = SimpleConnectionPool(minconn=1, maxconn=10, **db_params)
except psycopg2.OperationalError as e:
    print(f"Error creating the connection pool: {e}")
    exit(1)


# context manager
@contextmanager
def get_connection():
    try:
        connection = pool.getconn()
        yield connection
    except Exception as e:
        print(f"Error getting a database connection: {e}")
    finally:
        pool.putconn(connection)
