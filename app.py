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
    auto_allocate_btn_xpath = "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/form/table[1]/tbody/tr[2]/td/table/tbody/tr[4]/td[3]/input"
    update_payment_btn_xpath = (
        "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/form/input[4]"
    )

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

    def scrape_table(self):
        table = self.driver.find_element(By.XPATH, self.latest_month_table_xpath)
        soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")

        rows = soup.find_all("tr")

        for row in rows:
            if row.find("td", class_="th3"):
                continue

            cells = row.find_all("td")
            transaction_date = cells[0].text.strip()
            due_date = cells[1].text.strip()
            transaction = cells[2].text.strip()
            amount = cells[3].text.strip()
            balance = cells[4].text.strip()

            print(row)

            return table, transaction_date, due_date, transaction, amount, balance

    def decisions(
        self, table, column, transaction_date, due_date, transaction, amount, balance
    ):
        if len(self.values) >= 2:
            amount_due = self.values[0]
            prepaid_rent = self.values[1]

            if amount == f"($ {prepaid_rent})":
                self.prepaid_matches_amount(table, transaction, column)
            # else:
            #     self.auto_allocate_all(self, column)
        else:
            print("not enough values in self.values")

    def prepaid_matches_amount(self, table, transaction, column):
        try:
            link = table.find_element(By.LINK_TEXT, transaction)
            link.click()
            self.auto_allocate(column)
        except NoSuchElementException:
            print(f"No link found for transaction: {transaction}")

    def auto_allocate(self, column):
        try:
            auto_allocate_btn = self.driver.find_element(
                By.XPATH, self.auto_allocate_btn_xpath
            )
            update_payment_btn = self.driver.find_element(
                By.XPATH, self.update_payment_btn_xpath
            )
            auto_allocate_btn.click()
            update_payment_btn.click()
            self.driver.get(column)
        except NoSuchElementException:
            print("No Auto Allocate found on page")

    def open_redstars(self):
        # for column in url_columns:
        #     self.driver.get(column)
        #     self.login(username, password)
        #     self.values = []
        #     self.scrape_stars()
        #     if len(self.values) >= 1:
        #         (
        #             column,
        #             table,
        #             transaction_date,
        #             due_date,
        #             transaction,
        #             amount,
        #             balance,
        #         ) = self.scrape_table()
        #         self.decisions(
        #             table,
        #             column,
        #             transaction_date,
        #             due_date,
        #             transaction,
        #             amount,
        #             balance,
        #         )
        #     else:
        #         print("No red stars found on page")
        # self.driver.quit()
        for i in range(3):  # Run the loop 3 times
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            column = url_columns[i]
            self.driver.get(column)
            self.login(username, password)
            self.values = []
            self.scrape_stars()
            (
                table,
                transaction_date,
                due_date,
                transaction,
                amount,
                balance,
            ) = self.scrape_table()
            self.decisions(
                table, column, transaction_date, due_date, transaction, amount, balance
            )
        self.driver.quit()


if __name__ == "__main__":
    helper = redstar_helper()
    helper.driver.maximize_window()
    helper.open_redstars()
