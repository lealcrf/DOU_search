from ..filtro import Filtro


class FiltragemPorEscopo(Filtro):
    def banco_central_no_conteudo(self):
        return self.query(
            self.contains(self._df.escopo, "Gabinete de Segurança Institucional")
            & self.contains(self._df.conteudo, "Banco Central"),  # R2A10
            motivo="Gabinete de Segurança Institucional no escopo e menciona Banco Central no conteúdo",
        )

    def banco_central_na_ementa(self):
        return self.query(
            self.contains(self._df.escopo, "Secretaria Especial do Tesouro e Orçamento")
            & self.contains(self._df.ementa, "Banco Central"),
            motivo="'Secretaria Especial do Tesouro e Orçamento' no escopo e menciona o Banco Central no conteúdo",
        )
