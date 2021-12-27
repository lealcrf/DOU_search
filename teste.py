from dataclasses import dataclass
from typing import List


@dataclass
class Pattern:
    regex: str
    motivo: str = None

    def completar_motivo(self, coluna):
        motivo = "• " + self.motivo if self.motivo else self.criar_motivo_generico(coluna)
        padrao_estipulado = "{}[{}]".format(coluna, self.regex)
        
        return motivo + " => " + padrao_estipulado

    def criar_motivo_generico(self, coluna):
        if coluna in ["assinatura", "ementa"]:
            return "Achou \"{}\" na {}".format(self.regex, coluna)

        return "Achou \"{}\" no {}".format(self.regex, coluna)
