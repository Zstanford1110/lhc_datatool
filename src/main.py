import json
import os
import logging
import pandas as pd
from data_loader import load_data
from data_transformer import transform_data

def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        print('CSV file loaded successfully.')
        print(data.head())

        event_data_store = load_data(data)
        final_data_store = transform_data(event_data_store)

        # print(json.dumps(event_data_store.get_event_data("Main Menu Selections")))
        print(json.dumps(final_data_store.get_all_data()))

    except Exception as e:
        logging.exception("An error occurred!")

def main():
    input_directory = "../input"
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_directory, filename)
            load_csv(file_path)

if __name__ == "__main__":
    main()


