import mysql.connector
from mysql.connector import cursor
import pandas as pd
from pandas.core.frame import DataFrame
from model import Publicacao
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import requests
import json


try:
    # Firestore
    firebase_admin.initialize_app(
        credential=credentials.Certificate("cred.json"),
        options={"projectId": "sumula-dou"},
    )
    db = firestore.client()

    # MySQL local
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="matheus",
        password="oasuet10",
        database="test",
    )
    cursor = conn.cursor()

    ja_inicializou = True
except:
    pass


def pegar_publicacoes_do_DOU_DB(n_ultimas_publicacoes: int = None) -> DataFrame:
    """Pega publicacoes do banco de dados onde guardamos todas as DOU's

    ## Parametros

    n_ultimas_publicacoes: pega as n publicações mais recentes
    """

    sql = "SELECT * FROM publicacoes {}".format(
        f"ORDER BY data DESC LIMIT {n_ultimas_publicacoes}"
        if n_ultimas_publicacoes
        else ""
    )
    cursor.execute(sql)

    df = pd.DataFrame(Publicacao(*pub) for pub in cursor.fetchall())

    return df


def inserir_publicacoes_sumulaDB(df: DataFrame):
    """Coloca as publicações na base de dados da súmula (firestore)"""

    pubs = [i.to_dict() for i in df.iloc]

    for pub in pubs:
        pub.update({"data": str(pub["data"])})
        db.collection(pub["data"]).document(pub["id_materia"]).set(pub)


def get_link_da_publicacao_ingov(id_materia: str) -> str:
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


def enviar_sumula_para_o_teams(sumula: DataFrame):
    # | Agrupar publicações por escopo (secoes)
    secoes = dict()

    for pub in sumula.transpose().to_dict().values():
        pub = Publicacao(**pub).to_sumula()
        secoes.setdefault(pub["escopo"], []).append(pub)

    # Ordenar as publicações de cada espopo em ordem alfabética do título
    for escopo, pubs in secoes.items():
        secoes[escopo] = sorted(pubs, key=lambda pub: pub["titulo"])

    # | Enviar a publicação para o Teams
    dia = sumula.iloc[0].data.strftime("%d/%m/%Y")
    payload = {
        "cabecalho": "Publicações do dia " + dia,
        "escopos": [
            {"escopo": escopo, "publicacoes": pubs} for escopo, pubs in secoes.items()
        ],
    }

    flow_api = "https://prod-19.brazilsouth.logic.azure.com:443/workflows/c067f4e36ce342489f14345294f117e1/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=pECFeZEKwawc4dsOMD9XBtpNKc3f3zBsTgRZbQ9Vq1k"

    requests.post(
        flow_api,
        data=json.dumps(payload),
        headers={"content-type": "application/json"},
    )
