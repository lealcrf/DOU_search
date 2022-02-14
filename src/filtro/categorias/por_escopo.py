from ..filtro import Filtro, Criterio


class FiltragemPorEscopo(Filtro):
    def menciona_o_banco_central(self):
        yield from [
            Criterio(
                self.escopo.contem(r"Gabinete de Segurança Institucional")
                & self.conteudo.contem(r"Banco Central"),
                motivo="Gabinete de Segurança Institucional no escopo e menciona Banco Central no conteúdo",
            ),
            Criterio( #R2A2
                self.escopo.contem(r"Secretaria Especial do Tesouro e Orçamento")
                & self.conteudo.contem(r"Banco Central")  # T2022-2-13-Carlos
                & self.titulo.notna(),
                motivo="'Secretaria Especial do Tesouro e Orçamento' no escopo e menciona o Banco Central no conteúdo",
            ),
        ]
