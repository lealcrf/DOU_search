import re
from sys import flags
from types import ModuleType, NoneType
from typing import List
from numpy import NaN, isnan, nan
import numpy
from numpy.core.numeric import moveaxis
import pandas as pd
from pandas.core import series
from pandas.core.arrays.boolean import BooleanArray
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from utils import tirar_acentuacao
from teste import Pattern
import numpy as np


class Filtro:
    def __init__(self, df: DataFrame):
        self._df: pd.DataFrame = df.copy()
        self._df["motivo"] = None
        self._df.assinatura = df.assinatura.apply(tirar_acentuacao)

    def __call__(self) -> pd.DataFrame:
        """Executa todas as funções da classe, junta os resultados e os devolve como um DataFrame"""
        results = []
        for name in dir(self):
            if name[:2] != "__" and name:
                obj = getattr(self, name)

                if callable(obj) and name not in [
                    self.contains.__name__,
                    self.query.__name__,
                ]:
                    results.append(obj())

        return pd.concat(results).drop_duplicates(subset="id")

    def contains(self, col: Series, patterns: List[Pattern] | str) -> BooleanArray:
        """Procura na coluna os items que satisfaçam algum dos padrões

        - Se [patterns] for List[Pattern], vai adicionar o motivo contido em pattern.motivo na sumula
        - Se [patterns] for str, nenhum motivo será adicionado
        """
        pat_type = type(patterns)

        # Cria o regex a partir das/do [[patterns]]
        if pat_type is list:
            regex = "|".join([f"({p.regex})" for p in patterns])
        else:  # se for uma string
            regex = "({})".format(patterns)

        # Já que tiramos a acentuação do [df.assinatura], temos que fazer o mesmo com as keywords
        if col.name == "assinatura":
            regex = tirar_acentuacao(regex)

        def match(item):
            if item:
                match = re.search(regex, item, flags=re.IGNORECASE)
                if match:
                    if pat_type is list:
                        # Pega o Pattern.motivo correspondente ao regex do match
                        return patterns[match.lastindex - 1].motivo
                    elif pat_type is str:
                        # Temos que retornar alguma coisa pois usamos o método [notna()] para fazer o boolean vector que será retornado por essa função.
                        return patterns

        groups: Series = col.apply(match)

        if pat_type is not str:
            tmp_df = self._df

            def foo(antigo, novo):
                # Caso esse for o primeiro motivo no item
                if antigo is None and type(novo) is str:
                    return novo

                # Caso tenha mais motivos no item
                if antigo is str and type(novo) is str:
                    return antigo + "\n" + novo
                
            self._df.motivo = tmp_df.motivo.combine(groups, foo)
        
        
        return groups.notna()

    def query(self, mask: Series, motivo=None) -> pd.DataFrame:
        res_df = self._df[mask]

        # Caso ele queira apenas 1 motivo para toda query
        if motivo:
            res_df.motivo = motivo

        # Coloca essas mudanças no dataframe
        self._df = res_df

        return res_df
