from ..filtro import Filtro, Criterio


class FiltragemPorEmenta(Filtro):
    def gerais(self):
        yield from [
            Criterio(  # A[123]
                self.ementa.contem(r"Conselho de Controle de Atividades Financeiras"),
                motivo='"Conselho de Controle de Atividades Financeiras" na ementa',
            ),
            Criterio(  # A[123]
                self.ementa.contem(
                    r"Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização",
                ),
                motivo='"Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização" na ementa',
            ),
            Criterio(  # A[123]
                self.ementa.contem(r"Comitê de Estabilidade Financeira"),
                motivo='"Comitê de Estabilidade Financeira" na ementa',
            ),
            Criterio(  # A[123],
                self.ementa.contem(r"Educação financeira"),
                motivo='"Educação financeira" na ementa',
            ),
            Criterio(  # A[123]
                self.ementa.contem(r"Comitê Nacional de Educação Financeira"),
                motivo='"Comitê Nacional de Educação Financeira" na ementa',
            ),
            Criterio(  # A[123]
                self.ementa.contem(r"Imposto sobre Operações Financeiras"),
                motivo='"Imposto sobre Operações Financeiras" na ementa',
            ),
            Criterio(  # A44
                self.ementa.contem(
                    r"Programa Nacional de Apoio às Microempresas e Empresas de Pequeno Porte"
                ),
                motivo='"Programa Nacional de Apoio às Microempresas e Empresas de Pequeno Porte" na ementa',
            ),
            Criterio(  # A45
                self.ementa.contem(r"Lavagem de Dinheiro"),
                motivo='"Lavagem de Dinheiro" na ementa',
            ),
            Criterio(  # R2A1
                self.ementa.contem(r"Lei geral de proteção de dados|LGPD"),
                motivo='"Lei geral de proteção de dados" na ementa',
            ),
            Criterio(  # R2A6
                self.ementa.contem(r"Decreto nº 10.835"),
                motivo='"Decreto nº 10.835" na ementa',
            ),
            Criterio(  # R2A7
                self.ementa.contem(
                    r"Subdelega competências para a prática de atos de gestão de pessoas no âmbito do Ministério da Economia às autoridades que menciona"
                ),
                motivo="#TODO ver o motivo do critério R2A7",
            ),
            Criterio(  # R2A8
                self.ementa.contem(
                    r"(?:Sistema de Pessoal Civil da Administração (?:Pública)? Federal|SIPEC)"
                ),
                motivo="Publicação da SIPEC #TODO Terminar de fazer as restrições do R2A8",
            ),
            Criterio(  # R2A11
                self.ementa.contem(r"Lei nº 8.429"),
                motivo='"Lei nº 8.429" na ementa',
            ),
            Criterio(  # R2A11
                self.ementa.contem(r"Lei nº 14.133"),
                motivo='"Lei nº 14.133" na ementa',
            ),
            Criterio(  # R2Extra
                self.ementa.contem(r"Programa de Estímulo ao Crédito"),
                motivo='"Programa de Estímulo ao Crédito" na ementa',
            ),
            Criterio(
                self.ementa.contem(r"entidades da administração pública federal"),
                motivo='"entidades da administração pública federal" na ementa',
            ),  #! #TODO Temporário
            # Criterio(  # T2022-1-19, R2022-1-30 #TODO Ver melhor o problema
            #     self.ementa.contem(r"Decreto nº 71.733"),
            #     motivo='"Decreto 71.733" na ementa',
            # ),
        ]

    def especificos(self):
        yield from [
            Criterio(  # R3A2
                self.ementa.contem(r"poder executivo federal")
                & self.secao.contem(r"DO1")
                & self.escopo.contem(r"Atos do Poder Executivo")
                & self.titulo.nao_contem(r"SETO\s?/\s?ME"),
                motivo='Ato do Poder Executivo da seção 1 que contém "poder executivo federal" na ementa e não é SETO/ME',
            ),
            Criterio(  # R3A3
                self.ementa.contem(r"poder executivo federal")
                & self.secao.contem(r"DO1")
                & self.escopo.contem(r"Ministério da Economia")
                & self.titulo.nao_contem(r"SETO\s?/\s?ME"),
                motivo='Publicação do Ministério da Economia da seção 1 que contém "poder executivo federal" na ementa e não é SETO/ME',
            ),
            Criterio(  # A4
                self.ementa.contem(
                    "Administração Pública federal direta, autárquica e fundacional"
                )
                & self.escopo.contem(r"Ministério da Economia")
                & self.tipo_normativo.igual("Instrução Normativa"),
                motivo='"Administração Pública federal direta, autárquica e fundacional" na ementa de Instruções Normativas do Ministério da Economia',
            ),
        ]

    def menciona_o_banco_central(self):
        yield from [
            Criterio(  # TODO Implementa o filtro por exclusao e tira meu workaroung
                self.ementa.contem(r"Banco Central")
                & self.tipo_normativo.nao_contem(r"Instrução Normativa"),
                motivo="Menciona o Banco Central na ementa",
            ),
            Criterio(  # R2A10
                self.ementa.contem(r"Comitê Gestor da Segurança da Informação")
                & self.conteudo.contem(r"Banco Central"),
                motivo="Comitê Gestor da Segurança da Informação na ementa e menciona o Banco Central no conteúdo",
            ),
            Criterio(  # T-Carlos-2022-01-25
                self.ementa.contem(
                    r"Grupo de Ação Financeira contra a Lavagem de Dinheiro e o Financiamento do Terrorismo"
                )
                & self.conteudo.contem(r"Banco Central"),
                motivo='"Grupo de Ação Financeira contra a Lavagem de Dinheiro e o Financiamento do Terrorismo" na ementa e menciona o Banco Central',
            ),
        ]
