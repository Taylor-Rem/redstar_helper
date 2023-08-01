from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_operations import WebDriverOperations


class TableReader:
    def __init__(self, webdriver_operations):
        self.webdriver = webdriver_operations

    def choose_table(self, num):
        return f"/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[last(){num}]/tbody/tr[2]/td/table/tbody"

    def define_table(self, table_num):
        table_elements = self.webdriver.driver.find_elements(
            By.XPATH, self.choose_table(table_num)
        )
        table = table_elements[0] if table_elements else None
        if table:
            soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
            rows = soup.find_all("tr")
            return table, rows
        else:
            return None, None

    def get_transaction_and_amount(self, row):
        cells = row.find_all("td")
        transaction_element = cells[2].find("a")
        transaction = transaction_element.text.strip() if transaction_element else ""
        amount = cells[3].text.strip()
        return transaction, amount
