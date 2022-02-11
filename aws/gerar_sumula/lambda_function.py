from .erros import DataErradaNoDBError, SumulaVazia
from src.dou import DOU
from src.models.publicacao import Publicacao
from src.utils import DateRange, str_to_date, today_brazil_tz
import src.infrastructure.repository as repo


def lambda_handler(event, context):
    ultimos_dois_dous = repo.query_dou_remote(
        "SELECT DISTINCT TOP 2 * FROM c.data as d ORDER BY d DESC"
    )

    data_inicial = str_to_date(ultimos_dois_dous[1])
    data_final = str_to_date(ultimos_dois_dous[0])

    if data_final != today_brazil_tz():
        raise DataErradaNoDBError(data_final)

    dou = DOU(
        date_range=DateRange(data_inicial, data_final),
        get_from_remote_db=True,
    )

    sumula = dou.gerar_sumula()

    if sumula.empty:
        raise SumulaVazia(data_inicial, data_final)

    # | Organiza as publicações de modo a se assemelhar à súmula oficial
    # Pega só as publicações de hoje e as extras de ontem
    # Se a data mais antiga não for a de hoje, isso significa que teve súmula ontem
    if sumula.data.min() != today_brazil_tz():
        is_from_last_edition = sumula.data == sumula.data.min()
        is_not_extra = sumula.secao.str.contains("DO[123]$")

        # Tira as publicações que não são extra da edição anterior
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
