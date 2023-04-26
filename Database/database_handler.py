import os
import mysql.connector
from typing import List, Tuple

from dotenv import load_dotenv

load_dotenv()

db_server = os.getenv("DB_SERVER")
db_port = int(os.getenv("DB_PORT"))
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME_ITEMS")

class DatabaseHandler:
    def __init__(self):
        self.db_config = {
            "host": db_server,
            "port": db_port,
            "user": db_username,
            "password": db_password,
            "database": db_name,
            "connection_timeout": 10
        }

    def _connect(self) -> mysql.connector.MySQLConnection:
        return mysql.connector.connect(**self.db_config)

    def create_table(self, table_creation_query: str):
        conn = self._connect()
        cursor = conn.cursor()

        try:
            cursor.execute(table_creation_query)
            conn.commit()
        finally:
            conn.close()

    def insert_data(self, table_name: str, columns: List[str], values: Tuple):
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in values])})"

        conn = self._connect()
        cursor = conn.cursor()

        try:
            cursor.execute(query, values)
            conn.commit()

            return cursor.lastrowid

        finally:
            conn.close()

    def fetch_data(self, table_name: str,
                   columns: List[str],
                   conditions=None,
                   condition_values=None) -> List[Tuple]:

        query_columns = ','.join(columns)

        # Update these lines
        query = f"SELECT {query_columns} FROM {table_name}"
        if conditions:
            query += " WHERE " + conditions.replace("?", "%s")

        condition_values = () if condition_values is None else condition_values

        results = []

        with self._connect() as connection:
            cur = connection.cursor()
            cur.execute(query, condition_values)

            results = list(cur.fetchall())

        return results
