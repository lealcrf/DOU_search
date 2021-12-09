from ..filtro import Filtro


class FiltragemPorTitulo(Filtro):
    def filtrar_por_titulo(self):
        return self.query(
            self.match(
                self._df.titulo,
                [
                    "Resolução Coremec",  # A39
                    r"\sCMN\W",  # A43
                ],
            )
        )

    def banco_central_na_ementa(self):
        self.query(
            self.match(self._df.titulo, ["SUSEP", "PREVIC", "CONAF"])
            & self.match(self._df.ementa, "Banco Central"),  # R1
            motivo="Publicação da SUSEP, PREVIC OU CONAF que menciona o Banco Central na emenda",
        )
