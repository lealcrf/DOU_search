from pandas import DataFrame
from ..models.publicacao import Publicacao
import json
import requests
from .card_template import publicacao_to_card
from config import FLOW_ENDPOINT


def enviar_sumula_para_o_teams(sumula: DataFrame):
    secoes = limpar_e_ordenar_sumula_em_secoes(sumula)

    # TODO Faz alguma coisa para quando a súmula vier vazia, já que isso vai dar erro
    dia = sumula.iloc[0].data.strftime("%d/%m/%Y")

    payload = {
        "cabecalho": "Publicações do dia " + dia,
        "escopos": [
            {
                "escopo": escopo,
                "publicacoes": [{"publicacao": publicacao_to_card(pub)} for pub in pubs],
            }
            for escopo, pubs in secoes.items()
        ],
    }

    requests.post(
        FLOW_ENDPOINT,
        data=json.dumps(payload),
        headers={"content-type": "application/json"},
    )


def limpar_e_ordenar_sumula_em_secoes(sumula: DataFrame) -> dict[str, list]:
    secoes = dict()

    for pub in sumula.transpose().to_dict().values():
        pub = Publicacao(**pub).to_sumula()
        secoes.setdefault(pub["escopo"], []).append(pub)  # Limpa cada publicação

    # Ordenar as publicações de cada espopo em ordem alfabética do título
    for escopo, pubs in secoes.items():
        secoes[escopo] = sorted(pubs, key=lambda pub: pub["titulo"])

    return secoes
