from dotenv import load_dotenv
from src.dou import DOU
from src.utils import DateRange, str_to_date
from src.infrastructure.repository import query_dou_remote

load_dotenv()


def lambda_handler(event, context):
    ultimos_dois_dous = query_dou_remote(
        "SELECT DISTINCT TOP 2 * FROM c.data as d ORDER BY d DESC"
    )

    data_inicial = ultimos_dois_dous[1]
    data_final = ultimos_dois_dous[0]

    dou = DOU(
        date_range=DateRange(data_inicial, data_final),
        is_from_remote_db=True,
    )
    
    sumula = dou.gerar_sumula(versao_oficial=True)    
    
    if len(sumula) == 0:
        return {
            "body": f"Não encontrou publicações nos DOUs do dia {data_inicial} (pub extra) e {data_final}",
            "status": "VAZIO",
        }

    return {"body": sumula, "status": "OK"}
