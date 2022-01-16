from pandas import DataFrame
import config
from enum import Enum
from ..models.publicacao import Publicacao

class SumulaVazia(Exception):
    pass

class Endpoints(Enum):
    """Endpoints que são usados para se conectar com a api do teams"""

    TESTE = config.TEAMS_API_ENDPOINT_TESTE
    OFICIAL = config.TEAMS_API_ENDPOINT
    LIGIANE = config.TEAMS_API_ENDPOINT_LIGIANE


def limpar_e_ordenar_sumula_em_secoes(sumula: DataFrame) -> dict[str, list]:
    """Deixa as publicações em uma forma mais organizada e parecida com a súmula oficial

    Na súmula oficial, as publicações são divididas em escopos (que aqui eu estou chamando de seções). Dentro de cada seção, as publicações são ordenadas em ordem alfabética, com o título formatado para mostrar apenas o necessário.
    """
    secoes = dict()

    for pub in sumula.transpose().to_dict().values():
        pub = Publicacao(**pub).to_sumula()

        secoes.setdefault(pub["escopo"], []).append(pub)  # Limpa cada publicação

    # Ordenar as publicações de cada espopo em ordem alfabética do título
    for escopo, pubs in secoes.items():
        secoes[escopo] = sorted(pubs, key=lambda pub: pub["titulo"])

    return secoes
