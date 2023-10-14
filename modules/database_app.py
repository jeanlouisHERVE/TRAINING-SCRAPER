import sqlite3
# import platform

# other modules

from dotenv import load_dotenv

# get data from .env file
load_dotenv()

# variables
WINDOWS_DATABASE_PATH = "c:\\Users\\jeanl\\OneDrive\\Bureau\\TRAINING-SCRAPER\\database\\immoscraper.db"
LINUX_DATABASE_PATH = "/home/jean-louis/Bureau/TRAINING-SCRAPER/database/immoscraper.db"

connection = sqlite3.connect(WINDOWS_DATABASE_PATH)

# create database
CREATE_TRAINING_TABLE = """CREATE TABLE IF NOT EXISTS trainings (
                                id INTEGER NOT NULL PRIMARY KEY,
                                town STRING,
                                training_title,
                                training_department,
                                date_add_to_db TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (department_name) REFERENCES departments(name),
                                FOREIGN KEY (date_id) REFERENCES dates(id) ON DELETE CASCADE,
                                FOREIGN KEY (type_id) REFERENCES types(id));"""

CREATE_TRAINING_DATE_TABLE = """CREATE TABLE IF NOT EXISTS dates (
                                    training_id INTEGER,
                                    hour_start TEXT,
                                    hour_end TEXT,
                                    date TIMESTAMP);"""

CREATE_TRAINING_TYPE_TABLE = """CREATE TABLE IF NOT EXISTS types (
                                    id INTEGER NOT NULL PRIMARY KEY,
                                    name TEXT UNIQUE);"""

CREATE_DEPARTMENT = """CREATE TABLE IF NOT EXISTS departments (
                            number INTEGER PRIMARY KEY,
                            name TEXT UNIQUE);"""

# add data
INSERT_TRAINING = "INSERT INTO trainings () VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
INSERT_DATE = ""
INSERT_TYPE = ""
INSERT_DEPARTMENT = ""

# get data
GET_TRAINING = "SELECT * FROM properties #####;"
GET_TYPE = "SELECT * FROM types #####;"

# update data
UPDATE_TRAINING = """UPDATE trainings
                    SET price = ?
                    WHERE id = ?;"""


# delete data
DELETE_TRAINING_TABLE = "DELETE FROM trainings;"


def create_tables():
    with connection:
        print("Creating tables...")
        connection.execute(CREATE_TRAINING_TABLE)
        print("Tables created.")


def delete_tables():
    with connection:
        print("deleting tables...")
        connection.execute(DELETE_TRAINING_TABLE)
        print("Tables deleted.")


# def add_training()
#     with connection:
#         cursor = connection.execute(INSERT_TRAINING, (
#                                         )
#                                     ),
#         last_inserted_id = cursor.lastrowid
#     return last_inserted_id


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
