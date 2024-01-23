import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso, Lars
from sklearn.ensemble import RandomForestRegressor


def area_regression(db_connector):
    properties = db_connector.get_all_records("Property")

    x_train = properties['rooms'].to_numpy().reshape(-1, 1)
    y_train = properties['area'].to_numpy()

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

        plt.scatter(x_train, y_train, label="Wartości rzeczywiste", alpha=0.5)
        plt.scatter(x_train, y_pred, label=f"Przewidywanie {model_name}")
        plt.title('Liczba pokoi a powierzchnia nieruchomości')
        plt.legend()
        plt.show()


if __name__ == "__main__":
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
    area_regression(db_connector)
