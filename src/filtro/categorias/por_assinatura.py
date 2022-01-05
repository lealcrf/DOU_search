from ..filtro import Filtro, Pattern
# from teste import Pattern


class FiltragemPorAssinatura(Filtro):
    def assinadas_pelo_presidente_do_COAF(self):
        return self.query(
            (self.contains(self.df.assinatura, "RICARDO LIÁO"))  # A28
            & (self.df.tipo_normativo == "Portaria")  # A28
            # & (self.contains(self._df.secao, "DO1"))  # R2A1
        ).assign(motivo="Portaria assinada pelo pelo presidente do COAF")

    def presidente_e_diretores_do_BC(self):
        return self.query(
            self.contains(
                self.df.assinatura,
                [
                    Pattern(
                        "ROBERTO DE OLIVEIRA CAMPOS NETO",
                        "Assinatura do Presidente do BC",
                    ),
                    Pattern(
                        "Maurício Costa de Moura",
                        "Assinatura de um diretor do BC",
                    ),
                    Pattern(
                        "Paulo sérgio Neves de Souza",
                        "Assinatura de um diretor do BC",
                    ),
                    Pattern(
                        "Fabio Kanczuk",
                        "Assinatura de um diretor do BC",
                    ),
                    Pattern(
                        "Bruno Serra Fernandes",
                        "Assinatura de um diretor do BC",
                    ),
                    Pattern(
                        "Fernanda Magalhaes Rumenos Guardado",
                        "Assinatura de um diretor do BC",
                    ),
                    Pattern(
                        "João Manoel Pinho de Mello",
                        "Assinatura de um diretor do BC",
                    ),
                    Pattern(
                        "Otávio Ribeiro Damaso",
                        "Assinatura de um diretor do BC",
                    ),
                    Pattern(
                        "Carolina de Assis Barros",
                        "Assinatura de um diretor do BC",
                    ),
                ],
            ),
        )
