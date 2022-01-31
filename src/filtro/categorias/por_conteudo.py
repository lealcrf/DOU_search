from ..filtro import Filtro, Criterio


class FiltragemPorConteudo(Filtro):
    def gerais(self):
        yield from [
            Criterio(  # A8
                self.conteudo.contem(r"Comissão Técnica da Moeda e do Crédito"),
                motivo='"Comissão Técnica da Moeda e do Crédito" no conteúdo',
            ),
            Criterio(  # A23
                self.conteudo.contem(
                    r"Secretário-Executivo Adjunto da Secretaria-Executiva do Ministério do Trabalho e Previdência"
                ),
                motivo='"Secretário-Executivo Adjunto da Secretaria-Executiva do Ministério do Trabalho e Previdência" no conteúdoo',
            ),
            Criterio(  # A9
                self.conteudo.contem(
                    r"Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização",
                ),
                motivo='"Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização" no conteúdo',
            ),
        ]

    def nomeacoes_e_exoneracoes(self):
        yield from [
            Criterio(  # A6
                self.conteudo.contem(r"cargo de Presidente do Banco Central"),
                motivo="Nomeação/Exoneração do Presidente do Banco Central",
            ),
            Criterio(  # A7
                self.conteudo.contem(r"cargo de (?:Diretor|Diretora) do Banco Central"),
                motivo="Nomeação/Exoneração do Diretor(a) do Banco Central",
            ),
            Criterio(  # A10
                self.conteudo.contem(r"cargo de Ministro de Estado da Economia"),
                motivo="Nomeação/Exoneração do Ministro de Estado da Economia",
            ),
            Criterio(
                self.conteudo.contem(
                    r"cargo de Ministro de Estado do Trabalho e Previdência"
                ),
                motivo="Nomeação/Exoneração do Ministro de Estado do Trabalho e Previdência",
            ),
            Criterio(  # A11
                self.conteudo.contem(
                    r"cargo de Secretário Especial de Fazenda do Ministério da Economia"
                ),
                motivo="Nomeação/Exoneração do Secretário Especial de Fazenda do Ministério da Economia",
            ),
            Criterio(  # A12
                self.conteudo.contem(
                    r"cargo de Secretário-Executivo do Ministério da Economia"
                ),
                motivo="Nomeação/Exoneração do Secretário-Executivo do Ministério da Economia",
            ),
            Criterio(  # A13
                self.conteudo.contem(r"cargo de Secretário de Política Econômica"),
                motivo="Nomeação/Exoneração do Secretário de Política Econômica",
            ),
            Criterio(  # A14
                self.conteudo.contem(r"cargo de Secretário do Tesouro Nacional"),
                motivo="Nomeação/Exoneração do Secretário do Tesouro Nacional",
            ),
            Criterio(  # A15
                self.conteudo.contem(r"cargo de Presidente da Casa da Moeda do Brasil"),
                motivo="Nomeação/Exoneração do Presidente da Casa da Moeda do Brasil",
            ),
            Criterio(  # A16
                self.conteudo.contem(
                    r"cargo de Diretor da Comissão de Valores Mobiliários"
                ),
                motivo="Nomeação/Exoneração do Diretor da Comissão de Valores Mobiliários",
            ),
            Criterio(  # A17
                self.conteudo.contem(
                    r"cargo de Superintendente da Superintendência de Seguros Privados"
                ),
                motivo="Nomeação/Exoneração do Superintendente da Superintendência de Seguros Privados",
            ),
            Criterio(  # A18
                self.conteudo.contem(
                    r"cargo de Diretor da Superintendência de Seguros Privados"
                ),
                motivo="Nomeação/Exoneração do Diretor da Superintendência de Seguros Privados",
            ),
            Criterio(  # A19
                self.conteudo.contem(
                    r"cargo de Diretor-Superintendente da Superintendência Nacional de Previdência Complementar"
                ),
                motivo="Nomeação/Exoneração do Diretor-Superintendente da Superintendência Nacional de Previdência Complementar",
            ),
            Criterio(  # A20
                self.conteudo.contem(
                    r"cargo de Diretor de Licenciamento da Superintendência Nacional de Previdência Complementar"
                ),
                motivo="Nomeação/Exoneração do Diretor de Licenciamento da Superintendência Nacional de Previdência Complementar",
            ),
            Criterio(  # A21
                self.conteudo.contem(
                    r"cargo de Secretário Especial Adjunto da Secretaria Especial de Previdência e Trabalho do Ministério da Economia"
                ),
                motivo="Nomeação/Exoneração do Secretário Especial Adjunto da Secretaria Especial de Previdência e Trabalho do Ministério da Economia",
            ),
            Criterio(  # A22
                self.conteudo.contem(
                    r"cargo de Secretário-Executivo do Ministério do Trabalho e Previdência"
                ),
                motivo="Nomeação/Exoneração do Secretário-Executivo do Ministério do Trabalho e Previdência",
            ),
            Criterio(  # R2-A3
                self.conteudo.contem(
                    r"cargo de Secretário Especial do Tesouro e Orçamento do Ministério da Economia"
                ),
                motivo="Nomeação/Exoneração do Secretário Especial do Tesouro e Orçamento do Ministério da Economia",
            ),
            Criterio(  # R2-A9
                self.conteudo.contem(
                    r"cargo de Procurador-Geral Federal da Advocacia-Geral da União"
                ),
                motivo="Nomeação/Exoneração do Procurador-Geral Federal da Advocacia-Geral da União",
            ),
        ]

    def afastamentos(self):
        yield from [
            Criterio(  # A29
                self.conteudo.contem(
                    r"(?:Exposição|Exposições) de Motivos.{0,200}(?:afastamento|férias).{0,50} Presidente do Banco Central do Brasil"
                ),
                motivo="Afastamento do Presidente do BC",
            ),
            Criterio(  # A30
                self.conteudo.contem(
                    r"(?:Exposição|Exposições) de Motivos.{0,200}(?:afastamento|férias).{0,50} Ministro de Estado da Economia"
                ),
                motivo="Afastamento do Ministro de Estado da Economia",
            ),
            Criterio(  # A31
                self.conteudo.contem(
                    r"(?:A DIRETORA|O DIRETOR) DE ADMINISTRAÇÃO DO BANCO CENTRAL DO BRASIL"
                ),
                motivo="Despacho do Diretor de Administração",
            ),
            Criterio(  # A32
                self.conteudo.contem(
                    r"^.{0,100}PORTARIA.+O MINISTRO DE ESTADO DA ECONOMIA.+afastamento.+Banco Central",
                    # Já que o conteudo vem com o titulo junto, eu precisei dizer que o título (primeiros 100 caracteres) deve conter PORTARIA
                ),
                motivo="Portaria do Ministro da Economia afastando alguém do Banco Central",
            ),
            Criterio(  # Sempre que o presidente do COAF se ausenta, o Presidente do Banco Central do Brasil precisa fazer um despacho
                self.conteudo.contem(
                    r"Despacho do Presidente do Banco Central do Brasil.+Presidente do COAF"
                ),
                motivo="Afastamento do presidente do COAF",
            ),
        ]

    def especificos(self):
        yield from [
            Criterio(
                self.conteudo.contem(
                    r"temas jurídicos relevantes para a administração pública"
                )
                & self.escopo.contem(r"Subchefia para Assuntos Jurídicos"),
                motivo='Publicação da Subchefia para Assuntos Jurídicos que contém "temas jurídicos relevantes para a administração pública" no conteúdo',
            )
        ]
