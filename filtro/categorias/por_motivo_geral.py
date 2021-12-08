from utils import ColumnSearch, Pattern
from .filtrar_por_categoria import FiltrarPorCategoria



class FiltragemPorMotivoGeral(FiltrarPorCategoria):
    def publicacoes_DO1(self):
        """Todos as publicacões que não sejam Instruções normativas do Banco Central no DO1 entram na súmula"""

        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(self._df.escopo, [Pattern("Banco Central")]),
                ColumnSearch(self._df.secao, [Pattern("DO1")]),
            ],
            where=(self._df.tipo_normativo != "Instrução Normativa"),
        ).assign(motivo="Publicação do BC no DO1 que não é intrução normativa")
