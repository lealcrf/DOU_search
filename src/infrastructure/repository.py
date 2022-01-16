from datetime import date
import pandas as pd
from pandas.core.frame import DataFrame
from .models.publicacao import Publicacao
import config
from azure.cosmos import CosmosClient
import concurrent.futures
from datetime import timedelta
import requests



def pegar_publicacoes_dou_db_remote(do_dia: date, incluir_n_dias_passados: int = 0):

    client = CosmosClient(
        url=config.cosmos["ACCOUNT_URI"],
        credential=config.cosmos["ACCOUNT_KEY"],
    )

    db = client.get_database_client(config.cosmos["DATABASE_ID"])
    container = db.get_container_client("dou")

    data_inicial = str(do_dia - timedelta(days=incluir_n_dias_passados))
    data_final = str(do_dia)

    sql = f"SELECT * FROM c WHERE c.data BETWEEN '{data_inicial}' AND '{data_final}'"

    pubs = [
        Publicacao.from_database(json)
        for json in list(container.query_items(sql, enable_cross_partition_query=True))
    ]

    return pd.DataFrame(pubs)


# def inserir_publicacoes_dou_db(df: DataFrame):
#     """Coloca as publicações na database [dou] no (cosmosDB)"""

#     client = CosmosClient(
#         url=config.cosmos["ACCOUNT_URI"],
#         credential=config.cosmos["ACCOUNT_KEY"],
#     )
#     db = client.get_database_client(config.cosmos["DATABASE_ID"])
#     container = db.get_container_client("dou")

#     def _upsert(pub):
#         pub.update({"data": str(pub["data"])})

#         try:
#             container.upsert_item(pub)
#         except:
#             pub.update({"conteudo": pub["conteudo"][0:2500]})
#             container.upsert_item(pub)

#     total = 0
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         for _ in executor.map(_upsert, [i.to_dict() for i in df.iloc]):
#             total += 1
#             print(f"({total}/{len(df)}) = {round((total/len(df))*100, 2)}%")


def pegar_urls_do_ingov(ids: pd.Series) -> str:
    """Faz um scrape para achar o link da do site in.gov baseado no id da matéria"""

    res = requests.get(
        "https://nfk08v8za2.execute-api.sa-east-1.amazonaws.com/default/ingov_scraper",
        json={"ids": ids.tolist()},
    ).json()
    
    links = res["body"]
    return links