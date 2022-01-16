from datetime import date
from pandas import DataFrame
import requests
import json
from .card_template import publicacao_to_card, sumula_vazia_card
from .utils import Endpoints, SumulaVazia, limpar_e_ordenar_sumula_em_secoes


def enviar_sumula_para_o_teams(
    sumula: DataFrame, api_endpoint: Endpoints = Endpoints.TESTE
):
    """Envia a súmula formatada como card para o canal do projeto no teams"""
    try:
        # | Se o robô não achar nenhuma publicação, ele vai enviar uma mensagem avisando o ocorrido
        if sumula.empty:
            raise SumulaVazia()

        secoes = limpar_e_ordenar_sumula_em_secoes(sumula)

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
    except SumulaVazia:
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
        api_endpoint.value,
        data=json.dumps(payload),
        headers={"content-type": "application/json"},
    )
