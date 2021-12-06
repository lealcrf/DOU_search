from datetime import date
import pandas as pd
from filtro.filtro import Filtro
from repository import PublicacoesDB


class DOU:
    def __init__(self, df, dia: date = None):
        self._df = df
        self._dia = dia

    @property
    def filtrar(self) -> Filtro:
        if self._dia is None:
            return Filtro(self._df)
        else:
            return Filtro(self._df[self._df.data == self._dia])

    def gerar_sumula(self) -> pd.DataFrame:
        return pd.concat(
            [
                self.filtrar.por_motivo_geral(),
                self.filtrar.por_titulo(),
                self.filtrar.por_ementa(),
                self.filtrar.por_conteudo(),
                self.filtrar.por_assinatura(),
            ]
        ).drop_duplicates(subset="id")
