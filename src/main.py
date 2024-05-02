import os
import pandas as pd
from data_processor import process_data

def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        print("CSV file loaded successfully.")
        print(data.head())
        process_data(data)
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


