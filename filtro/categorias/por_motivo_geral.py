from ..filtro import Filtro


class FiltragemPorMotivoGeral(Filtro):
    def publicacoes_BC_DO1_nao_IN(self):
        return self.query(
            self.match(self._df.escopo, "Banco Central")
            & self.match(self._df.secao, "DO1")
            & (self._df.tipo_normativo != "Instrução Normativa"),
            motivo="Publicação do Banco Central no DO1 que não é instrução normativa",
        )
