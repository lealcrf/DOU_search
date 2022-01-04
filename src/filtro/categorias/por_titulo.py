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
                    Pattern("CONAF"),
                ],
            )
            & self.contains(self._df.ementa, "Banco Central"),  # R1
            motivo="Publicação da SUSEP, PREVIC OU CONAF que menciona o Banco Central na emenda",
        )