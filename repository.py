import mysql.connector
import json
from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection

class PublicacoesDB:
    def __init__(self):
        with open("credentials.json", "r") as f:
            cred = json.loads(f.read())

            self._conn = mysql.connector.connect(
                host=cred["ENDPOINT"],
                user=cred["USER"],
                password=cred["PASSWORD"],
                database=cred["DATABASE"],
            )
        
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self) -> MySQLConnection:
        return self._conn

    @property
    def cursor(self) -> MySQLCursor:
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=False):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
