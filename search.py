import datetime
from typing import Dict, List
import pandas as pd
import re
from subjects.banco_central import BancoCentral


from terms import ASSINATURAS, TERMOS_DE_POSSE
from utils import ColumnSearch, tirar_acentuacao


class Search:
    def __init__(self, df: pd.DataFrame, date: datetime.date = None, is_csv=False):
        if is_csv:
            self.df = df[df.data == str(date)] if date is not None else df
        else:
            self.df = df[df.data == date] if date is not None else df

    @property
    def banco_central(self):
        return BancoCentral(self)

    def gerar_sumula(self) -> pd.DataFrame:
        return pd.concat(
            [
                self.assinaturas_dos_diretores_e_presidente_do_BC(),
                self.atos_e_resolucoes_do_CMN(),
                self.banco_central_secao_1(),
                self.posse_e_exoneracao_de_cargo(),
            ]
        ).drop_duplicates(subset="id")

    def keyword_search(self, searches: List[ColumnSearch], where=None) -> pd.DataFrame:
        """Retorna as publicacões que tiverem todos os termos explicitados em [searches]"""

        result_df = self.df

        # Faz cada pesquisa individualmente, sendo o resultado da última o input da próxima
        for search in searches:
            dfs = []

            for column in search.columns:
                key_words_regex = f'({"|".join(search.keywords)})'

                dfs.append(
                    result_df[
                        column.str.contains(
                            key_words_regex, flags=re.IGNORECASE, regex=True, na=False
                        )
                    ]
                )
            result_df = pd.concat(dfs).drop_duplicates(subset="id")

        if where is None:
            return result_df

        return result_df[where]
