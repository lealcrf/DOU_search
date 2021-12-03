from utils import ColumnSearch, FiltrarPorCategoria
from termos import ASSINATURAS_DIRETORES_E_PRESIDENTE_DO_BC

class FiltragemPorAssinatura(FiltrarPorCategoria):
        
    def resoluções_assinadas_pelo_presidente_do_COAF(self):
        return self._filtro.keyword_search(
            searches=[ColumnSearch([self._filtro.df.assinatura], keywords=["RICARDO LIÁO"])],
            where=self._filtro.df.tipo_normativo == "Portaria",
        ).assign(motivo="Portaria assinada pelo pelo presidente do COAF")

        
    def assinaturas_dos_diretores_e_presidente_do_BC(self):
        """Qualquer coisa assinada por um diretor/presidente do BC entra na súmula

        Ao comparar as assinaturas, ele vai remover as acentuações, uma vez que o uso de acentuação é bem inconsistente
        """
        return self._filtro.keyword_search(
            searches=[
                ColumnSearch(
                    columns=[self._filtro.df.assinatura],
                    keywords=ASSINATURAS_DIRETORES_E_PRESIDENTE_DO_BC,
                )
            ]
        ).assign(motivo="Assinatura de um diretor ou pelo presidente do BC")
        
        


        