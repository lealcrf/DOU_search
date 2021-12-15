import mysql.connector
import json
from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection
import pandas as pd
from pandas.core.frame import DataFrame
from model import Publicacao
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class PublicacoesDB:
    def __init__(self, is_local=True):
        if is_local:
            self._conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="oasuet10",
                database="dou_db_local",
            )

        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()

    @property
    def connection(self) -> MySQLConnection:
        return self._conn

    @property
    def cursor(self) -> MySQLCursor:
        return self._cursor

    def commit(self):
        self.connection.commit()

    def _close(self, commit=False):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def _fetchall(self):
        resp = [Publicacao(*pub) for pub in self.cursor.fetchall()]
        return pd.DataFrame(resp)

    def query(self, sql, params=None) -> pd.DataFrame:
        self.cursor.execute(sql, params or ())
        return self._fetchall()


class SumulaDB:
    def __init__(self) -> None:
        cred = credentials.Certificate("cred.json")
        firebase_admin.initialize_app(cred, {"projectId": "sumula-dou"})
        self.db = firestore.client()

    def inserir_publicacoes(self, df: DataFrame):
        pubs = [i.to_dict() for i in df.iloc]

        for pub in pubs:
            pub.update({"data": str(pub["data"])})
            self.db.collection(pub["data"]).document(pub["id_materia"]).set(pub)
