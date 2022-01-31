from dataclasses import dataclass
import re
from typing import List
import pandas as pd
from pandas.core.arrays.boolean import BooleanArray
from pandas.core.frame import DataFrame
from pandas.core.series import Series
import itertools


@dataclass
class Criterio:
    condicao: BooleanArray
    motivo: str

    def aplicar_motivo(self, df: DataFrame):
        motivo_col: Series = df.loc[self.condicao, "motivo"]

        is_motivo_null = motivo_col.isna()
        motivo_col[~is_motivo_null] = motivo_col[~is_motivo_null] + "\n" + self.motivo
        motivo_col[is_motivo_null] = self.motivo

        df.loc[self.condicao, "motivo"] = motivo_col


class Filtro:
    def __init__(self, df: DataFrame):
        self.conteudo = df["conteudo"]
        self.secao = df["secao"]
        self.tipo_normativo = df["tipo_normativo"]
        self.escopo = df["escopo"]
        self.titulo = df["titulo"]
        self.ementa = df["ementa"]
        self.assinatura = df["assinatura"]

    def pegar_criterios(self):
        results = []

        for name in dir(self):
            if name[0] != "_" and name:
                obj = getattr(self, name)

                if callable(obj) and name != self.pegar_criterios.__name__:
                    results.append(obj())

        return itertools.chain.from_iterable(results)


@pd.api.extensions.register_series_accessor("contem")
class ContemPandasExtension:
    def __init__(self, coluna: Series):
        self.coluna = coluna

    def __call__(self, regex):
        return self.coluna.str.contains(regex, na=False, flags=re.IGNORECASE)


@pd.api.extensions.register_series_accessor("nao_contem")
class NaoContemPandasExtension:
    def __init__(self, coluna: Series):
        self.coluna = coluna

    def __call__(self, regex: str):
        return ~self.coluna.str.contains(regex, na=False, flags=re.IGNORECASE)
