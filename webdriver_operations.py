from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException

from config import username, password


class WebDriverOperations:
    def __init__(self):
        self.driver = self.setup_webdriver()
        self.wait = WebDriverWait(self.driver, 10)

    def setup_webdriver(self):
        service = Service()
        options = Options()
        return webdriver.Chrome(service=service, options=options)

    def quit_driver(self):
        self.driver.quit()

    def maximize_window(self):
        self.driver.maximize_window()

    def login(self, url, username, password):
        self.driver.get(url)
        try:
            username_input = self.driver.find_element(By.NAME, "username")
            password_input = self.driver.find_element(By.NAME, "password")
            username_input.send_keys(username)
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
        except NoSuchElementException:
            pass
