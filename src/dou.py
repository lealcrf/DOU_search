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
from datetime import date
import os


# Isso tira problemas de importação que surgem quando o script é rodado na Cloud
load_dotenv()
is_running_locally = os.getenv("IS_RUNNING_LOCALLY")
if is_running_locally:
    import src.infrastructure.local_repository as local_repo


class DOU:
    def __init__(
        self,
        date_range: DateRange = DateRange.same_day(),
        get_from_remote_db=False,
        df=None,  # Usado para desbugar
    ):
        if df is not None:
            self.df = df[(date_range.inicio <= df.data) & (df.data <= date_range.fim)]
        elif get_from_remote_db or (not is_running_locally):
            self.df = repo.pegar_dou_remote_db(date_range)
        else:
            self.df = local_repo.pegar_publicacoes_dou_db_local(date_range)

        if not self.df.empty:
            self.df.assinatura = self.df.assinatura.apply(tirar_acentuacao)

    # Acessar cada categoria de filtragem individualmente
    # TODO Tirar @property's. Usei property para facilitar na hora de desbugar, mas não é mais necessário
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
        """Mostra as publicações que se enquadram as condições inseridas

        É para ser usado mais como uma ferramenta para rápidamente testar a eficacia de uma condição
        """
        return self.df[condicoes].sort_values("data", ascending=False)

    def gerar_sumula(self, ingov_urls=False, oficial=False):
        # | Junta todos as funções de todas as categorias em apenas uma lista gigante de critérios
        ## estou usando generators para melhorar a performance
        criterios = chain(
            self.filtrar_por_assinatura.pegar_criterios(),
            self.filtrar_por_titulo.pegar_criterios(),
            self.filtrar_por_escopo.pegar_criterios(),
            self.filtrar_por_ementa.pegar_criterios(),
            self.filtrar_por_conteudo.pegar_criterios(),
        )

        # | Aplica todas as condições de cada critério e insere os motivos no dataframe principal

        # Lista final que contém os matches de cada condição
        ## Quando são encontradas publicações se enquadram em um critério, é gerado um BooleanArray indicando a localização dessas publicações. Um booleanarray é um array que marca 0 se a publicação não entrou e 1 se entrou
        all_conditions: list[BooleanArray] = []

        for criterio in criterios:
            criterio.aplicar_motivo(self.df)

            all_conditions.append(criterio.condicao)

        # Pega todos as publicações que correspondem aos critérios
        pubs_para_sumula: BooleanArray = functools.reduce(ior, all_conditions)

        sumula = self.df[pubs_para_sumula]

        # TODO  Passa o filtro de exclusao
        # sumula = FiltragemPorExclusao(sumula).excluir_instrucoes_normativas_do_banco_central()

        # | Se estiver rodando localmente, coloca os URLs do ingov
        ## As urls que recebemos do inlabs são para uma versão em pdf horrível do DOU. É necessário pegar o link do ingov, já que ele é bem formatado e é o atualmente usado pela SUCON
        if ingov_urls and is_running_locally:
            sumula["pdf"] = local_repo.pegar_urls_do_ingov(sumula.id_materia)

        # | Prepara a súmula para versão oficial
        if oficial:
            # Tira as publicações que não são extra da edição anterior
            if sumula.data.min() != date.today():
                is_from_last_edition = sumula.data == sumula.data.min()
                is_not_extra = sumula.secao.str.contains("DO[123]$")

                sumula = sumula[~(is_from_last_edition & is_not_extra)]

            # Divide as publicações por escopo (i.e. seções)
            sumula_seccionada = dict()
            for pub in sumula.transpose().to_dict().values():
                pub = Publicacao(**pub).to_sumula()
                sumula_seccionada.setdefault(pub["escopo"], []).append(pub)

            # Coloca as publicações de cada escopo em ordem alfabética
            for escopo, pubs in sumula_seccionada.items():
                sumula_seccionada[escopo] = sorted(pubs, key=lambda pub: pub["titulo"])

            return sumula_seccionada

        return sumula
