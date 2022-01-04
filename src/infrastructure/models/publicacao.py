from dataclasses import dataclass
from datetime import date, datetime
import re


@dataclass
class Publicacao:
    """Representa uma publicação no Diário Oficial da União

    - A ementa, título e assinatura podem ser None

    """

    id: str
    secao: str
    tipo_normativo: str
    data: date
    escopo: str
    titulo: str
    ementa: str
    conteudo: str
    assinatura: str
    pdf: str
    id_materia: str
    motivo: str = None

    @staticmethod
    def from_database(json):
        return Publicacao(
            id=json["id"],
            secao=json["secao"],
            tipo_normativo=json["tipo_normativo"],
            data=datetime.strptime(json["data"], "%Y-%m-%d").date(),
            escopo=json["escopo"],
            titulo=json["titulo"],
            ementa=json["ementa"],
            conteudo=json["conteudo"],
            assinatura=json["assinatura"],
            pdf=json["pdf"],
            id_materia=json["id_materia"],
            motivo=json["motivo"],
        )


    def to_sumula(self) -> dict:
        """Limpa a publicação para ser enviada à súmula"""

        # | Tira o excesso do titulo
        self.titulo = re.sub(r",? DE .+2021?", "", self.titulo.upper())

        escopos_importantes = [
            "Banco Central do Brasil",
            "Ministério da Economia",
            "Presidência da República",
            "Conselho de Controle de Atividades Financeiras",
            "Atos do Poder Legislativo",
            "Atos do Poder Executivo",
            "Ministério Público da União",
            "Ministério do Trabalho e Previdência",
        ]

        # | Caso alguma parte escopo for particularmente importante, deixa só a parte importante como escopo
        for escopo in self.escopo.split("/")[::-1]:  # por grau de importância
            if escopo in escopos_importantes:
                self.escopo = escopo  # Muda o escopo para ser só o importante
                break
            else:
                self.escopo = "Outros"

        self.ementa = self.ementa if self.ementa else ""

        # | Retorna só as partes que importam para a súmula
        return {
            "titulo": self.titulo,
            "url": self.pdf,
            "ementa": self.ementa,
            "escopo": self.escopo,
            # O • só é pra deixar mais fácil minha vida no jupyter, na súmula fica feio
            "motivos": self.motivo.replace("• ", "").replace('"', r"\"").splitlines(),
        }
