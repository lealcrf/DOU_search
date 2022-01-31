from ..filtro import Criterio, Filtro


class FiltragemPorExclusao(Filtro):
    def geral(self):
        return self.query(
            ~(
                (self.df.tipo_normativo == "Instrução Normativa")
                & self.contains(self.df.escopo, "Banco Central")
            )
        )
