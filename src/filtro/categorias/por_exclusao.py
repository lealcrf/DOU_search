from ..filtro import Criterio, Filtro


class FiltragemPorExclusao(Filtro):
    def geral(self):
        return self.query(
            ~(
                (self.df.tipo_normativo == "Instrução Normativa")
                & self.contains(self.df.escopo, "Banco Central")
            )
        )

    # def teste(self):
    #     yield from [
    #         Criterio(  # R2A8
    #             self.ementa.contem(
    #                 r"(?:Sistema de Pessoal Civil da Administração (?:Pública)? Federal|SIPEC)"
    #             ),
    #             motivo="Publicação da SIPEC #TODO Terminar de fazer as restrições do R2A8",
    #         ),
    #     ]
