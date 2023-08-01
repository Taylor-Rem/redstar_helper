from table_reader import TableReader
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from csv_reader import CsvReader


class ScrapePage:
    def __init__(self, webdriver_operations, table_reader):
        self.webdriver = webdriver_operations
        self.table_reader = table_reader

    def redstar_status(self):
        try:
            element = self.webdriver.driver.find_element(
                By.XPATH,
                '//font[@color="red"]/ancestor::td[@class="td1" or @class="td2"]',
            )
            return True
        except NoSuchElementException:
            return False

    def loop_through_table(self, table, rows, URL, table_num):
        for row in rows:
            if not self.redstar_status():
                break
            if row.find("td", class_="th3"):
                continue
            transaction, amount = self.table_reader.get_transaction_and_amount(row)
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
                    self.webdriver.wait
                    table = self.webdriver.driver.find_element(
                        By.XPATH, self.table_reader.choose_table(table_num)
                    )

    def auto_allocate(self):
        try:
            auto_allocate_btn = self.webdriver.driver.find_element(
                By.NAME, "realloc_trid"
            )
            update_payment_btn = self.webdriver.driver.find_element(By.NAME, "update")
            auto_allocate_btn.click()
            update_payment_btn.click()
        except NoSuchElementException:
            self.webdriver.driver.back()
            pass

    def scrape_table(self, URL):
        table, rows = self.table_reader.define_table(-4)
        self.loop_through_table(table, rows, URL, -4)

        if CsvReader().day < 15:
            if self.redstar_status():
                table, rows = self.table_reader.define_table(-5)
                self.loop_through_table(table, rows, URL, -5)
