import logging
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

logging.basicConfig(level=logging.INFO)


class redstar_helper:
    def __init__(self):
        self.driver = self.setup_webdriver()
        self.wait = WebDriverWait(self.driver, 10)
        self.primary_tab = None

    def setup_webdriver(self):
        options = Options()
        options.add_experimental_option("detach", True)
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def login(self, username, password):
        try:
            username_input = self.driver.find_element(By.NAME, "username")
            password_input = self.driver.find_element(By.NAME, "password")
            username_input.send_keys(username)
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
        except NoSuchElementException:
            pass

    def redstar_status(self):
        try:
            element = self.driver.find_element(
                By.XPATH,
                '//font[@color="red"]/ancestor::td[@class="td1" or @class="td2"]',
            )
            return True
        except NoSuchElementException:
            return False

    def choose_table(self, num):
        return f"/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[last(){num}]/tbody/tr[2]/td/table/tbody"

    def scrape_table(self, URL):
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        table, rows = self.define_table(-4)
        self.loop_through_table(table, rows, URL, -4)
        if self.redstar_status():
            table, rows = self.define_table(-5)
            self.loop_through_table(table, rows, URL, -5)

    def define_table(self, table_num):
        table_elements = self.driver.find_elements(
            By.XPATH, self.choose_table(table_num)
        )
        table = table_elements[0] if table_elements else None
        if table:
            soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
            rows = soup.find_all("tr")
            return table, rows
        else:
            return None, None

    def loop_through_table(self, table, rows, URL, table_num):
        for row in rows:
            if not self.redstar_status():
                break
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
                    self.driver.get(URL)
                    self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    table = self.driver.find_element(
                        By.XPATH, self.choose_table(table_num)
                    )

    def auto_allocate(self):
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        try:
            auto_allocate_btn = self.driver.find_element(By.NAME, "realloc_trid")
            update_payment_btn = self.driver.find_element(By.NAME, "update")
            auto_allocate_btn.click()
            update_payment_btn.click()
        except NoSuchElementException:
            pass

    def open_redstars(self):
        for URL in url_columns:
            self.driver.get(URL)
            self.login(username, password)
            if self.redstar_status():
                self.scrape_table(URL)
        self.driver.quit()


if __name__ == "__main__":
    helper = redstar_helper()
    helper.driver.maximize_window()
    helper.open_redstars()
