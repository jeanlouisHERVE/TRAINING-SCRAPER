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
                                training_dates,
                                training_department,
                                date_add_to_db TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"""
# TODO table pour les dates des formations + horaires
# TODO table pour les dates des types de formation

# add data
INSERT_TRAINING = """INSERT INTO trainings () VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""


# get data
GET_TRAINING = "SELECT * FROM properties #####;"


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
