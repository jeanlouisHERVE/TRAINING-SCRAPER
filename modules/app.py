#!/usr/bin/env python
# packages


# other modules
from dotenv import load_dotenv

# own packages
import database_app
import add_trainings_crf
from config import config

config_params = config()
connection = database_app.connect_database(config_params)

database_app.create_tables(connection)

# get data from .env file
load_dotenv()

# variables

menu_prompt = """-- Menu --

1) Add crf trainings
2) Exit

Enter your choice: """


def start_prompt():
    user_input = input(menu_prompt)
    while user_input != "2":
        if user_input == "1":
            add_trainings_crf.add_trainings(connection)
        else:
            print("Invalid input, please try again!")


# script
if __name__ == "__main__":
    start_prompt()
