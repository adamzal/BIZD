import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso, Lars
from sklearn.ensemble import RandomForestRegressor


def price_regression(db_connector):
    properties = db_connector.get_all_records("Property")

    x_train = properties[['rooms', 'area']]
    y_train = properties['sqm_price'].to_numpy() * properties['area'].to_numpy()

    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(),
        'Lasso Regression': Lasso(),
        'Lars Regression': Lars(),
        'Random Forest Regression': RandomForestRegressor()
    }

    for model_name, model in models.items():
        model.fit(x_train, y_train)
        y_pred = model.predict(x_train)

        plt.scatter(properties['rooms'], y_train, label="Wartości rzeczywiste", alpha=0.5)
        plt.scatter(properties['rooms'], y_pred, label=f"Przewidywanie {model_name}")
        plt.title('Liczba pokoi a cena nieruchomości')
        plt.legend()
        plt.show()

        plt.scatter(properties['area'], y_train, label="Wartości rzeczywiste", alpha=0.5)
        plt.scatter(properties['area'], y_pred, label=f"Przewidywanie {model_name}")
        plt.title('Powierzchnia nieruchomości a jej cena')
        plt.legend()
        plt.show()


if __name__ == '__main__':
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

    price_regression(db_connector)
