from utils import ColumnSearch, Pattern
from .filtrar_por_categoria import FiltrarPorCategoria


class FiltragemPorTitulo(FiltrarPorCategoria):
    def filtrar_por_titulo(self):
        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    self._df.titulo,
                    [
                        Pattern("Resolução Coremec", assunto="A39"),
                        Pattern(r"\sCMN\W", assunto="A43"),
                    ],
                )
            ],
        )

    def banco_central_na_ementa(self):
        self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    self._df.titulo,
                    [
                        Pattern("SUSEP", assunto="R1"),
                        Pattern("PREVIC", assunto="R1"),
                        Pattern("CONAF", assunto="R1"),
                    ],
                ),
                ColumnSearch(self._df.ementa, [Pattern("Banco Central")]),
            ]
        )
