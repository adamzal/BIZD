def show_base_statistics(db_connector):
    properties = db_connector.get_all_records("Property")
    print(properties.sqm_price.describe(include="all"), end="\n\n")

    print(properties.area.describe(include="all"), end="\n\n")

    transaction = db_connector.get_all_records("Transaction")
    print(transaction.final_price.describe(include="all"), end="\n\n")


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    from MYSQLConnector.connector import MYSQLConnector

    load_dotenv()

    db_connector = MYSQLConnector(
        os.getenv('DB_HOST'),
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_NAME')
    )

    show_base_statistics(db_connector)
