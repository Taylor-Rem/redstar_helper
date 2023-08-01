import pandas as pd
from datetime import datetime
import os, glob


class CsvReader:
    def __init__(self):
        self.now = datetime.now()
        self.day = self.now.day
        self.month = self.now.month
        self.year = self.now.year
        self.username = "taylorremund"
        self.path = f"/Users/{self.username}/Desktop/red_star_helper/{self.year}/{self.month}/{self.day}"

    def get_csv_filename(self):
        csv_files = glob.glob(os.path.join(self.path, "*.csv"))
        if len(csv_files) == 0:
            print(f"No CSV files found in the directory: {self.path}")
            return None
        elif len(csv_files) > 1:
            print(f"Multiple CSV files found in the directory: {self.path}")
            return None
        else:
            return os.path.basename(csv_files[0])

    def get_csv_path(self):
        return f"{self.path}/{self.get_csv_filename()}"

    def get_url_columns(self, file_path):
        df = pd.read_csv(file_path)
        return df.filter(like="URL").values.flatten().tolist()
