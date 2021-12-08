from utils import ColumnSearch, Pattern
from .filtrar_por_categoria import FiltrarPorCategoria


class FiltragemPorConteudo(FiltrarPorCategoria):
    def frases_gerais(self):
        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    self._df.conteudo,
                    [
                        Pattern(
                            "Comissão Técnica da Moeda e do Crédito",
                            assunto="A8",
                        ),
                        Pattern(
                            "Secretário-Executivo Adjunto da Secretaria-Executiva do Ministério do Trabalho e Previdência",
                            assunto="A23",
                        ),
                        Pattern(
                            "Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização",
                            assunto="A9",
                        ),
                    ],
                )
            ]
        )

    def nomeacao_e_exoneracao_de_cargo(self):
        """Toda posse/exoneração de um cargo importante vai pra súmula"""

        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    self._df.conteudo,
                    [
                        Pattern(
                            "cargo de Presidente do Banco Central",
                            assunto="A6| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Diretor do Banco Central",
                            assunto="A7| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Diretora do Banco Central",
                            assunto="A7| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Ministro de Estado da Economia",
                            assunto="A10| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Ministro de Estado do Trabalho e Previdência",
                            assunto="Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Secretário Especial de Fazenda do Ministério da Economia",
                            assunto="A11| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Secretário-Executivo do Ministério da Economia",
                            assunto="A12| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Secretário de Política Econômica",
                            assunto="A13| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Secretário do Tesouro Nacional",
                            assunto="A14| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Presidente da Casa da Moeda do Brasil",
                            assunto="A15| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Diretor da Comissão de Valores Mobiliários",
                            assunto="A16| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Superintendente da Superintendência de Seguros Privados",
                            assunto="A17| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Diretor da Superintendência de Seguros Privados",
                            assunto="A18| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Diretor-Superintendente da Superintendência Nacional de Previdência Complementar",
                            assunto="A19| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Diretor de Licenciamento da Superintendência Nacional de Previdência Complementar",
                            assunto="A20| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Secretário Especial Adjunto da Secretaria Especial de Previdência e Trabalho do Ministério da Economia",
                            assunto="A21| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Secretário-Executivo do Ministério do Trabalho e Previdência",
                            assunto="A22| Nomeação ou exoneração",
                        ),
                        # -----
                        Pattern(
                            "cargo de Secretário Especial do Tesouro e Orçamento do Ministério da Economia",
                            assunto="R2-A3| Nomeação ou exoneração",
                        ),
                        Pattern(
                            "cargo de Procurador-Geral Federal da Advocacia-Geral da União",
                            assunto="R2-A9| Nomeação ou exoneração",
                        ),
                    ],
                ),
            ],
        )

    def afastamento(self):
        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    self._df.conteudo,
                    [
                        Pattern(
                            "(Exposição|Exposições) de Motivos.+Presidente do Banco Central do Brasil",
                            assunto="A29| Afastamento",
                        ),
                        Pattern(
                            "(Exposição|Exposições) de Motivos.+Ministro de Estado da Economia",
                            assunto="A30| Afastamento",
                        ),
                        Pattern(
                            "A DIRETORA DE ADMINISTRAÇÃO DO BANCO CENTRAL DO BRASIL",
                            assunto="A31| Afastamento",
                        ),
                        Pattern(
                            "PORTARIA.+O MINISTRO DE ESTADO DA ECONOMIA;+afastamento",
                            assunto="A32| Afastamento",
                        ),
                        Pattern(
                            "Despacho do Presidente do Banco Central do Brasil.+Presidente do COAF",
                            assunto="Sempre que o presidente do COAF se ausenta, o Presidente do Banco Central do Brasil precisa fazer um despacho",
                        ),
                    ],
                )
            ],
        )
