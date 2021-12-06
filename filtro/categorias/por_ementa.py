import pandas as pd
from termos import KEYWORDS_EMENTA
from utils import ColumnSearch, FiltrarPorCategoria


class FiltragemPorEmenta(FiltrarPorCategoria):
    def keywords_ementa(self):
        return self._filtro.keyword_search(
            searches=[ColumnSearch([self._filtro.df.ementa], KEYWORDS_EMENTA)],
        ).assign(motivo="contém alguma das frases explicitadas em KEYWORDS_EMENTA")

    def menciona_o_banco_central_na_ementa(self):
        secretaria_do_tesouro = self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    [self._filtro.df.escopo],
                    ["Secretaria Especial do Tesouro e Orçamento"],
                ),
                ColumnSearch([self._filtro.df.ementa], ["Banco Central"]),
            ]
        ).assign(
            motivo="Publicação da Secretaria Especial do Tesouro e Orçamento que contém 'Banco Central' na ementa"
        )

        susep_previc_conaf = self._filtro.keyword_search(
            searches=[
                # TODO Saber se é COAF ou CONAF
                ColumnSearch([self._filtro.df.titulo], ["SUSEP", "PREVIC", "CONAF"]),
                ColumnSearch([self._filtro.df.ementa], ["Banco Central"]),
            ]
        ).assign(
            motivo="Publicação da SUSEP, PREVIC ou CONAF que contém 'Banco Central' na ementa"
        )

        return pd.concat(
            [
                secretaria_do_tesouro,
                susep_previc_conaf,
            ]
        ).drop_duplicates(subset="id")

    def instrucao_normativa_misterio_da_economia_administracao_publica(self):
        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    [self._filtro.df.ementa],
                    ["Administração Pública federal direta, autárquica e fundacional"],
                ),
                ColumnSearch([self._filtro.df.escopo], ["Ministério da Economia"]),
            ],
        ).assign(
            motivo="'Administração Pública federal direta, autárquica e fundacional' na ementa de publicações do  Ministério da Economia"
        )
