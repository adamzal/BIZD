import pandas as pd
from datetime import datetime
import os


def move_and_rename_csv(original_path, new_folder_path):
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = os.path.basename(original_path)
    new_filename = f"{file_name.split('.')[0]}_{current_datetime}.csv"
    new_file_path = os.path.join(new_folder_path, new_filename)
    os.rename(original_path, new_file_path)


def data_main(db_connector):
    new_folder_path = "archive/"

    clients_df = pd.read_csv("data/clients_data.csv", header=0, delimiter="\t", dtype=str)
    db_connector.add_data('Client', clients_df)
    move_and_rename_csv("data/clients_data.csv", new_folder_path)

    properties_df = pd.read_csv("data/properties_data.csv", header=0, delimiter="\t", dtype=str)
    db_connector.add_data('Property', properties_df)
    move_and_rename_csv("data/properties_data.csv", new_folder_path)

    workers_df = pd.read_csv("data/workers_data.csv", header=0, delimiter="\t", dtype=str)
    db_connector.add_data('Worker', workers_df)
    move_and_rename_csv("data/workers_data.csv", new_folder_path)

    transactions_df = pd.read_csv("data/transactions_data.csv", header=0, delimiter="\t", dtype=str)
    db_connector.add_data('Transaction', transactions_df)
    move_and_rename_csv("data/transactions_data.csv", new_folder_path)


if __name__ == '__main__':
    from dotenv import load_dotenv
    from MYSQLConnector.connector import MYSQLConnector

    load_dotenv()

    db_connector = MYSQLConnector(
        os.getenv('DB_HOST'),
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_NAME')
    )

    data_main(db_connector)
