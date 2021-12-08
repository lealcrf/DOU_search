from utils import ColumnSearch, Pattern
from .filtrar_por_categoria import FiltrarPorCategoria


class FiltragemPorAssinatura(FiltrarPorCategoria):
    def resoluções_assinadas_pelo_presidente_do_COAF(self):
        return self._filtro.keyword_search(
            searches=[ColumnSearch(self._df.assinatura, [Pattern("RICARDO LIÁO")])],
            where=self._df.tipo_normativo == "Portaria",
        ).assign(motivo="A28|assinatura - Portaria assinada pelo pelo presidente do COAF")

    def assinaturas_dos_diretores_e_presidente_do_BC(self):
        """Qualquer coisa assinada por um diretor/presidente do BC entra na súmula

        Ao comparar as assinaturas, ele vai remover as acentuações, uma vez que o uso de acentuação é bem inconsistente
        """
        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    self._df.assinatura,
                    patterns=[
                        Pattern(
                            "ROBERTO DE OLIVEIRA CAMPOS NETO",
                            assunto="Presidente do Banco Central",
                        ),
                        Pattern(
                            "Maurício Costa de Moura",
                            assunto="Diretor do Banco Central",
                        ),
                        Pattern(
                            "Paulo sérgio Neves Souza",
                            assunto="Diretor do Banco Central",
                        ),
                        Pattern(
                            "Fabio Kanczuk",
                            assunto="Diretor do Banco Central",
                        ),
                        Pattern(
                            "Bruno Serra Fernandes",
                            assunto="Diretor do Banco Central",
                        ),
                        Pattern(
                            "Fernanda Guardado",
                            assunto="Diretor do Banco Central",
                        ),
                        Pattern(
                            "João Manoel Pinho de Mello",
                            assunto="Diretor do Banco Central",
                        ),
                        Pattern(
                            "Otávio Ribeiro Damaso",
                            assunto="Diretor do Banco Central",
                        ),
                        Pattern(
                            "Carolina de Assis Barros",
                            assunto="Diretor do Banco Central",
                        ),
                    ],
                )
            ]
        )
