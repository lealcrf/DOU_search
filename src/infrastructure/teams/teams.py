from datetime import date
from pandas import DataFrame
from ..models.publicacao import Publicacao
import requests
import json
from .card_template import publicacao_to_card, sumula_vazia_card
from config import Endpoints


class SumulaVaziaException(Exception):
    pass


def enviar_sumula_para_o_teams(
    sumula: DataFrame, endpoint: Endpoints = Endpoints.FLOW_ENDPOINT_TESTE
):
    """Envia a súmula formatada como card para o canal do projeto no teams"""
    try:
        # | Se o robô não achar nenhuma publicação, ele vai enviar uma mensagem avisando o ocorrido
        if sumula.empty:
            raise SumulaVaziaException()

        secoes = _limpar_e_ordenar_sumula_em_secoes(sumula)

        payload = {
            "cabecalho": f"Publicações do dia {sumula.iloc[0].data.strftime('%d/%m/%Y')}",
            "escopos": [
                {
                    "escopo": escopo,
                    "publicacoes": [
                        {"publicacao": publicacao_to_card(pub)} for pub in pubs
                    ],
                }
                for escopo, pubs in secoes.items()
            ],
        }
    except SumulaVaziaException:
        payload = {
            "cabecalho": f"Publicações do dia {date.today().strftime('%d/%m/%Y')}",
            "escopos": [
                {
                    "escopo": "",
                    "publicacoes": [{"publicacao": sumula_vazia_card()}],
                }
            ],
        }

    requests.post(
        endpoint.value,
        data=json.dumps(payload),
        headers={"content-type": "application/json"},
    )


def _limpar_e_ordenar_sumula_em_secoes(sumula: DataFrame) -> dict[str, list]:
    """Deixa as publicações em uma forma mais organizada e parecida com a súmula oficial

    Na súmula oficial, as publicações são divididas em escopos (que aqui eu estou chamando de seções). Dentro de cada seção, as publicações são ordenadas em ordem alfabética, com o título formatado para mostrar apenas o necessário.
    """
    secoes = dict()

    for pub in sumula.transpose().to_dict().values():
        pub = Publicacao(**pub).to_sumula()

        secoes.setdefault(pub["escopo"], []).append(pub)  # Limpa cada publicação

    # Ordenar as publicações de cada espopo em ordem alfabética do título
    for escopo, pubs in secoes.items():
        secoes[escopo] = sorted(pubs, key=lambda pub: pub["titulo"])

    return secoes
