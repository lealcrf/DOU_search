from ..filtro import Criterio, Filtro


class FiltragemPorExclusao(Filtro):
    pass
    # def geral(self):
    #     return self.query(
    #         ~(
    #             (self.df.tipo_normativo == "Instrução Normativa")
    #             & self.contains(self.df.escopo, "Banco Central")
    #         )
    #     )
