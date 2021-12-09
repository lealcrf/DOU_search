import re
import pandas as pd
from pandas.core.series import Series
from utils import tirar_acentuacao


class Filtro:
    def __init__(self, dou):
        self._df = dou.df
        self._df.assinatura = self._df.assinatura.apply(tirar_acentuacao)

    def __call__(self) -> pd.DataFrame:
        """Executa todas as funções da classe, junta os resultados e os devolve como um DataFrame"""
        results = []
        for name in dir(self):
            obj = getattr(self, name)
            if callable(obj) and name[:2] != "__" and name not in ["match", "query"]:
                results.append(obj())

        return pd.concat(results).drop_duplicates(subset="id")

    def match(self, col: Series, patterns) -> Series:
        # patterns pode ser tanto uma str quanto uma List
        if type(patterns) is list:
            patterns = f'({"|".join(patterns)})'
        else:
            patterns = "({})".format(patterns)

        # Já que tiramos a acentuação do [df.assinatura], temos que fazer o mesmo com os padrões
        if col.name == "assinatura":
            patterns = tirar_acentuacao(patterns)

        res = col.str.extract(
            patterns,
            flags=re.IGNORECASE,
            expand=False,
        )

        self._df["motivo"] = col.name + "(" + res + ")"

        return res.notna()

    def query(self, filtro: Series, motivo=None) -> pd.DataFrame:
        if motivo:
            return self._df[filtro].assign(motivo=motivo)

        return self._df[filtro]
