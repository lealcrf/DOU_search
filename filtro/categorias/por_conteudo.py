from termos import AFASTAMENTO, KEYWORDS_CONTEUDO, NOMEACAO_E_EXONERACAO
from utils import ColumnSearch, FiltrarPorCategoria


class FiltragemPorConteudo(FiltrarPorCategoria):
    def filtrar_por_conteudo(self):
        return self._filtro.keyword_search(
            searches=[ColumnSearch([self._filtro.df.conteudo], KEYWORDS_CONTEUDO)],
        ).assign(motivo="contém alguma das frases explicitadas em KEYWORDS_CONTEUDO")

    def nomeacao_e_exoneracao_de_cargo(self):
        """Toda posse/exoneração de um cargo importante vai pra súmula"""

        return self._filtro.keyword_search(
            searches=[ColumnSearch([self._filtro.df.conteudo], NOMEACAO_E_EXONERACAO)],
        ).assign(motivo="posse e exoneração de cargo")

    def afastamento(self):
        return self._filtro.keyword_search(
            searches=[ColumnSearch([self._filtro.df.conteudo], AFASTAMENTO)],
        ).assign(motivo="Afastamento")
        
        
