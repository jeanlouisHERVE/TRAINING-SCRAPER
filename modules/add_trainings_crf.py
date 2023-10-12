# packages
# import os
# import re
import time
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
from modules.driver_manager import WebDriverManager

# own packages
# import database_app
import functions

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


def add_new_announces():
    print("------------------Add_crf_training_Start------------------")
    # connection to website
    # TODO add url
    driver.get()
    driver.implicitly_wait(5)
    # check an agree the terms section exists
    time.sleep(2)
    # TODO if concerned add css class
    check_accept_section()
    time.sleep(2)

    print("------------------Add_crf_training_End------------------")


def add_descriptions():
    print("------------------DESCRIPTION PART------------------")
    print("------------------End Add Description------------------")
