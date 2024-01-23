import random
import os
import pandas as pd
from faker import Faker

fake = Faker('pl_PL')


class WorkersDataGenerator:

    def __init__(self) -> None:
        self.columns = ["ID", "name", "surname", "role", "phone", 'email']
        self.dataset = pd.DataFrame(columns=self.columns).set_index(self.columns[0])

        if os.path.exists("generators/.workers_index.txt"):
            with open("generators/.workers_index.txt", "r") as index_file:
                file_line = index_file.readline()
                if file_line:
                    self.index = int(file_line)
                else:
                    self.index = 1
        else:
            self.index = 1

    def generate_data(self, n_row: int) -> None:
        data = []

        for _ in range(n_row):
            row = {}

            worker_id = self.index
            name = fake.first_name()
            surname = fake.last_name()

            role = "broker"
            if random.uniform(0, 1) >= 0.9:
                role = "manager"

            phone = fake.phone_number().replace(' ', '')
            e_mail = name.lower() + "." + surname.lower() + "@" + fake.free_email_domain()

            row[self.columns[0]] = worker_id
            row[self.columns[1]] = name
            row[self.columns[2]] = surname
            row[self.columns[3]] = role
            row[self.columns[4]] = phone
            row[self.columns[5]] = e_mail

            data += [row]

            self.index += 1

        self.dataset = pd.DataFrame(data, columns=self.columns).set_index(self.columns[0])

    def save_data(self) -> None:
        self.dataset.to_csv("data/workers_data.csv", sep="\t")

        os.system(f'attrib -h generators/.workers_index.txt')

        with open("generators/.workers_index.txt", "w") as index_file:
            index_file.truncate()
            index_file.writelines(str(self.index))

        os.system(f'attrib +h generators/.workers_index.txt')
