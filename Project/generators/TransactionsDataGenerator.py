import random
import os
import pandas as pd
from faker import Faker

fake = Faker('pl_PL')


class TransactionsDataGenerator:

    def __init__(self) -> None:
        self.properties_data = pd.read_csv("data/properties_data.csv", header=0, delimiter="\t")

        with open("generators/.clients_index.txt", "r") as index_file:
            file_line = index_file.readline()
            if file_line:
                self.clients_n = int(file_line)

        with open("generators/.workers_index.txt", "r") as index_file:
            file_line = index_file.readline()
            if file_line:
                self.workers_n = int(file_line)

        self.columns = ["ID", "property_id", "client_id", "worker_id", "tr_date", "final_price", "tr_status"]
        self.dataset = pd.DataFrame(columns=self.columns).set_index(self.columns[0])

        if os.path.exists("generators/.transaction_index.txt"):
            with open("generators/.transaction_index.txt", "r") as index_file:
                file_line = index_file.readline()
                if file_line:
                    self.index = int(file_line)
                else:
                    self.index = 1
        else:
            self.index = 1

    def generate_data(self) -> None:
        data = []

        for i in range(self.properties_data.shape[0]):
            row = {}

            if random.uniform(0, 1) >= .3:
                continue

            transaction_id = self.index
            transaction_status = random.choice(['started', 'completed', 'cancelled'])
            property_id = self.properties_data["ID"].iloc[i]
            client_id = random.randint(1, self.clients_n-1)
            worker_id = random.randint(1, self.workers_n-1)
            tr_date = fake.date_between(start_date="-5y", end_date="now")
            final_price = float(self.properties_data["area"].iloc[i]) * float(self.properties_data["sqm_price"].iloc[i])

            row[self.columns[0]] = transaction_id
            row[self.columns[1]] = property_id
            row[self.columns[2]] = client_id
            row[self.columns[3]] = worker_id
            row[self.columns[4]] = tr_date
            row[self.columns[5]] = final_price
            row[self.columns[6]] = transaction_status

            data += [row]

            self.index += 1

        self.dataset = pd.DataFrame(data, columns=self.columns).set_index(self.columns[0])

    def save_data(self) -> None:
        self.dataset.to_csv("data/transactions_data.csv", sep="\t")

        os.system(f'attrib -h generators/.transactions_index.txt')

        with open("generators/.transactions_index.txt", "w") as index_file:
            index_file.truncate()
            index_file.writelines(str(self.index))

        os.system(f'attrib +h generators/.transactions_index.txt')
