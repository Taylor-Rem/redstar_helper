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

import re, time

from big_panda import url_columns


class redstar_helper:
    latest_month_table_xpath = "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[last()-4]/tbody/tr[2]/td/table/tbody"

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

    def scrape_table(self, column):
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        table = self.driver.find_element(By.XPATH, self.latest_month_table_xpath)
        soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
        rows = soup.find_all("tr")
        for row in rows:
            if row.find("td", class_="th3"):
                continue
            cells = row.find_all("td")
            transaction_element = cells[2].find("a")
            transaction = (
                transaction_element.text.strip() if transaction_element else ""
            )
            amount = cells[3].text.strip()
            if amount.startswith("(") and amount.endswith(")"):
                try:
                    link = table.find_element(
                        By.XPATH, f'//a[contains(text(), "{transaction}")]'
                    )
                except NoSuchElementException:
                    pass
                if link:
                    link.click()
                    self.auto_allocate()
                    self.driver.get(column)
                    self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    table = self.driver.find_element(
                        By.XPATH, self.latest_month_table_xpath
                    )

    def auto_allocate(self):
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        try:
            auto_allocate_btn = self.driver.find_element(By.NAME, "realloc_trid")
            update_payment_btn = self.driver.find_element(By.NAME, "update")
            auto_allocate_btn.click()
            update_payment_btn.click()
        except NoSuchElementException:
            print("No Auto Allocate found on page")
            pass

    def open_redstars(self):
        for column in url_columns:
            self.driver.get(column)
            self.login(username, password)
            self.scrape_table(column)
        self.driver.quit()

    # for i in range(2):
    # self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    # column = url_columns[1]
    # self.driver.get(column)
    # self.login(username, password)
    # self.scrape_table(column)
    # self.driver.quit()


if __name__ == "__main__":
    helper = redstar_helper()
    helper.driver.maximize_window()
    helper.open_redstars()
