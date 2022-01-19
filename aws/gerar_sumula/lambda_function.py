from dotenv import load_dotenv
from src.dou import DOU
from src.models.publicacao import Publicacao
from src.utils import DateRange
import src.infrastructure.repository as repo

load_dotenv()


def lambda_handler(event, context):
    ultimos_dois_dous = repo.query_dou_remote(
        "SELECT DISTINCT TOP 2 * FROM c.data as d ORDER BY d DESC"
    )

    data_inicial = ultimos_dois_dous[1]
    data_final = ultimos_dois_dous[0]

    dou = DOU(
        date_range=DateRange(data_inicial, data_final),
        get_from_remote_db=True,
    )

    sumula = dou.gerar_sumula()

    if sumula.empty:
        return {
            "body": f"Não encontrou publicações nos DOUs do dia {data_inicial} (pub extra) e {data_final}",
            "status": "VAZIO",
        }

    # | Organiza as publicações de modo a se assemelhar à súmula oficial
    # Tira as publicações que não são extras da súmula passada
    unique_dates = sumula["data"].sort_values().unique()
    if len(unique_dates) == 2:
        is_from_last_edition = sumula.data == sumula.data.min()
        is_not_extra = sumula.secao.str.contains("DO[123]$")

        sumula = sumula[~(is_from_last_edition & is_not_extra)]

    # Divide as publicações por escopo (i.e. seções)
    sumula_seccionada = dict()
    for pub in sumula.transpose().to_dict().values():
        pub = Publicacao(**pub).to_sumula()
        sumula_seccionada.setdefault(pub["escopo"], []).append(pub)

    # Coloca as publicações de cada escopo em ordem alfabética
    for escopo, pubs in sumula_seccionada.items():
        sumula_seccionada[escopo] = sorted(pubs, key=lambda pub: pub["titulo"])

    return {"body": sumula_seccionada, "status": "OK"}
