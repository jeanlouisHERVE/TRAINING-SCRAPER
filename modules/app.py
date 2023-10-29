#!/usr/bin/env python
# packages


# other modules
from dotenv import load_dotenv

# own packages
import config
import database_app
import add_trainings_crf

database_name = config.get_database_name()
database_app.create_database(database_name)
database_app.create_tables()

# get data from .env file
load_dotenv()

# variables

menu_prompt = """-- Menu --

1) Add crf trainings
2) Delete database
3) Exit

Enter your choice: """


def start_prompt():
    user_input = input(menu_prompt)
    while user_input != "3":
        if user_input == "1":
            add_trainings_crf.add_trainings()
        elif user_input == "2":
            database_app.delete_tables()
        else:
            print("Invalid input, please try again!")


# script
if __name__ == "__main__":
    start_prompt()
