from datetime import date
from dotenv import load_dotenv
from src.dou import DOU
from src.utils import DateRange

load_dotenv()


def lambda_handler(event, context):

    data_inicial = date(2022, 1, 7)
    data_final = date(2022, 1, 7)

    dou = DOU(
        date_range=DateRange(data_inicial, data_final),
        is_remote_db=True,
    )

    if dou.df.empty:
        return {
            "body": f"Não encontrou publicações nos DOUs do dia {data_inicial} (apenas publicações extras) e {data_final}",
            "status": "VAZIO",
        }

    sumula = dou.gerar_sumula(versao_oficial=True)

    return {"body": sumula, "status": "OK"}
