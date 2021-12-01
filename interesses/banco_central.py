from utils import ColumnSearch
import pandas as pd


class BancoCentral:
    def __init__(self, search):
        self._search = search
        self._df = self._search.df

    def publicacoes_DO1(self):
        """Todos as publicacões que não sejam Instruções normativas do Banco Central no DO1 entram na súmula"""

        return self._search.keyword_search(
            searches=[
                ColumnSearch([self._df.escopo], ["Banco Central"]),
                ColumnSearch([self._df.secao], ["DO1"]),
            ],
            where=(self._df.tipo_normativo != "Instrução Normativa"),
        ).assign(motivo="Publicação do BC no DO1 que não é intrução normativa")

    def assinaturas_dos_diretores_e_presidente(self):
        """Qualquer coisa assinada por um diretor/presidente do BC entra na súmula

        Ao comparar as assinaturas, ele vai remover as acentuações, uma vez que o uso de acentuação é bem inconsistente
        """
        return self._search.keyword_search(
            searches=[
                ColumnSearch(
                    columns=[self._df.assinatura],
                    keywords=ASSINATURAS_DIRETORES_E_PRESIDENTE_DO_BC,
                )
            ]
        ).assign(motivo="Assinatura de um diretor ou pelo presidente do BC")

    def orgao_importante_menciona_o_banco_central_na_ementa(self):
        por_escopo = self._search.keyword_search(
            searches=[
                ColumnSearch(
                    [self._df.escopo], ["Secretaria Especial do Tesouro e Orçamento"]
                ),
                ColumnSearch([self._df.ementa], ["Banco Central"]),
            ]
        ).assign(
            motivo="Publicação da Secretaria Especial do Tesouro e Orçamento que contém 'Banco Central' na ementa"
        )

        por_titulo = self._search.keyword_search(
            searches=[
                # TODO Saber se é COAF ou CONAF
                ColumnSearch([self._df.titulo], ["SUSEP", "PREVIC", "CONAF"]),
                ColumnSearch([self._df.ementa], ["Banco Central"]),
            ]
        ).assign(
            motivo="Publicação da SUSEP, PREVIC ou CONAF que contém 'Banco Central' na ementa"
        )

        return pd.concat([por_escopo, por_titulo]).drop_duplicates(subset="id")


ASSINATURAS_DIRETORES_E_PRESIDENTE_DO_BC = [
    # * = Não aparece nenhuma vez no meu banco de dados
    "ROBERTO DE OLIVEIRA CAMPOS NETO",  # Presidente
    "Maurício Costa de Moura",  # * Diretor de Relacionamento, Cidadania e Supervisão de Conduta - Direc
    "Paulo sérgio Neves Souza",  # * Diretor de Fiscalização - Difis
    "Fabio Kanczuk",  # * Diretor de Política Econômica - Dipec
    "Bruno Serra Fernandes",  # Diretor de Política Monetária - Dipom
    "Fernanda Guardado",  # * Diretora de Assuntos Internacionais e de Gestão de Riscos Corporativos - Direx
    "João Manoel Pinho de Mello",  # Diretor de Organização do Sistema Financeiro e de Resolução - Diorf
    "Otávio Ribeiro Damaso",  # * Diretor de Regulação - Dinor
    "Carolina de Assis Barros",  # Diretora de Administração - Dirad
]
