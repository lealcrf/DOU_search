from ..filtro import Filtro, Criterio


class FiltragemPorAssinatura(Filtro):
    def especificos(self):
        yield from [
            Criterio(  # A28
                self.assinatura.contem("RICARDO LIÁO")
                & (self.tipo_normativo == "Portaria"),
                # & self.secao.contem("DO1"),  # R2A1
                motivo="Portaria assinada pelo pelo presidente do COAF",
            )
        ]

    def presidente_e_diretores_do_BC(self):
        yield from [
            Criterio(
                self.assinatura.contem(r"ROBERTO DE OLIVEIRA CAMPOS NETO"),
                motivo="Assinatura do Presidente do BC",
            ),
            Criterio(
                self.assinatura.contem(r"Maurício Costa de Moura"),
                motivo="Assinatura de um diretor do BC",
            ),
            Criterio(
                self.assinatura.contem(r"Paulo sérgio Neves de Souza"),
                motivo="Assinatura de um diretor do BC",
            ),
            Criterio(
                self.assinatura.contem(r"Fabio Kanczuk"),
                motivo="Assinatura de um diretor do BC",
            ),
            Criterio(
                self.assinatura.contem("Bruno Serra Fernandes"),
                motivo="Assinatura de um diretor do BC",
            ),
            Criterio(
                self.assinatura.contem("Fernanda Magalhaes Rumenos Guardado"),
                motivo="Assinatura de um diretor do BC",
            ),
            Criterio(
                self.assinatura.contem("João Manoel Pinho de Mello"),
                motivo="Assinatura de um diretor do BC",
            ),
            Criterio(
                self.assinatura.contem("Otávio Ribeiro Damaso"),
                motivo="Assinatura de um diretor do BC",
            ),
            Criterio(
                self.assinatura.contem("Carolina de Assis Barros"),
                motivo="Assinatura de um diretor do BC",
            ),
        ]
