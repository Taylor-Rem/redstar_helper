from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

from config import username, password

import re

from big_panda import url_columns


class redstar_helper:
    def __init__(self):
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        self.wait = WebDriverWait(self.driver, 10)
        self.primary_tab = None
        self.values = []

    def login(self, username, password):
        try:
            username_input = self.driver.find_element(By.NAME, "username")
            password_input = self.driver.find_element(By.NAME, "password")
            username_input.send_keys(username)
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
        except NoSuchElementException:
            pass

    def scrape_stars(self):
        elements = self.driver.find_elements(
            By.XPATH, '//font[@color="red"]/ancestor::td[@class="td1" or @class="td2"]'
        )
        for element in elements:
            value = element.text.split()[1].strip("$")
            self.values.append(value)
        print(self.values)

    def open_redstars(self):
        # for column in url_columns:
        #     self.driver.get(column)
        #     self.login(username, password)
        #     self.values = []
        #     self.scrape_stars()
        # self.driver.quit()
        for i in range(3):  # Run the loop 3 times
            column = url_columns[i]
            self.driver.get(column)
            self.login(username, password)
            self.values = []
            self.scrape_stars()
        self.driver.quit()


if __name__ == "__main__":
    helper = redstar_helper()
    helper.driver.maximize_window()
    helper.open_redstars()
