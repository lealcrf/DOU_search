from ..filtro import Filtro
from teste import Pattern


class FiltragemPorMotivoGeral(Filtro):
    def publicacoes_BC_DO1_nao_IN(self):
        return self.query(
            (self.contains(self._df.escopo, "Banco Central"))
            & (self.contains(self._df.secao, "DO1"))
            & (self._df.tipo_normativo != "Instrução Normativa")
            & (self._df.tipo_normativo != "Retificação"),
            motivo="Publicação do Banco Central no DO1 que não é instrução normativa",
        )

    # def publicacoes_BC_DO1_nao_IN(self):
    #     return self.query(
    #         self.contains(self._df.escopo, "Banco Central")
    #         & self.contains(self._df.secao, "DO1")
    #         & (self._df.tipo_normativo != "Instrução Normativa"),
    #         motivo="Publicação do Banco Central no DO1 que não é instrução normativa",
    #     )
