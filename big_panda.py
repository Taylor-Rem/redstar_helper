import pandas as pd

from create_folder import file_path

df = pd.read_csv(file_path)

url_columns = df.filter(like="URL").values.flatten().tolist()
