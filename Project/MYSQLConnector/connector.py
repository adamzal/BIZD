import mysql.connector
import pandas as pd


class MYSQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def _dbcon(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    @staticmethod
    def _close_dbcon(connection, cursor):
        cursor.close()
        connection.close()

    @staticmethod
    def _generate_insert_query(table: str, data: pd.DataFrame):
        df = data.drop(columns=['ID'])
        col_names = df.columns.tolist()
        vals = [[f"'{val}'" for val in row] for row in df.values.tolist()]
        vals = [', '.join(row) for row in vals]
        vals = [f'({val})' for val in vals]
        return f"INSERT INTO {table} (" + ", ".join(col_names) + ') VALUES ' + ', '.join(vals) + ';'

    def get_all_records(self, table: str) -> pd.DataFrame:
        connection = self._dbcon()
        cursor = connection.cursor()
        try:
            query = f"SELECT * FROM {table};"
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)
            self._close_dbcon(connection, cursor)
            return df

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self._close_dbcon(connection, cursor)
            return pd.DataFrame()

    def add_data(self, table: str, data: pd.DataFrame) -> None:
        connection = self._dbcon()
        cursor = connection.cursor()
        try:
            query = self._generate_insert_query(table, data)
            cursor.execute(query)
            connection.commit()
            self._close_dbcon(connection, cursor)
            return

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self._close_dbcon(connection, cursor)
            return

    def delete_transaction(self, id: int) -> None:
        connection = self._dbcon()
        cursor = connection.cursor()
        try:
            query = f"SELECT * FROM Transaction WHERE ID = {id};"
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)

            if df.shape[0] == 0:
                print(f'No transaction with id: {id}')
                self._close_dbcon(connection, cursor)
                return

            query = self._generate_insert_query('Historical_transaction', df)
            cursor.execute(query)
            connection.commit()

            del_query = f"DELETE FROM Transaction WHERE ID = {id};"
            cursor.execute(del_query)
            connection.commit()

            self._close_dbcon(connection, cursor)
            return

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self._close_dbcon(connection, cursor)
            return
