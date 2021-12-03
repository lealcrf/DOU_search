from typing import List
import unicodedata
import pandas as pd


def tirar_acentuacao(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


class ColumnSearch:
    def __init__(self, columns: List[pd.Series], keywords: List[str]):
        # Se for assinatura, remove a acentuação de tudo para fazer uma melhor comparação (a acentuação das assinaturas são consistentes)

        clean_columns = []

        tem_assinatura = False

        for column in columns:
            if column.name == "assinatura":
                tem_assinatura = True

                clean_columns.append(
                    column.str.normalize("NFKD")
                    .str.encode("ascii", errors="ignore")
                    .str.decode("utf-8")
                )

            else:
                clean_columns.append(column)

        self.columns = clean_columns

        if tem_assinatura:
            self.keywords = [tirar_acentuacao(i) for i in keywords]
        else:
            self.keywords = keywords


class FiltrarPorCategoria:
    def __init__(self, filtro):
        self._filtro = filtro

    def aplicar_filtros(self):
        results = []
        for name in dir(self):
            obj = getattr(self, name)
            if callable(obj) and name != "aplicar_filtros" and name[:2] != "__":
                results.append(obj())

        return pd.concat(results).drop_duplicates(subset="id")
