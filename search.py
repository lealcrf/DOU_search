import datetime
from typing import Dict, List
import pandas as pd
import re


from terms import ASSINATURAS, TERMOS_DE_POSSE
from utils import ColumnSearch, tirar_acentuacao


class Search:
    def __init__(self, df: pd.DataFrame, date: datetime.date = None, is_csv=False):
        if is_csv:
            self.df = df[df.data == str(date)] if date is not None else df
        else:
            self.df = df[df.data == date] if date is not None else df

    def keyword_search(self, searches: List[ColumnSearch], where=None) -> pd.DataFrame:
        """Retorna as publicacões que tiverem todos os termos explicitados em [searches]"""

        result_df = self.df

        # Faz cada pesquisa individualmente, sendo o resultado da última o input da próxima
        for search in searches:
            key_words_regex = f'({"|".join(search.keywords)})'

            result_df = result_df[
                search.column.str.contains(
                    key_words_regex, flags=re.IGNORECASE, regex=True, na=False
                )
            ]

        if where is None:
            return result_df

        return result_df[where]

    def atos_e_resolucoes_do_CMN(self):
        """Qualquer ato do CMN entra na súmula"""
        return self.keyword_search(
            columns=[self.df.titulo],
            keywords=[r"\sCMN\s"],
        ).assign(motivo="Ato do CMN")

    def posse_e_exoneracao_de_cargo(self):
        """Toda posse/exoneração de um cargo importante vai pra súmula"""

        return self.keyword_search(
            columns=[self.df.conteudo, self.df.titulo],
            keywords=TERMOS_DE_POSSE,
        ).assign(motivo="posse e exoneração de cargo")

    # def afastamentos(self):
    #     return self.keyword_search(
    #         columns=[self.df.conteudo],
    #         keywords=TERMOS_DE_AFASTAMENTO,
    #     ).assign(motivo="Afastamento")

    def coaf(self):
        ausencia_do_presidente = self.keyword_search(
            columns=[self.df.conteudo],
            keywords=[
                "Despacho do Presidente do Banco Central do Brasil.+Presidente do COAF"
            ],  # Sempre que o presidente do COAF se ausenta, o Presidente do Banco Central do Brasil precisa fazer um despacho
        ).assign(motivo="Presidente do COAF se ausentou (férias, substituído, etc)")

        resoluções_assinadas_pelo_presidente = self.keyword_search(
            columns=[self.df.assinatura],
            keywords=["RICARDO LIÁO"],
            where=(self.df.secao.str.contains("DO1"))
            & (self.df.tipo_normativo == "Resolução"),
        ).assign(motivo="Resolução assinada pelo presidente do COAF")

        return pd.concat(
            [ausencia_do_presidente, resoluções_assinadas_pelo_presidente]
        ).drop_duplicates(subset="id")

    def gerar_sumula(self) -> pd.DataFrame:
        return pd.concat(
            [
                self.assinaturas_dos_diretores_e_presidente_do_BC(),
                self.atos_e_resolucoes_do_CMN(),
                self.banco_central_secao_1(),
                self.posse_e_exoneracao_de_cargo(),
            ]
        ).drop_duplicates(subset="id")
