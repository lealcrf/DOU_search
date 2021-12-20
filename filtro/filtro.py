import re
from sys import flags
from types import ModuleType
from typing import List
from numpy import NaN
from numpy.core.numeric import moveaxis
import pandas as pd
from pandas.core.series import Series
from utils import tirar_acentuacao
from teste import Pattern
import numpy as np


class Filtro:
    def __init__(self, dou):
        self._df: pd.DataFrame = dou.df
        self._df.assinatura = self._df.assinatura.apply(tirar_acentuacao)

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

    def contains(self, col: Series, patterns: Pattern | List[Pattern] | str) -> Series:
        """Procura na coluna os items que satisfaçam algum dos padrões

        - Se [patterns] for Pattern ou List[Pattern], vai adicionar o motivo contido em pattern.motivo
        - Se [patterns] for str, faz o

        """

        p_type = type(patterns)

        # Cria o regex a partir de [[patterns]]
        if p_type is list:
            regex = "|".join([f"({p.regex})" for p in patterns])
        elif p_type is Pattern:
            regex = "({})".format(patterns.regex)
        else:
            regex = "({})".format(patterns)

        # Já que tiramos a acentuação do [df.assinatura], temos que fazer o mesmo com as keywords
        if col.name == "assinatura":
            regex = tirar_acentuacao(regex)

        def _pegar_motivo(row):
            if row:
                match = re.search(regex, row, flags=re.IGNORECASE)
                if match:
                    if p_type is list:
                        return patterns[match.lastindex - 1].motivo
                    elif p_type is Pattern:
                        return patterns.regex
                    else:
                        return ""
            return np.NaN

        groups = col.apply(_pegar_motivo)

        if p_type is not str:
            motivos = groups.dropna()

            if "motivo" not in self._df.columns:
                self._df["motivo"] = motivos

            else:
                # self._df.loc[motivos.index, "motivo"]

                # print(locs.value_counts())

                self._df.motivo = self._df.motivo + "\n" + motivos
                # print(self._df.motivo.dropna())

            # for row in locs.items():
            # print(row)

            # locs.apply(lambda row: row + "\n" + motivos.loc[row.index] if row else row)

            # print(locs)

            # locs[locs.isna()] = motivos

            # x: Series = self._df[self._df.index.isin(motivos.index)].motivo
            # print(locs + "sdasdasda" + motivos)
            # print(x + "\n" + motivos)

            # self._df.motivo = locs + "\n" + motivos

        return groups.notna()

    def query(self, filtro: Series, motivo=None) -> pd.DataFrame:
        df = self._df[filtro]
        
        if "motivo" in df.columns:
            print(df.motivo,"\n|===>",  "motivo" in df.columns, motivo)
        

        if motivo:
            if "motivo" in df.columns:
                # df.motivo = df.motivo.apply(lambda i: f"{i}\n{motivo}" if i else motivo)
                print(df.motivo)

                return df

            return df.assign(motivo=motivo)

        return 
