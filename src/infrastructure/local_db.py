import mysql.connector
import pandas as pd
from ..utils import DateRange
from ..models.publicacao import Publicacao


def pegar_publicacoes_dou_db_local(date_range: DateRange = None) -> pd.DataFrame:
    """Pega publicacoes do banco de dados onde guardamos todas as DOU's"""

    conn = mysql.connector.connect(
        host="127.0.0.1", user="matheus", password="oasuet10", database="test"
    )
    cursor = conn.cursor()

    if date_range:
        sql = f"SELECT * FROM publicacoes WHERE data BETWEEN'{date_range.inicio}' AND '{date_range.fim}'"
    else:
        sql = "SELECT * FROM publicacoes"

    cursor.execute(sql)

    df = pd.DataFrame(
        [Publicacao(*pub) for pub in cursor.fetchall()],
        columns=Publicacao.get_fields(),
    )

    conn.close()
    return df
