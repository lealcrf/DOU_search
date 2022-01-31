from ..filtro import Filtro, Criterio


class FiltragemPorTitulo(Filtro):
    def geral(self):
        yield from [
            Criterio(  # A39
                self.titulo.contem(r"Resolução Coremec"),
                motivo="Resolução Coremec no título",
            ),
            Criterio(  # A43
                self.titulo.contem(r"\sCMN\W"),
                motivo="Resolução CMN no título",
            ),
        ]

    def menciona_o_banco_central(self):
        yield from [
            Criterio(  # R1
                self.titulo.contem(r"SUSEP") & self.ementa.contem("Banco Central"),
                motivo="Publicação da SUSEP que menciona o Banco Central na Ementa",
            ),
            Criterio(  # R1
                self.titulo.contem(r"PREVIC") & self.ementa.contem("Banco Central"),
                motivo="Publicação da PREVIC que menciona o Banco Central na Ementa",
            ),
            Criterio(  # R1
                self.titulo.contem(r"COAF") & self.ementa.contem("Banco Central"),
                motivo="Publicação do COAF que menciona o Banco Central na Ementa",
            ),
            Criterio(  # Conversa com Carlos e Ligiane no dia 04/01/2022
                self.titulo.contem(r"PORTARIA SETO")
                & self.conteudo.contem("Banco Central"),
                motivo="Portaria SETO que menciona o Banco Central no Conteúdo",
            ),
        ]
