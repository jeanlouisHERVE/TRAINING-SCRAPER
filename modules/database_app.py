# import platform
import psycopg2

# other modules
from psycopg2 import sql
from dotenv import load_dotenv

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
                            postcode TEST,
                            name TEXT UNIQUE);"""

CREATE_ORGANISMS_TABLE = """CREATE TABLE IF NOT EXISTS organisms (
                            id INTEGER NOT NULL PRIMARY KEY,
                            name TEXT UNIQUE);"""

# add data
INSERT_COURSE = """
                    INSERT INTO courses (places_available, places_total, date_add_to_db, town_id, training_id,
                    organism_id, department_id, date_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;"""
INSERT_DATE = ""
INSERT_TRAINING = ""
INSERT_DEPARTMENT = ""
INSERT_TOWN = ""
INSERT_ORGANISM = ""

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


def create_tables():
    with connection:
        print("Creating tables...")
        connection.execute(CREATE_COURSE_TABLE)
        connection.execute(CREATE_DATE_TABLE)
        connection.execute(CREATE_TRAINING_TABLE)
        connection.execute(CREATE_DEPARTMENT_TABLE)
        connection.execute(CREATE_TOWN_TABLE)
        connection.execute(CREATE_ORGANISMS_TABLE)
        print("Tables created.")


def delete_tables():
    with connection:
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
        date_add_to_db: float,
        town_id: int,
        type_id: int,
        organism_id: int,
        department_id: int,
        date_id: int):
    with connection:
        cursor = connection.execute(INSERT_COURSE, (
                                                        places_available,
                                                        places_total,
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


def add_training_date():
    pass


def add_training_type():
    pass


def add_training_date():
    pass


def add_training_date():
    pass


def add_training_date():
    pass


# def get_training_by_url(url: str):
#     with connection:
#         cursor = connection.execute(GET_TRAINING, (url,))
#         return cursor.fetchone()


# def delete_property(id: int):
#     try:
#         with connection:
#             connection.execute(DELETE_T, (id, ))
#         print(f"OK : Property {id} has been deleted successfully.")
#     except sqlite3.Error as e:
#         print(f"KO : Error deleting property {id}: {e}")
