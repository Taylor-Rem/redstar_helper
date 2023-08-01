import logging
from config import username, password
from webdriver_operations import WebDriverOperations
from scrape_page import ScrapePage
from table_reader import TableReader

logging.basicConfig(level=logging.INFO)


class RedStarHelper:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, webdriver_operations, table_reader):
        if self.__initialized:
            return
        self.webdriver = webdriver_operations
        self.scrape_page = ScrapePage(webdriver_operations, table_reader)
        self.__initialized = True
        self.primary_tab = None

    def open_redstars(self, url_columns):
        for URL in url_columns:
            self.webdriver.login(URL, username, password)
            if self.scrape_page.redstar_status():
                self.scrape_page.scrape_table(URL)
        self.webdriver.quit_driver()
