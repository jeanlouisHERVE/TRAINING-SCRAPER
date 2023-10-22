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
            trainingsList = driver.find_element(By.CSS_SELECTOR, "div.liste-formations")
            print("trainingsList", trainingsList)
            trainings = trainingsList.find_elements(By.XPATH, ".//h2/following-sibling::ul")
            print("trainings", trainings)
            pairs = []
            for i in range(0, len(trainings), 2):
                pairs.append((trainings[i], trainings[i + 1]))
            print("pairs", pairs)

            # Now, the 'pairs' list contains pairs of (h2, ul) elements within the div with class "list"
            for pair in pairs:
                print("----------------START TRAINING----------------")
                h2 = pair[0].text
                ul = pair[1]

                # Find li elements within the ul
                li_elements = ul.find_elements(By.XPATH, ".//li")
                lis = [li.text for li in li_elements]

                print(f"H2: {h2}")
                # print(f"UL: {ul}")
                try:
                    geographical_elements = lis[0]
                    print(f"OK1 : {geographical_elements}")
                except (IndexError, NoSuchElementException):
                    print("KO : no geographical_elements")
                try:
                    hours = lis[1]
                    print(f"OK2 : {hours}")
                except (IndexError, NoSuchElementException):
                    print("KO : no hours elements")
                try:
                    available_places = lis[2]
                    print(f"OK3 : {available_places}")
                except (IndexError, NoSuchElementException):
                    print("KO : no available_place part")
                print("----------------END TRAINING----------------")
            input()
        except NoSuchElementException:
            print("KO : no list of trainings on this page")

    print("------------------Add_crf_training_End------------------")


def add_descriptions():
    print("------------------DESCRIPTION PART------------------")
    print("------------------End Add Description------------------")
