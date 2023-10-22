#!/usr/bin/python
# packages
# import os
# import re
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
# import database_app
# import functions
import data

# get data from .env file
load_dotenv()

# variables
driver = WebDriverManager.get_driver()
actions = ActionChains(driver)
current_time_utc = datetime.datetime.now(tz=pytz.utc).timestamp()
organism = "la croix rouge"


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
    for department_number in data.french_department_numbers:
        driver.get(f"https://inscription-formation.croix-rouge.fr/?type=PSC1&dep={department_number}")
        driver.implicitly_wait(5)
        check_accept_section("button.onetrust-close-btn-handler")
        print("department_number :", department_number)
        # check an agree the terms section exists
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
                    time = training_item.find_element(By.CSS_SELECTOR, 'span').text

                    print(f"Date: {organism}")
                    print(f"Date: {date}")
                    print(f"Training: {training_name}")
                    print(f"Location: {location}")
                    print(f"Time: {time}")
                    print("\n")
                print('------------------END TRAINING------------------')
        except NoSuchElementException:
            print("KO : no list of trainings on this page")

    print("------------------Add_crf_training_End------------------")


def add_descriptions():
    print("------------------DESCRIPTION PART------------------")
    print("------------------End Add Description------------------")
