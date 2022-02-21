from ..filtro import Filtro, Criterio


class FiltragemPorAssinatura(Filtro):
    def presidente_e_diretores_do_BC(self):
        yield from [
            Criterio(
                self.assinatura.contem(r"Roberto de Oliveira Campos Neto"),
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
                self.assinatura.contem(r"Bruno Serra Fernandes"),
                motivo="Assinatura de um diretor do BC",
            ),
            Criterio(
                self.assinatura.contem(r"Fernanda Magalhaes Rumenos Guardado"),
                motivo="Assinatura de um diretor do BC",
            ),
            Criterio(
                self.assinatura.contem(r"João Manoel Pinho de Mello"),
                motivo="Assinatura de um diretor do BC",
            ),
            Criterio(
                self.assinatura.contem(r"Otávio Ribeiro Damaso"),
                motivo="Assinatura de um diretor do BC",
            ),
            Criterio(
                self.assinatura.contem(r"Carolina de Assis Barros"),
                motivo="Assinatura de um diretor do BC",
            ),
        ]
