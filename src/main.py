import os
import pandas as pd
from data_processor import process_data
from event_data_store import EventDataStore

def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        print('CSV file loaded successfully.')
        print(data.head())
        event_data_store = process_data(data)
        # print(event_data_store.get_event_data('Hiring Booth'))
        print("User Count: ", event_data_store.get_user_count())
        print("Session Count: ", event_data_store.get_session_count())
    except Exception as e:
        print(f"Failed to load CSV file: {e}")

def main():
    input_directory = "../input"
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_directory, filename)
            load_csv(file_path)

if __name__ == "__main__":
    main()


