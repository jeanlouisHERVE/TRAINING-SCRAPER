#!/usr/bin/python
# import platform
import psycopg2

# other modules
from dotenv import load_dotenv
from config import config

# get data from .env file
load_dotenv()

# variables
WINDOWS_DATABASE_PATH = "c:\\Users\\jeanl\\OneDrive\\Bureau\\TRAINING-SCRAPER\\database\\trainingscraper.db"
LINUX_DATABASE_PATH = "/home/jean-louis/Bureau/TRAINING-SCRAPER/database/trainingscraper.db"
config_params = config()


def connect_database(config_params):
    try:
        connection = psycopg2.connect(**config_params)
        return connection
    except psycopg2.OperationalError as e:
        raise ConnectionError(f"Database connection failed: {e}")


# create database
CREATE_COURSES_TABLE = """CREATE TABLE IF NOT EXISTS courses (
                                id SERIAL NOT NULL PRIMARY KEY,
                                places_available INTEGER,
                                places_total INTEGER,
                                price INTEGER,
                                date_add_to_db TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                town_id INTEGER,
                                type_id INTEGER,
                                organism_id INTEGER,
                                FOREIGN KEY (town_id) REFERENCES towns(id),
                                FOREIGN KEY (type_id) REFERENCES types(id),
                                FOREIGN KEY (organism_id) REFERENCES organisms(id));"""

CREATE_DATES_TABLE = """CREATE TABLE IF NOT EXISTS dates (
                            id SERIAL NOT NULL PRIMARY KEY,
                            date TIMESTAMP);"""

CREATE_COURSE_DATE_TIME = """CREATE TABLE IF NOT EXISTS course_date_times (
                                course_id INTEGER,
                                date_id INTEGER,
                                hour_start TIME,
                                hour_end TIME,
                                PRIMARY KEY (course_id, date_id),
                                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                                FOREIGN KEY (date_id) REFERENCES dates(id));"""

CREATE_HOURS_TABLE = """CREATE TABLE IF NOT EXISTS hours (
                            id SERIAL NOT NULL PRIMARY KEY,
                            hour_start TEXT,
                            hour_end TEXT);"""

CREATE_DEPARTMENTS_TABLE = """CREATE TABLE IF NOT EXISTS departments (
                                id SERIAL NOT NULL PRIMARY KEY,
                                number TEXT,
                                name TEXT UNIQUE);"""

CREATE_TOWNS_TABLE = """CREATE TABLE IF NOT EXISTS towns (
                            id SERIAL NOT NULL PRIMARY KEY,
                            postcode TEXT,
                            name TEXT UNIQUE,
                            department_id INTEGER,
                            FOREIGN KEY (department_id) REFERENCES departments(id));"""

CREATE_TYPES_TABLE = """CREATE TABLE IF NOT EXISTS types (
                            id SERIAL NOT NULL PRIMARY KEY,
                            name TEXT UNIQUE,
                            description TEXT);"""

CREATE_ORGANISMS_TABLE = """CREATE TABLE IF NOT EXISTS organisms (
                            id SERIAL NOT NULL PRIMARY KEY,
                            name TEXT UNIQUE);"""

# add data
INSERT_COURSE = """
                    INSERT INTO courses (places_available, places_total, price,
                    date_add_to_db, town_id, type_id,
                    organism_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;"""
INSERT_DATE = """
                INSERT INTO dates (date)
                VALUES (%s)
                RETURNING id;"""
INSERT_COURSE_DATE_TIME = """
                            INSERT INTO course_date_times (course_id, date_id,
                            hour_start, hour_end)
                            VALUES (%s, %s, %s, %s);"""
INSERT_DEPARTMENT = """
                        INSERT INTO departments (number, name)
                        VALUES (%s, %s)
                        RETURNING id;"""
INSERT_TOWN = """
                INSERT INTO towns (postcode, name, department_id)
                VALUES (%s, %s, %s)
                RETURNING id;"""
INSERT_TYPE = """
                INSERT INTO towns (name, description)
                VALUES (%s, %s)
                RETURNING id;"""
INSERT_ORGANISM = """
                    INSERT INTO organisms (name)
                    VALUES (%s)
                    RETURNING id;"""

# get data
GET_COURSES = "SELECT * FROM courses;"
GET_DATES = "SELECT * FROM dates;"
GET_DATE = "SELECT * FROM dates WHERE date = %s;"
GET_COURSE_DATE_TIME = "SELECT * FROM course_date_times WHERE course_id = %s;"
GET_DEPARTMENTS = "SELECT * FROM departments;"
GET_DEPARTMENT_FROM_NUMBER = "SELECT * FROM departments WHERE number = %s;"
GET_TOWNS = "SELECT * FROM towns;"
GET_TOWN_FROM_NAME = "SELECT * FROM towns WHERE name = %s;"
GET_TYPES = "SELECT * FROM types;"
GET_TYPE_FROM_NAME = "SELECT * FROM types WHERE name = %s;"
GET_ORGANISMS = "SELECT * FROM organisms;"
GET_ORGANISM_FROM_NAME = "SELECT * FROM organisms WHERE name = %s;"

# update data
UPDATE_COURSE = """UPDATE trainings
                    SET price = ?
                    WHERE id = ?;"""


# delete data
DELETE_COURSES_TABLE = "DELETE FROM courses;"
DELETE_DATES_TABLE = "DELETE FROM dates;"
DELETE_COURSE_DATE_TIME_TABLE = "DELETE FROM course_date_times;"
DELETE_DEPARTMENTS_TABLE = "DELETE FROM departments;"
DELETE_TOWNS_TABLE = "DELETE FROM towns;"
DELETE_TYPES_TABLE = "DELETE FROM types;"
DELETE_ORGANISMS_TABLE = "DELETE FROM organisms;"


def create_tables():
    commands = (CREATE_DATES_TABLE,
                CREATE_DATES_TABLE,
                CREATE_COURSE_DATE_TIME,
                CREATE_DEPARTMENTS_TABLE,
                CREATE_TOWNS_TABLE,
                CREATE_TYPES_TABLE,
                CREATE_ORGANISMS_TABLE,
                CREATE_COURSES_TABLE)
    conn = None
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        print("Creating tables...")
        for command in commands:
            cur.execute(command)
        print("Tables created.")
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def delete_tables():
    commands = (DELETE_DATES_TABLE,
                DELETE_DATES_TABLE,
                DELETE_COURSE_DATE_TIME_TABLE,
                DELETE_DEPARTMENTS_TABLE,
                DELETE_TOWNS_TABLE,
                DELETE_TYPES_TABLE,
                DELETE_ORGANISMS_TABLE,
                DELETE_COURSES_TABLE)
    conn = None
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        print("Deleting tables...")
        for command in commands:
            cur.execute(command)
        print("Tables deleted.")
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_course(
        places_available: int,
        places_total: int,
        price: int,
        date_add_to_db: float,
        town_id: int,
        type_id: int,
        organism_id: int,
        date_id: int):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(INSERT_COURSE, (
                                    places_available,
                                    places_total,
                                    price,
                                    date_add_to_db,
                                    town_id,
                                    type_id,
                                    organism_id,
                                    date_id,
                                    )
                    )
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return last_inserted_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_date(
                    date: float,
                    hour_start: str,
                    hour_end: str):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(INSERT_DATE, (
                                    date,
                                    hour_start,
                                    hour_end,
                                    )
                    )
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return last_inserted_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_course_date_time(
                    course_id: int,
                    date_id: int,
                    hour_start: float,
                    hour_end: float):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(INSERT_COURSE_DATE_TIME, (
                                    course_id,
                                    date_id,
                                    hour_start,
                                    hour_end,
                                    )
                    )
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_department(
                    number: str,
                    name: str):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(INSERT_DEPARTMENT, (
                                        name,
                                        number,
                                        )
                    )
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return last_inserted_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_town(
                postcode: str,
                name: str,
                department_id: int):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(INSERT_TOWN, (
                                    postcode,
                                    name,
                                    department_id,
                                    )
                    )
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return last_inserted_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_type(
                name: str,
                description: str):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(INSERT_TYPE, (
                                    name,
                                    description,
                                    )
                    )
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return last_inserted_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_organism(
                    name: str):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(INSERT_ORGANISM, (
                                        name,
                                        )
                    )
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return last_inserted_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_courses():
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_COURSES)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_dates():
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_DATES)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_date_(date: float):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_DATE, (date,))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_course_date_time(course_id: int):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_COURSE_DATE_TIME, (course_id,))
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_departments():
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_DEPARTMENTS)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_department_from_number(number: int):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_DEPARTMENT_FROM_NUMBER, (number,))
        result = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_towns():
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_TOWNS)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_town_from_name(name):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_TOWN_FROM_NAME, (name,))
        result = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_types():
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_TYPES)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_type_from_name(name):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_TYPE_FROM_NAME, (name,))
        result = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_organisms():
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_COURSES)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_organism_from_name(name: str):
    try:
        conn = connect_database(config_params)
        cur = conn.cursor()
        cur.execute(GET_ORGANISM_FROM_NAME, (name,))
        result = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
