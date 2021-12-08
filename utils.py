import re
from typing import List
import unicodedata
import pandas as pd
import numpy as np
from pandas.core.series import Series


def tirar_acentuacao(string: str):
    if string is not None:
        return "".join(
            c
            for c in unicodedata.normalize("NFD", string)
            if unicodedata.category(c) != "Mn"
        )


def tirar_acentuacao_column(column: Series):
    return (
        column.str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )


class Pattern:
    def __init__(self, regex, assunto=None):
        self.regex = regex
        self.assunto = assunto +"|"if assunto else ""


class ColumnSearch:
    def __init__(self, column: Series, patterns: List[Pattern]):
        # Se for assinatura, remove a acentuação de tudo para fazer uma melhor comparação (a acentuação das assinaturas são consistentes)
        self.column = column
        self.patterns = []
                
        for pat in patterns:
            pat.assunto = f"{pat.assunto}{column.name} contém \"{pat.regex}\" "
            if column.name == "assinatura":
                pat.regex = tirar_acentuacao(pat.regex)

            self.patterns.append(pat)

    def get_result(self, df: pd.DataFrame):
        regexes = [pattern.regex for pattern in self.patterns]

        result = df[
            self.column.str.contains(
                f'({"|".join(regexes)})',
                flags=re.IGNORECASE,
                regex=True,
                na=False,
            )
        ]

        conditions = [
            result[self.column.name].str.contains(
                pattern.regex,
                flags=re.IGNORECASE,
                regex=True,
                na=False,
            )
            for pattern in self.patterns
        ]

        values = [pattern.assunto for pattern in self.patterns]

        motivo = np.select(conditions, values)

        if result.get("motivo") is None:
            result["motivo"] = motivo
        else:
            result.motivo = result.motivo.apply(lambda x: f"{x} + {motivo[0]}")

        return result
