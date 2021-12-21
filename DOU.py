from datetime import date
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from filtro.categorias.por_assinatura import FiltragemPorAssinatura
from filtro.categorias.por_conteudo import FiltragemPorConteudo

from filtro.categorias.por_ementa import FiltragemPorEmenta
from filtro.categorias.por_escopo import FiltragemPorEscopo
from filtro.categorias.por_motivo_geral import FiltragemPorMotivoGeral
from filtro.categorias.por_titulo import FiltragemPorTitulo
from repository import get_link_da_publicacao_ingov


class DOU:
    def __init__(self, df: DataFrame, dia: date = None):
        self.df = df[df.data == dia] if dia else df
        # self.df = df[df.data >= dia] if dia else df

    @property
    def filtrar_por_assinatura(self):
        return FiltragemPorAssinatura(self)

    @property
    def filtrar_por_conteudo(self):
        return FiltragemPorConteudo(self)

    @property
    def filtrar_por_ementa(self):
        return FiltragemPorEmenta(self)

    @property
    def filtrar_por_escopo(self):
        return FiltragemPorEscopo(self)

    @property
    def filtrar_por_motivo_geral(self):
        return FiltragemPorMotivoGeral(self)

    @property
    def filtrar_por_titulo(self):
        return FiltragemPorTitulo(self)
    
    # def query(self, filtro: Series, motivo=None) -> pd.DataFrame:
    #     if motivo:
    #         return self.df[filtro].assign(motivo=motivo)

    #     return self.df[filtro]

    def gerar_sumula(self, com_link_ingov = False) -> pd.DataFrame:
        sumula = pd.concat(
            [
                self.filtrar_por_motivo_geral(),
                self.filtrar_por_titulo(),
                self.filtrar_por_escopo(),
                self.filtrar_por_ementa(),
                self.filtrar_por_conteudo(),
                self.filtrar_por_assinatura(),
            ]
        ).drop_duplicates(subset="id")
        
        
        sumula.pdf = sumula.apply(lambda x: get_link_da_publicacao_ingov(x.pdf) )
        
        # if com_link_ingov:
            # for pub in sumula.iloc:
                # pub.pdf =  get_link_da_publicacao_ingov(pub.id_materia)
                
        return sumula
