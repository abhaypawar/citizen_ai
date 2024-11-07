import pandas as pd
import json

def get_scheme_data():
    # Open the JSON file and load its data
    with open("jsondb/schemes.json", "r") as f:
        data = json.load(f)

    # Convert the loaded JSON data into a pandas DataFrame
    return pd.DataFrame(data)
