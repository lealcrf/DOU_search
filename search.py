import datetime
from typing import List
import pandas as pd
import re


from terms import ASSINATURAS, COAF, TERMOS_DE_POSSE
from utils import tirar_acentuacao


class Search:
    def __init__(self, df: pd.DataFrame, date: datetime.date = None):
        self.df = df[df.data == date] if date is not None else df

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

    def assinaturas_dos_diretores_e_presidente(self):
        """Qualquer coisa assinada por um diretor/presidente do BC entra na súmula

        Ao comparar as assinaturas, ele vai remover as acentuações, uma vez que o uso de acentuação é bem inconsistente
        """
        return self.keyword_search(
            columns=[
                self.df.assinatura.str.normalize("NFKD")
                .str.encode("ascii", errors="ignore")
                .str.decode("utf-8")
            ],
            keywords=[tirar_acentuacao(assinatura) for assinatura in ASSINATURAS],
        ).assign(motivo = "Assinatura de um diretor ou pelo presidente do BC")

    def atos_e_resolucoes_do_CMN(self):
        """Qualquer ato do CMN entra na súmula"""
        return self.keyword_search(
            columns=[self.df.titulo],
            keywords=[r"\sCMN\s"],
        ).assign(motivo="Ato do CMN")

    def banco_central_secao_1(self):
        """Todos as publicacões que não sejam Instruções normativas do Banco Central no DO1 entram na súmula"""

        return self.keyword_search(
            columns=[self.df.escopo],
            keywords=["Banco Central"],
            where=(self.df.tipo_normativo != "Instrução Normativa")
            & (self.df.secao.str.contains("DO1")),
        ).assign(motivo="Publicação do BC no DO1 que não é intrução normativa")

    def posse_e_exoneracao_de_cargo(self):
        """Toda posse/exoneração de um cargo importante vai pra súmula"""

        return self.keyword_search(
            columns=[self.df.conteudo, self.df.titulo],
            keywords=TERMOS_DE_POSSE,
        ).assign(motivo = "posse e exoneração de cargo")

    def gerar_sumula(self) -> pd.DataFrame:
        return pd.concat(
            [
                self.assinaturas_dos_diretores_e_presidente(),
                self.atos_e_resolucoes_do_CMN(),
                self.banco_central_secao_1(),
                self.posse_e_exoneracao_de_cargo(),
            ]
        ).drop_duplicates(subset="id")
