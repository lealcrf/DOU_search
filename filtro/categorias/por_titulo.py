from termos import KEYWORDS_TITULO
from utils import ColumnSearch, FiltrarPorCategoria


class FiltragemPorTitulo(FiltrarPorCategoria):
        
    def filtrar_por_titulo(self):
        return self._filtro.keyword_search(
            searches=[ColumnSearch([self._filtro.df.titulo], KEYWORDS_TITULO)],
        ).assign(motivo="contém alguma das frases explicitadas em KEYWORDS_TITULO")
        
    def atos_e_resolucoes_do_CMN(self):
        """Qualquer ato do CMN entra na súmula"""

        return self._filtro.keyword_search(
            searches=[ColumnSearch([self._filtro.df.titulo], [r"\sCMN\W"])]
        ).assign(motivo="Ato do CMN")