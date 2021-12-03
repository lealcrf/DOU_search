from utils import ColumnSearch, FiltrarPorCategoria


class FiltragemPorMotivoGeral(FiltrarPorCategoria):
    def publicacoes_DO1(self):
        """Todos as publicacões que não sejam Instruções normativas do Banco Central no DO1 entram na súmula"""

        return self._filtro.keyword_search(
            searches=[
                ColumnSearch([self._filtro.df.escopo], ["Banco Central"]),
                ColumnSearch([self._filtro.df.secao], ["DO1"]),
            ],
            where=(self._filtro.df.tipo_normativo != "Instrução Normativa"),
        ).assign(motivo="Publicação do BC no DO1 que não é intrução normativa")
