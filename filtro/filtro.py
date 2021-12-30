from dataclasses import dataclass
import re
from typing import List
import pandas as pd
from pandas.core.arrays.boolean import BooleanArray
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from utils import tirar_acentuacao
from teste import Pattern


class Filtro:
    def __init__(self, df: DataFrame):
        self._df: pd.DataFrame = df.copy()
        # self._df["motivo"] = None
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

        return pd.concat(results)

    def contains(
        self, col: Series, patterns: List[Pattern] | str | List[str]
    ) -> BooleanArray:
        """Procura na coluna os items que satisfaçam algum dos padrões

        - Se [patterns] for List[Pattern], vai adicionar o motivo contido em pattern.motivo na sumula
        - Se [patterns] for str, nenhum motivo será adicionado
        """
        p_type = type(patterns)
        try:
            inner_type = str if type(patterns[0]) == str else Pattern
        except:
            inner_type = None

        # | Cria o regex a partir das/do [[patterns]]
        # Se [patters] for list[Pattern]
        if (p_type is list) and (inner_type is Pattern):
            # Substitui o motivo dos Patterns que tem motivo vazio por um motivo generico
            for p in patterns:
                p.motivo = p.completar_motivo(col.name)

            regex = "|".join([f"({p.regex})" for p in patterns])

        # Se [patterns] for list[str]
        elif (p_type is list) and (inner_type is str):
            regex = "|".join(["({})".format(p) for p in patterns])

        # Se [patterns] for str
        elif p_type is str:
            regex = "({})".format(patterns)

        # Já que tiramos a acentuação do [df.assinatura], temos que fazer o mesmo com as keywords
        if col.name == "assinatura":
            regex = tirar_acentuacao(regex)

        # (Função Auxiliar) retorna o motivo se o item foi escolhido, caso contrário retorna None
        def _match_motivos(item):
            if item:
                match = re.search(regex, item, flags=re.IGNORECASE)
                if match:
                    if (p_type is list) and (inner_type is Pattern):
                        # Pega o Pattern.motivo correspondente ao regex do match
                        return patterns[match.lastindex - 1].motivo
                    elif (p_type is str) or (p_type is list and inner_type is str):
                        # Apenas [Pattern]'s tem motivo, no entanto temos que retornar alguma coisa, já que vamos usar  o método [notna()] para fazer o boolean vector que será retornado por essa função.
                        return patterns

        # | Cria um df contendo o motivo das publicações que entraram e None nas que não entraram
        motivos: Series = col.apply(_match_motivos)

        # | Adiciona os motivos
        if (p_type is list) and (inner_type is Pattern):  # Só [Pattern] tem motivo
            tmp = self._df

            def _junta_motivo(antigo, novo):
                # Caso esse for o primeiro motivo no item
                if antigo is None and type(novo) is str:
                    return novo

                # Caso tenha mais motivos no item
                if antigo is str and type(novo) is str:
                    return antigo + "\n" + novo

            self._df.motivo = tmp.motivo.combine(motivos, _junta_motivo)

        # | Retorna um boolean array que diz quais são os items que passaram no filtro
        return motivos.notna()

    def query(self, condicoes: BooleanArray, motivo=None) -> pd.DataFrame:
        res_df = self._df[condicoes]

        # Caso ele queira apenas 1 motivo para toda query
        if motivo:
            res_df.motivo = motivo

        # Coloca essas mudanças no dataframe para
        self._df.update(res_df)

        # Retorna apenas o que foi achado pela pesquisa
        return res_df

@dataclass
class Pattern:
    regex: str
    motivo: str = None

    def completar_motivo(self, coluna):
        motivo = "• " + (
            self.motivo if self.motivo else self.criar_motivo_generico(coluna)
        )
        padrao_estipulado = "{}[{}]".format(coluna, self.regex)
        return motivo + " => " + padrao_estipulado

    def criar_motivo_generico(self, coluna):
        if coluna in ["assinatura", "ementa"]:
            return 'Achou "{}" na {}'.format(self.regex, coluna)

        return 'Achou "{}" no {}'.format(self.regex, coluna)