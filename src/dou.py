import pandas as pd
from .utils import DateRange, tirar_acentuacao
from .filtro.categorias.por_assinatura import FiltragemPorAssinatura
from .filtro.categorias.por_conteudo import FiltragemPorConteudo
from .filtro.categorias.por_ementa import FiltragemPorEmenta
from .filtro.categorias.por_escopo import FiltragemPorEscopo
from .filtro.categorias.por_titulo import FiltragemPorTitulo
from .infrastructure.repository import (
    pegar_urls_do_ingov,
    pegar_dou_remote_db,
)
from .models.publicacao import Publicacao


class DOU:
    def __init__(self, date_range: DateRange, is_from_remote_db=False, df=None):
        if df is not None:
            self.df = df[(date_range.inicio <= df.data) & (df.data <= date_range.fim)]
        elif is_from_remote_db:
            self.df = pegar_dou_remote_db(date_range)
        else:
            try:
                from .infrastructure.local_db import pegar_publicacoes_dou_db_local

                self.df = pegar_publicacoes_dou_db_local(date_range)
            except ModuleNotFoundError:
                pass

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

    def gerar_sumula(self, com_link_ingov=False, versao_oficial=False):
        resultado = pd.concat(
            [
                self.filtrar_por_titulo(),
                self.filtrar_por_escopo(),
                self.filtrar_por_ementa(),
                self.filtrar_por_conteudo(),
                self.filtrar_por_assinatura(),
            ]
        )

        # | Adiciona motivo se a publicação foi achada por mais de uma categoria de filtragem
        duplicados = resultado[resultado.duplicated("id", keep=False)]
        sumula = resultado.drop_duplicates(subset="id")

        for i in duplicados.groupby("id").groups.values():
            index = i[0]

            motivos = duplicados.loc[index].motivo.to_list()
            motivos = "\n".join(motivos)

            sumula.loc[index].motivo = motivos

        # | Adiciona o link para o in.gov
        if com_link_ingov:
            sumula["pdf"] = pegar_urls_do_ingov(ids=sumula.id_materia)

        if versao_oficial:
            # | Organiza as publicações de modo a se assemelhar à súmula oficial

            # Tira as publicações que não são extras da súmula passada
            unique_dates = sumula["data"].sort_values().unique()
            if len(unique_dates) == 2:
                is_from_last_edition = sumula.data == sumula.data.min()
                is_not_extra = sumula.secao.str.contains("DO[123]$")

                sumula = sumula[~(is_from_last_edition & is_not_extra)]

            # Divide as publicações por escopo (i.e. seções)
            secoes = dict()
            for pub in sumula.transpose().to_dict().values():
                pub = Publicacao(**pub).to_sumula()
                secoes.setdefault(pub["escopo"], []).append(pub)
                
            # Coloca as publicações de cada escopo em ordem alfabética
            for escopo, pubs in secoes.items():
                secoes[escopo] = sorted(pubs, key=lambda pub: pub["titulo"])

            # Retorna um dict[secao, list[publicações]]
            return secoes

        return sumula
