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
import data

# get data from .env file
load_dotenv()

# variables
driver = WebDriverManager.get_driver()
actions = ActionChains(driver)
current_time_utc = datetime.datetime.now(tz=pytz.utc).timestamp()
organism = "la croix rouge"
departments_numbers = data.french_department_numbers
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
    for department_number in departments_numbers:
        print(f"------------------Add_crf_training_Start : {department_number}------------------")
        driver.get("https://inscription-formation.croix-rouge.fr/?dep={}".format(department_number))
        driver.implicitly_wait(5)
        input()
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
                    time_element = training_item.find_element(By.CSS_SELECTOR, 'span').text

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
                    if not database_app.get_date(date):
                        date_id = database_app.add_date()
                    else:
                        date_elements = database_app.get_date(date)
                        date_id = date_elements[0]
                    print(f"Date: {utc_date}")
                    print(f"date_id: {date_id}")

                    # course_date_time
                    print(f"Time: {time_element}")
                    start_hour, end_hour = functions.extract_start_and_end_time(time_element)
                    start_hour_timestamp = functions.add_clock_elements_to_utc_timestamp(utc_date, start_hour)
                    end_hour_timestamp = functions.add_clock_elements_to_utc_timestamp(utc_date, end_hour)
                    print(f"start_hour_timestamp: {start_hour_timestamp}")
                    print(f"end_hour_timestamp: {end_hour_timestamp}")
                    database_app.add_course_date_time()
                    # TODO implement start and end times

                    input()
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

                    print("---------RECAP COURSE DATA---------")
                    places_available = 0
                    places_total = 0
                    price = 0

                    print("places_available", places_available)
                    print("places_total", places_total)
                    print("price", price)
                    print("date_id", date_id)
                    print("town_id", town_id)
                    print("type_id", type_id)
                    print("organism_id", organism_id)

                    if not database_app.get_course_id(organism_id, date_id, town_id, type_id):
                        database_app.add_course(places_available,
                                                places_total,
                                                price,
                                                date_id,
                                                town_id,
                                                type_id,
                                                organism_id)
                    else:
                        print("KO : Course already exists.")
                print('------------------END TRAINING------------------')
        except NoSuchElementException:
            print("KO : no list of trainings on this page")

        print(f"------------------Add_crf_training_End : {department_number}------------------")


def add_descriptions():
    print("------------------DESCRIPTION PART------------------")
    print("------------------End Add Description------------------")
