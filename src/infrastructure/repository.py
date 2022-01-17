import os
import pandas as pd
from pandas.core.frame import DataFrame
from ..models.publicacao import Publicacao
from azure.cosmos import CosmosClient
import concurrent.futures
import requests
from ..utils import DateRange

def pegar_publicacoes_dou_db_remote(date_range: DateRange = None) -> DataFrame:

    client = CosmosClient(
        url=os.getenv("COSMOS_ACCOUNT_URI"),
        credential=os.getenv("COSMOS_ACCOUNT_KEY"),
    )

    db = client.get_database_client(os.getenv("COSMOS_DATABASE_ID"))
    container = db.get_container_client("dou")

    if date_range:
        sql = f"SELECT * FROM c WHERE c.data BETWEEN '{date_range.inicio}' AND '{date_range.fim}'"
    else:
        sql = f"SELECT * FROM c"

    pubs = [
        Publicacao.from_database(json)
        for json in list(container.query_items(sql, enable_cross_partition_query=True))
    ]

    return pd.DataFrame(pubs, columns=Publicacao.get_fields())


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
