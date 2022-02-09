import functools
from itertools import chain
from operator import ior
from pandas.core.arrays.boolean import BooleanArray

import src.infrastructure.repository as repo
from .utils import DateRange, tirar_acentuacao
from .filtro.categorias.por_assinatura import FiltragemPorAssinatura
from .filtro.categorias.por_conteudo import FiltragemPorConteudo
from .filtro.categorias.por_ementa import FiltragemPorEmenta
from .filtro.categorias.por_escopo import FiltragemPorEscopo
from .filtro.categorias.por_titulo import FiltragemPorTitulo
from .filtro.categorias.por_exclusao import FiltragemPorExclusao
from .models.publicacao import Publicacao
from dotenv import load_dotenv
import os

load_dotenv()

is_running_locally = os.getenv("IS_RUNNING_LOCALLY")
if is_running_locally:
    import src.infrastructure.local_repository as local_repo


class DOU:
    def __init__(
        self,
        date_range: DateRange = DateRange.same_day(),
        get_from_remote_db=False,
        df=None,
    ):
        if df is not None:
            self.df = df[(date_range.inicio <= df.data) & (df.data <= date_range.fim)]
        elif get_from_remote_db or (not is_running_locally):
            self.df = repo.pegar_dou_remote_db(date_range)
        else:
            self.df = local_repo.pegar_publicacoes_dou_db_local(date_range)

        if not self.df.empty:
            self.df.assinatura = self.df.assinatura.apply(tirar_acentuacao)

    @property
    def filtrar_por_assinatura(self):
        return FiltragemPorAssinatura(self.df)

    @property
    def filtrar_por_conteudo(self):
        return FiltragemPorConteudo(self.df)

    @property
    def filtrar_por_ementa(self):
        return FiltragemPorEmenta(self.df)

    @property
    def filtrar_por_escopo(self):
        return FiltragemPorEscopo(self.df)

    @property
    def filtrar_por_titulo(self):
        return FiltragemPorTitulo(self.df)
    
    def filtrar(self, condicoes):
        return self.df[condicoes].sort_values("data", ascending=False)

    def gerar_sumula(self, ingov_urls=False):

        criterios = chain(
            self.filtrar_por_assinatura.pegar_criterios(),
            self.filtrar_por_titulo.pegar_criterios(),
            self.filtrar_por_escopo.pegar_criterios(),
            self.filtrar_por_ementa.pegar_criterios(),
            self.filtrar_por_conteudo.pegar_criterios(),
            # FiltragemPorExclusao(self.df).teste()
        )

        all_conditions: list[BooleanArray] = []

        for criterio in criterios:
            criterio.aplicar_motivo(self.df)

            all_conditions.append(criterio.condicao)

        pubs_para_sumula: BooleanArray = functools.reduce(ior, all_conditions)     
   
        sumula = self.df[pubs_para_sumula]

        # # | #TODO  Passa o filtro de exclusao 
        # sumula = FiltragemPorExclusao(sumula).excluir_instrucoes_normativas_do_banco_central()

        # | Coloca os URLs do ingov
        if ingov_urls and is_running_locally:
            sumula["pdf"] = local_repo.pegar_urls_do_ingov(sumula.id_materia)

        return sumula
