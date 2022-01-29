from ..filtro import Filtro, Criterio


class FiltragemPorConteudo(Filtro):
    def frases_gerais(self):
        return self.query(
            self.contains(
                self.df.conteudo,
                [
                    Criterio("Comissão Técnica da Moeda e do Crédito"),  # A8
                    Criterio(
                        "Secretário-Executivo Adjunto da Secretaria-Executiva do Ministério do Trabalho e Previdência"
                    ),  # A23
                    Criterio(
                        "Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização",
                    ),  # A9
                    # ******************************** Nomeação/Exoneração ****************************************
                    Criterio(
                        "cargo de Presidente do Banco Central",
                        "Nomeação/Exoneração do Presidente do Banco Central",
                    ),  # A6
                    Criterio(
                        "cargo de (?:Diretor|Diretora) do Banco Central",
                        "Nomeação/Exoneração do Diretor(a) do Banco Central",
                    ),  # A7
                    Criterio(
                        "cargo de Ministro de Estado da Economia",
                        "Nomeação/Exoneração do Ministro de Estado da Economia",
                    ),  # A10
                    Criterio(
                        "cargo de Ministro de Estado do Trabalho e Previdência",
                        "Nomeação/Exoneração do Ministro de Estado do Trabalho e Previdência",
                    ),
                    Criterio(
                        "cargo de Secretário Especial de Fazenda do Ministério da Economia",
                        "Nomeação/Exoneração do Secretário Especial de Fazenda do Ministério da Economia",
                    ),  # A11
                    Criterio(
                        "cargo de Secretário-Executivo do Ministério da Economia",
                        "Nomeação/Exoneração do Secretário-Executivo do Ministério da Economia",
                    ),  # A12
                    Criterio(
                        "cargo de Secretário de Política Econômica",
                        "Nomeação/Exoneração do Secretário de Política Econômica",
                    ),  # A13
                    Criterio(
                        "cargo de Secretário do Tesouro Nacional",
                        "Nomeação/Exoneração do Secretário do Tesouro Nacional",
                    ),  # A14
                    Criterio(
                        "cargo de Presidente da Casa da Moeda do Brasil",
                        "Nomeação/Exoneração do Presidente da Casa da Moeda do Brasil",
                    ),  # A15
                    Criterio(
                        "cargo de Diretor da Comissão de Valores Mobiliários",
                        "Nomeação/Exoneração do Diretor da Comissão de Valores Mobiliários",
                    ),  # A16
                    Criterio(
                        "cargo de Superintendente da Superintendência de Seguros Privados",
                        "Nomeação/Exoneração do Superintendente da Superintendência de Seguros Privados",
                    ),  # A17
                    Criterio(
                        "cargo de Diretor da Superintendência de Seguros Privados",
                        "Nomeação/Exoneração do Diretor da Superintendência de Seguros Privados",
                    ),  # A18
                    Criterio(
                        "cargo de Diretor-Superintendente da Superintendência Nacional de Previdência Complementar",
                        "Nomeação/Exoneração do Diretor-Superintendente da Superintendência Nacional de Previdência Complementar",
                    ),  # A19
                    Criterio(
                        "cargo de Diretor de Licenciamento da Superintendência Nacional de Previdência Complementar",
                        "Nomeação/Exoneração do Diretor de Licenciamento da Superintendência Nacional de Previdência Complementar",
                    ),  # A20
                    Criterio(
                        "cargo de Secretário Especial Adjunto da Secretaria Especial de Previdência e Trabalho do Ministério da Economia",
                        "Nomeação/Exoneração do Secretário Especial Adjunto da Secretaria Especial de Previdência e Trabalho do Ministério da Economia",
                    ),  # A21
                    Criterio(
                        "cargo de Secretário-Executivo do Ministério do Trabalho e Previdência",
                        "Nomeação/Exoneração do Secretário-Executivo do Ministério do Trabalho e Previdência",
                    ),  # A22
                    Criterio(
                        "cargo de Secretário Especial do Tesouro e Orçamento do Ministério da Economia",
                        "Nomeação/Exoneração do Secretário Especial do Tesouro e Orçamento do Ministério da Economia",
                    ),  # R2-A3
                    Criterio(
                        "cargo de Procurador-Geral Federal da Advocacia-Geral da União",
                        "Nomeação/Exoneração do Procurador-Geral Federal da Advocacia-Geral da União",
                    ),  # R2-A9
                    # ******************************** Afastamentos ****************************************
                    Criterio(
                        "(?:Exposição|Exposições) de Motivos.{0,200}(?:afastamento|férias).{0,50} Presidente do Banco Central do Brasil",
                        "Afastamento do Presidente do BC",
                    ),  # A29",
                    Criterio(
                        "(?:Exposição|Exposições) de Motivos.{0,200}(?:afastamento|férias).{0,50} Ministro de Estado da Economia",
                        "Afastamento do Ministro de Estado da Economia",
                    ),  # A30",
                    Criterio(
                        "(?:A DIRETORA|O DIRETOR) DE ADMINISTRAÇÃO DO BANCO CENTRAL DO BRASIL",
                        "Despacho do Diretor de Administração",
                    ),  # A31",
                    Criterio(
                        "^.{0,100}PORTARIA.+O MINISTRO DE ESTADO DA ECONOMIA.+afastamento.+Banco Central",
                        # Já que o conteudo vem com o titulo junto, eu precisei dizer que o título (primeiros 100 caracteres) deve conter PORTARIA
                        "Portaria do Ministro da Economia afastando alguém do Banco Central",
                    ),  # A32",
                    Criterio(
                        "Despacho do Presidente do Banco Central do Brasil.+Presidente do COAF",
                        "Afastamento do presidente do COAF",
                    ),  # Sempre que o presidente do COAF se ausenta, o Presidente do Banco Central do Brasil precisa fazer um despacho",
                    Criterio(
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
