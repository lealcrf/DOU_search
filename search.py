import datetime
from typing import List
import pandas as pd
import re

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

        df = pd.concat(frames).drop_duplicates()

        if where is None:
            return df

        return df[where]

    def diretores_e_presidente(self):
        """Qualquer coisa assinada por um diretor/presidente do BC entra na súmula"""
        return self.keyword_search(
            columns=[self.df.assinatura.str.normalize("NFD")],
            keywords=ASSINATURA_DIRETORES_E_PRESIDENTE,
        )

    def atos_do_CMN(self):
        """Qualquer ato do CMN entra na súmula"""
        return self.keyword_search(
            columns=[self.df.titulo],
            keywords=["CMN"],
        )

    def banco_central_secao_1(self):
        """Todos as publicacões que não sejam Instruções normaltivas do Banco Central no DO1 entram na súmula"""
        return self.keyword_search(
            columns=[self.df.escopo],
            keywords=["Banco Central"],
            where=(self.df.tipo_normativo != "Instrução Normativa")
            & (self.df.secao.str.contains("DO1")),
        )

    def posse_de_cargo(self):
        """Toda posse/exoneração de um cargo importante vai pra súmula"""

        return self.keyword_search(
            columns=[self.df.conteudo, self.df.titulo],
            keywords=TERMOS_DE_POSSE,
        )

    def gerar_sumula(self) -> pd.DataFrame:
        return pd.concat(
            [
                self.diretores_e_presidente(),
                self.atos_do_CMN(),
                self.banco_central_secao_1(),
                self.posse_de_cargo(),
            ]
        ).drop_duplicates()
