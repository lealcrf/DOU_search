from datetime import date
import requests
from .card_template import publicacao_to_card, sumula_vazia_card
import os
from enum import Enum

class SumulaVazia(Exception):
    pass


class Endpoints(Enum):
    """Endpoints que são usados para se conectar com a api do teams"""

    AREA_DE_TESTE = os.getenv("TEAMS_API_ENDPOINT_TESTE")
    OFICIAL = os.getenv("TEAMS_API_ENDPOINT")
    LIGIANE = os.getenv("TEAMS_API_ENDPOINT_LIGIANE")


def enviar_sumula_para_o_teams(
    sumula: dict,
    dia: date,
    api_endpoint: Endpoints = Endpoints.AREA_DE_TESTE,
):
    """Envia a súmula em fortado de cards para o canal do projeto no teams"""
    try:
        # | Se o robô não achar nenhuma publicação, ele vai enviar uma mensagem avisando o ocorrido
        if len(sumula) == 0:
            raise SumulaVazia()

        payload = {
            "cabecalho": "Publicações do dia " + dia.strftime("%d/%m/%Y"),
            "escopos": [
                {
                    "escopo": escopo,
                    "publicacoes": [
                        {"publicacao": publicacao_to_card(pub)} for pub in pubs
                    ],
                }
                for escopo, pubs in sumula.items()
            ],
        }
    except SumulaVazia:
        payload = {
            "cabecalho": f"Publicações do dia " + dia.strftime("%d/%m/%Y"),
            "escopos": [
                {
                    "escopo": "",
                    "publicacoes": [{"publicacao": sumula_vazia_card()}],
                }
            ],
        }

    requests.post(api_endpoint.value, json=payload)
