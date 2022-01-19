from ..filtro import Filtro, Pattern


class FiltragemPorConteudo(Filtro):
    def frases_gerais(self):
        return self.query(
            self.contains(
                self.df.conteudo,
                [
                    Pattern("Comissão Técnica da Moeda e do Crédito"),  # A8
                    Pattern(
                        "Secretário-Executivo Adjunto da Secretaria-Executiva do Ministério do Trabalho e Previdência"
                    ),  # A23
                    Pattern(
                        "Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização",
                    ),  # A9
                    # ******************************** Nomeação/Exoneração ****************************************
                    Pattern(
                        "cargo de Presidente do Banco Central",
                        "Nomeação/Exoneração do Presidente do Banco Central",
                    ),  # A6
                    Pattern(
                        "cargo de (?:Diretor|Diretora) do Banco Central",
                        "Nomeação/Exoneração do Diretor(a) do Banco Central",
                    ),  # A7
                    Pattern(
                        "cargo de Ministro de Estado da Economia",
                        "Nomeação/Exoneração do Ministro de Estado da Economia",
                    ),  # A10
                    Pattern(
                        "cargo de Ministro de Estado do Trabalho e Previdência",
                        "Nomeação/Exoneração do Ministro de Estado do Trabalho e Previdência",
                    ),
                    Pattern(
                        "cargo de Secretário Especial de Fazenda do Ministério da Economia",
                        "Nomeação/Exoneração do Secretário Especial de Fazenda do Ministério da Economia",
                    ),  # A11
                    Pattern(
                        "cargo de Secretário-Executivo do Ministério da Economia",
                        "Nomeação/Exoneração do Secretário-Executivo do Ministério da Economia",
                    ),  # A12
                    Pattern(
                        "cargo de Secretário de Política Econômica",
                        "Nomeação/Exoneração do Secretário de Política Econômica",
                    ),  # A13
                    Pattern(
                        "cargo de Secretário do Tesouro Nacional",
                        "Nomeação/Exoneração do Secretário do Tesouro Nacional",
                    ),  # A14
                    Pattern(
                        "cargo de Presidente da Casa da Moeda do Brasil",
                        "Nomeação/Exoneração do Presidente da Casa da Moeda do Brasil",
                    ),  # A15
                    Pattern(
                        "cargo de Diretor da Comissão de Valores Mobiliários",
                        "Nomeação/Exoneração do Diretor da Comissão de Valores Mobiliários",
                    ),  # A16
                    Pattern(
                        "cargo de Superintendente da Superintendência de Seguros Privados",
                        "Nomeação/Exoneração do Superintendente da Superintendência de Seguros Privados",
                    ),  # A17
                    Pattern(
                        "cargo de Diretor da Superintendência de Seguros Privados",
                        "Nomeação/Exoneração do Diretor da Superintendência de Seguros Privados",
                    ),  # A18
                    Pattern(
                        "cargo de Diretor-Superintendente da Superintendência Nacional de Previdência Complementar",
                        "Nomeação/Exoneração do Diretor-Superintendente da Superintendência Nacional de Previdência Complementar",
                    ),  # A19
                    Pattern(
                        "cargo de Diretor de Licenciamento da Superintendência Nacional de Previdência Complementar",
                        "Nomeação/Exoneração do Diretor de Licenciamento da Superintendência Nacional de Previdência Complementar",
                    ),  # A20
                    Pattern(
                        "cargo de Secretário Especial Adjunto da Secretaria Especial de Previdência e Trabalho do Ministério da Economia",
                        "Nomeação/Exoneração do Secretário Especial Adjunto da Secretaria Especial de Previdência e Trabalho do Ministério da Economia",
                    ),  # A21
                    Pattern(
                        "cargo de Secretário-Executivo do Ministério do Trabalho e Previdência",
                        "Nomeação/Exoneração do Secretário-Executivo do Ministério do Trabalho e Previdência",
                    ),  # A22
                    Pattern(
                        "cargo de Secretário Especial do Tesouro e Orçamento do Ministério da Economia",
                        "Nomeação/Exoneração do Secretário Especial do Tesouro e Orçamento do Ministério da Economia",
                    ),  # R2-A3
                    Pattern(
                        "cargo de Procurador-Geral Federal da Advocacia-Geral da União",
                        "Nomeação/Exoneração do Procurador-Geral Federal da Advocacia-Geral da União",
                    ),  # R2-A9
                    # ******************************** Afastamentos ****************************************
                    Pattern(
                        "(?:Exposição|Exposições) de Motivos.{0,200}(?:afastamento|férias).{0,50} Presidente do Banco Central do Brasil",
                        "Afastamento do Presidente do BC",
                    ),  # A29",
                    Pattern(
                        "(?:Exposição|Exposições) de Motivos.{0,200}(?:afastamento|férias).{0,50} Ministro de Estado da Economia",
                        "Afastamento do Ministro de Estado da Economia",
                    ),  # A30",
                    Pattern(
                        "(?:A DIRETORA|O DIRETOR) DE ADMINISTRAÇÃO DO BANCO CENTRAL DO BRASIL",
                        "Despacho do Diretor de Administração",
                    ),  # A31",
                    Pattern(
                        "^.{0,100}PORTARIA.+O MINISTRO DE ESTADO DA ECONOMIA.+afastamento.+Banco Central",
                        # Já que o conteudo vem com o titulo junto, eu precisei dizer que o título (primeiros 100 caracteres) deve conter PORTARIA
                        "Portaria do Ministro da Economia afastando alguém do Banco Central",
                    ),  # A32",
                    Pattern(
                        "Despacho do Presidente do Banco Central do Brasil.+Presidente do COAF",
                        "Afastamento do presidente do COAF",
                    ),  # Sempre que o presidente do COAF se ausenta, o Presidente do Banco Central do Brasil precisa fazer um despacho",
                    Pattern(
                        "Ministros? de Estado.*Decreto nº 71.733|Decreto nº 71.733.*Ministros? de Estado",
                        '"Ministro de Estado" e "Decreto 71.733" concomitantemente na ementa ou no texto',
                    ),#T2022-1-19
                ],
            )
        )

    def da_subchefia_para_assuntos_juridicos(self):
        return self.query(
            self.contains(
                self.df.conteudo,
                "temas jurídicos relevantes para a administração pública",
            )
            & self.contains(self.df.escopo, "Subchefia para Assuntos Jurídicos"),
            motivo='• Publicação da Subchefia para Assuntos Jurídicos que contém "temas jurídicos relevantes para a administração pública" no conteúdo',
        )
