from ..filtro import Filtro


class FiltragemPorExclusao(Filtro):
    def excluir_instrucoes_normativas_do_banco_central(self):
        return self.query(
            ~(
                (self.df.tipo_normativo == "Instrução Normativa")
                & self.contains(self.df.escopo, "Banco Central")
            )
        )
