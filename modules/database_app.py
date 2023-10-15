# import platform
import psycopg2

# other modules
# from psycopg2 import sql
from dotenv import load_dotenv
from contextlib import contextmanager
# from psycopg2.extras import execute_values

# get data from .env file
load_dotenv()

# variables
WINDOWS_DATABASE_PATH = "c:\\Users\\jeanl\\OneDrive\\Bureau\\TRAINING-SCRAPER\\database\\immoscraper.db"
LINUX_DATABASE_PATH = "/home/jean-louis/Bureau/TRAINING-SCRAPER/database/immoscraper.db"

connection = psycopg2.connect(WINDOWS_DATABASE_PATH)

# create database
CREATE_COURSE_TABLE = """CREATE TABLE IF NOT EXISTS courses (
                                id INTEGER NOT NULL PRIMARY KEY,
                                places_available INTEGER,
                                places_total INTEGER,
                                price INTEGER,
                                date_add_to_db TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (town_id) REFERENCES towns(id),
                                FOREIGN KEY (type_id) REFERENCES types(id),
                                FOREIGN KEY (organism_id) REFERENCES organisms(id),
                                FOREIGN KEY (department_id) REFERENCES departments(id),
                                FOREIGN KEY (date_id) REFERENCES dates(id) ON DELETE CASCADE,
                        );"""

CREATE_DATE_TABLE = """CREATE TABLE IF NOT EXISTS dates (
                                    training_id INTEGER,
                                    hour_start TEXT,
                                    hour_end TEXT,
                                    date TIMESTAMP);"""

CREATE_TRAINING_TABLE = """CREATE TABLE IF NOT EXISTS trainings (
                                    id INTEGER NOT NULL PRIMARY KEY,
                                    name TEXT UNIQUE,
                                    description LONGTEXT);"""

CREATE_DEPARTMENT_TABLE = """CREATE TABLE IF NOT EXISTS departments (
                            id INTEGER NOT NULL PRIMARY KEY,
                            number INTEGER PRIMARY KEY,
                            name TEXT UNIQUE);"""

CREATE_TOWN_TABLE = """CREATE TABLE IF NOT EXISTS towns (
                            id INTEGER NOT NULL PRIMARY KEY,
                            postcode TEXT,
                            name TEXT UNIQUE);"""

CREATE_ORGANISMS_TABLE = """CREATE TABLE IF NOT EXISTS organisms (
                            id INTEGER NOT NULL PRIMARY KEY,
                            name TEXT UNIQUE);"""

# add data
INSERT_COURSE = """
                    INSERT INTO courses (places_available, places_total, price, date_add_to_db, town_id, training_id,
                    organism_id, department_id, date_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;"""
INSERT_DATE = """
                INSERT INTO courses (training_id, hour_start, hour_end)
                VALUES (%s, %s, %s)
                RETURNING id;"""
INSERT_TRAINING = """
                    INSERT INTO courses (name, description)
                    VALUES (%s, %s)
                    RETURNING id;"""
INSERT_DEPARTMENT = """
                        INSERT INTO courses (number, name)
                        VALUES (%s, %s)
                        RETURNING id;"""
INSERT_TOWN = """
                INSERT INTO courses (postcode, name)
                VALUES (%s, %s)
                RETURNING id;"""
INSERT_ORGANISM = """
                    INSERT INTO courses (name)
                    VALUES (%s)
                    RETURNING id;"""

# get data
GET_COURSE = "SELECT * FROM properties #####;"
GET_TYPE = "SELECT * FROM types #####;"

# update data
UPDATE_COURSE = """UPDATE trainings
                    SET price = ?
                    WHERE id = ?;"""


# delete data
DELETE_COURSE_TABLE = "DELETE FROM courses;"
DELETE_DATE_TABLE = "DELETE FROM dates;"
DELETE_TRAINING_TABLE = "DELETE FROM trainings;"
DELETE_DEPARTMENT_TABLE = "DELETE FROM departments;"
DELETE_TOWN_TABLE = "DELETE FROM towns;"
DELETE_ORGANISMS_TABLE = "DELETE FROM organism;"


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


def create_tables():
    with get_cursor(connection) as cursor:
        print("Creating tables...")
        cursor.execute(CREATE_COURSE_TABLE)
        cursor.execute(CREATE_DATE_TABLE)
        cursor.execute(CREATE_TRAINING_TABLE)
        cursor.execute(CREATE_DEPARTMENT_TABLE)
        cursor.execute(CREATE_TOWN_TABLE)
        cursor.execute(CREATE_ORGANISMS_TABLE)
        print("Tables created.")


def delete_tables():
    with get_cursor(connection) as cursor:
        print("deleting tables...")
        connection.execute(DELETE_COURSE_TABLE)
        connection.execute(DELETE_DATE_TABLE)
        connection.execute(DELETE_TRAINING_TABLE)
        connection.execute(DELETE_DEPARTMENT_TABLE)
        connection.execute(DELETE_TOWN_TABLE)
        connection.execute(DELETE_ORGANISMS_TABLE)
        print("Tables deleted.")


def add_course(
        places_available: int,
        places_total: int,
        price: int,
        date_add_to_db: float,
        town_id: int,
        type_id: int,
        organism_id: int,
        department_id: int,
        date_id: int):
    with get_cursor(connection) as cursor:
        connection.execute(INSERT_COURSE, (
                                            places_available,
                                            places_total,
                                            price,
                                            date_add_to_db,
                                            town_id,
                                            type_id,
                                            organism_id,
                                            department_id,
                                            date_id
                                            )
                           )
        last_inserted_id = cursor.lastrowid
    return last_inserted_id


def add_date(
                    hour_start: str,
                    hour_end: str,
                    date: float):
    with get_cursor(connection) as cursor:
        connection.execute(INSERT_DATE, (
                                            hour_start,
                                            hour_end,
                                            date
                                            )
                           )
        last_inserted_id = cursor.lastrowid
    return last_inserted_id


def add_training(
                    name: str,
                    description: str):
    with get_cursor(connection) as cursor:
        connection.execute(INSERT_TRAINING, (
                                            name,
                                            description,
                                            )
                           )
        last_inserted_id = cursor.lastrowid
    return last_inserted_id


def add_department(
                    number: str,
                    name: str):
    with get_cursor(connection) as cursor:
        connection.execute(INSERT_DEPARTMENT, (
                                            name,
                                            number,
                                            )
                           )
        last_inserted_id = cursor.lastrowid
    return last_inserted_id


def add_town(
                name: str):
    with get_cursor(connection) as cursor:
        connection.execute(INSERT_DEPARTMENT, (
                                            name,
                                            )
                           )
        last_inserted_id = cursor.lastrowid
    return last_inserted_id


def add_organism(
                    name: str):
    with get_cursor(connection) as cursor:
        connection.execute(INSERT_DEPARTMENT, (
                                            name,
                                            )
                           )
        last_inserted_id = cursor.lastrowid
    return last_inserted_id
