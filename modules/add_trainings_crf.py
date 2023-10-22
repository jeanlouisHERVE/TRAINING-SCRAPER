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
import functions
import data

# get data from .env file
load_dotenv()

# variables
driver = WebDriverManager.get_driver()
actions = ActionChains(driver)
# TODO add crf url
current_time_utc = datetime.datetime.now(tz=pytz.utc).timestamp()
functions = functions


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
            day_headers = training_container.find_elements(By.TAG_NAME, 'h2')

            for day_header in day_headers:
                date = day_header.text
                ul_element = day_header.find_elements(By.XPATH, './following-sibling::ul')

                training_items = ul_element.find_elements(By.TAG_NAME, 'li')
                for training_item in training_items:
                    training_name = training_item.find_element(By.CSS_SELECTOR, 'strong').text
                    location = training_item.find_element(By.CSS_SELECTOR, 'strong')[1].text
                    time = training_item.find_element(By.CSS_SELECTOR, 'span').text

                    print(f"Date: {date}")
                    print(f"Training: {training_name}")
                    print(f"Location: {location}")
                    print(f"Time: {time}")
                    print("\n")
                    input()
        except NoSuchElementException:
            print("KO : no list of trainings on this page")

    print("------------------Add_crf_training_End------------------")


def add_descriptions():
    print("------------------DESCRIPTION PART------------------")
    print("------------------End Add Description------------------")
