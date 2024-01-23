import random
import os
import pandas as pd
from faker import Faker

fake = Faker('pl_PL')


class PropertiesDataGenerator:

    def __init__(self) -> None:
        self.columns = ["ID", "type", "address", "area", "rooms", "sqm_price", "description"]
        self.dataset = pd.DataFrame(columns=self.columns).set_index(self.columns[0])

        if os.path.exists("generators/.properties_index.txt"):
            with open("generators/.properties_index.txt", "r") as index_file:
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

            property_id = self.index
            property_type = random.choice(['flat', 'building'])
            address = fake.address()

            if property_type == "building":
                rooms_number = random.randint(5, 10)
                area = 0

                for _ in range(rooms_number):
                    area += random.randint(10, 20)

                sqm_price = random.randint(5000, 10000)

            elif property_type == "flat":
                rooms_number = random.randint(2, 5)
                area = 0

                for _ in range(rooms_number):
                    area += random.randint(10, 15)

                sqm_price = random.randint(7000, 12000)

            description = fake.text(max_nb_chars=100)

            row[self.columns[0]] = property_id
            row[self.columns[1]] = property_type
            row[self.columns[2]] = address
            row[self.columns[3]] = area
            row[self.columns[4]] = rooms_number
            row[self.columns[5]] = sqm_price
            row[self.columns[6]] = description

            data += [row]

            self.index += 1

        self.dataset = pd.DataFrame(data, columns=self.columns).set_index(self.columns[0])

    def save_data(self) -> None:
        self.dataset.to_csv("data/properties_data.csv", sep="\t")

        os.system(f'attrib -h generators/.properties_index.txt')

        with open("generators/.properties_index.txt", "w") as index_file:
            index_file.truncate()
            index_file.writelines(str(self.index))

        os.system(f'attrib +h generators/.properties_index.txt')
