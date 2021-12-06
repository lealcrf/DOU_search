AFASTAMENTO = [
    "(Exposição|Exposições) de Motivos.+Presidente do Banco Central do Brasil",
    "(Exposição|Exposições) de Motivos.+Ministro de Estado da Economia",
    "A DIRETORA DE ADMINISTRAÇÃO DO BANCO CENTRAL DO BRASIL",
    "PORTARIA.+O MINISTRO DE ESTADO DA ECONOMIA;+afastamento",
    "Despacho do Presidente do Banco Central do Brasil.+Presidente do COAF",  # Sempre que o presidente do COAF se ausenta, o Presidente do Banco Central do Brasil precisa fazer um despacho
]

ASSINATURAS_DIRETORES_E_PRESIDENTE_DO_BC = [
    # * = Não aparece nenhuma vez no meu banco de dados
    "ROBERTO DE OLIVEIRA CAMPOS NETO",  # Presidente
    "Maurício Costa de Moura",  # * Diretor de Relacionamento, Cidadania e Supervisão de Conduta - Direc
    "Paulo sérgio Neves Souza",  # * Diretor de Fiscalização - Difis
    "Fabio Kanczuk",  # * Diretor de Política Econômica - Dipec
    "Bruno Serra Fernandes",  # Diretor de Política Monetária - Dipom
    "Fernanda Guardado",  # * Diretora de Assuntos Internacionais e de Gestão de Riscos Corporativos - Direx
    "João Manoel Pinho de Mello",  # Diretor de Organização do Sistema Financeiro e de Resolução - Diorf
    "Otávio Ribeiro Damaso",  # * Diretor de Regulação - Dinor
    "Carolina de Assis Barros",  # Diretora de Administração - Dirad
]



NOMEACAO_E_EXONERACAO = [
    # Assunto 6:
    "cargo de Presidente do Banco Central",
    # Assunto 7:
    "cargo de Diretor do Banco Central",
    "cargo de Diretora do Banco Central",
    # Assunto 11:
    "cargo de Secretário Especial de Fazenda do Ministério da Economia",
    # Assunto 12:
    "cargo de Secretário-Executivo do Ministério da Economia",
    # Assunto 13:
    "cargo de Secretário de Política Econômica",
    # Assunto 14:
    "cargo de Secretário do Tesouro Nacional",
    # Segunda reunião - Assunto 3
    "cargo de Secretário Especial do Tesouro e Orçamento do Ministério da Economia",
    # Assunto 15:
    "cargo de Presidente da Casa da Moeda do Brasil",
    # Assunto 16:
    "cargo de Diretor da Comissão de Valores Mobiliários",
    # Assunto 17:
    "cargo de Superintendente da Superintendência de Seguros Privados",
    # Assunto 18:
    "cargo de Diretor da Superintendência de Seguros Privados",
    # Assunto 19:
    "cargo de Diretor-Superintendente da Superintendência Nacional de Previdência Complementar",
    # Assunto 20:
    "cargo de Diretor de Licenciamento da Superintendência Nacional de Previdência Complementar",
    # Assunto 21:
    "cargo de Secretário Especial Adjunto da Secretaria Especial de Previdência e Trabalho do Ministério da Economia",
    # Assunto 22:
    "cargo de Secretário-Executivo do Ministério do Trabalho e Previdência",
    ###################################################################
    # Assunto 10:
    "cargo de Ministro de Estado da Economia",
    #
    "cargo de Ministro de Estado do Trabalho e Previdência",
]

KEYWORDS_CONTEUDO = [
    "Comissão Técnica da Moeda e do Crédito",
    "Secretário-Executivo Adjunto da Secretaria-Executiva do Ministério do Trabalho e Previdência",
    "Comitê de Regulação e Fiscalização dos Mercados Financeiro, de Capitais, de Seguros, de Previdência e Capitalização",
]
KEYWORDS_TITULO = [
    "Resolução Coremec",
]

KEYWORDS_EMENTA = [
    "Lavagem de Dinheiro",
    "Programa Nacional de Apoio às Microempresas e Empresas de Pequeno Porte",
    "Proteção de Dados",
    # Segunda reunião - Assunto 6
    "Decreto nº 10.835", # Solução temporária
    # Segunda reunião - Assunto 7
    "Subdelega competências para a prática de atos de gestão de pessoas no âmbito do Ministério da Economia às autoridades que menciona",
    
    
]
