from redstar_helper import RedStarHelper
from webdriver_operations import WebDriverOperations
from table_reader import TableReader
from csv_reader import CsvReader


def main():
    csv_reader = CsvReader()
    file_path = csv_reader.get_csv_path()
    url_columns = csv_reader.get_url_columns(file_path)

    webdriver_operations = WebDriverOperations()
    webdriver_operations.maximize_window()

    table_reader = TableReader(webdriver_operations)

    helper = RedStarHelper(webdriver_operations, table_reader)
    helper.open_redstars(url_columns)


if __name__ == "__main__":
    main()
