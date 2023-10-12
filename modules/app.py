#!/usr/bin/env python
# packages
import os

# other modules
from dotenv import load_dotenv

# own packages
import database_app
import modules.add_trainings_crf as add_trainings_crf

database_app.create_tables()

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
            add_trainings_crf.add_new_announces()
        else:
            print("Invalid input, please try again!")


# script
if __name__ == "__main__":
    start_prompt()