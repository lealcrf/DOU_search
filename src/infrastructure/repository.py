from datetime import date
import mysql.connector
import pandas as pd
from pandas.core.frame import DataFrame
from .models.publicacao import Publicacao
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from azure.cosmos import CosmosClient
import concurrent.futures
from datetime import timedelta


def pegar_publicacoes_dou_db_local(do_dia: date = None) -> DataFrame:
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


def pegar_publicacoes_dou_db_remote(do_dia: date, incluir_n_dias_passados: int = 0):

    client = CosmosClient(
        url=config.cosmos["ACCOUNT_URI"],
        credential=config.cosmos["ACCOUNT_KEY"],
    )

    db = client.get_database_client(config.cosmos["DATABASE_ID"])
    container = db.get_container_client("dou")

    data_inicial = str(do_dia-timedelta(days=incluir_n_dias_passados))
    data_final = str(do_dia)

    sql = f"SELECT * FROM c WHERE c.data BETWEEN '{data_inicial}' AND '{data_final}'"

    pubs = [
        Publicacao.from_database(json)
        for json in list(container.query_items(sql, enable_cross_partition_query=True))
    ]

    return pd.DataFrame(pubs)


def inserir_publicacoes_dou_db(df: DataFrame):
    """Coloca as publicações na database [dou] no (cosmosDB)"""

    client = CosmosClient(
        url=config.cosmos["ACCOUNT_URI"],
        credential=config.cosmos["ACCOUNT_KEY"],
    )
    db = client.get_database_client(config.cosmos["DATABASE_ID"])
    container = db.get_container_client("dou")

    def _upsert(pub):
        pub.update({"data": str(pub["data"])})

        try:
            container.upsert_item(pub)
        except:
            pub.update({"conteudo": pub["conteudo"][0:1500]})
            container.upsert_item(pub)

    total = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in executor.map(_upsert, [i.to_dict() for i in df.iloc]):
            total += 1
            print(f"({total}/{len(df)}) = {round((total/len(df))*100, 2)}%")


def pegar_url_do_ingov(id_materia: str) -> str:
    """Faz um scrape para achar o link da do site in.gov baseado no id da matéria"""

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(
            f'https://www.in.gov.br/consulta/-/buscar/dou?q="{id_materia}"&s=todos&exactDate=all&sortType=0'
        )
        print("✅ " + id_materia)
    except:
        print("❌ " + id_materia)

    element: WebElement = driver.find_element(By.XPATH, "//h5[@class='title-marker']/a")
    link = element.get_property("href")

    driver.close()
    return link
