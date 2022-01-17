from ..filtro import Filtro, Pattern


class FiltragemPorEmenta(Filtro):
    def frases_gerais(self):
        return self.query(
            condicoes=self.contains(
                self.df.ementa,
                [
                    Pattern("Conselho de Controle de Atividades Financeiras"),  # A[123]
                    Pattern(
                        "Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização"
                    ),  # A[123]
                    Pattern("Comitê de Estabilidade Financeira"),  # A[123]
                    Pattern("Educação financeira"),  # A[123],
                    Pattern("Comitê Nacional de Educação Financeira"),  # A[123]
                    Pattern("Imposto sobre Operações Financeiras"),  # A[123]
                    Pattern(
                        "Programa Nacional de Apoio às Microempresas e Empresas de Pequeno Porte"
                    ),  # A44
                    Pattern("Lavagem de Dinheiro"),  # A45
                    Pattern("Lei geral de proteção de dados"),  # R2A1
                    Pattern("LGPD"),  # R2A1
                    Pattern("Decreto nº 10.835"),  # R2A6
                    Pattern(
                        "Subdelega competências para a prática de atos de gestão de pessoas no âmbito do Ministério da Economia às autoridades que menciona"
                    ),  # R2A7
                    Pattern(
                        "(?:Sistema de Pessoal Civil da Administração (?:Pública)? Federal|SIPEC)"
                    ),  # R2A8
                    Pattern("Lei nº 8.429"),  # R2A11
                    Pattern("Lei nº 14.133"),  # R2A11
                    Pattern("Programa de Estímulo ao Crédito"),  # R2Extra
                    Pattern(
                        "entidades da administração pública federal"
                    ),  #! #TODO Temporário
                    Pattern("Banco Central"),
                ],
            )
        )

    def na_secao_1(self):
        # TODO VER PORQUE O MEU FILTRO É TÃO LENTO, E VER SE TEM ALGUMA COISA QUE EU POSSO FAZER QUE SE PAREÇA COM ISSO
        # return (
        #     self._df.ementa.str.contains(
        #         "(Poder Executivo Federal|administração pública federal direta e indireta)"
        #     )
        #     & self._df.secao.str.contains("DO1")
        #     & self._df.escopo.str.contains(
        #         "(Atos do Poder Executivo|Ministério da Economia)"
        #     )
        #     & (~self._df.titulo.str.contains("SETO\s?/\s?ME", na=False))
        # )

        return self.query(
            self.contains(
                self.df.ementa,
                [
                    Pattern(
                        "poder executivo federal",
                        'Publicação com escopo "Atos do Poder Executivo" ou "Ministério da Economia" da seção 1 que contém "poder executivo federal" na ementa e não é SETO/ME  Secretaria do Tesouro',
                    ),  # R3A2
                    Pattern(
                        "administração pública federal direta e indireta",
                        'Publicação com escopo "Atos do Poder Executivo" ou "Ministério da Economia" da seção 1 que contém "administração pública federal direta e indireta" na ementa e não é SETO/ME  Secretaria do Tesouro',
                    ),  # R3A3
                ],
            )
            & self.contains(self.df.secao, "DO1")
            & self.contains(
                self.df.escopo,
                [Pattern("Atos do Poder Executivo"), Pattern("Ministério da Economia")],
            )
            & (~self.contains(self.df.titulo, "SETO\s?/\s?ME")),
            motivo='Publicações com escopo "Atos do Poder Executivo" e "Ministério da Economia" da seção 1 que contenham "poder executivo federal" ou "Administração Pública Federal Direta e Indireta" na ementa, excluindo as publicações da (SETO/ME) da Secretaria do Tesouro',
        )  # https://teams.microsoft.com/l/message/19:1bfa966669b646c0a164a0731890fc03@thread.tacv2/1641231369273?tenantId=2a7030a7-3850-453e-96b7-cd5f58ba9ec2&groupId=b6ac4626-ee30-42ff-a204-c14fcbdb1313&parentMessageId=1641231369273&teamName=Projeto%20S%C3%BAmula%20DOU&channelName=Crit%C3%A9rios%20de%20busca&createdTime=1641231369273

    def menciona_bc_no_conteudo(self):
        return self.query(
            self.contains(self.df.ementa, "Comitê Gestor da Segurança da Informação")
            & self.contains(self.df.conteudo, "Banco Central"),
            motivo="Comitê Gestor da Segurança da Informação na ementa e menciona o Banco Central no conteúdo",  # R2A10
        )

    def instrucao_normativa_misterio_da_economia_administracao_publica(self):
        return self.query(
            self.contains(
                self.df.ementa,
                "Administração Pública federal direta, autárquica e fundacional",
            )
            & self.contains(self.df.escopo, "Ministério da Economia")
            & (self.df.tipo_normativo == "Instrução Normativa")  # A4,
        ).assign(
            motivo='• "Administração Pública federal direta, autárquica e fundacional" na ementa de Instruções Normativas do Ministério da Economia'
        )
