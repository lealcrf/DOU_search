from ..filtro import Filtro, Criterio


class FiltragemPorTitulo(Filtro):
    def filtrar_por_titulo(self):
        return self.query(
            self.contains(
                self.df.titulo,
                [
                    Criterio("Resolução Coremec"),  # A39
                    Criterio(
                        r"\sCMN\W",
                        "Resolução CMN no título",
                    ),  # A43
                ],
            )
        )

    def banco_central_na_ementa(self):
        self.query(
            self.contains(
                self.df.titulo,
                [
                    Criterio("SUSEP"),
                    Criterio("PREVIC"),
                    Criterio("COAF"),
                ],
            )
            & self.contains(self.df.ementa, "Banco Central"),  # R1
            motivo="Publicação da SUSEP, PREVIC OU COAF que menciona o Banco Central na emenda",
        )

    def banco_central_no_conteudo(self):
        return self.query(
            self.contains(self.df.titulo, "PORTARIA SETO")
            & self.contains(self.df.conteudo, "Banco Central"),
            motivo='Publicações que contenham "PORTARIA SETO" no título e mencionem o Banco Central no conteúdo',
            # Conversa com Carlos e Ligiane no dia 04/01/2022
        )
