from utils import ColumnSearch, Pattern
from .filtrar_por_categoria import FiltrarPorCategoria


class FiltragemPorEscopo(FiltrarPorCategoria):
    def banco_central_no_conteudo(self):
        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    self._df.escopo,
                    [
                        Pattern(
                            "Gabinete de Segurança Institucional",
                            assunto="R2A10",
                        )
                    ],
                ),
                ColumnSearch(
                    self._df.conteudo,
                    [Pattern("Banco Central")],
                ),
            ]
        )

    def banco_central_na_ementa(self):
        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    self._df.escopo,
                    [Pattern("Secretaria Especial do Tesouro e Orçamento")],
                ),
                ColumnSearch(self._df.ementa, [Pattern("Banco Central")]),
            ]
        )
