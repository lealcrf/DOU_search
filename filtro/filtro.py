from typing import List
import pandas as pd
import re

from .categorias.por_assinatura import FiltragemPorAssinatura
from .categorias.por_conteudo import FiltragemPorConteudo
from .categorias.por_titulo import FiltragemPorTitulo
from .categorias.por_ementa import FiltragemPorEmenta
from .categorias.por_motivo_geral import FiltragemPorMotivoGeral

from utils import ColumnSearch


class Filtro:
    def __init__(self, df):
        self.df = df

    @property
    def por_conteudo(self):
        return FiltragemPorConteudo(self)

    @property
    def por_titulo(self):
        return FiltragemPorTitulo(self)

    @property
    def por_ementa(self):
        return FiltragemPorEmenta(self)

    @property
    def por_assinatura(self):
        return FiltragemPorAssinatura(self)

    @property
    def por_motivo_geral(self):
        return FiltragemPorMotivoGeral(self)

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

