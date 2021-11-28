import datetime
from typing import List
import pandas as pd
import re
from interesses.banco_central import BancoCentral
from interesses.geral import Geral

from utils import ColumnSearch


class Search:
    def __init__(self, df: pd.DataFrame, date: datetime.date = None, is_csv=False):
        if is_csv:
            self.df = df[df.data == str(date)] if date is not None else df
        else:
            self.df = df[df.data == date] if date is not None else df

    @property
    def banco_central(self):
        return BancoCentral(self)
        
    @property
    def geral(self):
        return Geral(self)
        

    def gerar_sumula(self) -> pd.DataFrame:
        return pd.concat(
            [
                self.banco_central.assinaturas_dos_diretores_e_presidente(), 
                self.banco_central.publicacoes_DO1(),
                self.banco_central.orgao_importante_menciona_o_banco_central_na_ementa(),
                self.geral.atos_e_resolucoes_do_CMN(),
                self.geral.posse_e_exoneracao_de_cargo(),
                self.geral.coaf(),
            ]
        ).drop_duplicates(subset="id")

    def keyword_search(self, searches: List[ColumnSearch], where=None) -> pd.DataFrame:
        # TODO Deixar essa função mais clean
        
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
