from ..filtro import Filtro


class FiltragemPorConteudo(Filtro):
    def frases_gerais(self):
        return self.query(
            self.match(
                self._df.conteudo,
                [
                    "Comissão Técnica da Moeda e do Crédito",  # A8
                    "Secretário-Executivo Adjunto da Secretaria-Executiva do Ministério do Trabalho e Previdência",  # A23
                    "Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização",  # A9
                    # ******************************** Afastamento/Exoneração ****************************************
                    "cargo de Presidente do Banco Central",  # A6
                    "cargo de Diretor do Banco Central",  # A7
                    "cargo de Diretora do Banco Central",  # A7
                    "cargo de Ministro de Estado da Economia",  # A10
                    "cargo de Ministro de Estado do Trabalho e Previdência",
                    "cargo de Secretário Especial de Fazenda do Ministério da Economia",  # A11
                    "cargo de Secretário-Executivo do Ministério da Economia",  # A12
                    "cargo de Secretário de Política Econômica",  # A13
                    "cargo de Secretário do Tesouro Nacional",  # A14
                    "cargo de Presidente da Casa da Moeda do Brasil",  # A15
                    "cargo de Diretor da Comissão de Valores Mobiliários",  # A16
                    "cargo de Superintendente da Superintendência de Seguros Privados",  # A17
                    "cargo de Diretor da Superintendência de Seguros Privados",  # A18
                    "cargo de Diretor-Superintendente da Superintendência Nacional de Previdência Complementar",  # A19
                    "cargo de Diretor de Licenciamento da Superintendência Nacional de Previdência Complementar",  # A20
                    "cargo de Secretário Especial Adjunto da Secretaria Especial de Previdência e Trabalho do Ministério da Economia",  # A21
                    "cargo de Secretário-Executivo do Ministério do Trabalho e Previdência",  # A22
                    "cargo de Secretário Especial do Tesouro e Orçamento do Ministério da Economia",  # R2-A3
                    "cargo de Procurador-Geral Federal da Advocacia-Geral da União",  # R2-A9
                ],
            )
        )

    def afastamento(self):
        return self.query(
            self.match(
                self._df.conteudo,
                [
                    "Exposi.+ de Motivos.+Presidente do Banco Central do Brasil",  # A29",
                    "Exposi.+ de Motivos.+Ministro de Estado da Economia",  # A30",
                    "A DIRETORA DE ADMINISTRAÇÃO DO BANCO CENTRAL DO BRASIL",  # A31",
                    "PORTARIA.+O MINISTRO DE ESTADO DA ECONOMIA.+afastamento",  # A32",
                    "Despacho do Presidente do Banco Central do Brasil.+Presidente do COAF",  # Sempre que o presidente do COAF se ausenta, o Presidente do Banco Central do Brasil precisa fazer um despacho",
                ],
            ),
            motivo="Afastamento",
        )
