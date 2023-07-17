import pandas as pd

from datetime import datetime
import os, glob

now = datetime.now()
day = now.day
month = now.month
year = now.year
username = "taylorremund"

path = f"/Users/{username}/Desktop/red_star_helper/{year}/{month}/{day}"


def get_csv_filename(path):
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    if len(csv_files) == 0:
        print(f"No CSV files found in the directory: {path}")
        return None
    elif len(csv_files) > 1:
        print(f"Multiple CSV files found in the directory: {path}")
        return None
    else:
        return os.path.basename(csv_files[0])


file_path = f"{path}/{get_csv_filename(path)}"

df = pd.read_csv(file_path)

url_columns = df.filter(like="URL").values.flatten().tolist()
