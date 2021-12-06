from termos import AFASTAMENTO, KEYWORDS_CONTEUDO, NOMEACAO_E_EXONERACAO
from utils import ColumnSearch, FiltrarPorCategoria
import pandas as pd


class FiltragemPorConteudo(FiltrarPorCategoria):
    def keywords_conteudo(self):
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

    def menciona_o_banco_central_no_conteudo(self):
        gabinete_de_segurança_institucional = self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    [self._filtro.df.escopo], ["Gabinete de Segurança Institucional"]
                ),
                ColumnSearch([self._filtro.df.conteudo], ["Banco Central"]),
            ]
        ).assign(
            motivo="Publicação do Gabinete de Segurança Institucional que menciona o Banco Central no conteúdo"
        )

        comite_gestor_da_seguranca_da_informacao = self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    [self._filtro.df.ementa],
                    ["Comitê Gestor da Segurança da Informação"],
                ),
                ColumnSearch([self._filtro.df.conteudo], ["Banco Central"]),
            ]
        ).assign(
            motivo="Citou o Comitê Gestor da Segurança da Informação na ementa e o Banco Central no conteúdo"
        )

        return pd.concat(
            [
                gabinete_de_segurança_institucional,
                comite_gestor_da_seguranca_da_informacao,
            ]
        ).drop_duplicates(subset="id")
