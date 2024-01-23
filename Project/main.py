from dotenv import load_dotenv
import os

from MYSQLConnector.connector import MYSQLConnector
from generators.main import generators_main
from data.main import data_main
from regressions.area_regression import area_regression
from regressions.price_regression import price_regression
from statistics.basic_statistics import show_base_statistics
from statistics.hypothesis_tests import hypothesis_main
from visualizations.visualizations import visualize

load_dotenv()

if __name__ == '__main__':
    db_connector = MYSQLConnector(
        os.getenv('DB_HOST'),
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_NAME')
    )

    generators_main()
    data_main(db_connector)

    show_base_statistics(db_connector)
    hypothesis_main(db_connector)
    area_regression(db_connector)
    price_regression(db_connector)
    visualize(db_connector)
