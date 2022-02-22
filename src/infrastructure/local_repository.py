import mysql.connector
import pandas as pd
from src.utils import DateRange
from ..models.publicacao import Publicacao
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pegar_urls_do_ingov(ids: pd.Series):
    """Faz um scrape para achar o link do site in.gov baseado no id da matéria"""

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    urls = []
    for _id in ids:
        # Vai no painel de procura (q esta setado pra procurar o id_materia contido em pub["id"])
        search = f'https://www.in.gov.br/consulta/-/buscar/dou?q="{_id}"&s=todos&exactDate=all&sortType=0'
        driver.get(search)

        # Pega o link do primeiro resultado
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h5[@class='title-marker']/a"))
        )
        url = element.get_property("href")

        urls.append(url)

    driver.quit()
    return urls


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
