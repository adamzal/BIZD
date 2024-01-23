import random

from generators.ClientsDataGenerator import ClientsDataGenerator
from generators.PropertiesDataGenerator import PropertiesDataGenerator
from generators.WorkersDataGenerator import WorkersDataGenerator
from generators.TransactionsDataGenerator import TransactionsDataGenerator


def generators_main():
    CDG = ClientsDataGenerator()
    CDG.generate_data(random.randint(10, 100))
    CDG.save_data()

    PDG = PropertiesDataGenerator()
    PDG.generate_data(random.randint(100, 1000))
    PDG.save_data()

    WDG = WorkersDataGenerator()
    WDG.generate_data(random.randint(1, 3))
    WDG.save_data()

    TDG = TransactionsDataGenerator()
    TDG.generate_data()
    TDG.save_data()
