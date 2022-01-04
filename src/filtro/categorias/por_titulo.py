from ..filtro import Filtro, Pattern


class FiltragemPorTitulo(Filtro):
    def filtrar_por_titulo(self):
        return self.query(
            self.contains(
                self._df.titulo,
                [
                    Pattern("Resolução Coremec"),  # A39
                    Pattern(
                        r"\sCMN\W",
                        "Resolução CMN no título",
                    ),  # A43
                ],
            )
        )

    def banco_central_na_ementa(self):
        self.query(
            self.contains(
                self._df.titulo,
                [
                    Pattern("SUSEP"),
                    Pattern("PREVIC"),
                    Pattern("COAF"),
                ],
            )
            & self.contains(self._df.ementa, "Banco Central"),  # R1
            motivo="Publicação da SUSEP, PREVIC OU COAF que menciona o Banco Central na emenda",
        )

    def banco_central_no_conteudo(self):
        return self.query(
            self.contains(self._df.titulo, "PORTARIA SETO")
            & self.contains(self._df.conteudo, "Banco Central"),
            motivo='Publicações que contenham "PORTARIA SETO" no título e mencionem o Banco Central no conteúdo',
            # Conversa com Carlos e Ligiane no dia 04/01/2022
        )
