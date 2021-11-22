import datetime
from typing import List
import pandas as pd
import re
import operator
from functools import reduce

from terms import ASSINATURA_DIRETORES_E_PRESIDENTE, TERMOS_DE_POSSE


class Search:
    def __init__(self, df: pd.DataFrame, date: datetime.date = None):
        self.df = df[df.data == str(date)] if date is not None else df

    def keyword_search(
        self, columns: List[pd.Series], keywords: List[str], where=None
    ) -> pd.DataFrame:

        regex = f'({"|".join(keywords)})'
        frames = [
            self.df[
                column.str.contains(regex, flags=re.IGNORECASE, regex=True, na=False)
            ]
            for column in columns
        ]

        df = pd.concat(frames)

        if where is None:
            return df

        return df[where]

    def diretores_e_presidente(self) -> pd.DataFrame:
        return self.keyword_search(
            columns=[self.df.assinatura.str.normalize("NFD")],
            keywords=ASSINATURA_DIRETORES_E_PRESIDENTE,
        )

    def atos_do_CMN(self) -> pd.DataFrame:
        return self.keyword_search(
            columns=[self.df.titulo],
            keywords=["CMN"],
        )

    def banco_central_secao_1(self) -> pd.DataFrame:
        return self.keyword_search(
            columns=[self.df.escopo],
            keywords=["Banco Central"],
            where=(self.df.secao.str.contains("DO1")),
        )

    def posse_de_cargo(self) -> pd.DataFrame:
        return self.keyword_search(
            columns=[self.df.conteudo, self.df.titulo],
            keywords=TERMOS_DE_POSSE,
        )
