from numpy import where
from utils import ColumnSearch, Pattern
from .filtrar_por_categoria import FiltrarPorCategoria


class FiltragemPorEmenta(FiltrarPorCategoria):
    def frases_gerais(self):
        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    self._df.ementa,
                    [
                        Pattern(
                            "Conselho de Controle de Atividades Financeiras",
                            assunto="A[123]",
                        ),
                        Pattern(
                            "Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização",
                            assunto="A[123]",
                        ),
                        Pattern("Comitê de Estabilidade Financeira", assunto="A[123]"),
                        Pattern("Educação financeira", assunto="A[123]"),
                        Pattern(
                            "Comitê Nacional de Educação Financeira", assunto="A[123]"
                        ),
                        Pattern(
                            "Imposto sobre Operações Financeiras", assunto="A[123]"
                        ),
                        Pattern(
                            "Programa Nacional de Apoio às Microempresas e Empresas de Pequeno Porte",
                            assunto="A44",
                        ),
                        Pattern("Lavagem de Dinheiro", assunto="A45"),
                        Pattern("Lei geral de proteção de dados", assunto="R2A1"),
                        Pattern("LGPD", assunto="R2A1"),
                        Pattern("Decreto nº 10.835", assunto="R2A6"),
                        Pattern(
                            "Subdelega competências para a prática de atos de gestão de pessoas no âmbito do Ministério da Economia às autoridades que menciona",
                            assunto="R2A7",
                        ),
                        Pattern(
                            "Sistema de Pessoal Civil da Administração Federal",
                            assunto="R2A8",
                        ),
                        Pattern("Lei nº 8.429", assunto="R2A11"),
                        Pattern("Lei nº 14.133", assunto="R2A11"),
                        Pattern("Programa de Estímulo ao Crédito", assunto="R2Extra"),
                    ],
                ),
            ],
        )

    def banco_central_no_conteudo(self):
        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    self._df.ementa,
                    [
                        Pattern(
                            "Comitê Gestor da Segurança da Informação",
                            assunto="R2A10",
                        )
                    ],
                ),
                ColumnSearch(self._df.conteudo, [Pattern("Banco Central")]),
            ]
        )

    def instrucao_normativa_misterio_da_economia_administracao_publica(self):
        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    self._df.ementa,
                    [
                        Pattern(
                            "Administração Pública federal direta, autárquica e fundacional",
                            assunto="A4",
                        )
                    ],
                ),
                ColumnSearch(self._df.escopo, [Pattern("Ministério da Economia")]),
            ],
            where=self._df.tipo_normativo == "Instrução Normativa",
        ).assign(motivo = "A4| 'Administração Pública federal direta, autárquica e fundacional' na ementa de Instruções Normativas do Ministério da Economia")
