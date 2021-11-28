from typing import List
import unicodedata

import pandas as pd


def tirar_acentuacao(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


class ColumnSearch:
    def __init__(self, column: pd.Series, keywords: List[str]):
        # Se for assinatura, remove a acentuação de tudo para fazer uma melhor comparação (a acentuação das assinaturas são consistentes)
        if column.name == "assinatura":
            self.column = (
                column.str.normalize("NFKD")
                .str.encode("ascii", errors="ignore")
                .str.decode("utf-8")
            )
            self.keywords = [tirar_acentuacao(assinatura) for assinatura in keywords]
        else:
            self.column = column
            self.keywords = keywords
