#!/usr/bin/python
# packages
# import os
import re
# import time
import pytz
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
    )
from selenium.webdriver.common.action_chains import ActionChains

# other modules
from dotenv import load_dotenv
from driver_manager import WebDriverManager

# own packages
import database_app
import functions

# get data from .env file
load_dotenv()

# variables
driver = WebDriverManager.get_driver()
actions = ActionChains(driver)
current_time_utc = datetime.datetime.now(tz=pytz.utc).timestamp()
organism = "la croix rouge"
pattern_extract_department_numbers = r'^[0-9]+'
pattern_retrieve_numbers = r'\d+\s*-\s*'


# functions
def check_accept_section(cssSelector: str):

    driver.implicitly_wait(5)
    try:
        accept = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector))
                )
        accept.click()
    except (
        NoSuchElementException,
        StaleElementReferenceException,
        TimeoutException
    ):
        print("KO : no accept part")


def add_trainings():
    print("------------------Add_crf_training_Start------------------")
    # connection to website
    driver.get("https://inscription-formation.croix-rouge.fr/")
    driver.implicitly_wait(5)
    # check an agree the terms section exists
    check_accept_section("button.onetrust-close-btn-handler")
    # collect data
    try:
        training_container = driver.find_element(By.CSS_SELECTOR, 'div.liste-formations')
        print("training_container :", training_container)
        day_headers = training_container.find_elements(By.TAG_NAME, 'h2')
        print("day_headers :", day_headers)
        for day_header in day_headers:
            print('------------------START TRAINING------------------')
            date = day_header.text
            print("date :", date)

            ul_element = day_header.find_element(By.XPATH, './following-sibling::ul')
            print("ul_element :", ul_element)
            training_items = ul_element.find_elements(By.CSS_SELECTOR, 'li')
            print("training_items :", training_items)
            for training_item in training_items:
                strong_elements = training_item.find_elements(By.CSS_SELECTOR, 'strong')
                training_name = strong_elements[0].text
                location = strong_elements[1].text
                department_number = str(re.findall(pattern_extract_department_numbers, location)[0])
                town = re.sub(pattern_retrieve_numbers, '', location)
                time = training_item.find_element(By.CSS_SELECTOR, 'span').text

                # organism
                print(f"Organism: {organism}")
                if not database_app.get_organism_from_name(organism):
                    organism_id = database_app.add_organism(organism)
                else:
                    organism_elements = database_app.get_organism_from_name(organism)
                    organism_id = organism_elements[0]
                print(f"Organism_id: {organism_id}")

                # date
                print(f"Date: {date}")
                utc_date = functions.date_converter_french_date_to_utc_timestamp(date)
                print(f"Date: {utc_date}")

                # type
                print(f"Training: {training_name}")
                # TODO implement description
                description = ""
                if not database_app.get_type_from_name(training_name):
                    type_id = database_app.add_type(training_name, description)
                else:
                    training_elements = database_app.get_type_from_name(training_name)
                    type_id = training_elements[0]
                print(f"type_id: {type_id}")

                print(f"Location: {location}")
                # department
                print(f"department_number: {department_number}")
                if department_number:
                    department_name = functions.get_department_name(department_number)
                print(f"department_name {department_name}")
                if not database_app.get_department_from_number(department_number):
                    department_id = database_app.add_department(department_number, department_name)
                else:
                    department_elements = database_app.get_department_from_number(department_number)
                    department_id = department_elements[0]
                print(f"department_id: {department_id}")

                # town
                print(f"town: {town}")
                postcode = ""
                # TODO implement postcode
                if not database_app.get_town_from_name(town):
                    town_id = database_app.add_town(postcode, town, department_id)
                else:
                    town_elements = database_app.get_town_from_name(town)
                    town_id = town_elements[0]
                print(f"town_id: {town_id}")
                print(f"Time: {time}")
                print("\n")
            print('------------------END TRAINING------------------')
    except NoSuchElementException:
        print("KO : no list of trainings on this page")

    print("------------------Add_crf_training_End------------------")


def add_descriptions():
    print("------------------DESCRIPTION PART------------------")
    print("------------------End Add Description------------------")
