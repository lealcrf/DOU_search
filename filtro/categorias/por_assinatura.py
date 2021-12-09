from ..filtro import Filtro


class FiltragemPorAssinatura(Filtro):
    def resoluções_assinadas_pelo_presidente_do_COAF(self):
        return self.query(
            self.match(self._df.assinatura, "RICARDO LIÁO")
            & (self._df.tipo_normativo == "Portaria")  # A28
        ).assign(motivo="Portaria assinada pelo pelo presidente do COAF")

    def presidente_e_diretores_do_BC(self):
        return self.query(
            self.match(
                self._df.assinatura,
                [
                    "ROBERTO DE OLIVEIRA CAMPOS NETO",
                    "Maurício Costa de Moura",
                    "Paulo sérgio Neves Souza",
                    "Fabio Kanczuk",
                    "Bruno Serra Fernandes",
                    "Fernanda Guardado",
                    "João Manoel Pinho de Mello",
                    "Otávio Ribeiro Damaso",
                    "Carolina de Assis Barros",
                ],
            ),
            motivo="Assinatura do presidente ou dos diretores do Banco Central",
        )
