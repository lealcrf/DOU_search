import json
import math


def publicacao_to_card(pub):

    rows_necessarias = math.ceil(len(pub["motivos"]) / 2)

    body = [
        titulo(pub["titulo"], pub["url"]),
        ementa(pub["ementa"]),
        *[row(pub["motivos"], n_row) for n_row in range(rows_necessarias)],
    ]

    return "{}".format(
        json.dumps(
            {
                "type": "AdaptiveCard",
                "body": body,
                "msteams": {"width": "Full"},
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.2",
            }
        ),
    )


def sumula_vazia_card():
    return "{}".format(
        json.dumps(
            {
                "type": "AdaptiveCard",
                "body": [ementa("O robô não achou nenhuma publicação hoje")],
                "msteams": {"width": "Full"},
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.2",
            }
        ),
    )


def titulo(titulo, url):
    return {
        "type": "Container",
        "items": [
            {
                "type": "TextBlock",
                "size": "Large",
                "weight": "Bolder",
                "text": f"[{titulo}]({url})",
                "color": "Accent",
                "horizontalAlignment": "Center",
            }
        ],
        "style": "emphasis",
        # "style": "Attention",
    }


def ementa(ementa):
    return {
        "type": "Container",
        "items": [
            {
                "type": "TextBlock",
                "text": ementa,
                "wrap": True,
            },
        ],
    }


def row(motivos, n_row):
    index_motivo_inicial = n_row * 2
    index_motivo_final = 2 * (n_row + 1)

    if index_motivo_final > len(motivos):
        index_motivo_final -= 1

    return {
        "type": "ColumnSet",
        "columns": [
            {
                "type": "Column",
                "width": "stretch",
                "items": [
                    # | Divide a lista em pedaços de 2, preenchendo os slots disponíveis com os motivos correspondentes
                    {
                        "type": "TextBlock",
                        "text": motivos[index],
                        "wrap": True,
                    }
                ],
                "style": "emphasis",
                "spacing": "Small",
            }
            for index in range(index_motivo_inicial, index_motivo_final)
        ],
    }
