import pandas as pd

class FiltrarPorCategoria:
    def __init__(self, filtro):
        self._filtro = filtro
        self._df = filtro.df

    def __call__(self) -> pd.DataFrame:
        """ Executa todas as funções da classe, junta os resultados e os devolve como um DataFrame """
        results = []
        for name in dir(self):
            obj = getattr(self, name)
            if callable(obj) and name[:2] != "__":
                results.append(obj())

        return pd.concat(results).drop_duplicates(subset="id")
