import random
import os
import pandas as pd
from faker import Faker

fake = Faker('pl_PL')


class ClientsDataGenerator:

    def __init__(self) -> None:
        self.columns = ["ID", "name", "surname", "pesel", "email", "phone", "city", "postcode"]
        self.dataset = pd.DataFrame(columns=self.columns).set_index(self.columns[0])

        if os.path.exists("generators/.clients_index.txt"):
            with open("generators/.clients_index.txt", "r") as index_file:
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

            if random.uniform(0, 1) >= 0.5:
                name = fake.first_name_male()
                surname = fake.last_name_male()
                pesel = fake.pesel(sex="male")
            else:
                name = fake.first_name_female()
                surname = fake.last_name_female()
                pesel = fake.pesel(sex="female")

            client_id = self.index
            phone = fake.phone_number().replace(' ', '')
            post_code = fake.postcode()
            city = fake.city()
            e_mail = name.lower() + "." + surname.lower() + "@" + fake.free_email_domain()

            row[self.columns[0]] = client_id
            row[self.columns[1]] = name
            row[self.columns[2]] = surname
            row[self.columns[3]] = pesel
            row[self.columns[4]] = e_mail
            row[self.columns[5]] = phone
            row[self.columns[6]] = city
            row[self.columns[7]] = post_code

            data += [row]

            self.index += 1

        self.dataset = pd.DataFrame(data, columns=self.columns).set_index(self.columns[0])

    def save_data(self) -> None:
        self.dataset.to_csv("data/clients_data.csv", sep="\t")

        os.system(f'attrib -h generators/.clients_index.txt')

        with open("generators/.clients_index.txt", "w") as index_file:
            index_file.truncate()
            index_file.writelines(str(self.index))

        os.system(f'attrib +h generators/.clients_index.txt')
