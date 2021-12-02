import pandas as pd
from utils import ColumnSearch


class Geral:
    def __init__(self, search):
        self._search = search
        self._df = self._search.df

    def atos_e_resolucoes_do_CMN(self):
        """Qualquer ato do CMN entra na súmula"""

        return self._search.keyword_search(
            searches=[ColumnSearch([self._df.titulo], [r"\sCMN\s"])]
        ).assign(motivo="Ato do CMN")

    def posse_e_exoneracao_de_cargo(self):
        """Toda posse/exoneração de um cargo importante vai pra súmula"""

        return self._search.keyword_search(
            searches=[ColumnSearch([self._df.conteudo], POSSE_E_EXONERACAO)],
        ).assign(motivo="posse e exoneração de cargo")

    def afastamento(self):
        return self._search.keyword_search(
            searches=[ColumnSearch([self._df.conteudo], AFASTAMENTO)],
        ).assign(motivo="Afastamento")

    def instrucao_normativa_misterio_da_economia_administracao_publica(self):
        return self._search.keyword_search(
            searches=[
                ColumnSearch(
                    [self._df.ementa],
                    ["Administração Pública federal direta, autárquica e fundacional"],
                ),
                # ColumnSearch([self._df.tipo_normativo], ["Instrução Normativa"]),
                ColumnSearch([self._df.escopo], ["Ministério da Economia"]),
            ],
        ).assign(
            motivo="'Administração Pública federal direta, autárquica e fundacional' na ementa de Instruções normativas do Ministério da Economia"
        )

    # TODO Tirar isso daqui e separar para afastamento e assinatura
    def coaf(self):
        """
        - Quando o presidente do COAF se ausenta, é substituido em caso de férias ou faz uma viagem
        - Quando uma portaria é assinada pelo presidente do COAF
        """

        # Sempre que o presidente do COAF se ausenta, o Presidente do Banco Central do Brasil precisa fazer um despacho
        ausencia_do_presidente = self._search.keyword_search(
            searches=[
                ColumnSearch(
                    [self._df.conteudo],
                    [
                        "Despacho do Presidente do Banco Central do Brasil.+Presidente do COAF"
                    ],
                ),
            ]
        ).assign(motivo="Presidente do COAF se ausentou (férias, substituído, etc)")

        resoluções_assinadas_pelo_presidente = self._search.keyword_search(
            searches=[ColumnSearch([self._df.assinatura], keywords=["RICARDO LIÁO"])],
            where=self._df.tipo_normativo == "Portaria",
        ).assign(motivo="Portaria assinada pelo pelo presidente do COAF")

        return pd.concat(
            [ausencia_do_presidente, resoluções_assinadas_pelo_presidente]
        ).drop_duplicates(subset="id")

    def filtrar_por_conteudo(self):
        return self._search.keyword_search(
            searches=[ColumnSearch([self._df.conteudo], KEYWORDS_CONTEUDO)],
        ).assign(motivo="contém alguma das frases explicitadas em KEYWORDS_CONTEUDO")

    def filtrar_por_titulo(self):
        return self._search.keyword_search(
            searches=[ColumnSearch([self._df.titulo], KEYWORDS_TITULO)],
        ).assign(motivo="contém alguma das frases explicitadas em KEYWORDS_TITULO")

    def filtrar_por_ementa(self):
        return self._search.keyword_search(
            searches=[ColumnSearch([self._df.ementa], KEYWORDS_EMENTA)],
        ).assign(motivo="contém alguma das frases explicitadas em KEYWORDS_EMENTA")


AFASTAMENTO = [
    "(Exposição|Exposições) de Motivos.+Presidente do Banco Central do Brasil",
    "(Exposição|Exposições) de Motivos.+Ministro de Estado da Economia",
    "A DIRETORA DE ADMINISTRAÇÃO DO BANCO CENTRAL DO BRASIL",
    "PORTARIA.+O MINISTRO DE ESTADO DA ECONOMIA;+afastamento",
]

POSSE_E_EXONERACAO = [
    # Assunto 6:
    "cargo de Presidente do Banco Central",
    # Assunto 7:
    "cargo de Diretor do Banco Central",
    "cargo de Diretora do Banco Central",
    # Assunto 11:
    "cargo de Secretário Especial de Fazenda do Ministério da Economia",
    # Assunto 12:
    "cargo de Secretário-Executivo do Ministério da Economia",
    # Assunto 13:
    "cargo de Secretário de Política Econômica",
    # Assunto 14:
    "cargo de Secretário do Tesouro Nacional",
    # Assunto 15:
    "cargo de Presidente da Casa da Moeda do Brasil",
    # Assunto 16:
    "cargo de Diretor da Comissão de Valores Mobiliários",
    # Assunto 17:
    "cargo de Superintendente da Superintendência de Seguros Privados",
    # Assunto 18:
    "cargo de Diretor da Superintendência de Seguros Privados",
    # Assunto 19:
    "cargo de Diretor-Superintendente da Superintendência Nacional de Previdência Complementar",
    # Assunto 20:
    "cargo de Diretor de Licenciamento da Superintendência Nacional de Previdência Complementar",
    # Assunto 21:
    "cargo de Secretário Especial Adjunto da Secretaria Especial de Previdência e Trabalho do Ministério da Economia",
    # Assunto 22:
    "cargo de Secretário-Executivo do Ministério do Trabalho e Previdência",
    ###################################################################
    # Assunto 10:
    "cargo de Ministro de Estado da Economia",
    #
    "cargo de Ministro de Estado do Trabalho e Previdência",
]

KEYWORDS_CONTEUDO = [
    "Comissão Técnica da Moeda e do Crédito",
    "Secretário-Executivo Adjunto da Secretaria-Executiva do Ministério do Trabalho e Previdência",
    "Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização",
]
KEYWORDS_TITULO = [
    "Resolução Coremec",
]

KEYWORDS_EMENTA = [
    "Lavagem de Dinheiro",
    "Programa Nacional de Apoio às Microempresas e Empresas de Pequeno Porte",
    "Proteção de Dados",
]
