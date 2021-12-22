from ..filtro import Filtro
from teste import Pattern


class FiltragemPorAssinatura(Filtro):
    def assinadas_pelo_presidente_do_COAF(self):
        return self.query(
            (self.contains(self._df.assinatura, "RICARDO LIÁO"))  # A28
            & (self._df.tipo_normativo == "Portaria")  # A28
            & (self.contains(self._df.secao, "DO1"))  # R2A1
        ).assign(motivo="Portaria assinada pelo pelo presidente do COAF")

    def presidente_e_diretores_do_BC(self):
        return self.query(
            self.contains(
                self._df.assinatura,
                [
                    Pattern(
                        "ROBERTO DE OLIVEIRA CAMPOS NETO",
                        'Assinatura do Presidente do BC - "Roberto De Oliveira Campos Neto"',
                    ),
                    Pattern(
                        "Maurício Costa de Moura",
                        'Assinatura de um diretor do BC - "Maurício Costa de Moura"',
                    ),
                    Pattern(
                        "Paulo sérgio Neves Souza",
                        'Assinatura de um diretor do BC - "Paulo sérgio Neves Souza"',
                    ),
                    Pattern(
                        "Fabio Kanczuk",
                        'Assinatura de um diretor do BC - "Fabio Kanczuk"',
                    ),
                    Pattern(
                        "Bruno Serra Fernandes",
                        'Assinatura de um diretor do BC - "Bruno Serra Fernandes"',
                    ),
                    Pattern(
                        "Fernanda Guardado",
                        'Assinatura de um diretor do BC - "Fernanda Guardado"',
                    ),
                    Pattern(
                        "João Manoel Pinho de Mello",
                        'Assinatura de um diretor do BC - "João Manoel Pinho de Mello"',
                    ),
                    Pattern(
                        "Otávio Ribeiro Damaso",
                        'Assinatura de um diretor do BC - "Otávio Ribeiro Damaso"',
                    ),
                    Pattern(
                        "Carolina de Assis Barros",
                        'Assinatura de um diretor do BC - "Carolina de Assis Barros"',
                    ),
                ],
            ),
        )
