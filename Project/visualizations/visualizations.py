import matplotlib.pyplot as plt


def visualize(db_connector):
    mct = db_connector.get_all_records("month_count_transaction")
    mct = mct.sort_values(by="tr_month")
    plt.bar(mct.tr_month, mct.tr_count)
    plt.title("Liczba wszystkich transakcji w miesiącu")
    plt.show()

    yct = db_connector.get_all_records("year_count_transaction")
    yct = yct.sort_values(by="tr_year")
    plt.bar(yct.tr_year, yct.tr_count)
    plt.title("Liczba wszystkich transakcji w roku")
    plt.show()

    mspt = db_connector.get_all_records("month_sum_price_transaction")
    mspt = mspt.sort_values(by="tr_month")
    plt.bar(mspt.tr_month, mspt.tr_sum_price)
    plt.title("Suma wszystkich transakcji w miesiącu")
    plt.show()

    yspt = db_connector.get_all_records("year_sum_price_transaction")
    yspt = yspt.sort_values(by="tr_year")
    plt.bar(yspt.tr_year, yspt.tr_sum_price)
    plt.title("Suma wszystkich transakcji w roku")
    plt.show()


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    from MYSQLConnector.connector import MYSQLConnector

    load_dotenv()

    db_connector = MYSQLConnector(
        os.getenv('DB_HOST'),
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_NAME')
    )

    visualize(db_connector)
