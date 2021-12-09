from ..filtro import Filtro


class FiltragemPorEmenta(Filtro):
    def frases_gerais(self):
        return self.query(
            self.match(
                self._df.ementa,
                [
                    "Conselho de Controle de Atividades Financeiras",  # A[123]
                    "Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização",  # A[123]
                    "Comitê de Estabilidade Financeira",  # A[123]
                    "Educação financeira",  # A[123],
                    "Comitê Nacional de Educação Financeira",  # A[123]
                    "Imposto sobre Operações Financeiras",  # A[123]
                    "Programa Nacional de Apoio às Microempresas e Empresas de Pequeno Porte",  # A44
                    "Lavagem de Dinheiro",  # A45
                    "Lei geral de proteção de dados",  # R2A1
                    "LGPD",  # R2A1
                    "Decreto nº 10.835",  # R2A6
                    "Subdelega competências para a prática de atos de gestão de pessoas no âmbito do Ministério da Economia às autoridades que menciona",  # R2A7
                    "Sistema de Pessoal Civil da Administração Federal",  # R2A8
                    "Lei nº 8.429",  # R2A11
                    "Lei nº 14.133",  # R2A11
                    "Programa de Estímulo ao Crédito",  # R2Extra
                ],
            )
        )

    def menciona_bc_no_conteudo(self):
        df = self._df

        return self.query(
            self.match(df.ementa, "Comitê Gestor da Segurança da Informação")  # R2A10
            & self.match(df.conteudo, "Banco Central"),
            motivo="Comitê Gestor da Segurança da Informação na ementa e menciona o Banco Central no conteúdo",
        )

    def instrucao_normativa_misterio_da_economia_administracao_publica(self):
        return self.query(
            self.match(
                self._df.ementa,
                "Administração Pública federal direta, autárquica e fundacional",
            )
            & self.match(self._df.escopo, "Ministério da Economia")
            & (self._df.tipo_normativo == "Instrução Normativa")  # A4,
        ).assign(
            motivo="'Administração Pública federal direta, autárquica e fundacional' na ementa de Instruções Normativas do Ministério da Economia"
        )
