from datetime import date
import mysql.connector
import pandas as pd

from .models.publicacao import Publicacao

def pegar_publicacoes_dou_db_local(do_dia: date = None) -> pd.DataFrame:
    """Pega publicacoes do banco de dados onde guardamos todas as DOU's"""

    conn = mysql.connector.connect(
        host="127.0.0.1", user="matheus", password="oasuet10", database="test"
    )
    cursor = conn.cursor()

    sql = "SELECT * FROM publicacoes" + (
        f" WHERE data='{str(do_dia)}'" if do_dia else ""
    )

    cursor.execute(sql)

    df = pd.DataFrame(Publicacao(*pub) for pub in cursor.fetchall())

    conn.close()
    return df
