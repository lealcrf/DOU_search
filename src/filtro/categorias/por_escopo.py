from ..filtro import Filtro, Criterio


class FiltragemPorEscopo(Filtro):
    def especificos(self):
        yield from [
            Criterio(  # M1
                self.tipo_normativo.igual("Portaria") & self.secao.contem("DO1"),
                motivo="Portaria do COAF na seção 1",
            )
        ]

    def menciona_o_banco_central(self):
        yield from [
            Criterio(
                self.escopo.contem(r"Gabinete de Segurança Institucional")
                & self.conteudo.contem(r"Banco Central"),
                motivo="Gabinete de Segurança Institucional no escopo e menciona Banco Central no conteúdo",
            ),
            Criterio(  # R2A2
                self.escopo.contem(r"Secretaria Especial do Tesouro e Orçamento")
                & self.conteudo.contem(r"Banco Central")  # T2022-2-13-Carlos
                & self.titulo.notna(),
                motivo="'Secretaria Especial do Tesouro e Orçamento' no escopo e menciona o Banco Central no conteúdo",
            ),
            Criterio(  # R1
                self.titulo.contem(r"Superintendência de Seguros Privados")
                & self.ementa.contem("Banco Central"),
                motivo="Publicação da SUSEP que menciona o Banco Central na Ementa",
            ),
            Criterio(  # R1
                self.titulo.contem(
                    r"Superintendência Nacional de Previdência Complementar"
                )
                & self.ementa.contem("Banco Central"),
                motivo="Publicação da PREVIC que menciona o Banco Central na Ementa",
            ),
            Criterio(  # R1
                self.titulo.contem(r"COAF") & self.ementa.contem("Banco Central"),
                motivo="Publicação do COAF que menciona o Banco Central na Ementa",
            ),
        ]
